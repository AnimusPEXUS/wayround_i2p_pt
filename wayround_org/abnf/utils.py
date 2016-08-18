
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

        for i in list(rules.keys()):
            for jj in range(len(parents) - 1, -1, -1):

                j = parents[jj]

                if i in j:
                    raise Exception(
                        "error: parent `{}' already has rule `{}'".format(
                            j,
                            i
                            )
                        )

        self._rules = rules
        self._parents = parents

        return

    def __iter__(self):
        c = [iter(self._rules)]
        for ii in range(len(self._parents) - 1, -1, -1):

            i = self._parents[ii]
            c.append(iter(i))

        ret = itertools.chain(*c)
        return iter(ret)

    def __getitem__(self, key):

        ret = None
        not_found = True

        if key in self._rules:

            not_found = False

            ret = self._rules[key]

        else:

            for ii in range(len(self._parents) - 1, -1, -1):

                i = self._parents[ii]

                if key in i:
                    ret = i[key]
                    not_found = False
                    break

        if not_found:
            raise KeyError("rule `{}' not found".format(key))

        if callable(ret):
            ret = ret()
        ret = ret.format_map(self)

        return ret

    def __contains__(self, key):
        ret = False
        for i in self:
            if i == key:
                ret = True
                break
        return ret

    def keys(self):
        ret = list(self._rules.keys())
        for ii in range(len(self._parents) - 1, -1, -1):

            i = self._parents[ii]
            ret += list(i.keys())
        ret.sort()
        return ret
