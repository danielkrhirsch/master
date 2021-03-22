import platform

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import os.path

if platform.architecture()[0] == "64bit":
    libdir = "stream_engine/lib/x64/"
elif platform.architecture()[0] == "32bit":
    libdir = "stream_engine/lib/x32/"
else:
    raise ValueError("could not determine 64 or 32 bits")


stream_engine_extension = Extension(
    name="stream_engine",
    sources=["cython/stream_engine.pyx"],
    libraries=["tobii_stream_engine"],
    library_dirs=[libdir],
    include_dirs=["stream_engine/include/tobii"],
    runtime_library_dirs=[libdir]
)

setup(
    ext_modules = cythonize([stream_engine_extension])
)
