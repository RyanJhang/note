
class demo:
    def __init__(self):
        self._name = '預設'

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @name.deleter
    def name(self):
        del self._name
        print('del complite')


if __name__ == "__main__":
    d = demo()
    print(d.name)
