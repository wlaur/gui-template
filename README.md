# gui-template

Template repository for a PyQt5 GUI app.

The application is started with `python app.py`


The UI layouts are defined as `.ui` files that can be edited using Qt Designer.
`python build.py ui` will convert the files to `.py`-modules that can be used in the application.

`python build.py compile` creates a stand-alone application that is compiled with `nuitka`.
InnoSetup is used to create an installer (`ISCC.exe` must be in `PATH`) .


## TODO

* `%APPDATA%/App name/data/log.txt` is left after uninstalling the compiled version
* The icons are copied from Google image search (and inverted), might be an issue