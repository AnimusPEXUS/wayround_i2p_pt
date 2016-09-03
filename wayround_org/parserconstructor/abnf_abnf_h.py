

"""
This module is hand-written abnf2ast parser
"""


# import regex

import wayround_org.parserconstructor.ast
import wayround_org.parserconstructor.abnf_core_h


RULES = wayround_org.parserconstructor.utils.Rules(
    {
        'rulelist': r'(({rule})|({c-wsp})*{c-nl})+',

        'rule': r'({rulename})({defined-as})({elements})({c-nl})',
        # ; continues if next line starts
        # ;  with white space

        'rulename': r'({ALPHA})(({ALPHA})|({DIGIT})|-)*',

        'defined-as': r'({c-wsp})*(=|(=\/))({c-wsp})*',
        # ; basic rules definition and
        # ;  incremental alternatives

        'elements': r'({alternation})({c-wsp})*',

        'c-wsp': r'(({WSP})|(({c-nl})({WSP})))',

        'c-nl': r'(({comment})|({CRLF}))',
        # ; comment or newline

        'comment': r';(({WSP})|({VCHAR}))*({CRLF})',

        'alternation': (
            r'({concatenation})(({c-wsp})*\/({c-wsp})*({concatenation}))*'
            ),

        'concatenation': r'({repetition})(({c-wsp})+({repetition}))*',

        'repetition': r'({repeat})?({element})',

        'repeat': r'((({DIGIT})+)|((({DIGIT})*)\*(({DIGIT})*)))',

        'element': (
            r'('
            r'({rulename})'
            r'|({group})'
            r'|({option})'
            r'|({char-val})'
            r'|({num-val})'
            r'|({prose-val})'
            r')'
            ),

        'group': (
            r'\('
            r'({c-wsp})*'
            r'({alternation})'
            r'({c-wsp})*'
            r'\)'
            ),

        'option': (
            r'\['
            r'({c-wsp})*'
            r'({alternation})'
            r'({c-wsp})*'
            r'\]'
            ),

        'char-val': (
            r'({DQUOTE})'
            r'([\x20-\x21]|[\x23-\x7e])*'
            r'({DQUOTE})'
            ),
        # ; quoted string of SP and VCHAR
        # ;  without DQUOTE

        'num-val': r'\%(({bin-val})|({dec-val})|({hex-val}))',

        'bin-val': r'b({BIT})+((\.({BIT})+)+|(\-({BIT})+))?',
        # ; series of concatenated bit values
        # ;  or single ONEOF range

        'dec-val': r'd({DIGIT})+((\.({DIGIT})+)+|(\-({DIGIT})+))?',

        'hex-val': r'x({HEXDIG})+((\.({HEXDIG})+)+|(\-({HEXDIG})+))?',

        'prose-val': (
            r'\<'
            r'([\x20-\x3d]|[\x3f-\x7e])*'
            r'\>'
            ),
        # ; bracketed string of SP and VCHAR
        # ;  without angles
        # ; prose description, to be used as
        # ;  last resort
        },
    [wayround_org.parserconstructor.abnf_core_h.RULES]
    )


def parse(text, error_log):
    ret = parse_next_rulelist(text, 0, error_log)
    return ret


