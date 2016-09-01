
import regex
import itertools

RULENAME_RE = (
    r'\{'
    r'([\x41-\x5A]|[\x61-\x7A])'
    r'((([\x41-\x5A]|[\x61-\x7A]))|([\x30-\x39])|-)*'
    r'\}'
    )
RULENAME_RE_C = regex.compile(RULENAME_RE)


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

        self.rule_c = _RuleC(self)

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

        if res is None:
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
