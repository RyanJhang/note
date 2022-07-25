import sys

a = "我"
b = "me"

c = a.encode("utf-8")
d = b.encode("utf-8")

print(a, len(a), sys.getsizeof(a))  # 我 1
print(b, len(b), sys.getsizeof(b))  # me 2
print(c, len(c), sys.getsizeof(c))  # b'\xe6\x88\x91' 3
print(d, len(d), sys.getsizeof(d))  # b'me' 2
