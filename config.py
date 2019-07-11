import platform

name = "PyMCRTPC"
version = "v0.1"

if platform.system() == "Windows":
    system = "win"
elif platform.system() == "Darwin":
    system = "osx"
else:
    system = "linux"