import timeit
import cProfile
import time

def subf1():
    time.sleep(2)

def main():

    time.sleep(1)
    subf1()

if __name__ == "__main__":
    print(timeit.timeit("x = 2 + 3"))

    cProfile.run('main()')
