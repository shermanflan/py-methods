try:

    with open("C:\\Users\\ricardogu\\Desktop\\test.txt", "r", encoding="utf-8") as f:
        K = int(f.readline())
        rooms = list(map(int, f.readline().split(' ')))

        fams = len(rooms)//K
        total = sum(rooms)
        #print(total)
        for i in range(1, fams + 1):
            total -= i * K
    
        print(total)
except Exception as e:
    print(e)