
import os.path

import wayround_org.parserconstructor.abnf_abnf_h


def main():

    filename = os.path.normpath(
        os.path.join(
            __file__,
            '..',
            '..',
            'wayround_org',
            'parserconstructor',
            'abnf.abnf'
            )
        )

    print("going to parse file: {}".format(filename))

    if not os.path.isfile(filename):
        raise Exception("file not found: {}".format(filename))

    with open(filename) as f:
        txt = f.read()

    error_log = []

    res = wayround_org.parserconstructor.abnf_abnf_h.parse(txt, error_log)

    if len(error_log) != 0:
        print("{} error(s)".format(len(error_log)))

    for i in error_log:
        print("{}: {}".format(i.index0, i.text))

    return res


if __name__ == '__main__':
    exit(main())
