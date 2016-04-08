from optparse import OptionParser
from collections import namedtuple

from _ccv import ffi, lib

Feature = namedtuple("Feature", "x1 y1 x2 y2 confidence")


def ccv_read(inp, ttype, rows=0, cols=0, scanline=0):
    """
    Read an image from a filename specified by inp and a matching ttype.

    Returns an internal ccv_dense_matrix_t*
    """
    image = ffi.new('ccv_dense_matrix_t*[1]')
    lib.ccv_read_impl(inp, image, ttype, rows, cols, scanline)
    if image[0] == ffi.NULL:
        raise Exception("Failed to read %s with ttype %d" % (inp, ttype))
    return image[0]


def prepare_scd_cascade(inp):
    casc = ffi.new('ccv_scd_classifier_cascade_t*[1]');
    casc[0] = lib.ccv_scd_classifier_cascade_read(inp)
    if casc[0] == ffi.NULL:
        raise Exception("Failed to read SCD cascade from %s" % inp)
    return casc


def prepare_bbf_cascade(inp):
    casc = ffi.new('ccv_bbf_classifier_cascade_t*[1]');
    casc[0] = lib.ccv_bbf_read_classifier_cascade(inp)
    if casc[0] == ffi.NULL:
        raise Exception("Failed to read BBF cascade from %s" % inp)
    return casc


def ccv_array_get(array, index, cast_to='ccv_comp_t*'):
    arr = array.data + (array.rsize * index)
    return ffi.cast(cast_to, arr)


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
    lib.ccv_matrix_free(image)
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
    lib.ccv_matrix_free(image)

    lib.ccv_disable_cache()
    return rects


def main(classifier, cascade, verbose, *filenames):
    if classifier == 'scd':
        cascade = prepare_scd_cascade(cascade)
        detector = scd_detect_objects
    else:
        cascade = prepare_bbf_cascade(cascade)
        detector = bbf_detect_objects

    result = {}
    for name in filenames:
        # face recognition
        r = detector(name, cascade)
        result[name] = r
        if not verbose:
            continue
        for x in r:
            print x

    if classifier == 'scd':
        lib.ccv_scd_classifier_cascade_free(cascade[0])
    else:
        lib.ccv_bbf_classifier_cascade_free(cascade[0])

    return result


if __name__ == "__main__":
    usage = "usage: %prog [options] filename..."
    parser = OptionParser(usage=usage)
    parser.add_option('--bbf', dest='bbf', action="store_true",
        help='Use BBF detector')
    parser.add_option('--scd', dest='scd', action="store_true",
        help='Use SCD detector')
    parser.add_option('-c', '--cascade', dest='cascade',
        help='Path to cascade to read')
    parser.add_option('--quiet', dest='quiet', action="store_true")
    options, args = parser.parse_args()
    if not options.bbf and not options.scd:
        options.scd = True

    if options.bbf and options.scd:
        parser.error("pick one between --bbf and --scd")
    if not options.cascade:
        parser.error("no cascade specified")

    if not args:
        parser.error("no filenames to read")

    classifier = 'bbf' if options.bbf else 'scd'
    cascade = options.cascade
    verbose = not options.quiet

    main(classifier, cascade, verbose, *args)
