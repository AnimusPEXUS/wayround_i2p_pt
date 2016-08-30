
import regex
import itertools


class Rules:

    def __init__(self, rules, parents=None):

        if parents is None:
            parents = []

        if not isinstance(parents, list):
            raise TypeError("`parents' must be list of Rules")

        for i in parents:
            if not isinstance(i, Rules):
                raise TypeError("`parents' must be list of Rules")

        self._rules = {}

        for i in parents:
            for j in i:
                if j in self._rules:
                    raise Exception(
                        "error: parent `{}' resets rule `{}'".format(
                            i,
                            j
                            )
                        )
                self._rules[j] = i[j]

        for i in rules:
            if i in self._rules:
                raise Exception(
                    "`rules' param trying reset parent's rule `{}'".format(i)
                    )
            self._rules[i] = rules[i]

        return

    def __iter__(self):
        ret = iter(self._rules)
        return ret

    def __getitem__(self, key):

        ret = self._rules[key]

        ret = ret.format_map(self._rules)

        return ret

    def __len__(self):
        ret = len(self._rules)
        return ret

    def __contains__(self, key):
        ret = key in self._rules
        return ret

    def keys(self):
        ret = self._rules.keys()
        return ret


def and_(text, start, parser_list):

    ret = []

    for i in parser_list:

        res = i(text, start)

        if not isinstance(res, wayround_org.parserconstructor.ast.Node):
            ret = None

        if ret is None:
            break

        if ret is not None:
            ret.append(res)

    return ret


def or_(text, start, parser_list):
    """
    return: None or list with one and only one element
    """

    ret = []

    for i in parser_list:

        res = i(text, loop_start)

        if isinstance(res, wayround_org.parserconstructor.ast.Node):
            ret.append(res)
            break

    if len(ret) == 0:
        ret = None

    return ret


def any_number(text, start, callback, *args, **kwargs):
    """
    text and start are passed to callback inconditionally. args and kwargs may
    be passed by your desire
    """

    ret = []

    while True:

        res = callback(text, start, *args, **kwargs)

        if is None:
            break

        for i in res:
            ret.append(i)

    return ret


def parse_next_re(text, start, re_, name='string'):
    """
    creates special ast node representing simple string. matching text directly

    if re_ is str - it will be compiled with regex.compile().

    re_ may be result of re.compile() or regex.compile().

    In any case, if re_ is not string, this function tries to call it's
    .match() method.
    """

    ret = wayround_org.parserconstructor.ast.Node()
    ret.name = name

    if isinstance(re_, str):
        re_ = regex.compile(re_)

    res = re_.match(text, pos=start)

    if res is None:
        ret = None

    if ret is not None:
        ret.index0 = res.start()
        ret.index1 = res.end()

    return ret

