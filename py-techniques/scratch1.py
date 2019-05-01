# Test update!
# File harness
try:

    with open("C:\\Users\\rguzman\\Desktop\\test.txt", "r", encoding="utf-8") as f:
        n, m = map(int, f.readline().rstrip().split())

        arr = map(int, f.readline().rstrip().split())

        A = set(map(int, f.readline().rstrip().split()))
        B = set(map(int, f.readline().rstrip().split()))

        #C = set(arr)
        #A = A & C
        #B = B & C
        happy = 0

        for n in arr:
            if n in A:
                happy += 1
            elif n in B:
                happy -= 1
            
        print(happy)

except Exception as e:
    print(e)