using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

using System.IO;
using Newtonsoft.Json;
using System.Data;
using System.Diagnostics;

namespace JSONStreamer
{
    public class LegacyCo
    {
        public string ARNumber { get; set; }
        public string CompanyName { get; set; }
        public Dictionary<string, int> Locations { get; set; }
    }

    public class Program
    {
        /*
         * Iterative JSON streaming using Newtonsoft.
         */
        public static void Main(string[] args)
        {
            if (args.Length < 1) {
                throw new ArgumentException("Error: Input missing.");
            }

            string file = args[0];
            string serverDb = null, serverName = null;
            List<string> ulties = new List<string>();
            List<LegacyCo> legacies = new List<LegacyCo>();
            Dictionary<string, int> tmpLoco = null;
            string tmpCo = null, tmpAR = null;
            string source = Path.GetFileName(file);
            Stopwatch timer = new Stopwatch();

            timer.Start();

            // Scan server metadata first.
            using (StreamReader s = File.OpenText(file)) { // utf-8 default
                using (JsonTextReader j = new JsonTextReader(s)) {
                    while (j.Read()) {
                        if (j.TokenType == JsonToken.PropertyName && j.Path == "server_db") {
                            serverDb = j.ReadAsString();
                        }
                        else if (j.TokenType == JsonToken.PropertyName && j.Path == "server_name") {
                            serverName = j.ReadAsString();
                        }

                        if (serverName != null && serverDb != null) {
                            break;
                        }
                    }
                }
            }

            // Now, scan company data.
            using (StreamReader s = File.OpenText(file)) { // utf-8 default
                using (JsonTextReader j = new JsonTextReader(s)) {
                    while (j.Read()) {
                        // Scan Ultipro AR numbers.
                        if (j.TokenType == JsonToken.PropertyName
                            && (string)j.Value == "ar_number" && j.Path.StartsWith("ultipro")) {
                            tmpAR = j.ReadAsString();
                            ulties.Add(tmpAR);
                        }
                        // New legacy company.
                        else if (j.TokenType == JsonToken.StartObject
                            && j.Path.StartsWith("standalone") && j.Depth == 2) {
                            // Store aggregate locations in a hashtable per company.
                            tmpLoco = new Dictionary<string, int>();
                        }
                        else if (j.TokenType == JsonToken.PropertyName
                            && (string)j.Value == "location" && j.Path.StartsWith("standalone")) {
                            string loco = j.ReadAsString() ?? "Unknown";

                            if (tmpLoco.ContainsKey(loco)) {
                                tmpLoco[loco] += 1;
                            }
                            else {
                                tmpLoco[loco] = 1;
                            }
                        }
                        else if (j.TokenType == JsonToken.PropertyName
                            && (string)j.Value == "company_name" && j.Path.StartsWith("standalone")) {
                            tmpCo = j.ReadAsString();
                        }
                        else if (j.TokenType == JsonToken.PropertyName
                            && (string)j.Value == "ar_number" && j.Path.StartsWith("standalone")) {
                            tmpAR = j.ReadAsString();
                        }
                        // End legacy company.
                        else if (j.TokenType == JsonToken.EndObject
                            && j.Path.StartsWith("standalone") && j.Depth == 2) {
                            var tmpLeg = new LegacyCo {
                                ARNumber = tmpAR
                                , CompanyName = tmpCo
                                , Locations = tmpLoco
                            };
                            legacies.Add(tmpLeg);
                        }
                    }
                }
            }

            timer.Stop();
            Console.WriteLine("Inserted {0} ultipro companies, {1} legacy locations", ulties.Count, legacies.Count);
            Console.WriteLine("Elapsed: {0}", timer.Elapsed.ToString());
        }
    }
}
