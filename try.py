import pickle

a = pickle.dumps({'foo': 'bar'})
print(a) 
b = pickle.loads(a)
print(b)
