# write your code here
while True:
    elems = input().split(" ")
    try:
        if len(elems) == 2:
            print(int(elems[0]) + int(elems[1]))
        elif len(elems) == 1:
            if elems[0] == '/exit':
                print("Bye!")
                break
            print(int(elems[0]))
    except ValueError:
        pass
