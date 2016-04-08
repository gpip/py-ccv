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
./configure
make libccv.so
```

Build the Python wrapper (`ARCHFLAGS` was used on a OSX build, adjust for your platform):

```
cd ../../py-ccv
pip install -r requirements.txt
ARCHFLAGS='-arch x86_64' INCDIR=../ccv/lib LIBDIR=../ccv/lib python build_wrapper.py
```


## Face Detection Usage

(`DYLD_LIBRARY_PATH` was used on OSX, adjust it for your platform)

##### Face detection using SCD

```
$ DYLD_LIBRARY_PATH=../ccv/lib python face_detect.py -c ../ccv/samples/face.sqlite3 img/lena.png
img/lena.png Feature(x1=229, y1=216, x2=381, y2=368, confidence=5.014610767364502)
```

##### Face detection using BBF

```
$ DYLD_LIBRARY_PATH=../ccv/lib python face_detect.py --bbf -c ../ccv/samples/face img/lena.png
img/lena.png Feature(x1=230, y1=211, x2=384, y2=365, confidence=0.4947386682033539)
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

##### Using face_detect as a library

```
import face_detect

names = ['img/lena.png']
result = face_detect.main('scd', '../ccv/samples/face.sqlite3', False, *names)

# face_detect.main is a generator which yields tuples of
# (<filename>, [<list of face_detect.Feature>])
for name, rects in result:
    print name, rects
```


##### Visualization

This wrapper does not include an utility to draw the resulting rectangles, so the following example uses ImageMagick:

```
$ convert img/lena.png -fill none -stroke blue -strokewidth 3 -draw "rectangle 229,216 381,368" result.png
```

![](http://i.imgur.com/yzcxwqk.png)


## Using the library

```
import sys
from ccv import ccv_read, ccv_write, sobel, lib

# Read file passed.
inp = ccv_read(sys.argv[1])
# Apply Sobel.
res = sobel(inp, lib.CCV_8U | lib.CCV_C1)
# Save the result as "sobel.jpg"
ccv_write(res, "sobel.jpg")
```

Pointers returned by the higher level wrapper, `ccv`, are automatically freed.