def parse_next_rulelist(text, start, error_log):
    r'(({rule})|({c-wsp})*{c-nl})+'

    ret = wayround_org.parserconstructor.ast.Node('rulelist', start)

    res = wayround_org.parserconstructor.utils.any_number(
        text,
        start,
        wayround_org.parserconstructor.utils.or_,
        [
            parse_next_rule,
            parse_next_c_wsp
            ]
        )

    if res is None:
        ret = None

    if ret is not None:
        ret.append_children_from_list(res)

    if ret is not None:

        res = wayround_org.parserconstructor.utils.any_number(
            text,
            start,
            wayround_org.parserconstructor.utils.or_,
            [
                parse_next_rule,
                parse_next_c_wsp
                ]
            )

    if ret is not None:

        if res is None:
            ret = None

    if ret is not None:

        if len(res) < 1:
            ret = None

    if ret is not None:

        for i in res:
            ret.append_children_from_list(res)

    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_rule(text, start, error_log):
    r'({rulename})({defined-as})({elements})({c-nl})'

    ret = wayround_org.parserconstructor.ast.Node('rule', start)

    res = wayround_org.parserconstructor.utils.and_(
        text,
        start,
        [
            parse_next_rulename,
            parse_next_defined_as,
            parse_next_elements,
            parse_next_c_nl
            ]
        )

    if res is None:
        ret = None

    if ret is not None:
        ret.append_children_from_list(res)

    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_rulename(text, start, error_log):
    r'({ALPHA})(({ALPHA})|({DIGIT})|-)*'

    ret = wayround_org.parserconstructor.ast.Node('rulename', start)

    res = parse_next_ALPHA(text, start)

    if not isinstance(res, wayround_org.parserconstructor.ast.Node):
        ret = None

    if ret is not None:
        ret.append_child(res)

    if ret is not None:
        res = wayround_org.parserconstructor.utils.any_number(
            text,
            start,
            wayround_org.parserconstructor.utils.or_,
            [
                parse_next_ALPHA,
                parse_next_DIGIT,
                parse_next_hyphen
                ]
            )

        ret.append_children_from_list(res)

    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_hyphen(text, start, error_log):
    ret = wayround_org.parserconstructor.utils.parse_next_re(
        text,
        start,
        r'\-'
        )
    return ret


def parse_next_defined_as(text, start, error_log):
    r'({c-wsp})*(=|(=\/))({c-wsp})*'

    ret = wayround_org.parserconstructor.ast.Node('defined-as', start)

    start = parse_next_c_wsp_any_number(text, start, ret)

    res = wayround_org.parserconstructor.utils.parse_next_re(
        text, start, r'((=\/)|=)'
        )

    if res is None:
        ret = None

    if ret is not None:
        ret.append_child(res)

    if ret is not None:
        start = parse_next_c_wsp_any_number(text, start, ret)

    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_elements(text, start, error_log):
    r'({alternation})({c-wsp})*'

    ret = wayround_org.parserconstructor.ast.Node('elements', start)

    res = parse_next_alternation(text, start)
    if res is None:
        ret = None

    if res is not None:

        ret.append_child(res)

        start = res.index1

        start = parse_next_c_wsp_any_number(text, start, ret)

    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_c_wsp(text, start, error_log):
    r'(({WSP})|(({c-nl})({WSP})))'

    ret = wayround_org.parserconstructor.ast.Node('c-wsp', start)

    res = parse_next_c_nl(text, start)

    if res is not None:
        ret.append_child(res)
        start = res.index1

    res = parse_next_WSP(text, start)

    if res is None:
        ret = None

    if ret is not None:
        ret.append_child(res)

    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_c_nl(text, start, error_log):
    r'(({comment})|({CRLF}))'

    ret = wayround_org.parserconstructor.ast.Node('c-nl', start)

    res = wayround_org.parserconstructor.utils.or_(
        text,
        start,
        [
            parse_next_comment,
            parse_next_CRLF
            ]
        )

    if res is None:
        ret = None

    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_comment(text, start, error_log):
    r';(({WSP})|({VCHAR}))*({CRLF})',

    ret = wayround_org.parserconstructor.ast.Node('comment', start)

    res = wayround_org.parserconstructor.utils.parse_next_re(
        text, start, r';'
        )

    if res is None:
        ret = None

    if ret is not None:
        ret.append_child(res)
        start = res.index1

    if ret is not None:

        res = wayround_org.parserconstructor.utils.any_number(
            text,
            start,
            wayround_org.parserconstructor.utils.or_,
            [
                parse_next_WSP,
                parse_next_VCHAR
                ]
            )

        ret.append_children_from_list(res)

        if len(res) != 0:
            start = res[-1].index1

        res = parse_next_CRLF(text, start)

    if res is None:
        ret = None

    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_alternation(text, start, error_log):
    r'({concatenation})(({c-wsp})*\/({c-wsp})*({concatenation}))*'

    ret = wayround_org.parserconstructor.ast.Node('alternation', start)

    res = parse_next_concatenation(text, start)

    if res is None:
        ret = None

    if ret is not None:
        ret.append_child(res)

        start = res.index1

    if ret is not None:
        while True:

            start = parse_next_c_wsp_any_number(text, start, ret)

            res = wayround_org.parserconstructor.utils.parse_next_re(
                text, start, r'\/'
                )

            if res is None:
                ret = None

            if ret is None:
                break

            if ret is not None:
                ret.append_child(res)

                start = res.index1

            start = parse_next_c_wsp_any_number(text, start, ret)

            res = parse_next_concatenation(text, start)

            if res is None:
                ret = None

            if ret is None:
                break

            if ret is not None:
                ret.append_child(res)

                start = res.index1

    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_x_any_number(text, start, error_log, parser_callback, target_node):

    res = wayround_org.parserconstructor.utils.any_number(
        text,
        start,
        wayround_org.parserconstructor.utils.or_,
        [parser_callback]
        )

    if len(res) != 0:
        target_node.append_children_from_list(res)
        start = res[-1].index1

    return start


