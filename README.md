# gui-template

Template repository for a PyQt5 GUI app.

The application is started with `python app.py`

`build.py` creates a stand-alone application that is compiled with `nuitka`.
InnoSetup is used to create an installer (`ISCC.exe` must be in `PATH`) .


## TODO

* `%APPDATA%/App name/data/log.txt` is left after uninstalling the compiled version
* The icons are copied from Google image search (and inverted), might be an issue