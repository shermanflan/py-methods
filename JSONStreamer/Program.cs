using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

using System.IO;
using Newtonsoft.Json;
using System.Data;
using System.Data.SqlTypes;
using System.Data.SqlClient;
//using System.Data.Odbc;
using System.Diagnostics;

namespace JSONStreamer
{
    public class Program
    {
        /*
         * TODO:
         * Consider writing to a CSV file and then bulk loading the data.
         * For server name and db, do a post update keyed off the source.
         * Alternatively, use a custom data flow source to implement this.
         * Also, consider reading twice - once for server name and db (quit
         * as soon as both are read) and then once for the rest. This would 
         * eliminate the need for an UPDATE.
         */
        public static void Main(string[] args)
        {
            //string path = @"C:\Users\ricardogu\Desktop\CIT-10465\data\source";
            //string file = Path.Combine(path, @"test6_breach_report_11-27.json");
            //string conxnString = @"DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=ScratchDB;Trusted_Connection=yes;";
            //string conxnString = @"Server=localhost;Database=ScratchDB;Trusted_Connection=True;";
            ///*
            if (args.Length < 2)
            {
                throw new ArgumentException("Error: Input missing.");
            }

            string file = args[0];
            string conxnString = args[1];
            //*/
            string serverDb = null, serverName = null;
            Dictionary<string, int> tmpLoco = null;
            string tmpCo = null, tmpAR = null;
            string source = Path.GetFileName(file);
            DateTime startBatch = DateTime.Now; // TODO: consider pulling in from SSIS parameters
            //DateTime endBatch;
            Stopwatch timer = new Stopwatch();

            int ultiCount = 0, legacyCount = 0;
            //string qryUlti = @"
            //    INSERT INTO dbo.PerceptUltiCo(ARNumber, CustomerServer, CustomerDatabase, Source, Created, CreatedBy)
            //    VALUES(?, ?, ?, ?, ?, SYSTEM_USER)
            //";
            string qryUlti = @"
                INSERT INTO dbo.PerceptUltiCo (ARNumber, CustomerServer, CustomerDatabase, Source, Created, CreatedBy)
                VALUES (@pAR, @pServerName, @pServerDB, @pSource, @pCreated, SYSTEM_USER);
            ";
            //string qryLegacy = @"
            //    INSERT INTO dbo.PerceptLegacyCo(ARNumber, CustomerName, CustomerServer, CustomerDatabase, Location, EECount, Source, Created, CreatedBy)
            //    VALUES(?, ?, ?, ?, ?, ?, ?, ?, SYSTEM_USER)
            //";
            string qryLegacy = @"
                INSERT INTO dbo.PerceptLegacyCo (ARNumber, CustomerName, CustomerServer, CustomerDatabase, Location, EECount, Source, Created, CreatedBy)
                VALUES(@pAR, @pLegacy, @pServerName, @pServerDB, @pLoco, @pCount, @pSource, @pCreated, SYSTEM_USER)
            ";

            timer.Start();
            //using (OdbcConnection connection = new OdbcConnection(conxnString))
            using (SqlConnection connection = new SqlConnection(conxnString))
            {
                connection.Open();

                var ultiCmd = new SqlCommand(qryUlti, connection);
                ultiCmd.Parameters.Add("@pAR", SqlDbType.NVarChar);
                ultiCmd.Parameters.Add("@pServerName", SqlDbType.VarChar);
                ultiCmd.Parameters.Add("@pServerDB", SqlDbType.VarChar);
                ultiCmd.Parameters.Add("@pSource", SqlDbType.VarChar);
                ultiCmd.Parameters.Add("@pCreated", SqlDbType.DateTime2);

                //OdbcCommand ultiCmd = new OdbcCommand(qryUlti, connection);
                //ultiCmd.Parameters.Add("@pAR", OdbcType.NVarChar);
                //ultiCmd.Parameters.Add("@pServerName", OdbcType.VarChar);
                //ultiCmd.Parameters.Add("@ServerDB", OdbcType.VarChar);
                //ultiCmd.Parameters.Add("@pSource", OdbcType.VarChar);
                //var param = new OdbcParameter();
                //param.ParameterName = "@pCreated";
                //param.DbType = DbType.DateTime;
                //param.Value = startBatch;
                //param.Scale = 3;
                //ultiCmd.Parameters.Add(param);

                var legacyCmd = new SqlCommand(qryLegacy, connection);
                legacyCmd.Parameters.Add("@pAR", SqlDbType.NVarChar);
                legacyCmd.Parameters.Add("@pLegacy", SqlDbType.NVarChar);
                legacyCmd.Parameters.Add("@pServerName", SqlDbType.VarChar);
                legacyCmd.Parameters.Add("@pServerDB", SqlDbType.VarChar);
                legacyCmd.Parameters.Add("@pLoco", SqlDbType.NVarChar);
                legacyCmd.Parameters.Add("@pCount", SqlDbType.Int);
                legacyCmd.Parameters.Add("@pSource", SqlDbType.VarChar);
                legacyCmd.Parameters.Add("@pCreated", SqlDbType.DateTime2);

                //OdbcCommand legacyCmd = new OdbcCommand(qryLegacy, connection);
                //legacyCmd.Parameters.Add("@pAR", OdbcType.NVarChar);
                //legacyCmd.Parameters.Add("@pLegacy", OdbcType.NVarChar);
                //legacyCmd.Parameters.Add("@pServerName", OdbcType.VarChar);
                //legacyCmd.Parameters.Add("@ServerDB", OdbcType.VarChar);
                //legacyCmd.Parameters.Add("@pLoco", OdbcType.NVarChar);
                //legacyCmd.Parameters.Add("@pCount", OdbcType.Int);
                //legacyCmd.Parameters.Add("@pSource", OdbcType.VarChar);
                //param = new OdbcParameter();
                //param.ParameterName = "@pCreated";
                //param.DbType = DbType.DateTime;
                //param.Scale = 3;
                //legacyCmd.Parameters.Add(param);

                // Scan server metadata first.
                using (StreamReader s = File.OpenText(file)) // utf-8 default
                {
                    using (JsonTextReader j = new JsonTextReader(s))
                    {
                        while (j.Read())
                        {
                            if (j.TokenType == JsonToken.PropertyName && j.Path == "server_db")
                            {
                                serverDb = j.ReadAsString();
                            }
                            else if (j.TokenType == JsonToken.PropertyName && j.Path == "server_name")
                            {
                                serverName = j.ReadAsString();
                            }

                            if (serverName != null && serverDb != null)
                            {
                                break;
                            }
                        }
                    }
                }

                // Now, scan company data.
                using (StreamReader s = File.OpenText(file)) // utf-8 default
                {
                    using (JsonTextReader j = new JsonTextReader(s))
                    {
                        while (j.Read())
                        {
                            // Scan Ultipro AR numbers.
                            if (j.TokenType == JsonToken.PropertyName
                                && (string)j.Value == "ar_number" && j.Path.StartsWith("ultipro"))
                            {
                                tmpAR = j.ReadAsString();
                                ultiCmd.Parameters["@pAR"].Value = tmpAR;
                                ultiCmd.Parameters["@pServerName"].Value = serverName;
                                ultiCmd.Parameters["@pServerDB"].Value = serverDb;
                                ultiCmd.Parameters["@pSource"].Value = source;
                                ultiCmd.Parameters["@pCreated"].Value = startBatch;

                                ultiCount += ultiCmd.ExecuteNonQuery();
                            }
                            // New legacy company.
                            else if (j.TokenType == JsonToken.StartObject
                                && j.Path.StartsWith("standalone") && j.Depth == 2)
                            {
                                // Store aggregate locations in a hashtable per company.
                                tmpLoco = new Dictionary<string, int>();
                            }
                            else if (j.TokenType == JsonToken.PropertyName
                                && (string)j.Value == "location" && j.Path.StartsWith("standalone"))
                            {
                                string loco = j.ReadAsString() ?? "Unknown";

                                if (tmpLoco.ContainsKey(loco))
                                {
                                    tmpLoco[loco] += 1;
                                }
                                else
                                {
                                    tmpLoco[loco] = 1;
                                }
                            }
                            else if (j.TokenType == JsonToken.PropertyName
                                && (string)j.Value == "company_name" && j.Path.StartsWith("standalone"))
                            {
                                tmpCo = j.ReadAsString();
                            }
                            else if (j.TokenType == JsonToken.PropertyName
                                && (string)j.Value == "ar_number" && j.Path.StartsWith("standalone"))
                            {
                                tmpAR = j.ReadAsString();
                            }
                            // End legacy company.
                            else if (j.TokenType == JsonToken.EndObject
                                && j.Path.StartsWith("standalone") && j.Depth == 2)
                            {
                                // For non-null locations, write to database
                                if (tmpLoco.Count > 0)
                                {
                                    try
                                    {
                                        foreach (var kv in tmpLoco)
                                        {
                                            legacyCmd.Parameters["@pAR"].Value = tmpAR ?? SqlString.Null;
                                            //legacyCmd.Parameters["@pAR"].Value = (object)tmpAR ?? DBNull.Value;
                                            legacyCmd.Parameters["@pLegacy"].Value = tmpCo;
                                            legacyCmd.Parameters["@pServerName"].Value = serverName;
                                            legacyCmd.Parameters["@pServerDB"].Value = serverDb;
                                            legacyCmd.Parameters["@pLoco"].Value = kv.Key;
                                            legacyCmd.Parameters["@pCount"].Value = kv.Value;
                                            legacyCmd.Parameters["@pSource"].Value = source;
                                            legacyCmd.Parameters["@pCreated"].Value = startBatch;
                                            legacyCount += legacyCmd.ExecuteNonQuery();
                                        }
                                    }
                                    catch (Exception e)
                                    {
                                        Console.WriteLine(e.ToString());
                                        Console.WriteLine("{0}, {1}", tmpCo, tmpLoco.Keys);
                                        return;
                                    }
                                }
                            }
                        }
                    }
                }

            } // Connection is automatically closed.

            timer.Stop();
            Console.WriteLine("Inserted {0} ultipro companies, {1} legacy locations", ultiCount, legacyCount);
            Console.WriteLine("Elapsed: {0}", timer.Elapsed.ToString());
        }
    }
}