def parse_next_c_wsp_any_number(text, start, error_log, target_node):
    ret = parse_next_x_any_number(text, start, parse_next_c_wsp, target_node)
    return ret


def parse_next_concatenation(text, start, error_log):
    r'({repetition})(({c-wsp})+({repetition}))*'

    ret = wayround_org.parserconstructor.ast.Node('concatenation', start)

    res = parse_next_repetition(text, start)

    if res is None:
        ret = None

    if ret is not None:
        ret.append_child(res)
        start = res.index1

        while True:

            _start = parse_next_c_wsp_any_number(text, start, ret)

            if _start == start:
                break

            start = _start

            del _start

            res = parse_next_repetition(text, start)

            if res is None:
                break

            if ret is not None:
                ret.append_child(res)

                start = res.index1

    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_repetition(text, start, error_log):
    r'({repeat})?({element})'

    ret = wayround_org.parserconstructor.ast.Node('repetition', start)

    res = parse_next_repeat(text, start)

    if res is not None:
        ret.append_child(res)
        start = res.index1

    res = parse_next_element(text, start)

    if res is None:
        ret = None

    if ret is not None:
        ret.append_child(res)

    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_repeat(text, start, error_log):
    r'((({DIGIT})+)|((({DIGIT})*)\*(({DIGIT})*)))'

    ret = wayround_org.parserconstructor.ast.Node('repeat', start)

    _start = parse_next_x_any_number(text, start, parse_next_DIGIT, ret)

    first_part_length = _start - start

    start = _start

    del _start

    res = wayround_org.parserconstructor.utils.parse_next_re(
        text, start, r'\*'
        )

    if res is None:
        if first_part_length == 0:
            ret = None
    else:

        ret.append_child(res)

        start = res.index1

        parse_next_x_any_number(text, start, parse_next_DIGIT, ret)

    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_element(text, start, error_log):
    r'(({rulename})|({group})|({option})|({char-val})|({num-val})|({prose-val}))'

    ret = wayround_org.parserconstructor.ast.Node('element', start)

    res = wayround_org.parserconstructor.utils.or_(
        text,
        start,
        [
            parse_next_rulename,
            parse_next_group,
            parse_next_option,
            parse_next_char_val,
            parse_next_num_val,
            parse_next_prose_val
            ]
        )

    if res is None or len(res) != 1:
        ret = None

    if ret is not None:
        ret.append_child(res[0])

    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_group(text, start, error_log):
    r'\(({c-wsp})*({alternation})({c-wsp})*\)'

    ret = wayround_org.parserconstructor.ast.Node('group', start)

    res = wayround_org.parserconstructor.utils.parse_next_re(
        text, start, r'\('
        )

    if res is None:
        ret = None

    if ret is not None:
        ret.append_child(res)
        start = res.index1

    start = parse_next_c_wsp_any_number(text, start, ret)

    res = parse_next_alternation(text, start)

    if ret is not None:
        start = parse_next_c_wsp_any_number(text, start, ret)

        res = wayround_org.parserconstructor.utils.parse_next_re(
            text, start, r'\)'
            )

        if res is None:
            ret = None

        if ret is not None:
            ret.append_child(res)
            start = res.index1

    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_option(text, start, error_log):
    r'\[({c-wsp})*({alternation})({c-wsp})*\]'

    ret = wayround_org.parserconstructor.ast.Node('option', start)

    res = wayround_org.parserconstructor.utils.parse_next_re(
        text, start, r'\['
        )

    if res is None:
        ret = None

    if ret is not None:
        ret.append_child(res)
        start = res.index1

    start = parse_next_c_wsp_any_number(text, start, ret)

    res = parse_next_alternation(text, start)

    if ret is not None:
        start = parse_next_c_wsp_any_number(text, start, ret)

        res = wayround_org.parserconstructor.utils.parse_next_re(
            text, start, r'\]'
            )

        if res is None:
            ret = None

        if ret is not None:
            ret.append_child(res)
            start = res.index1

    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_char_val(text, start, error_log):
    r'({DQUOTE})([\x20-\x21]|[\x23-\x7e])*({DQUOTE})'
    # ; quoted string of SP and VCHAR
    # ;  without DQUOTE

    ret = wayround_org.parserconstructor.ast.Node('char-val', start)

    res = wayround_org.parserconstructor.utils.parse_next_re(
        text, start, r'\"'
        )

    if res is None:
        ret = None

    if ret is not None:
        ret.append_child(res)
        start = res.index1

    if ret is not None:

        res = wayround_org.parserconstructor.utils.parse_next_re(
            text, start, r'([\x20-\x21]|[\x23-\x7e])*'
            )

        if res is None:
            ret = None

        if ret is not None:
            ret.append_child(res)
            start = res.index1

    if ret is not None:

        res = wayround_org.parserconstructor.utils.parse_next_re(
            text, start, r'\"'
            )

        if res is None:
            ret = None

        if ret is not None:
            ret.append_child(res)

    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_num_val(text, start, error_log):
    r'\%(({bin-val})|({dec-val})|({hex-val}))'

    ret = wayround_org.parserconstructor.ast.Node('num-val', start)

    res = wayround_org.parserconstructor.utils.parse_next_re(
        text, start, r'\%'
        )

    if res is None:
        ret = None

    if ret is not None:
        ret.append_child(res)

    if ret is not None:

        res = wayround_org.parserconstructor.utils.or_(
            text,
            start,
            [
                parse_next_bin_val,
                parse_next_dec_val,
                parse_next_hex_val,
                parse_next_prose_val
                ]
            )

        if res is None or len(res) != 1:
            ret = None

    if ret is not None:
        ret.append_child(res[0])

    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_x_val(text, start, error_log, prefix, target_node):

    if prefix not in 'bdx':
        raise ValueError("`prefix' is invalid")

    ret = True

    if prefix == 'b':
        digit_re = RULES['BIT']
        digit_parser = parse_next_BIT
    elif prefix == 'd':
        digit_re = RULES['DIGIT']
        digit_parser = parse_next_DIGIT
    elif prefix == 'x':
        digit_re = RULES['HEXDIG']
        digit_parser = parse_next_HEXDIG
    else:
        raise Exception("programming error")

    res = wayround_org.parserconstructor.utils.parse_next_re(
        text, start, prefix
        )

    if res is None:
        ret = False

    if ret:
        target_node.append_child(res)
        start = res.index1

    if ret:
        _start = parse_next_x_any_number(
            text, start, digit_parser, target_node)

        if start == _start:
            ret = False
        else:
            start = _start

        del _start

    if ret:
        if text[start] == '.' and digit_parser(text, start + 1) is not None:

            dotted_elements = []

            while True:

                res = wayround_org.parserconstructor.utils.parse_next_re(
                    text,
                    start,
                    r'\.({})+'.format(digit_re)
                    )

                if res is None:
                    break

                if res is not None:
                    dotted_elements.append(res)
                    start = res.index1

            if len(dotted_elements) > 1:
                target_node.append_children_from_list(dotted_elements)

            del dotted_elements

        elif text[start] == '-' and digit_parser(text, start + 1) is not None:

            res = wayround_org.utils.parse_next_re(
                text,
                start,
                r'\-({})+'.format(
                    digit_re
                    )
                )

            if res is not None:
                target_node.append_child(res)

        else:
            pass

    return start


