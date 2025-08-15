from typing import List, Union

from pydantic import BaseModel, parse_obj_as


class User(BaseModel):
    name: str
    age: int


class User2(BaseModel):
    name2: str
    age2: int


class UserList(BaseModel):
    users: List[User | User2] = []

users = [
    {"name": "user1", "age": 15}, 
    {"name2": "user2", "age2": 28}
]
m = UserList(users=users)
print(m.dict())

# a = parse_obj_as(List[User, User2], users)
# b = UserList.parse_obj(b)

# b.users
# print(b.dict())

for m in m.users:
    print(m)
    print(type(m))


class a:
    def __init__(self, u: UserList):
        self.u = u


a(u)
