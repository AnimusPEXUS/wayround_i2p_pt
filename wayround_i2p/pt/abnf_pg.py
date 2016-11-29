
"""
This module is for generating parsers from given ABNF AST
"""

import wayround_i2p.pt.ast


def render_rule_function_name(in_str):
    ret = in_str.replace('-', '_')
    ret = 'parse_next_{}'.format(ret)
    return ret


def render_rule_names(in_ast):
    ret = {}

    rules = in_ast.get_children_by_name('rule')

    for i in rules:
        rulename_node = i.get_child_by_name('rulename')
        rule_name = rulename_node.get_text()

        if not rule_name in ret:
            ret[rule_name] = {}

        ret[rule_name]['rule_function_name'] = \
            render_rule_function_name(rule_name)

    return ret


def render_module(filename, in_ast, parent_table_list):

    if not isinstance(filename, str):
        raise TypeError("`filename' must be str")

    if not isinstance(in_ast, wayround_i2p.pt.ast.Node):
        raise TypeError("`in_ast' must be inst of wayround_i2p.pt.ast.Node")

    if in_ast.parent is not None:
        raise ValueError("`in_ast' must be root node (.parent must be None)")

    if in_ast.text is None:
        raise ValueError("`in_ast' must have .text defined")

    ret = 0

    if in_ast.name != 'rulelist':
        ret = 1

    output_functions_texts = []

    if ret == 0:

        rule_names = render_rule_names(in_ast)

        rules = in_ast.get_children_by_name('rule')

        for i in rules:
            rulename_node = i.get_child_by_name('rulename')
            if rulename_node is None:
                raise ValueError("discovered rule with no rule name")

            print(
                "rendering code for rule: {}".format(
                    rulename_node.get_text()
                    )
                )

            res = render_rule_code(rule_names, i, output_functions_texts)

            if res != 0:
                print("    failed")
                ret = 1
                break

            print("    ok")

    if ret == 0:
        with open(filename, 'w') as f:
            for i in output_functions_texts:
                f.write(i)

                if output_functions_texts.index(
                        i
                        ) < len(output_functions_texts):
                    f.write('\n')

    return ret


def render_rule_code(rule_names, rule_node, output_functions_texts):

    ret = 0

    rulename_node = rule_node.get_child_by_name('rulename')

    rule_name = rulename_node.get_text()

    rule_function_name = rule_names[rule_name]['rule_function_name']

    rule_text = rule_node.get_text()
    rule_text = rule_text.split('\n')
    for i in range(len(rule_text)):
        rule_text[i] = '    {}'.format(rule_text[i])

    rule_text = '\n'.join(rule_text)
    rule_text = rule_text.strip()

    txt = ''

    txt += """
def {rule_function_name}(text, start, error_log):

    \"""
    {rule_text}
    \"""

    ret = wayround_i2p.pt.ast.Node('{rule_name}', start)

""".format(
        rule_function_name=rule_function_name,
        rule_name=rule_name,
        rule_text=rule_text
    )

    txt += """

    if ret is not None:
        ret.reset_indexes_by_children()

    return ret
"""

    output_functions_texts.append(txt)

    return ret