def parse_next_bin_val(text, start, error_log):
    r'b({BIT})+((\.({BIT})+)+|(\-({BIT})+))?'
    # ; series of concatenated bit values
    # ;  or single ONEOF range

    ret = wayround_org.parserconstructor.ast.Node('bin-val', start)

    if not parse_next_x_val(text, start, 'b', ret):
        ret = None

    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_dec_val(text, start, error_log):
    r'd({DIGIT})+((\.({DIGIT})+)+|(\-({DIGIT})+))?'

    ret = wayround_org.parserconstructor.ast.Node('dec-val', start)

    if not parse_next_x_val(text, start, 'd', ret):
        ret = None

    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_hex_val(text, start, error_log):
    r'x({HEXDIG})+((\.({HEXDIG})+)+|(\-({HEXDIG})+))?'

    ret = wayround_org.parserconstructor.ast.Node('hex-val', start)

    if not parse_next_x_val(text, start, 'x', ret):
        ret = None

    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_prose_val(text, start, error_log):
    r'\<([\x20-\x3d]|[\x3f-\x7e])*\>'

    ret = wayround_org.parserconstructor.ast.Node('prose-val', start)

    res = wayround_org.parserconstructor.utils.parse_next_re(
        text, start, r'\<'
        )

    if res is None:
        ret = None

    if ret is not None:
        ret.append_child(res)
        start = res.index1

    if ret is not None:

        res = wayround_org.parserconstructor.utils.parse_next_re(
            text, start, r'([\x20-\x3d]|[\x3f-\x7e])*'
            )

        if res is None:
            ret = None

        if ret is not None:
            ret.append_child(res)
            start = res.index1

    if ret is not None:

        res = wayround_org.parserconstructor.utils.parse_next_re(
            text, start, r'\>'
            )

        if res is None:
            ret = None

        if ret is not None:
            ret.append_child(res)

    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_HEXDIG(text, start, error_log):

    ret = wayround_org.parserconstructor.ast.Node('HEXDIG', start)

    res = RULES.compiled['HEXDIG'].match(text, pos=start)

    if res is None:
        ret = None

    if ret is not None:
        ret.index0 = res.start()
        ret.index1 = res.end()

    return ret


