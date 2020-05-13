# Object Detection Prep (od_prep)

Od prep is a simple helper library that prepares a annotated object detection dataset to be processed in the format required by the `get_annotations` method for `fastai` especially when creating annotations with `labelmg`

### Expectations

The library expects information to stored in category based folders. 

For example

```

annotated 
    |______ category1
                |_______01.xml
                |_______02.xml
                |_______03.xml
    |_______ category2
                |_______01.xml
                |_______02.xml
images
    |_________category1
                |_______01.jpg
                |_______02.jpg
                |_______03.jpg
    |__________category2
                |_______01.jpg
                |_______02.jpg

```

### Usage

```python
annotations_path = '/mnt/c/Users/sidra/Dropbox/ML-Images/downloaded_images/annotated/annotations'
images_path = "/mnt/c/Users/sidra/Dropbox/ML-Images/downloaded_images/annotated/images"

from builder.od_prep import OdPrep
o = OdPrep(annot_folder=annotations_path, images_folder=images_path)
ff = o()
print(ff.all_data)
```

`ff.all_data` creates the required dataset for the `get_annotations` method in the form a dict with keys for `annotations`, `images` and `categories`

The ideal approach would then be to store it as a file 

```python

with open(ALL_DATA_JSON_PATH, 'w') as f: f.write(json.dumps(ff.all_data))

```

Then simply use the file with `get_annotations`

```python
img, lbl_bbox = get_annotations(ALL_DATA_JSON_PATH)
img2bbox = dict(zip(img, lbl_bbox))

```

Our data then looks like 

```python
{'5.jpg': [[[31, 163, 239, 372],
   [45, 81, 253, 204],
   [29, 119, 235, 288],
   [13, 24, 224, 104]],
  ['trèStiQue Tint, Moisturize & Blend Face Stick',
   'trèStiQue Tint, Moisturize & Blend Face Stick',
   'trèStiQue Tint, Moisturize & Blend Face Stick Box',
   'trèStiQue Tint, Moisturize & Blend Face Stick Box']],
 '6.jpg': [[[1, 45, 225, 216]],
  ['trèStiQue Tint, Moisturize & Blend Face Stick Box']],
 '11.jpg': [[[24, 30, 243, 185]],
  ['trèStiQue Tint, Moisturize & Blend Face Stick']],
 '1.jpg': [[[1, 72, 224, 226]],
  ['trèStiQue Tint, Moisturize & Blend Face Stick']],
 '4.jpg': [[[67, 83, 289, 266], [4, 7, 196, 98]],
  ['trèStiQue Tint, Moisturize & Blend Face Stick',
   'trèStiQue Tint, Moisturize & Blend Face Stick Box']],
 '9.jpg': [[[22, 50, 224, 207]],
  ['trèStiQue Tint, Moisturize & Blend Face Stick']],
 '7.jpg': [[[1, 52, 225, 222]],
  ['trèStiQue Tint, Moisturize & Blend Face Stick']],
 '2.jpg': [[[24, 21, 239, 162]],
  ['trèStiQue Tint, Moisturize & Blend Face Stick']],
 '8.jpg': [[[26, 23, 208, 257]],
  ['trèStiQue Tint, Moisturize & Blend Face Stick']],
 '10.jpg': [[[27, 24, 237, 188]],
  ['trèStiQue Tint, Moisturize & Blend Face Stick']],
 '3.jpg': [[[5, 34, 302, 162]],
  ['trèStiQue Tint, Moisturize & Blend Face Stick']],
 '14.jpg': [[[1, 13, 203, 252]],
  ['Laura Mercier Caviar du Jour Caviar Chrome Mini Set box']],
 '17.jpg': [[[86, 132, 299, 288],
   [85, 159, 298, 339],
   [86, 181, 300, 383],
   [86, 204, 301, 427],
   [12, 1, 224, 198]],
  ['Laura Mercier Caviar du Jour Caviar Chrome Mini Set',
   'Laura Mercier Caviar du Jour Caviar Chrome Mini Set',
   'Laura Mercier Caviar du Jour Caviar Chrome Mini Set',
   'Laura Mercier Caviar du Jour Caviar Chrome Mini Set',
   'Laura Mercier Caviar du Jour Caviar Chrome Mini Set box']] ... (truncated)
```


Then define the `get_y_func` method 

```python
def get_y_func(o):
    bbox_classes = imgs2bbox.get(o.name, None)
    if not bbox_classes: raise Exception # or do whatever you need to
    bbox, classes = bbox_classes
    return [bbox, classes]

```

And pass it to the `ObjectItemList`

```python

data = ObjectItemList.from_folder(ALL_IMAGES_PATH)
data = data.split_by_rand_pct(valid_pct=0.3)
data = data.label_from_func(get_y_func)
data = data.transform(tfms,
                     tfm_y=True, size=224, resize_method=ResizeMethod.SQUISH)
data = data.databunch(bs=bs, collate_fn=bb_pad_collate)
data = data.normalize(imagenet_stats)
```




