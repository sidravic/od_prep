
import pytest
from fastai.basic_data import Path
import pdb
from builder.annotations import Annotate, AnnotationsBuilder

def test_annotate(xml_path=Path('/mnt/c/Users/sidra/Dropbox/ML-Images/downloaded_images/annotated/annotations/01c7c62c-10b0-4e07-a0f1-b450334328d0/01.xml')):
    xml_path = Path(xml_path)
    annotate = Annotate()
    try:
        annotations = annotate(xml_path)
        a = annotations[0]
        assert a['height'] == 224.0
        assert a['width'] == 225.0
        assert a['filename'] == '01.jpg'
        assert a['folder'] == '01c7c62c-10b0-4e07-a0f1-b450334328d0'
        assert a['category'] == 'Paco Rabanne Invictus Eau de Toilette'
        assert a['bbox'] == ['62', '47', '150', '166']        
        
    except Exception as e:
        pytest.fail(f'Failed with Exception: {e}')


def test_annotations(folder_path=Path('/mnt/c/Users/sidra/Dropbox/ML-Images/downloaded_images/annotated/annotations')):
    ab = AnnotationsBuilder()
    
    annotations = ab(folder_path)
    assert isinstance(annotations, list) 
    assert len(annotations) == 194
    for a in annotations:
        assert sorted(a[0].keys()) == ['bbox', 'category', 'filename', 'folder', 'height', 'path', 'width']
    
