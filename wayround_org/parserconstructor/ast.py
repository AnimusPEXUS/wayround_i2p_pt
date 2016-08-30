

class Node:

    def __init__(self):

        self._src_text = None

        self._name = None

        self._index0 = None
        self._index1 = None

        self._parent = None

        self._children = []
        return

    @property
    def src_text(self):
        return self._src_text

    @src_text.setter
    def src_text(self, value):
        if not isinstance(value, str):
            raise TypeError("`src_text' must be str")
        self._src_text = value
        return

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("`name' must be str")
        self._name = value
        return

    def text(self):
        ret = self._src_text[self._index0:self._index1]
        return ret

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
        for i in lst:
            self.append_child(i)
        return

    def reset_indexes_by_children(self):
        if len(self) != 0:
            self.index0 = self[0].index0
            self.index1 = self[-1].index1
        else:
            raise Exception("this node has no children")
        return
