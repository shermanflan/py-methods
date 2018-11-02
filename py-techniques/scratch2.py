# File harness
try:

    with open("C:\\Users\\ricardogu\\Desktop\\test.txt", "r", encoding="utf-8") as f: #home
    #with open("C:\\Users\\rguzman\\Desktop\\test.txt", "r", encoding="utf-8") as f: #work
        n = int(f.readline().rstrip())

        for _ in range(n):
            prisoners, candies, seat1 = tuple(map(int, f.readline().rstrip().split()))
            
            q, r = divmod(candies, prisoners)
            if seat1 + max(0, r-1) > prisoners:
                print(f'{(seat1 + max(0, r-1))%prisoners}') # make zero indexed
            else:
                print(f'{seat1 + max(0, r-1)}')

except Exception as e:
    print(e)