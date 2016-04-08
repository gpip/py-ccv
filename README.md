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
Feature(x1=229, y1=216, x2=381, y2=368, confidence=5.014610767364502)
```

##### Face detection using BBF

```
$ DYLD_LIBRARY_PATH=../ccv/lib python face_detect.py --bbf -c ../ccv/samples/face img/lena.png
Feature(x1=230, y1=211, x2=384, y2=365, confidence=0.4947386682033539)
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

##### Using as a library

```
import face_detect

result = face_detect.main('scd', '../ccv/samples/face.sqlite3', False,
                          # Specify one or more filenames now
                          'img/lena.png')

# face_detect.main returns a dict containing
# {<filename>: <list of face_detect.Feature>}
for name, rects in result.iteritems():
    print name, rects
```


##### Visualize

This wrapper does not include an utility to draw the resulting rectangles, so the following example uses ImageMagick:

```
$ convert img/lena.png -fill none -stroke blue -strokewidth 3 -draw "rectangle 229,216 381,368" result.png
```
