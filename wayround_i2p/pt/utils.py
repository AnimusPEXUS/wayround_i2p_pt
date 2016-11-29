
import regex
import itertools

import wayround_i2p.pt.ast


RULENAME_RE = (
    r'\{'
    r'([\x41-\x5A]|[\x61-\x7A])'
    r'((([\x41-\x5A]|[\x61-\x7A]))|([\x30-\x39])|-)*'
    r'\}'
    )
RULENAME_RE_C = regex.compile(RULENAME_RE)


class ErrorNote:

    def __init__(self, text, index0, index1=None):
        if index1 is None:
            index1 = index0
        self.text = text
        self.index0 = index0
        self.index1 = index1
        return


class _RuleC:

    def __init__(self, rules):
        if not isinstance(rules, Rules):
            raise TypeError("`rules' must be Rules inst")
        self._rules = rules
        self._c = {}
        return

    def __getitem__(self, key):
        if key in self._c:
            ret = self._c[key]
        else:
            ret = regex.compile(self._rules[key])
            self._c[key] = ret
        return ret


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
        self._res = {}

        for parent in parents:
            for rule in parent:
                if rule in self.rule_raw:
                    raise Exception(
                        "error: parent `{}' resets rule `{}'".format(
                            parent,
                            rule
                            )
                        )
                self._rules[rule] = parent[rule]

        for i in rules:
            if i in self._rules:
                raise Exception(
                    "`rules' param trying reset parent's rule `{}'".format(i)
                    )
            self._rules[i] = rules[i]

        self.compiled = _RuleC(self)

        return

    @property
    def rule_raw(self):
        return self._rules

    def __iter__(self):
        ret = iter(self._rules)
        return ret

    def __getitem__(self, key):

        if key in self._res:
            ret = self._res[key]

        else:
            ret = self._rules[key]

            count_down = 10

            while RULENAME_RE_C.search(ret) is not None:
                ret = ret.format_map(self._rules)
                count_down -= 1

                if count_down == -1:
                    raise RecursionError("depth limit reached")

            self._res[key] = ret

        return ret

    def __len__(self):
        ret = len(self._rules)
        return ret

    def __contains__(self, key):
        ret = key in self._rules
        return ret

    def keys(self):
        ret = list(self._rules.keys())
        return ret


def and_(text, start, error_log, parser_list):

    check_parser_list(parser_list)

    ret = []

    for i in parser_list:

        res = i(text, start, error_log)

        if not isinstance(res, wayround_i2p.pt.ast.Node):
            error_log.append(
                ErrorNote(
                    "AND statement didn't succeeded with parser {}".format(i),
                    start
                    )
                )
            ret = None

        if ret is None:
            break

        if ret is not None:
            ret.append(res)
            start = res.index1

    return ret


def or_(text, start, error_log, parser_list):
    """
    return: None or list with one and only one element
    """

    check_parser_list(parser_list)

    ret = []

    for i in parser_list:

        res = i(text, start, error_log)

        if isinstance(res, wayround_i2p.pt.ast.Node):
            ret.append(res)
            # start = res.index1 # not needed here
            break

    if len(ret) == 0:
        error_log.append(
            ErrorNote(
                "OR statement didn't succeeded at any case",
                start
                )
            )
        ret = None

    return ret


def any_number(text, start, error_log, callback, *args, **kwargs):
    """
    text and start are passed to callback inconditionally. args and kwargs may
    be passed by your desire
    """

    ret = []

    while True:

        res = callback(text, start, error_log, *args, **kwargs)

        # NOTE: if res is None, this is not error in context of any_number(),
        #       as such error must be treated as resulting number eql to 0
        #
        #       so if res is not None, then it's must be list and it's contents
        #       need to be added to ret list

        if res is None:
            break

        if res is not None:

            if not isinstance(res, list):
                raise ValueError(
                    "`callback()' must return None or list of Node")

            for i in res:
                if not isinstance(i, wayround_i2p.pt.ast.Node):
                    raise ValueError(
                        "`callback()' must return None or list of Node"
                        )

            for i in res:
                ret.append(i)
                start = i.index1

    return ret


def parse_next_re(text, start, error_log, re_, name='string'):
    """
    creates special ast node representing simple string. matching text directly

    if re_ is str - it will be compiled with regex.compile().

    re_ may be result of re.compile() or regex.compile().

    In any case, if re_ is not string, this function tries to call it's
    .match() method.
    """

    ret = wayround_i2p.pt.ast.Node(name, start)

    if isinstance(re_, str):
        re_ = regex.compile(re_)

    res = re_.match(text, pos=start)

    if res is None:
        error_log.append(
            ErrorNote(
                "Can't parse string as re ({})".format(re_),
                start
                )
            )
        ret = None

    if ret is not None:
        ret.index0 = res.start()
        ret.index1 = res.end()

    return ret


def check_parser_list(parser_list):
    if not isinstance(parser_list, list):
        raise TypeError("`parser_list' must be list")

    for i in parser_list:
        if not callable(i):
            raise ValueError("`parser_list' items must be callable")

    return
