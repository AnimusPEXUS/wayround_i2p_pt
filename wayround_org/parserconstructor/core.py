
import wayround_org.abnf.utils


RULES = wayround_org.abnf.utils.Rules(
    {
        'ALPHA': r'([\x41-\x5A]|[\x61-\x7A])',  # ; A-Z / a-z'

        'BIT': r'[01]',

        'CHAR': r'[\x01-\x7F]',
        # ; any 7-bit US-ASCII character,
        # ;  excluding NUL

        'CR': r'\x0D',
        # ; carriage return

        'CRLF': r'{CR}{LF}',
        # ; Internet standard newline

        'CTL': r'([\x00-\x1F]|\x7F)',
        # ; controls

        'DIGIT': r'[\x30-\x39]',
        # ; 0-9

        'DQUOTE': r'\x22',
        # ; " (Double Quote)

        'HEXDIG': r'(({DIGIT})|A|B|C|D|E|F)',

        'HTAB': r'\x09',
        # ; horizontal tab

        'LF': r'\x0A',
        # ; linefeed

        'LWSP': r'(({WSP})|({CRLF})({WSP}))*',
        # ; Use of this linear-white-space rule
        # ;  permits lines containing only white
        # ;  space that are no longer legal in
        # ;  mail headers and have caused
        # ;  interoperability problems in other
        # ;  contexts.
        # ; Do not use when defining mail
        # ;  headers and use with caution in
        # ;  other contexts.

        'OCTET': r'[\x00-\xFF]',
        # ; 8 bits of data

        'SP': r'\x20',

        'VCHAR': r'[\x21-\x7E]',
        # ; visible (printing) characters

        'WSP': r'(({SP})|({HTAB}))'
        # ; white space
        }
    )
