
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

    with open(filename) as f:
        txt = f.read()

    res = wayround_org.parserconstructor.abnf_abnf_h.parse(txt)

    return res


if __name__ == '__main__':
    exit(main())
