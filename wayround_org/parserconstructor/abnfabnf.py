
import regex

import wayround_org.abnf.core


RULES = wayround_org.abnf.utils.Rules(
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
            r'([\x20-\x21]|[\x23-\x7e])'
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
    [wayround_org.abnf.core.RULES]
    )
