
def parse_next_ALPHA(text, start, error_log):

    """
    ALPHA          =  %x41-5A / %x61-7A   ; A-Z / a-z
    """

    ret = wayround_i2p.pt.ast.Node('ALPHA', start)



    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_BIT(text, start, error_log):

    """
    BIT            =  "0" / "1"
    """

    ret = wayround_i2p.pt.ast.Node('BIT', start)



    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_CHAR(text, start, error_log):

    """
    CHAR           =  %x01-7F
                           ; any 7-bit US-ASCII character,
                           ;  excluding NUL
    """

    ret = wayround_i2p.pt.ast.Node('CHAR', start)



    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_CR(text, start, error_log):

    """
    CR             =  %x0D
                           ; carriage return
    """

    ret = wayround_i2p.pt.ast.Node('CR', start)



    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_CRLF(text, start, error_log):

    """
    CRLF           =  CR LF
                           ; Internet standard newline
    """

    ret = wayround_i2p.pt.ast.Node('CRLF', start)



    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_CRoLF(text, start, error_log):

    """
    CRoLF           =  [ CR ] LF
                           ; Non-standard modification
                           ; by WayRound.org at Wed Sep 7 20:52:41 MSK 2016
    """

    ret = wayround_i2p.pt.ast.Node('CRoLF', start)



    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_CTL(text, start, error_log):

    """
    CTL            =  %x00-1F / %x7F
                           ; controls
    """

    ret = wayround_i2p.pt.ast.Node('CTL', start)



    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_DIGIT(text, start, error_log):

    """
    DIGIT          =  %x30-39
                           ; 0-9
    """

    ret = wayround_i2p.pt.ast.Node('DIGIT', start)



    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_DQUOTE(text, start, error_log):

    """
    DQUOTE         =  %x22
                           ; " (Double Quote)
    """

    ret = wayround_i2p.pt.ast.Node('DQUOTE', start)



    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_HEXDIG(text, start, error_log):

    """
    HEXDIG         =  DIGIT / "A" / "B" / "C" / "D" / "E" / "F"
    """

    ret = wayround_i2p.pt.ast.Node('HEXDIG', start)



    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_HTAB(text, start, error_log):

    """
    HTAB           =  %x09
                           ; horizontal tab
    """

    ret = wayround_i2p.pt.ast.Node('HTAB', start)



    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_LF(text, start, error_log):

    """
    LF             =  %x0A
                           ; linefeed
    """

    ret = wayround_i2p.pt.ast.Node('LF', start)



    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_LWSP(text, start, error_log):

    """
    LWSP           =  *(WSP / CRLF WSP)
                           ; Use of this linear-white-space rule
                           ;  permits lines containing only white
                           ;  space that are no longer legal in
                           ;  mail headers and have caused
                           ;  interoperability problems in other
                           ;  contexts.
                           ; Do not use when defining mail
                           ;  headers and use with caution in
                           ;  other contexts.
    """

    ret = wayround_i2p.pt.ast.Node('LWSP', start)



    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_OCTET(text, start, error_log):

    """
    OCTET          =  %x00-FF
                           ; 8 bits of data
    """

    ret = wayround_i2p.pt.ast.Node('OCTET', start)



    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_SP(text, start, error_log):

    """
    SP             =  %x20
    """

    ret = wayround_i2p.pt.ast.Node('SP', start)



    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_VCHAR(text, start, error_log):

    """
    VCHAR          =  %x21-7E
                           ; visible (printing) characters
    """

    ret = wayround_i2p.pt.ast.Node('VCHAR', start)



    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_WSP(text, start, error_log):

    """
    WSP            =  SP / HTAB
                           ; white space
    """

    ret = wayround_i2p.pt.ast.Node('WSP', start)



    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_rulelist(text, start, error_log):

    """
    rulelist       =  1*( rule / (*c-wsp c-nl) )
    """

    ret = wayround_i2p.pt.ast.Node('rulelist', start)



    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_rule(text, start, error_log):

    """
    rule           =  rulename defined-as elements c-nl
                           ; continues if next line starts
                           ;  with white space
    """

    ret = wayround_i2p.pt.ast.Node('rule', start)



    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_rulename(text, start, error_log):

    """
    rulename       =  ALPHA *(ALPHA / DIGIT / "-")
    """

    ret = wayround_i2p.pt.ast.Node('rulename', start)



    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_defined_as(text, start, error_log):

    """
    defined-as     =  *c-wsp ("=" / "=/") *c-wsp
                           ; basic rules definition and
                           ;  incremental alternatives
    """

    ret = wayround_i2p.pt.ast.Node('defined-as', start)



    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_elements(text, start, error_log):

    """
    elements       =  alternation *c-wsp
    """

    ret = wayround_i2p.pt.ast.Node('elements', start)



    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_c_wsp(text, start, error_log):

    """
    c-wsp          =  WSP / (c-nl WSP)
    """

    ret = wayround_i2p.pt.ast.Node('c-wsp', start)



    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_c_nl(text, start, error_log):

    """
    c-nl           =  comment / CRLF
                           ; comment or newline
    """

    ret = wayround_i2p.pt.ast.Node('c-nl', start)



    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_comment(text, start, error_log):

    """
    comment        =  ";" *(WSP / VCHAR) CRLF
    """

    ret = wayround_i2p.pt.ast.Node('comment', start)



    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_alternation(text, start, error_log):

    """
    alternation    =  concatenation
                      *(*c-wsp "/" *c-wsp concatenation)
    """

    ret = wayround_i2p.pt.ast.Node('alternation', start)



    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_concatenation(text, start, error_log):

    """
    concatenation  =  repetition *(1*c-wsp repetition)
    """

    ret = wayround_i2p.pt.ast.Node('concatenation', start)



    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_repetition(text, start, error_log):

    """
    repetition     =  [repeat] element
    """

    ret = wayround_i2p.pt.ast.Node('repetition', start)



    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_repeat(text, start, error_log):

    """
    repeat         =  1*DIGIT / (*DIGIT "*" *DIGIT)
    """

    ret = wayround_i2p.pt.ast.Node('repeat', start)



    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_element(text, start, error_log):

    """
    element        =  rulename / group / option /
                      char-val / num-val / prose-val
    """

    ret = wayround_i2p.pt.ast.Node('element', start)



    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_group(text, start, error_log):

    """
    group          =  "(" *c-wsp alternation *c-wsp ")"
    """

    ret = wayround_i2p.pt.ast.Node('group', start)



    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_option(text, start, error_log):

    """
    option         =  "[" *c-wsp alternation *c-wsp "]"
    """

    ret = wayround_i2p.pt.ast.Node('option', start)



    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_char_val(text, start, error_log):

    """
    char-val       =  DQUOTE *(%x20-21 / %x23-7E) DQUOTE
                           ; quoted string of SP and VCHAR
                           ;  without DQUOTE
    """

    ret = wayround_i2p.pt.ast.Node('char-val', start)



    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_num_val(text, start, error_log):

    """
    num-val        =  "%" (bin-val / dec-val / hex-val)
    """

    ret = wayround_i2p.pt.ast.Node('num-val', start)



    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_bin_val(text, start, error_log):

    """
    bin-val        =  "b" 1*BIT
                      [ 1*("." 1*BIT) / ("-" 1*BIT) ]
                           ; series of concatenated bit values
                           ;  or single ONEOF range
    """

    ret = wayround_i2p.pt.ast.Node('bin-val', start)



    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_dec_val(text, start, error_log):

    """
    dec-val        =  "d" 1*DIGIT
                      [ 1*("." 1*DIGIT) / ("-" 1*DIGIT) ]
    """

    ret = wayround_i2p.pt.ast.Node('dec-val', start)



    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_hex_val(text, start, error_log):

    """
    hex-val        =  "x" 1*HEXDIG
                      [ 1*("." 1*HEXDIG) / ("-" 1*HEXDIG) ]
    """

    ret = wayround_i2p.pt.ast.Node('hex-val', start)



    if ret is not None:
        ret.reset_indexes_by_children()

    return ret


def parse_next_prose_val(text, start, error_log):

    """
    prose-val      =  "<" *(%x20-3D / %x3F-7E) ">"
                           ; bracketed string of SP and VCHAR
                           ;  without angles
                           ; prose description, to be used as
                           ;  last resort
    """

    ret = wayround_i2p.pt.ast.Node('prose-val', start)



    if ret is not None:
        ret.reset_indexes_by_children()

    return ret

