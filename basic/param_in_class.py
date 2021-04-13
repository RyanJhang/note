class Param:
    classvar  = "default"

    def __init__(self):
        self.somevar = 'Some value'


if __name__ == "__main__":
    p1 = Param()

    print(Param.__dict__)
    print(p1.__dict__)
    print("----" * 10)

    p1.classvar = 2
    p1.somevar = 2

    print(Param.__dict__)
    print(p1.__dict__)
    print("----" * 10)
    
    Param.classvar = 0

    print(Param.__dict__)
    print(p1.__dict__)
    print("----" * 10)
