# stlprintbrowser

Simple app for collecting and browsing miniature files for 3D printing

In config.ini file change database path to suitable for you

python _run.py_ to run application  

python _import_stl_model.py_ [parameters] [directory] to import data from folder to database (this script treats one folder as one model) 

Parameters:

- --m - directories in directory are treated as models and all of them are imported
- --a "author" - author for imported models
- --n "name prefix" - additional prefix will be added to name
- --t "tags" - tags added to imported model(s) ';' is separator