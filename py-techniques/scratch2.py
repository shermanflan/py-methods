from collections import defaultdict

def contacts(queries):
    #book = []
    results = []
    index = defaultdict(list)
    
    for q in queries:
        cmd, name = q[0], q[1]
        #print(cmd, name)
        if cmd == 'add':
            if name[0] in index:
                index[name[0]].append(name)
            else:
                index[name[0]] = [name]
                
            #book.append(name)
        elif cmd == 'find':
            lookup = index[name[0]]
            found = [n for n in lookup if n.startswith(name)]
            results.append(len(found))
        else:
            raise Exception('Invalid command!')
    #print(index)       
    return results


# File harness
try:

    with open("C:\\Users\\ricardogu\\Desktop\\test.txt", "r", encoding="utf-8") as f:
        queries = []
        for _ in range(int(f.readline().rstrip())):

            queries.append(f.readline().rstrip().split())
    
    #print(queries)
    results = contacts(queries)
    print(results)
except Exception as e:
    print(e)