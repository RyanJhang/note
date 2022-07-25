def leng(lt):
    match lt:
        case []:
            return 0
        case [_, *tail]:
            return 1 + leng(tail)

lt = [1, 3, 2, 5, 8]
length = leng(lt)
length