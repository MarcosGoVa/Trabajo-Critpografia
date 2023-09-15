import pickle
import base64

a = pickle.dumps({'foo': 'bar'})
a_64 = base64.b64encode(a).decode("utf-8")
print(a)
print(a_64) 

b_bytes = base64.b64decode(a_64)
print(b_bytes)
b = pickle.loads(b_bytes)
print(b)
