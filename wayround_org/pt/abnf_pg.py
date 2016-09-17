
"""
This module is for generating parsers from given ABNF AST
"""

import wayround_org.pt.ast


def render_module(output_filename, in_ast, parent_table_list):

    if not isinstance(filename, str):
        raise TypeError("`filename' must be str")

    if not isinstance(in_ast, wayround_org.pt.ast.Node):
        raise TypeError("`in_ast' must be inst of wayround_org.pt.ast.Node")

    if in_ast.parent is not None:
        raise ValueError("`in_ast' must be root node (.parent must be None)")

    if in_ast.text is None:
        raise ValueError("`in_ast' must have .text defined")

    ret = 0

    if parent_table_list.name != 'rulelist':
        ret = 1

    if ret == 0:

        rules = in_ast.get_children_by_name('rule')

        for i in rules:
            rulename_node = i.get_child_by_name('rulename')
            if rulename_node is None:
                raise ValueError("discovered rule with no rule name")

            print("rule with name `{}' found".format(rulename_node.get_text()))

    return ret
