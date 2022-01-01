import os

def try_remove_file(path: str):
    try:
        os.unlink(path)
    except OSError:
        if os.path.exists(path):
            print('Error: could not unlink socket file')