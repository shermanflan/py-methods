from glob import glob
import os


# TODO: Add exception handling
def rm(file_path):
    batches = glob(file_path)

    for f in batches:
        os.remove(f)
