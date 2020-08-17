while True:
    elems = input().split(" ")
    try:
        if elems[0] == '/exit':
            print('Bye!')
            break
        elif elems[0] == '/help':
            print("The program calculates the sum of numbers")
        print(sum([int(x) for x in elems]))
    except ValueError:
        pass
