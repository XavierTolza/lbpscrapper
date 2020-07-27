import sys
from os.path import abspath, join, dirname, isdir, basename

__project_name__ = basename(dirname(abspath(__file__)))
__data_folder__ = abspath(join(dirname(abspath(__file__)), f"../{__project_name__}/data"))
if not isdir(__data_folder__):
    __data_folder__ = join(sys.prefix, __project_name__)
if not isdir(__data_folder__):
    raise ValueError("Cannot data folder: %s" % __data_folder__)

del abspath, join, dirname, isdir, basename