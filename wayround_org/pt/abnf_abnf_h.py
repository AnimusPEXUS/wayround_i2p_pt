

"""
This module is hand-written abnf2ast parser

NOTE: CRoLF is used instead of CRLF
"""


# import regex

import wayround_org.pt.ast
import wayround_org.pt.abnf_core_h


RULES = wayround_org.pt.utils.Rules(
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

        'c-nl': r'(({comment})|({CRoLF}))',
        # ; comment or newline

        'comment': r';(({WSP})|({VCHAR}))*({CRoLF})',

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
    [wayround_org.pt.abnf_core_h.RULES]
    )


def parse(text, error_log):
    ret = parse_next_rulelist(text, 0, error_log)
    return ret


def parse_next_rulelist(text, start, error_log):
    r'(({rule})|(({c-wsp})*({c-nl})))+'

    ret = wayround_org.pt.ast.Node('rulelist', start)

    children_of_children = []

    while True:

        res = parse_next_rule(text, start, error_log)

        if res is not None:
            children_of_children.append(res)
            start = res.index1
            continue

        children = []

        res = wayround_org.pt.utils.any_number(
            text,
            start,
            error_log,
            wayround_org.pt.utils.or_,
            [
                parse_next_c_wsp
                ]
            )

        for i in res:
            children.append(i)
            start = i.index1

        res = parse_next_c_nl(text, start, error_log)

        if res is None:
            # this case is whan OR didn't worked
            break

        children.append(res)
        start = res.index1

    if len(children_of_children) == 0:
        ret = None

    if ret is not None:
        ret.append_children_from_list(children_of_children)

    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_rule(text, start, error_log):
    r'({rulename})({defined-as})({elements})({c-nl})'

    ret = wayround_org.pt.ast.Node('rule', start)

    res = wayround_org.pt.utils.and_(
        text,
        start,
        error_log,
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

    ret = wayround_org.pt.ast.Node('rulename', start)

    res = parse_next_ALPHA(text, start, error_log)

    if not isinstance(res, wayround_org.pt.ast.Node):
        ret = None

    if ret is not None:
        ret.append_child(res)
        start = res.index1

    if ret is not None:
        res = wayround_org.pt.utils.any_number(
            text,
            start,
            error_log,
            wayround_org.pt.utils.or_,
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
    ret = wayround_org.pt.utils.parse_next_re(
        text,
        start,
        error_log,
        r'\-'
        )
    return ret


def parse_next_defined_as(text, start, error_log):
    r'({c-wsp})*(=|(=\/))({c-wsp})*'

    ret = wayround_org.pt.ast.Node('defined-as', start)

    children = []

    start = parse_next_c_wsp_any_number(text, start, error_log, children)

    res = wayround_org.pt.utils.parse_next_re(
        text, start, error_log, r'((=\/)|=)'
        )

    if res is None:
        ret = None

    if ret is not None:
        children.append(res)

        start = res.index1

        start = parse_next_c_wsp_any_number(text, start, error_log, children)

        ret.append_children_from_list(children)

        ret.reset_indexes_by_children()

    return ret


def parse_next_elements(text, start, error_log):
    r'({alternation})({c-wsp})*'

    ret = wayround_org.pt.ast.Node('elements', start)

    res = parse_next_alternation(text, start, error_log)

    if res is None:
        ret = None

    if res is not None:

        ret.append_child(res)

        start = res.index1

        children = []

        start = parse_next_c_wsp_any_number(text, start, error_log, children)

        ret.append_children_from_list(children)

        del children

        ret.reset_indexes_by_children()

    return ret


def parse_next_c_wsp(text, start, error_log):
    r'(({WSP})|(({c-nl})({WSP})))'

    ret = wayround_org.pt.ast.Node('c-wsp', start)

    res = parse_next_c_nl(text, start, error_log)

    if res is not None:
        ret.append_child(res)
        start = res.index1

    res = parse_next_WSP(text, start, error_log)

    if res is None:
        ret = None

    if ret is not None:
        ret.append_child(res)

        ret.reset_indexes_by_children()

    return ret


def parse_next_c_nl(text, start, error_log):
    r'(({comment})|({CRoLF}))'

    ret = wayround_org.pt.ast.Node('c-nl', start)

    res = wayround_org.pt.utils.or_(
        text,
        start,
        error_log,
        [
            parse_next_comment,
            parse_next_CRoLF
            ]
        )

    if res is None:
        ret = None

    else:
        if len(res) == 0:
            ret = None

    if ret is not None:
        ret.append_children_from_list(res)
        ret.reset_indexes_by_children()

    return ret


def parse_next_comment(text, start, error_log):
    r';(({WSP})|({VCHAR}))*({CRoLF})',

    ret = wayround_org.pt.ast.Node('comment', start)

    res = wayround_org.pt.utils.parse_next_re(
        text, start, error_log, r';'
        )

    if res is None:
        ret = None

    if ret is not None:
        ret.append_child(res)
        start = res.index1

    if ret is not None:

        res = wayround_org.pt.utils.any_number(
            text,
            start,
            error_log,
            wayround_org.pt.utils.or_,
            [
                parse_next_WSP,
                parse_next_VCHAR
                ]
            )

        ret.append_children_from_list(res)

        if len(res) != 0:
            start = res[-1].index1

        res = parse_next_CRoLF(text, start, error_log)

        if res is None:
            ret = None
        else:
            ret.append_child(res)

    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_alternation(text, start, error_log):
    r'({concatenation})(({c-wsp})*\/({c-wsp})*({concatenation}))*'

    ret = wayround_org.pt.ast.Node('alternation', start)

    res = parse_next_concatenation(text, start, error_log)

    if res is None:
        ret = None

    if ret is not None:
        ret.append_child(res)

        start = res.index1

        while True:

            children = []

            start = parse_next_c_wsp_any_number(
                text,
                start,
                error_log,
                children
                )

            res = wayround_org.pt.utils.parse_next_re(
                text, start, error_log, r'\/'
                )

            if res is None:
                children = []

            if len(children) == 0:
                break

            children.append(res)

            start = res.index1

            start = parse_next_c_wsp_any_number(
                text,
                start,
                error_log,
                children
                )

            res = parse_next_concatenation(text, start, error_log)

            if res is None:
                children = []

            if len(children) == 0:
                break

            children.append(res)

            start = res.index1

            ret.append_children_from_list(children)

    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_x_any_number(
        text, start, error_log,
        parser_callback, target_list
        ):

    if not isinstance(target_list, list):
        raise TypeError("`target_list' must be list")

    res = wayround_org.pt.utils.any_number(
        text,
        start,
        error_log,
        wayround_org.pt.utils.or_,
        [parser_callback]
        )

    if len(res) != 0:
        for i in res:
            target_list.append(i)
        start = res[-1].index1

    return start


def parse_next_c_wsp_any_number(text, start, error_log, target_list):
    ret = parse_next_x_any_number(
        text,
        start,
        error_log,
        parse_next_c_wsp,
        target_list
        )
    return ret


def parse_next_concatenation(text, start, error_log):
    r'({repetition})(({c-wsp})+({repetition}))*'

    ret = wayround_org.pt.ast.Node('concatenation', start)

    res = parse_next_repetition(text, start, error_log)

    if res is None:
        ret = None

    if ret is not None:
        ret.append_child(res)
        start = res.index1

        while True:

            start2 = start

            children = []

            _start = parse_next_c_wsp_any_number(
                text,
                start2,
                error_log,
                children
                )

            if _start == start:
                break

            start2 = _start

            del _start

            res = parse_next_repetition(text, start2, error_log)

            if res is None:
                break

            if ret is not None:
                children.append(res)

                start2 = res.index1

            ret.append_children_from_list(children)
            start = start2
            del start2

    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_repetition(text, start, error_log):
    r'({repeat})?({element})'

    ret = wayround_org.pt.ast.Node('repetition', start)

    res = parse_next_repeat(text, start, error_log)

    if res is not None:
        ret.append_child(res)
        start = res.index1

    res = parse_next_element(text, start, error_log)

    if res is None:
        ret = None

    if ret is not None:
        ret.append_child(res)

    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_repeat(text, start, error_log):
    r'((({DIGIT})+)|((({DIGIT})*)\*(({DIGIT})*)))'

    ret = wayround_org.pt.ast.Node('repeat', start)

    children = []

    _start = parse_next_x_any_number(
        text,
        start,
        error_log,
        parse_next_DIGIT,
        children
        )

    first_part_length = _start - start

    start = _start

    del _start

    res = wayround_org.pt.utils.parse_next_re(
        text, start, error_log, r'\*'
        )

    if res is None:
        if first_part_length == 0:
            ret = None
    else:

        children.append(res)

        start = res.index1

        parse_next_x_any_number(
            text,
            start,
            error_log,
            parse_next_DIGIT,
            children
            )

    if ret is not None:
        ret.append_children_from_list(children)
        ret.reset_indexes_by_children()

    return ret


def parse_next_element(text, start, error_log):
    r'(({rulename})|({group})|({option})|({char-val})|({num-val})|({prose-val}))'

    ret = wayround_org.pt.ast.Node('element', start)

    res = wayround_org.pt.utils.or_(
        text,
        start,
        error_log,
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

    ret = wayround_org.pt.ast.Node('group', start)

    res = wayround_org.pt.utils.parse_next_re(
        text,
        start,
        error_log,
        r'\('
        )

    if res is None:
        error_log.append(
            wayround_org.pt.utils.ErrorNote(
                "Can't parse as group: not starts with '('",
                start
                )
            )
        ret = None

    if ret is not None:
        ret.append_child(res)
        start = res.index1

    if ret is not None:
        children = []
        start = parse_next_c_wsp_any_number(text, start, error_log, children)
        ret.append_children_from_list(children)
        del children

    if ret is not None:
        res = parse_next_alternation(text, start, error_log)

        if res is None:
            error_log.append(
                wayround_org.pt.utils.ErrorNote(
                    "Can't parse as group: can't parse alternation",
                    start
                    )
                )
            ret = None

    if ret is not None:
        ret.append_child(res)
        start = res.index1

    if ret is not None:
        children = []
        start = parse_next_c_wsp_any_number(text, start, error_log, children)
        ret.append_children_from_list(children)
        del children

        res = wayround_org.pt.utils.parse_next_re(
            text, start, error_log, r'\)'
            )

        if res is None:
            error_log.append(
                wayround_org.pt.utils.ErrorNote(
                    "Can't parse as group: not ends with ')'",
                    start
                    )
                )
            ret = None

        if ret is not None:
            ret.append_child(res)
            start = res.index1

    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_option(text, start, error_log):
    r'\[({c-wsp})*({alternation})({c-wsp})*\]'

    ret = wayround_org.pt.ast.Node('option', start)

    children = []

    res = wayround_org.pt.utils.parse_next_re(
        text, start, error_log, r'\['
        )

    if res is None:
        ret = None

    if ret is not None:
        children.append(res)
        start = res.index1

        start = parse_next_c_wsp_any_number(text, start, error_log, children)

        res = parse_next_alternation(text, start, error_log)

        if res is None:
            ret = None
        else:
            start = res.index1

    if ret is not None:

        start = parse_next_c_wsp_any_number(text, start, error_log, children)

        res = wayround_org.pt.utils.parse_next_re(
            text, start, error_log, r'\]'
            )

        if res is None:
            ret = None

        if ret is not None:
            children.append(res)
            start = res.index1

    if ret is not None:
        ret.append_children_from_list(children)
        ret.reset_indexes_by_children()

    return ret


def parse_next_char_val(text, start, error_log):
    r'({DQUOTE})([\x20-\x21]|[\x23-\x7e])*({DQUOTE})'
    # ; quoted string of SP and VCHAR
    # ;  without DQUOTE

    ret = wayround_org.pt.ast.Node('char-val', start)

    res = wayround_org.pt.utils.parse_next_re(
        text, start, error_log, r'\"'
        )

    if res is None:
        ret = None

    if ret is not None:
        ret.append_child(res)
        start = res.index1

    if ret is not None:

        res = wayround_org.pt.utils.parse_next_re(
            text, start, error_log, r'([\x20-\x21]|[\x23-\x7e])*'
            )

        if res is None:
            ret = None

        if ret is not None:
            ret.append_child(res)
            start = res.index1

    if ret is not None:

        res = wayround_org.pt.utils.parse_next_re(
            text, start, error_log, r'\"'
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

    ret = wayround_org.pt.ast.Node('num-val', start)

    res = wayround_org.pt.utils.parse_next_re(
        text, start, error_log, r'\%'
        )

    if res is None:
        ret = None

    if ret is not None:
        ret.append_child(res)
        start = res.index1

    if ret is not None:

        res = wayround_org.pt.utils.or_(
            text,
            start,
            error_log,
            [
                parse_next_bin_val,
                parse_next_dec_val,
                parse_next_hex_val,
                parse_next_prose_val
                ]
            )

        if res is None:
            ret = None

        else:

            if len(res) != 1:
                ret = None

    if ret is not None:
        ret.append_child(res[0])

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

    res = wayround_org.pt.utils.parse_next_re(
        text, start, error_log, prefix
        )

    if res is None:
        ret = False

    if ret:
        target_node.append_child(res)
        start = res.index1

    if ret:

        children = []

        _start = parse_next_x_any_number(
            text, start, error_log, digit_parser, children
            )

        if start == _start:
            ret = False
        else:
            start = _start

        del _start

        target_node.append_children_from_list(children)

        del children

    if ret:
        if (
                text[start] == '.'
                and digit_parser(text, start + 1, []) is not None
                ):

            dotted_elements = []

            while True:

                res = wayround_org.pt.utils.parse_next_re(
                    text,
                    start,
                    error_log,
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

        elif (
                text[start] == '-'
                and digit_parser(text, start + 1, []) is not None
                ):

            res = wayround_org.pt.utils.parse_next_re(
                text,
                start,
                error_log,
                r'\-({})+'.format(
                    digit_re
                    )
                )

            if res is not None:
                target_node.append_child(res)

        else:
            pass

    return ret


def parse_next_bin_val(text, start, error_log):
    r'b({BIT})+((\.({BIT})+)+|(\-({BIT})+))?'
    # ; series of concatenated bit values
    # ;  or single ONEOF range

    ret = wayround_org.pt.ast.Node('bin-val', start)

    if not parse_next_x_val(text, start, error_log, 'b', ret):
        ret = None

    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_dec_val(text, start, error_log):
    r'd({DIGIT})+((\.({DIGIT})+)+|(\-({DIGIT})+))?'

    ret = wayround_org.pt.ast.Node('dec-val', start)

    if not parse_next_x_val(text, start, error_log, 'd', ret):
        ret = None

    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_hex_val(text, start, error_log):
    r'x({HEXDIG})+((\.({HEXDIG})+)+|(\-({HEXDIG})+))?'

    ret = wayround_org.pt.ast.Node('hex-val', start)

    if not parse_next_x_val(text, start, error_log, 'x', ret):
        ret = None

    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_prose_val(text, start, error_log):
    r'\<([\x20-\x3d]|[\x3f-\x7e])*\>'

    ret = wayround_org.pt.ast.Node('prose-val', start)

    res = wayround_org.pt.utils.parse_next_re(
        text, start, error_log, r'\<'
        )

    if res is None:
        ret = None

    if ret is not None:
        ret.append_child(res)
        start = res.index1

    if ret is not None:

        res = wayround_org.pt.utils.parse_next_re(
            text, start, error_log, r'([\x20-\x3d]|[\x3f-\x7e])*'
            )

        if res is None:
            ret = None

        if ret is not None:
            ret.append_child(res)
            start = res.index1

    if ret is not None:

        res = wayround_org.pt.utils.parse_next_re(
            text, start, error_log, r'\>'
            )

        if res is None:
            ret = None

        if ret is not None:
            ret.append_child(res)

    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_HEXDIG(text, start, error_log):

    ret = wayround_org.pt.ast.Node('HEXDIG', start)

    res = RULES.compiled['HEXDIG'].match(text, pos=start)

    if res is None:
        ret = None

    if ret is not None:
        ret.index0 = res.start()
        ret.index1 = res.end()

    return ret


def parse_next_DIGIT(text, start, error_log):

    ret = wayround_org.pt.ast.Node('DIGIT', start)

    res = RULES.compiled['DIGIT'].match(text, pos=start)

    if res is None:
        ret = None

    if ret is not None:
        ret.index0 = res.start()
        ret.index1 = res.end()

    return ret


def parse_next_BIT(text, start, error_log):

    ret = wayround_org.pt.ast.Node('BIT', start)

    res = RULES.compiled['BIT'].match(text, pos=start)

    if res is None:
        ret = None

    if ret is not None:
        ret.index0 = res.start()
        ret.index1 = res.end()

    return ret


def parse_next_ALPHA(text, start, error_log):

    ret = wayround_org.pt.ast.Node('ALPHA', start)

    res = RULES.compiled['ALPHA'].match(text, pos=start)

    if res is None:
        ret = None

    if ret is not None:
        ret.index0 = res.start()
        ret.index1 = res.end()

    return ret


def parse_next_WSP(text, start, error_log):

    ret = wayround_org.pt.ast.Node('WSP', start)

    res = RULES.compiled['WSP'].match(text, pos=start)

    if res is None:
        ret = None

    if ret is not None:
        ret.index0 = res.start()
        ret.index1 = res.end()

    return ret


def parse_next_CRoLF(text, start, error_log):

    ret = wayround_org.pt.ast.Node('CRoLF', start)

    res = RULES.compiled['CRoLF'].match(text, pos=start)

    if res is None:
        ret = None

    if ret is not None:
        ret.index0 = res.start()
        ret.index1 = res.end()

    return ret


def parse_next_VCHAR(text, start, error_log):

    ret = wayround_org.pt.ast.Node('VCHAR', start)

    res = RULES.compiled['VCHAR'].match(text, pos=start)

    if res is None:
        ret = None

    if ret is not None:
        ret.index0 = res.start()
        ret.index1 = res.end()

    return ret
