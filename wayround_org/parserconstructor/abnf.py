
import regex

import wayround_org.parserconstructor.ast


BIT_RE = r'[01]'

DIGIT_RE = r'[\x30-\x39]'

HEXDIG_RE = r'(({DIGIT})|A|B|C|D|E|F)'


def parse(text):
    ret = parse_next_rulelist(text, 0)
    return ret


def parse_next_rulelist(text, start):
    r'(({rule})|({c-wsp})*{c-nl})+'

    ret = wayround_org.parserconstructor.ast.Node()
    ret.name = 'rulelist'

    loop_start = start

    res = wayround_org.parserconstructor.utils.any_number(
        text,
        start,
        wayround_org.parserconstructor.utils.or_,
        (
            [
                parse_next_rule,
                parse_next_c_wsp
                ],
            )
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
            (
                [
                    parse_next_rule,
                    parse_next_c_wsp
                    ],
                )
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


def parse_next_rule(text, start):
    r'({rulename})({defined-as})({elements})({c-nl})'

    ret = wayround_org.parserconstructor.ast.Node()
    ret.name = 'rule'

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

    if res is not None:
        for i in res:
            ret.add_child(i)

    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_rulename(text, start):
    r'({ALPHA})(({ALPHA})|({DIGIT})|-)*'

    ret = wayround_org.parserconstructor.ast.Node()
    ret.name = 'rulename'

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
            (
                [
                    parse_next_ALPHA,
                    parse_next_DIGIT,
                    parse_next_hyphen
                    ],
                )
            )

        ret.append_children_from_list(res)

    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_defined_as(text, start):
    r'({c-wsp})*(=|(=\/))({c-wsp})*'

    ret = wayround_org.parserconstructor.ast.Node()
    ret.name = 'defined-as'

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


def parse_next_elements(text, start):
    r'({alternation})({c-wsp})*'

    ret = wayround_org.parserconstructor.ast.Node()
    ret.name = 'elements'

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


def parse_next_c_wsp(text, start):
    r'(({WSP})|(({c-nl})({WSP})))'

    ret = wayround_org.parserconstructor.ast.Node()
    ret.name = 'c-wsp'

    res = parse_next_c_nl(text, start)

    if res is not None:
        start = res.index1
        ret.append_child(res)

    res = parse_next_WSP(text, start)

    if res is None:
        ret = None

    if ret is not None:
        ret.append_child(res)

    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_c_nl(text, start):
    r'(({comment})|({CRLF}))'
    # ; comment or newline
    ret = wayround_org.parserconstructor.ast.Node()
    ret.name = 'c-nl'

    res = wayround_org.parserconstructor.utils.or_(
        text,
        start,
        [
            parse_next_comment,
            parse_next_CRLF
            ],
        )

    if res is None:
        ret = None

    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_comment(text, start):
    r';(({WSP})|({VCHAR}))*({CRLF})',
    ret = wayround_org.parserconstructor.ast.Node()
    ret.name = 'comment'

    start = parse_next_c_wsp_any_number(text, start, ret)

    res = parse_next_CRLF(text, start)

    if res is None:
        ret = None

    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_alternation(text, start):
    r'({concatenation})(({c-wsp})*\/({c-wsp})*({concatenation}))*'
    ret = wayround_org.parserconstructor.ast.Node()
    ret.name = 'alternation'

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


def parse_next_x_any_number(text, start, parser_callback, target_node):

    res = wayround_org.parserconstructor.utils.any_number(
        text,
        start,
        wayround_org.parserconstructor.utils.or_,
        (
            [
                parser_callback
                ],
            )
        )

    if len(res) != 0:
        target_node.append_children_from_list(res)
        start = res[-1].index1

    return start


def parse_next_c_wsp_any_number(text, start, target_node):
    ret = parse_next_x_any_number(text, start, parse_next_c_wsp, target_node)
    return ret


def parse_next_concatenation(text, start):
    r'({repetition})(({c-wsp})+({repetition}))*'
    ret = wayround_org.parserconstructor.ast.Node()
    ret.name = 'concatenation'

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


def parse_next_repetition(text, start):
    r'({repeat})?({element})'
    ret = wayround_org.parserconstructor.ast.Node()
    ret.name = 'repetition'

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


