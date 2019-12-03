# PDF Renamefy
PDF Renamefy is very simple script for Python 3 that finds all the PDF file in a given root directory and its sub-directories,
parses the title of each one from its metadata and renames it accordingly.

###Usage:
Before using it for the first time, install the dependencies by running the following command:
```
$pip install -r requirements.txt
```
and then to run the script:
```
$python -m renamefy <directory> <filename maximum length>
```

...in which **directory** is the full path you would like to look for PDF files, and **filename maximum length**
is the length at which the filename will be truncated in case the title is too long or was incorrectly set.

If no parameter is passed, **directory** is set to the current directory and **filename maximum length** is set to
**120** characters.

###Requirements:
* `colorama>=0.4.1`
* `coloredlogs>=10.0`
* `humanfriendly>=4.18`
* `pdfrw==0.4`
* `pyreadline>=2.1`
* `tqdm>=4.40.0`
* `verboselogs>=1.7`

