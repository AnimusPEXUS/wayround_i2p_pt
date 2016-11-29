
import os.path
import pprint
import collections

import yaml

import wayround_i2p.pt.abnf_abnf_h


def main():

    ret = 0

    filename = os.path.normpath(
        os.path.join(
            __file__,
            '..',
            '..',
            'wayround_i2p',
            'pt',
            'abnf.abnf'
            )
        )

    filename_out = os.path.normpath(
        os.path.join(
            __file__,
            '..',
            'abnf_01_work_result.yaml'
            )
        )

    print("input: {}".format(filename))
    print("output: {}".format(filename_out))

    if not os.path.isfile(filename):
        raise Exception("file not found: {}".format(filename))

    with open(filename) as f:
        txt = f.read()

    error_log = []

    res = wayround_i2p.pt.abnf_abnf_h.parse(txt, error_log)

    if res is not None:

        print("parsed ok")

        res.text = txt

        with open(filename_out, 'w') as f:
            f.write(
                yaml.dump(
                    res.render_dict(
                        #dict_constructor=collections.OrderedDict,
                        )
                    )
                )

    else:

        ret = 1

        print("parsing failed")

        print("{} error(s)".format(len(error_log)))

        for i in error_log:
            print("{}: {}".format(i.index0, i.text))

    return ret


if __name__ == '__main__':
    exit(main())