def parse_next_repeat(text, start):
    r'((({DIGIT})+)|((({DIGIT})*)\*(({DIGIT})*)))'
    ret = wayround_org.parserconstructor.ast.Node()
    ret.name = 'repeat'

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


def parse_next_element(text, start):
    r'(({rulename})|({group})|({option})|({char-val})|({num-val})|({prose-val}))'
    ret = wayround_org.parserconstructor.ast.Node()
    ret.name = 'element'

    res = wayround_org.parserconstructor.utils.or_(
        text,
        start,
        [
            parse_next_rulename,
            parse_next_group,
            parse_next_option,
            parse_next_char - val,
            parse_next_num - val,
            parse_next_prose - val
            ]
        )

    if res is None or len(res) != 1:
        ret = None

    if ret is not None:
        ret.append_child(res[0])

    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_group(text, start):
    r'\(({c-wsp})*({alternation})({c-wsp})*\)'
    ret = wayround_org.parserconstructor.ast.Node()
    ret.name = 'group'

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


def parse_next_option(text, start):
    r'\[({c-wsp})*({alternation})({c-wsp})*\]'
    ret = wayround_org.parserconstructor.ast.Node()
    ret.name = 'option'

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


def parse_next_char_val(text, start):
    r'({DQUOTE})([\x20-\x21]|[\x23-\x7e])*({DQUOTE})'
    # ; quoted string of SP and VCHAR
    # ;  without DQUOTE
    ret = wayround_org.parserconstructor.ast.Node()
    ret.name = 'char-val'

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


def parse_next_num_val(text, start):
    r'\%(({bin-val})|({dec-val})|({hex-val}))'
    ret = wayround_org.parserconstructor.ast.Node()
    ret.name = 'num-val'

    res = wayround_org.parserconstructor.utils.parse_next_re(
        text, start, r'\%'

        if res is None:
        ret=None

        if ret is not None:
        ret.append_child(res)
        )

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


def parse_next_x_val(text, start, prefix, target_node):

    if prefix not in 'bdx':
        raise ValueError("`prefix' is invalid")

    ret = True

    if prefix == 'b':
        digit_re = BIT_RE
    elif prefix == 'd':
        digit_re = DIGIT_RE
    elif prefix == 'x':
        digit_re = HEXDIG_RE
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

                res = parse_next_re(text, start, r'\.({})+'.format(digit_re))

                if res is None:
                    break

                if res is not None:
                    dotted_elements.append(res)
                    start = res.index1

            if len(dotted_elements) > 1:
                tet.append_children_from_list(dotted_elements)

            del dotted_elements

        elif text[start] == '-' and digit_parser(text, start + 1) is not None:

            res = parse_next_re(text, start, r'\-({})+'.format(digit_re))

            if res is not None:
                ret.append_child(res)

        else:
            pass

    return start


def parse_next_bin_val(text, start):
    r'b({BIT})+((\.({BIT})+)+|(\-({BIT})+))?'
    # ; series of concatenated bit values
    # ;  or single ONEOF range
    ret = wayround_org.parserconstructor.ast.Node()
    ret.name = 'bin-val'

    if not parse_parse_next_x_val(text, start, 'b', parse_next_BIT, ret):
        ret = None

    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_(text, start):
    r'd({DIGIT})+((\.({DIGIT})+)+|(\-({DIGIT})+))?'
    ret = wayround_org.parserconstructor.ast.Node()
    ret.name = 'dec-val'

    if not parse_parse_next_x_val(text, start, 'd', parse_next_DEC, ret):
        ret = None

    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_hex_val(text, start):
    r'x({HEXDIG})+((\.({HEXDIG})+)+|(\-({HEXDIG})+))?'
    ret = wayround_org.parserconstructor.ast.Node()
    ret.name = 'hex-val'

    if not parse_parse_next_x_val(text, start, 'x', parse_next_HEX, ret):
        ret = None

    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_prose_val(text, start):
    r'\<([\x20-\x3d]|[\x3f-\x7e])*\>'
    ret = wayround_org.parserconstructor.ast.Node()
    ret.name = 'prose-val'

    if ret is not None:
        ret.reset_indexes_by_children()

    return ret
