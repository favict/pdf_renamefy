#!/usr/bin/env python

"""

PDF Renamefy is very simple script for Python 3 that finds all the PDF file in a given root directory and its
sub-directories, parses the title of each one from its metadata and renames it accordingly.

"""

import os
import sys

from pdfrw import PdfReader
from pdfrw.errors import PdfParseError
from tqdm import tqdm

from renamefy.helpers import format_string, generate_random_string, get_filenames
from renamefy.log import logging, TrackProgress


def rename_file(filename_max_length, path, filename):
    full_name = os.path.join(path, filename)

    try:
        pdf_title = PdfReader(full_name).Info.Title
    except (PdfParseError, AttributeError):
        TrackProgress.failure += 1
    else:
        if isinstance(pdf_title, str) and len(pdf_title) > 0:
            new_name = format_string(pdf_title)[:filename_max_length]
            new_full_name = os.path.join(path, new_name + '.pdf')
            try:
                os.rename(full_name, new_full_name)
            except FileExistsError:
                TrackProgress.file_exists += 1
                random_tag = generate_random_string(5)
                os.rename(full_name, os.path.join(path, new_name) + "_" + random_tag + '.pdf')
            finally:
                TrackProgress.success += 1
        else:
            TrackProgress.failure += 1
    finally:
        return None


def renamefy():
    args = sys.argv

    if len(args) == 1:
        logging.info('No parameters detected, running defaults (path=current_dir, filename_max_length=120)')

    if 1 <= len(args) <= 3:
        default_filename_length_limit = 120
        filename_length_limit = int(next((x for x in args if x.isdigit()), default_filename_length_limit))

        default_lookup_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        lookup_dir = r'{}'.format(next((x for x in args[1:] if not x.isdigit()), default_lookup_dir))

        path_is_absolute = os.path.exists(lookup_dir)
        path_is_relative = os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)), lookup_dir))

        if path_is_absolute or path_is_relative:
            pdf_files = get_filenames(lookup_dir)
            if len(pdf_files) > 0:
                logging.info("Starting to work on {}".format(lookup_dir))

                for file in tqdm(pdf_files):
                    rename_file(filename_length_limit, **file)

                end_message = "\n {} PDF files were renamed \n\t{} of which already existed\n {} " \
                              "failed because no title was found "

                logging.log(level=35, msg=end_message.format(
                    TrackProgress.success,
                    TrackProgress.file_exists,
                    TrackProgress.failure,
                    )
                )
            else:
                logging.warning("No PDF files were found in {}, exiting...".format(lookup_dir))
        else:
            logging.error("'{}' is not a valid path, try again.".format(args[1]))
    else:
        logging.error("Invalid parameters. Usage: python {} <directory> <filename_max_length>".format(__file__))


if __name__ == "__main__":
    renamefy()
