import pdb
import itertools
from pandas.core.common import flatten

def flatten_list(l): return list(flatten(l))

class Categories():
    def __init__(self, annotated=None):
        self.annotated = annotated
        self.cat = None

    def __call__(self, annotated):
        self.annotated = annotated
        return self.invoke()

    def invoke(self, invert=False):

        self.cat = [ a['category'] for a in self.annotated  ]
        self.cat = set(flatten_list(self.cat))
        self.cat = dict([(i+1, c) for i, c in enumerate(self.cat)])
        return self.cat

    def categories(self, invert=False):
        if invert: return dict([(v, k) for k, v in self.cat.items()])
        else: return self.cat

    def get_category_id(self, category_name):
        return self.categories(invert=True)[category_name]
    

__all__ = [Categories]