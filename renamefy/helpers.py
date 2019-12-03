from fnmatch import fnmatch
import os
import random
import string
from unicodedata import normalize


def format_string(raw_string):
    raw_string = str(normalize('NFKD', raw_string)).encode('ASCII', 'ignore').decode('ASCII').lower().replace(' ', '_')
    final_string = ''.join(
        [c if ((c.isascii() and c.isalnum()) or c == "_") else "" for c in raw_string]
    )
    return final_string


def generate_random_string(string_length):
    alphabet = string.ascii_letters
    random_string = ''.join(random.choice(alphabet) for i in range(string_length))
    return random_string


def get_filenames(root):
    pattern = '*.pdf'
    filenames = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            if fnmatch(name, pattern):
                filenames.append({'path': path, 'filename': name})
    return filenames