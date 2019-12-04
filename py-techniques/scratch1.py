def sort_the_files(n, result):
    # Write your solution here
    def rec(n, level, filename, files):
        if len(files) == 1000 or filename >= n:
            return
        
        if level > 0:
            files.append("IMG{0}.jpg".format(filename))
        
        for digit in range(10):
            if digit == 0 and level == 0:
                continue
            rec(n, level+1, filename*10+digit, files)
    
        return
    
    rec(n, 0, 0, result)
    
    return '\n'.join(result)

if __name__ == "__main__":

    files = []
    result = sort_the_files(100, files)
    print(f"{len(files)}")
    print(f"{result}")