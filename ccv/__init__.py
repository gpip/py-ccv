import os
from collections import namedtuple

from _ccv import ffi, lib

Feature = namedtuple("Feature", "x1 y1 x2 y2 confidence")

_matrix_ref = lambda ptr: ffi.gc(ptr, lib.ccv_matrix_free)

def _check_datatype(dtype):
    if not dtype:
        return  # CCV will make a guess.
    assert dtype & 0xFF000, "Invalid data type: %d" % dtype


def ccv_read(inp, ttype=None, rows=0, cols=0, scanline=0):
    """
    Read an image from a filename specified by inp and a matching ttype.

    Returns an internal ccv_dense_matrix_t*
    """
    if ttype is None:
        ttype = lib.CCV_IO_RGB_COLOR | lib.CCV_IO_ANY_FILE

    image = ffi.new('ccv_dense_matrix_t*[1]')
    res = lib.ccv_read_impl(inp, image, ttype, rows, cols, scanline)
    if res != lib.CCV_IO_FINAL:
        raise Exception("Failed to read %s with ttype %d: %d" % (inp, ttype, res))
    if image[0] == ffi.NULL:
        raise Exception("NULL image")
    return _matrix_ref(image[0])


def ccv_slice(inp, x, y, rows, cols, ttype=0):
    """
    Slice an input matrix given offsets x and y, and number of rows
    and columns. A new matrix is returned.
    """
    _check_datatype(ttype)
    output = ffi.new('ccv_matrix_t*[1]')
    lib.ccv_slice(inp, output, ttype, y, x, rows, cols)
    if output[0] == ffi.NULL:
        raise Exception("NULL output")
    return _matrix_ref(output[0])


def ccv_array_get(array, index, cast_to='ccv_comp_t*'):
    arr = array.data + (array.rsize * index)
    return ffi.cast(cast_to, arr)


def ccv_write(im, outname):
    ext = os.path.splitext(outname)[1].lower()
    if ext in ('.jpeg', '.jpg'):
        outtype = lib.CCV_IO_JPEG_FILE
    elif ext == '.bmp':
        outtype = lib.CCV_IO_BMP_FILE
    elif ext == '.png':
        outtype = lib.CCV_IO_PNG_FILE
    else:
        raise Exception("Unknown extension %r" % ext)

    res = lib.ccv_write(im, outname, ffi.NULL, outtype, ffi.NULL)
    if res != lib.CCV_IO_FINAL:
        raise Exception("Failed to write %s: %d" % (outname, res))


def sobel(im, mtype, dx=1, dy=1):
    if (dx and not dx % 2) or (dy and not dy % 2):
        raise Exception("dx and dy must be odd if specified")
    if not dx and not dy:
        raise Exception("both dx and dy are missing")
    _check_datatype(mtype)

    output = ffi.new('ccv_dense_matrix_t*[1]')
    lib.ccv_sobel(im, output, mtype, dx, dy)
    if output[0] == ffi.NULL:
        raise Exception("NULL output")
    return _matrix_ref(output[0])


def gradient(im, dx=1, dy=1):
    if not dx % 2 or not dy % 2:
        raise Exception("dx and dy must be odd")

    theta = ffi.new('ccv_dense_matrix_t*[1]')
    magnitude = ffi.new('ccv_dense_matrix_t*[1]')
    lib.ccv_gradient(im, theta, 0, magnitude, 0, dx, dy)
    if theta[0] == ffi.NULL or magnitude[0] == ffi.NULL:
        raise Exception("NULL output")
    return _matrix_ref(theta[0]), _matrix_ref(magnitude[0])


def visualize(mat, outtype=0):
    """
    Convert an input matrix into a matrix within visual range,
    so that one can output it into PNG or similar.
    """
    _check_datatype(outtype)
    output = ffi.new('ccv_matrix_t*[1]')
    lib.ccv_visualize(mat, output, outtype)
    if output[0] == ffi.NULL:
        raise Exception("NULL output")
    return _matrix_ref(output[0])


def prepare_scd_cascade(inp):
    casc = ffi.new('ccv_scd_classifier_cascade_t*[1]')
    casc[0] = lib.ccv_scd_classifier_cascade_read(inp)
    if casc[0] == ffi.NULL:
        raise Exception("Failed to read SCD cascade from %s" % inp)
    return ffi.gc(casc, lambda x: lib.ccv_scd_classifier_cascade_free(x[0]))


def prepare_bbf_cascade(inp):
    casc = ffi.new('ccv_bbf_classifier_cascade_t*[1]')
    casc[0] = lib.ccv_bbf_read_classifier_cascade(inp)
    if casc[0] == ffi.NULL:
        raise Exception("Failed to read BBF cascade from %s" % inp)
    return ffi.gc(casc, lambda x: lib.ccv_bbf_classifier_cascade_free(x[0]))


def scd_detect_objects(filename, cascade):
    """
    SURF-Cascade object detection. This can be used for face recognition.

    Returns a list of Features.
    """
    ttype = lib.CCV_IO_RGB_COLOR | lib.CCV_IO_ANY_FILE
    assert ttype == 800
    image = ccv_read(filename, ttype)

    rects = []
    faces = lib.ccv_scd_detect_objects(image, cascade, 1, lib.ccv_scd_default_params)
    for i in xrange(faces.rnum):
        entry = ccv_array_get(faces, i)
        rect = entry.rect
        rects.append(Feature(rect.x, rect.y, rect.x + rect.width, rect.y + rect.height,
                             entry.classification.confidence))

    lib.ccv_array_free(faces)
    return rects


def bbf_detect_objects(filename, cascade):
    """
    Brightness Binary Feature object detection. This can be used for face recognition.

    Returns a list of Features.
    """
    lib.ccv_enable_default_cache()

    image = ccv_read(filename, lib.CCV_IO_GRAY | lib.CCV_IO_ANY_FILE)

    rects = []
    seq = lib.ccv_bbf_detect_objects(image, cascade, 1, lib.ccv_bbf_default_params)
    for i in xrange(seq.rnum):
        comp = ccv_array_get(seq, i)
        rect = comp.rect
        rects.append(Feature(rect.x, rect.y, rect.x + rect.width, rect.y + rect.height,
                             comp.classification.confidence))

    lib.ccv_array_free(seq)

    lib.ccv_disable_cache()
    return rects
