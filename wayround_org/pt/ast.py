

class Node:

    def __init__(self, name, index0):

        self._name = None

        self._index0 = None
        self._index1 = None

        self._parent = None

        self._children = []

        self.name = name
        self.index0 = index0

        return

    def __getitem__(self, index):
        return self._children[index]

    def __len__(self):
        return len(self._children)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("`name' must be str")
        self._name = value
        return

    @property
    def index0(self):
        return self._index0

    @index0.setter
    def index0(self, value):
        if not isinstance(value, int):
            raise TypeError("`index0' must be int")
        self._index0 = value
        return

    @property
    def index1(self):
        return self._index1

    @index1.setter
    def index1(self, value):
        if not isinstance(value, int):
            raise TypeError("`index1' must be int")
        self._index1 = value
        return

    @property
    def parent(self):
        ret = self._parent
        return ret

    @parent.setter
    def parent(self, value):

        # TODO: circular recursion detection

        if not isinstance(value, Node):
            raise TypeError("`value' must be inst of Node")

        self._parent = value

        return

    def append_child(self, value):

        # TODO: circular recursion detection

        if not isinstance(value, Node):
            raise TypeError("`value' must be inst of Node")

        self._children.append(value)
        value.parent = self

        return

    def append_children_from_list(self, lst):
        if not isinstance(lst, list):
            raise TypeError("`lst' must be list of Node")

        for i in lst:
            if not isinstance(i, Node):
                raise TypeError("`lst' must be list of Node")

        for i in lst:
            self.append_child(i)
        return

    def reset_indexes_by_children(self):
        if len(self) != 0:
            self.index0 = self[0].index0
            self.index1 = self[-1].index1
        else:
            if self.index0 is None:
                raise Exception(
                    "this node has no children ({}:{}),"
                    " and self.index0 is None".format(
                        self,
                        self.name
                        )
                    )
            self.index1 = self.index0
        return

    def get_text(self, text):
        ret = None
        if self.index0 is not None and self.index1 is not None:
            ret = text[self.index0:self.index1]
        else:
            raise Exception("index0 or index1 is None")
        return ret

    def render_dict(self, slice_text=False, dict_constructor=dict):

        if (
            slice_text != False
                and type(slice_text) not in [str, bytes]):
            raise TypeError(
                "if slice_text is not None, then it"
                " must be str or bytes type"
                )

        ret = dict_constructor()
        ret['name'] = self.name
        ret['index0'] = self.index0
        ret['index1'] = self.index1

        if slice_text != False:
            ret['text'] = self.get_text(slice_text)

        c = []

        for i in self._children:
            c.append(
                i.render_dict(
                    slice_text=slice_text,
                    dict_constructor=dict_constructor
                    )
                )

        ret['children'] = c

        return ret

    def root(self):
        ret = self
        while ret.parent is not None:
            ret = self.parent
        return ret
