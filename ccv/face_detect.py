from optparse import OptionParser

import ccv


def main(classifier, cascade, verbose, *filenames):
    if classifier == 'scd':
        cascade = ccv.prepare_scd_cascade(cascade)
        detector = ccv.scd_detect_objects
    elif classifier == 'bbf':
        cascade = ccv.prepare_bbf_cascade(cascade)
        detector = ccv.bbf_detect_objects
    else:
        raise Exception('Unknown classifier %r' % classifier)

    for name in filenames:
        # face recognition
        r = detector(name, cascade)
        yield (name, r)
        if not verbose:
            continue
        for x in r:
            print name, x


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

    list(main(classifier, cascade, verbose, *args))
