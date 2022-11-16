import yaml , os.path
from yaml import FullLoader

Books = yaml.load(open(os.path.join(
               os.path.dirname(__file__)+"/static/",
               "data.yml")
            ), Loader=FullLoader)

i=0
for book in Books:
    book['id'] = i
    i += 1

def get_sample():
    return Books[0:10]