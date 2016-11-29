
import os.path
import pprint
import collections

import yaml

import wayround_i2p.pt.abnf_abnf_h
import wayround_i2p.pt.abnf_pg
import wayround_i2p.pt.ast


def main():

    filename = os.path.normpath(
        os.path.join(
            __file__,
            '..',
            'abnf_01_work_result.yaml'
            )
        )

    print("going to load file: {}".format(filename))

    if not os.path.isfile(filename):
        raise Exception("file not found: {}".format(filename))

    with open(filename) as f:
        res = f.read()

    print("parsing yaml")
    res = yaml.load(res)

    if res is None:
        raise Exception("couldn't load file contents")

    print("loading node")
    res = wayround_i2p.pt.ast.Node.new_from_dict(res)

    print("starting module renderer")
    wayround_i2p.pt.abnf_pg.render_module(
        'abnf_02_work_result.py',
        res,
        []
        )

    return 1


if __name__ == '__main__':
    exit(main())