def parse_next_DIGIT(text, start, error_log):

    ret = wayround_org.parserconstructor.ast.Node('DIGIT', start)

    res = RULES.compiled['DIGIT'].match(text, pos=start)

    if res is None:
        ret = None

    if ret is not None:
        ret.index0 = res.start()
        ret.index1 = res.end()

    return ret


def parse_next_BIT(text, start, error_log):

    ret = wayround_org.parserconstructor.ast.Node('BIT', start)

    res = RULES.compiled['BIT'].match(text, pos=start)

    if res is None:
        ret = None

    if ret is not None:
        ret.index0 = res.start()
        ret.index1 = res.end()

    return ret


def parse_next_ALPHA(text, start):

    ret = wayround_org.parserconstructor.ast.Node('ALPHA', start)

    res = RULES.compiled['ALPHA'].match(text, pos=start)

    if res is None:
        ret = None

    if ret is not None:
        ret.index0 = res.start()
        ret.index1 = res.end()

    return ret


def parse_next_WSP(text, start, error_log):

    ret = wayround_org.parserconstructor.ast.Node('WSP', start)

    res = RULES.compiled['WSP'].match(text, pos=start)

    if res is None:
        ret = None

    if ret is not None:
        ret.index0 = res.start()
        ret.index1 = res.end()

    return ret


def parse_next_CRLF(text, start, error_log):

    ret = wayround_org.parserconstructor.ast.Node('CRLF', start)

    res = RULES.compiled['CRLF'].match(text, pos=start)

    if res is None:
        ret = None

    if ret is not None:
        ret.index0 = res.start()
        ret.index1 = res.end()

    return ret


def parse_next_VCHAR(text, start, error_log):

    ret = wayround_org.parserconstructor.ast.Node('CRLF', start)

    res = RULES.compiled['CRLF'].match(text, pos=start)

    if res is None:
        ret = None

    if ret is not None:
        ret.index0 = res.start()
        ret.index1 = res.end()

    return ret
