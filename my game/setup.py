import sys
from cx_Freeze import setup, Executable

options = {
    "build_exe": {
	"include_files":["images","scores.txt"]
    }
}

executables = [Executable("game.py")]
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="ninja attack to castle",
    version="0.1",
    description="MY game made to attack castle",
    options=options,
    executables=executables,
)