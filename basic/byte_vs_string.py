a = "我"
b = "me"

c = a.encode("utf-8")
d = b.encode("utf-8")

print(a, len(a))  # 我 1
print(b, len(b))  # me 2
print(c, len(c))  # b'\xe6\x88\x91' 3
print(d, len(d))  # b'me' 2
