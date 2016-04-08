## Build

Clone both `ccv` and `py-ccv`:

```
mkdir ccv_build
cd ccv_build
git clone https://github.com/liuliu/ccv
git clone https://github.com/gpip/py-ccv
```

Patch `ccv` so it can be compiled as a dynamic lib, and compile it:

```
cd ccv/lib
patch -p2 < ../../py-ccv/dynlib.patch
cd ccv/lib
./configure
make libccv.so
```

Build the Python wrapper (`ARCHFLAGS` was used on a OSX build, adjust for your platform):

```
cd ../../py-ccv
ARCHFLAGS='-arch x86_64' INCDIR=../ccv/lib LIBDIR=../ccv/lib python build_wrapper.py
```


## Usage

(`DYLD_LIBRARY_PATH` was used on OSX, adjust it for your platform)

##### Face detection using SCD

```
$ DYLD_LIBRARY_PATH=../ccv/lib python face_detect.py -c ../ccv/samples/face.sqlite3 img/lena.png
Feature(x=229, y=216, width=152, height=152, confidence=5.014610767364502)
```

##### Face detection using BBF

```
$ DYLD_LIBRARY_PATH=../ccv/lib python face_detect.py --bbf -c ../ccv/samples/face img/lena.png
Feature(x=230, y=211, width=154, height=154, confidence=0.4947386682033539)
```

##### Help

```
$ DYLD_LIBRARY_PATH=../ccv/lib python face_detect.py --help
Usage: face_detect.py [options] filename...

Options:
  -h, --help            show this help message and exit
  --bbf                 Use BBF detector
  --scd                 Use SCD detector
  -c CASCADE, --cascade=CASCADE
                        Path to cascade to read
  --quiet
```
