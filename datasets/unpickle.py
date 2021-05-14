import pickle

with open('re_oie2016_test_spanish.pkl', 'rb') as pickled_one:
    data = pickle.load(pickled_one)
print(data)    