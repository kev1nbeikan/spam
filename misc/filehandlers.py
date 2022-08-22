import logging
import os
from os import mkdir
from os.path import exists


class FileHandlerBase:
    def open(self, file):
        pass

    def exists(self, file):
        pass

    def mkdir(self, path):
        pass

    def remove(self, file):
        pass

    def zp_extract(self, zp, path):
        pass


class LocalFileHandler(FileHandlerBase):
    def open(self, file):
        return open(file)

    def exists(self, file):
        return exists(file)

    def mkdir(self, path):
        if not self.exists(path):
            mkdir(path)

    def remove(self, file):
        if self.exists(file):
            try:
                os.remove(file)
            except:
                return

    def zp_extract(self, zp, path):
        zp.extractall(path)

    def listdir(self, path):
        if self.exists(path):
            return os.listdir(path)
        return []

    def remove_all_from_dir(self, path: str):
        print(self.listdir(path))
        if not path.endswith('/'):
            path += '/'
        for file in self.listdir(path):
            self.remove(path + file)