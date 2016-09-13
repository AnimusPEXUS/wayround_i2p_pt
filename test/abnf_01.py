
import os.path
import pprint
import collections

import wayround_org.pt.abnf_abnf_h


def main():

    filename = os.path.normpath(
        os.path.join(
            __file__,
            '..',
            '..',
            'wayround_org',
            'pt',
            'abnf.abnf'
            )
        )

    print("going to parse file: {}".format(filename))

    if not os.path.isfile(filename):
        raise Exception("file not found: {}".format(filename))

    with open(filename) as f:
        txt = f.read()

    error_log = []

    res = wayround_org.pt.abnf_abnf_h.parse(txt, error_log)

    if res is not None:
        print("parsing complete")

        pprint.pprint(
            res.render_dict(
                dict_constructor=collections.OrderedDict,
                slice_text=txt
                )
            )

    else:
        print("parsing failed")

        print("{} error(s)".format(len(error_log)))

        for i in error_log:
            print("{}: {}".format(i.index0, i.text))

    return res


if __name__ == '__main__':
    exit(main())
