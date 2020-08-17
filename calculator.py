# write your code here
while True:
    elems = input().split(" ")
    try:
        if elems[0] == '/exit':
            print('Bye!')
            break
        print(sum([int(x) for x in elems]))
    except ValueError:
        pass
