
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
