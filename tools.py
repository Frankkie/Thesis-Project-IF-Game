"""
Some useful functions for file management.

Functions:
    copytree(scr, dst, symlinks=False, ignore=None):
        Copy all the contents of directory scr to directory dst.
    empty_folder(folder):
        Empty the directory folder from all subfolders and files.

"""


import os
import shutil


def copytree(src, dst, symlinks=False, ignore=None):
    """
    Copy all the contents of directory scr to directory dst.

    :param src: String
        Source directory.
    :param dst: String
        Destination directory.
    :param symlinks: default False
    :param ignore: default None
    :return: None

    """
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


def empty_folder(folder):
    """
    Empty the directory folder from all subfolders and files.
    Print a diagnostic message if the directory cannot be emptied for any reason.

    :param folder: string
        The dir to be emptied.
    :return:

    """
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))