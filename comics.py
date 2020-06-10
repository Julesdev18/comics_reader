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

    def generate_metadata(self, name, author='<Unknown>', tags='', quality='-/10'):
        library = {}
        try:
            with open('library/library.json') as library_json:
                library = json.load(library_json)
        except:
            with open('library/library.json', 'w') as library_json:
                json.dump(library, library_json)
            with open('library/library.json') as library_json:
                library = json.load(library_json)
        library[name] = {
            'author': author,
            'tags': tags,
            'quality': quality
        }
        with open('library/library.json', 'w') as library_json:
            json.dump(library, library_json)
    
    def getMetadata(self, name):
        creation_time = time.ctime(os.path.getctime(self.filename))
        year = creation_time.split()[-1]

        file_metadata = {}
        with open('library/library.json') as library_json:
            try:
                library = json.load(library_json)
                if name in library:
                    file_metadata = library[name]

                    self._metadata = {
                        'title': name,
                        'author': file_metadata['author'],
                        'year': year,
                        'tags': file_metadata['tags'],
                        'quality': file_metadata['quality']
                    }
                self._metadata['year'] = year
            except:
                self._metadata['year'] = year
            return self._metadata
    
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
