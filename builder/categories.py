class Categories():
    def __init__(self, annotated=None):
        self.annotated = annotated
        self.cat = None

    def __call__(self, annotated):
        self.annotated = annotated
        return self.invoke()

    def invoke(self, invert=False):
        self.cat = set([a['category'] for annotation in self.annotated for a in annotation])
        self.cat = dict([(i+1, c) for i, c in enumerate(self.cat)])
        return self.cat

    def categories(self, invert=False):
        if invert: return dict([(v, k) for k, v in self.cat.items()])
        else: return self.cat

__all__ = [Categories]