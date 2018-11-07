from collections import deque, defaultdict

def weightedUniformStrings(s, queries):
    answers, U = [], {}
    pos = 0
    
    # Build U hashtable
    while pos < len(s):
        weight = ord(s[pos])-ord('a')+1
        U[s[pos]] = weight
        
        end = pos + 1
        while end < len(s) and s[pos] == s[end]:
            # Add to U
            U[s[pos:end+1]] = weight*len(s[pos:end+1])
            end += 1
        
        pos = end
    
    print(U)
    # Query U
    for q in queries:
        if q in U.values():
            answers.append('Yes')
        else:
            answers.append('No')
    
    return answers

def main():
    # File harness
    try:

        with open("C:\\Users\\ricardogu\\Desktop\\test.txt", "r", encoding="utf-8") as f:
            s = f.readline().rstrip()
            #n = int(f.readline().rstrip())

            queries = []

            for _ in range(int(f.readline().rstrip())):

                q = int(f.readline().rstrip())
                queries.append(q)

            print(weightedUniformStrings(s, queries))

    except Exception as e:
        print(e)

if __name__ == '__main__':
    # execute only if run as the entry point into the program
    main()