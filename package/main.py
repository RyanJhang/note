import datetime
import math

def myfunc1():
    print("This is myfunc1.")

def test_variables():
    x = 5
    y = "variables test."
    print(x)
    print(y)

def test_strVar():
    x = "Hello world."
    print(x)

def test_global_var():
    global gy
    print(gy)


def test_cast():
    x = int(5)
    y = str(3)
    print(x, y)

def test_numbers():
    x = 123
    y = 12.3
    z = 0x112233445566778899AABBCCDD
    print(x, y, z)


def test_if(x):
    if x > 456:
        print("x > 456")
    else:
        print("x <= 456")

def test_string():
    x = "I am str."
    y = len(x)
    z = x[1]
    w = x[2:]
    print(x, y, z, w)

    if "am" in x:
        print("yes")
    else:
        print("wrong")

def test_list():
    x = list()
    x.append(1)
    x.append(2)
    x.append(3)
    x.append(4)
    x.append("five")
    print(x)
    print(len(x))
    for i in x:
        print(i)
    x = x[1:]
    x[2:4] = [22, 33]

def test_dict():
    x = {}
    x["one"] = 1
    x["two"] = 2
    x["three"] = 3
    y = x["one"]
    z = x["two"]
    if "one" in x:
        print(y)

    for k in x:
        print(k, x[k])

def test_for():
    s = 0
    for i in range(101):
        s = s + i
    print(s)

def test_while():
    s = 0
    i = 1
    while i <= 100:
        s = s + i
        i += 1
    print(s)

def test_exception():
    x = 1
    try:
        x = x + "1"
        print(x)
    except NameError:
        print("Variable x is not defined")
    except:
        print("Something else went wrong")

def test_datetime():
    x = datetime.datetime.now()
    print(x)

def test_format():
    x = 1
    y = "One"
    z = "%s is %d" % (y, x)
    print(z)

def test_math():
    x = math.ceil(1.4)
    y = math.floor(1.4)

    print(x) # returns 2
    print(y) # returns 1

def test_arg(x, y, z):
    x = x + 1
    y = y + "2"
    z = z[:]
    print(x, y, z)


class test_class:
    def __init__(self):
        self.aa = 1

    def test_class_hh(self):
        print(self.aa)

    
if "__main__" == __name__:
    gy = 123
    myfunc1()
    test_variables()
    test_strVar()
    test_global_var()
    test_cast()
    test_numbers()
    test_string()
    test_list()
    test_dict()
    test_for()
    test_while()
    test_exception()
    test_datetime()
    test_format()
    test_math()
    test_arg(1, "2", [4, 5, 6])
