import logging
import cloudpickle
import pickle

squared = lambda x: x ** 2
pickled_lambda = cloudpickle.dumps(squared)

new_squared = pickle.loads(pickled_lambda)
print (new_squared(2))