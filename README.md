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

Build and install the Python wrapper (`ARCHFLAGS` was used on a OSX build, adjust for your platform):

```
cd ../../py-ccv
ARCHFLAGS='-arch x86_64' INCDIR=../ccv/lib LIBDIR=../ccv/lib python setup.py install
```

## Build only this wrapper

If you already have `libccv.so` then you might want to install directly via pip:

```
LDFLAGS="-L$(pwd)/ccv/lib" CFLAGS="-I$(pwd)/ccv/lib" pip install ccv
```

Remember to adjust the paths according to where `libccv.so` and `ccv.h` are installed in your system.


## Face Detection Usage

(`DYLD_LIBRARY_PATH` was used on OSX, adjust it for your platform)

##### Face detection using SCD

```
$ DYLD_LIBRARY_PATH=../ccv/lib python -m ccv.face_detect -c ../ccv/samples/face.sqlite3 img/lena.png
img/lena.png Feature(x1=229, y1=216, x2=381, y2=368, confidence=5.014610767364502)
```

##### Face detection using BBF

```
$ DYLD_LIBRARY_PATH=../ccv/lib python -m ccv.face_detect --bbf -c ../ccv/samples/face img/lena.png
img/lena.png Feature(x1=230, y1=211, x2=384, y2=365, confidence=0.4947386682033539)
```

##### Help

```
$ DYLD_LIBRARY_PATH=../ccv/lib python -m ccv.face_detect.py --help
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
from ccv import face_detect

names = ['img/lena.png']
result = face_detect.main('scd', '../ccv/samples/face.sqlite3', False, *names)

# face_detect.main is a generator which yields tuples of
# (<filename>, [<list of face_detect.Feature>])
for name, rects in result:
    print name, rects
```


##### Visualization

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
res = sobel(inp, lib.CCV_8U)
# Save the result as "sobel.jpg"
ccv_write(res, "sobel.jpg")
```

Pointers returned by the higher level wrapper, `ccv`, are automatically freed.

##### Functions available from `import ccv`

###### `ccv.ccv_read(filename, ttype=None)`
Read an image from a filename and return an internal `ccv_dense_matrix_t*`.
`ttype` can be specified to typically convert the input image to grayscale: `ttype=ccv.lib.CCV_IO_GRAY | ccv.lib.CCV_IO_ANY_FILE`.

---

###### `ccv.ccv_write(im, outname)`
Write an image (returned from `ccv_read` or other compatible functions) to a filename specified by `outname`.

---

###### `ccv.ccv_slice(im, x, y, rows, cols)`
Slice an input matrix given offsets `x` and `y`, and number of `rows` and columns. A new matrix is returned.

> `ccv_slice` can be used to effectively crop a region of an input image and return a cropped image.

---

###### `ccv.sobel(im, ttype, dx=1, dy=1)`
Apply the Sobel operator to the input and return a new matrix. `dx` and `dy` dictate the window size for the operator, and is optimized for values of `1` and `3`. `ttype` defined the type of the output matrix, which for typical images should be set to `ccv.lib.CCV_8U`.

---

###### `ccv.gradient(im, dx=1, dy=1)`
Compute the gradient at each pixel and return, respectively, theta and magnitude matrices of type `ccv.lib.CCV_32F`. Typically, these matrices will be converted via `ccv.visualize` if you want to visually inspect them.

---

###### `ccv.visualize(mat)`
Convert an input matrix into a matrix within visual range.

---

###### `ccv.prepare_scd_cascade(inp)`
Read SCD classifier cascade from `inp` and return a `ccv_scd_classifier_cascade_t*`.

---

###### `ccv.prepare_bbf_cascade(inp)`
Read BBF classifier cascade from `inp` and return a `ccv_bbf_classifier_cascade_t*`.

---

###### `ccv.scd_detect_objects(filename, cascade)`
Use SURF-Cascade object detection by reading an image from `filename` and using the `cascade` obtained from `ccv.prepare_scd_cascade`. A list of `ccv.Feature` is returned.

---

###### `ccv.bbf_detect_objects(filename, cascade)`
Use Brightness Binary Feature object detection by reading an image from `filename` and using the `cascade` obtained from `ccv.prepare_bbf_cascade`. A list of `ccv.Feature` is returned.

---

###### `ccv.Feature`
A namedtuple with parameters `x1`, `y1`, `x2`, `y2`, and `confidence`.
