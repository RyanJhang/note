class t:
    def __init__(self):
        self.a = 321

class test(t):
    a = "123"

    def __init__(self, data) -> None:
        self.data = data + "2"
        self.a = self.t(self.data)
        print("test")
        print(self.a)

    def t(self, data=None):
        return


class test2(test):
    a = "321"

    def t(self, data="test2"):

        print(data)
        return data + "3"


if __name__ == '__main__':
    t = test2(data="1")
    print("run")
    print(t.a)
