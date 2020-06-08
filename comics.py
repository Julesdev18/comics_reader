import os
import subprocess
import time
import zipfile
import collections
import rarfile
import json

class COMICParser:
    def __init__(self, filename, *args):
        self.filename = filename
        self.book = None
        self.image_list = None
        self.book_extension = os.path.splitext(self.filename)
        self._metadata = {}

    def read_book(self):
        if self.book_extension[1] == '.cbz':
            self.book = zipfile.ZipFile(
                self.filename, mode='r', allowZip64=True)
            self.image_list = [
                i.filename for i in self.book.infolist()
                if not i.is_dir() and is_image(i.filename)]

        elif self.book_extension[1] == '.cbr':
            self.book = rarfile.RarFile(self.filename)
            self.image_list = [
                i.filename for i in self.book.infolist()
                if not i.isdir() and is_image(i.filename)]

        self.image_list.sort()
        return self.image_list

    def generate_metadata(self, author='<Unknown>', isbn = None, tags=[], quality=0):
        title = os.path.basename(self.book_extension[0]).strip(' ')
        cover = self.book.read(self.image_list[0])

        creation_time = time.ctime(os.path.getctime(self.filename))
        year = creation_time.split()[-1]

        """NOTE: C'est ici qu'il serait malin d'enregister les informations dans un fichier..."""
        
        self._metadata = {"cover":cover, "title": title, "author":author, "year":year, "tags":tags, "quality":quality}
        return self._metadata
    
    def getMetadata(self):
        return self._metadata

    def generate_content(self):
        return self.image_list
    
    def get_filename(self):
        return self.filename
    
def unzip(source_filename, dest_dir):
    with zipfile.ZipFile(source_filename) as zf:
        zf.extractall(dest_dir)

def unrar(source_filename, dest_dir):
    with rarfile.RarFile(source_filename) as rf:
        rf.extractall(dest_dir)

def is_image(filename):
    valid_image_extensions = ['.png', '.jpg', '.bmp']
    if os.path.splitext(filename)[1].lower() in valid_image_extensions:
        return True
    else:
        return False

def add_comic():
    FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
    path = os.path.normpath('library')
    if os.path.isdir(path):
        subprocess.run([FILEBROWSER_PATH, path])
    else:
        os.mkdir('library')
        subprocess.run([FILEBROWSER_PATH, path])