from cx_Freeze import setup, Executable
import os


#os.environ['TCL_LIBRARY'] = "C:\\Users\\marit\\AppData\\Local\\Programs\\Python\\Python36\\tcl\\tcl8.6"
#os.environ['TK_LIBRARY'] = "C:\\Users\\marit\\AppData\\Local\\Programs\\Python\\Python36\\tcl\\tk8.6"

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

base = None

additional_mods = ['numpy.core._methods', 'numpy.lib.format']
executables = [Executable("start.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {
        'packages': packages,
        'includes': additional_mods,
        'include_files': [
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
        ],
    },
}

setup(
    name="<any name>",
    options=options,
    version="<any number>",
    description='<any description>',
    executables=executables
)
