import json
#from types import SimpleNamespace
import pickle



# Reading a JSON file
with open('spanish_corpus_testset_gamulla.json', encoding='utf-8') as f:
    data = json.load(f)
    # Parse JSON into an object with attributes corresponding to dict keys.
    #x = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
    #print(x.name, x.hometown.name, x.hometown.id)
    

    with open('spanish_corpus_testset_gamulla.pkl', 'wb') as f:
        pickle.dump(data, f)    