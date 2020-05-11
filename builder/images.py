import shutil
from fastai.basic_data import Path



class ImageFolderError(Exception): pass
class DestinationFolderNotEmpty(Exception): pass

class Images():
    def __init__(self, images_folder=None, dest_folder=None):
        self.images_folder = images_folder
        self.dest_folder = dest_folder
        self.file_details = {}
        

    def set_dest_folder(self):
        if not self.images_folder: raise ImageFolderError('Please specify a valid `images_folder`')
        
        parent_folder = self.images_folder.parent
        all_images_path = Path(parent_folder/'all_images')
        all_images_path.mkdir(exist_ok=True)
        self.dest_folder = all_images_path
        return self.dest_folder

    def __call__(self, dest_folder=None):
        if dest_folder: self.dest_folder = dest_folder
        
        self.rename()
        return self.file_details


    def rename(self):
        self.images_folder = Path(self.images_folder)

        if not self.dest_folder: self.set_dest_folder()
        if len(self.dest_folder.ls()) > 0: raise DestinationFolderNotEmpty('Destination Folder is not empty')

        file_details = []
        idx = 0

        for folder in self.images_folder.ls():
            for img_file in Path(folder).ls():
                if img_file.name in ['metadata.json', 'urls.txt', '.ipynb_checkpoints']: continue

                idx += 1
                old_filename = img_file.absolute().__str__()
                new_path = Path(self.dest_folder/f'{idx}.jpg')
                shutil.copy(img_file, new_path)
                file_details.append({'filename': f'{idx}.jpg', 'id': idx, 'old_name': old_filename })
        
        self.file_details = file_details
        return file_details

    def old_to_new(self):
        """
        Returns a dictionary of old filenames to new
        """

        return dict([ (("/").join(i['old_name'].split('/')[-2:]),
                      i['filename'])  for i in self.file_details ])

    def new_for_old(self, old_filename):
        """
        Returns new filename for an old
        """

        o2n = self.old_to_new()
        return o2n[old_filename]

    def id_for_name(self, name): return int(name[:-4])


__all__ = [Images]