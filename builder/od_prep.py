from fastai.basic_data import Path
from .annotations import AnnotationsBuilder
from .images import Images
from .categories import Categories

class OdPrep():
    def __init__(self, annot_folder, images_folder, all_images_folder=None):
        self.annot_folder = Path(annot_folder)
        self.images_folder = Path(images_folder)
        if all_images_folder: self.all_images_folder = Path(all_images_folder)
        else: self.all_images_folder = None

        self.annotator = AnnotationsBuilder()
        self.image_builder = Images(images_folder=images_folder, dest_folder=all_images_folder)
        self.categories_builder = Categories()

        self.all_annotations = []
        self.all_categories = []
        self.all_images = []


    def __call__(self):
        self.annotator(annot_folder=self.annot_folder)
        self.image_builder()
        self.categories_builder(annotated=self.annotator.annots)
        self.build_annotations(self.annotator.annots)
        self.build_images(self.annotator.annots)
        self.build_categories(self.annotator.annots)
        return self.all_data


    def build_annotations(self, annots):
        all_annotations = []
        for a in annots:
                      
            old_name = f'{a["folder"]}/{a["filename"]}'
            new_name = self.image_builder.new_for_old(old_name)
            image_id = self.image_builder.id_for_name(new_name)
            id = image_id
            
            _ann = {
                'segmentation': [[]],
                'area': (a['height'] * a['width']),
                'iscrowd': 0,
                'image_id': image_id,
                'bbox': [ list(map(int, bb)) for bb in a['bbox'] ],
                'category_id': [self.categories_builder.get_category_id(c) for c in a['category']],
                'id': id,
                'ignore': 0 }

            all_annotations.append(_ann)
        self.all_annotations = all_annotations
        return self.all_annotations    


    def build_categories(self, annots):        
        self.all_categories =  [{'id': k, 'name': v, 'supercategory': None} for k,v in self.categories_builder.categories().items()]
        return self.all_categories

    def build_images(self, annots):
        all_images = []
        for a in annots:            
            old_name = f'{a["folder"]}/{a["filename"]}'
            new_name = self.image_builder.new_for_old(old_name)
            image_id = self.image_builder.id_for_name(new_name)

            _image = {
                'file_name': new_name,
                'height': a['height'],
                'width': a['width'],
                'id': image_id
            }
            
            if _image not in all_images: all_images.append(_image)                            
                    
        self.all_images = all_images
        return self.all_images

    @property
    def all_data(self):
        return {'annotations': self.all_annotations, 'images': self.all_images, 'categories': self.all_categories}
    
