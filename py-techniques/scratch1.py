if __name__ == "__main__":

    x = -1
    print(f'x: {x:08b}')
    print(f'(x<<(2+1): {x<<(2+1):08b}')

    y = 1
    print(f'y: {y:08b}')
    print(f'(y<<6)-1: {(y<<6)-1:08b}')

    z = 255
    print(f'z: {z:08b}')
    print(f'z&(y<<6)-1: {z & ((y<<6)-1):08b}')

    print(f'z&(x<<(2+1)): {z & (x<<(2+1)):08b}')
