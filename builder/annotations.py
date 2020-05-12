import xmltodict
from fastai.basic_data import Path
from .utils import flatten_list



class Annotate():
    def __init__(self, xml_file=None):
        self.xml_file = xml_file        
        self.annotation_details = {}

    def __call__(self, xml_file):
        self.xml_file = xml_file
        return self.invoke()

    def invoke(self):
        return (self.convert_to_json()
                    .populate_details())
        
    def convert_to_json(self):
        with open(self.xml_file, 'r') as f:
            self.annotation_details = xmltodict.parse(f.read())
        return self    

    def populate_details(self):
        d = self.annotation_details
        annot_objects = d['annotation']['object']
        annot_objects = annot_objects if isinstance(annot_objects, list) else [annot_objects]
        
        height, width, area = self._get_hw_area(d['annotation']['size'])        
        filename = d['annotation']['filename']
        path = d['annotation']['path']        
        annotated = []
        
        for idx, o in enumerate(annot_objects):  
            id = idx + 1                             
            category = o['name']
            bbox = self._get_bbox(o['bndbox'])            
            annotated.append(self._prepare_annotation(height, width, area, 
                                filename, path, self.xml_file, category, 
                                bbox, id))
        return annotated
        
    def _get_hw_area(self, size):
        height = float(size['height'])
        width = float(size['width'])
        area = height * width
        return [height, width, area]

    def _get_bbox(self, bb): 
        bb =  [bb['xmin'], bb['ymin'], bb['xmax'], bb['ymax']]
        bb = list(map(int, bb))
        return bb

    def _prepare_annotation(self, height, width, area, filename, path, xml_file, category, bbox, id):
        return {
            'height': height,
            'width': width,
            'filename': filename,
            'path': path,
            'folder': xml_file.parent.__str__().split('/')[-1],
            'category': category,
            'bbox': bbox,
            'id': id
        }


class AnnotationsBuilder():
    def __init__(self, annot_folder=None):        
        self.annot_folder = annot_folder
        self.annotator = Annotate()
        self.annots = None

    def __call__(self, annot_folder):        
        self.annot_folder = Path(annot_folder)
        self.annots = [self.annotator(xml_file) for folder in self.annot_folder.ls() for xml_file in folder.ls()]
        self.annots = flatten_list(self.annots)
        return self.annots    


__all__ = [Annotate, AnnotationsBuilder]