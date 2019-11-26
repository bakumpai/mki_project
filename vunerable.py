import pickle
import base64
import os

arr = []

for i in range(100):
    arr.append("bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb")

exp = pickle.dumps("oke");

print(base64.urlsafe_b64encode(exp))
