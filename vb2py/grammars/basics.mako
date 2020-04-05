

NEWLINE ::=
        "\n"

<wsp> ::=
            (" "/"\t")

# Also includes the hack for a unicode marker
<safe_letter> ::=
             letter / '~~'

<letter> ::=
             lowercase / uppercase

lowercase ::=
             [a-z]

uppercase ::=
             [A-Z]

<digit> ::=
             [0-9]

stringliteral ::=
             '"', stringitem*, '"'

<stringitem> ::=
             stringchar / escapeseq / '""'

stringchar ::= -('"' / NEWLINE)+

dateliteral ::=
			"#", integer, "/", integer, ("/", integer)?, (wsp+, timeliteral)?, (wsp+, ampm)?, "#"

ampm ::=
            c"AM" / c"PM"

timeliteral ::=
            integer, ":", integer, (":", integer)?

escapeseq ::=
             "\\", stringchar

longinteger ::=
             integer, ("l" / "L")

integer ::=
             "-"?, decimalinteger, ("%" / "&" / "@" / "!")?

decimalinteger ::=
             digit+

hexinteger ::=
             "&", "H"?, hexdigit+, "&"?

octinteger ::=
             ("&O" / "0"), octdigit+, "&"?

binaryinteger ::=
             "&B", binarydigit, (binarydigit / "_")*, "&"?

<nonzerodigit> ::=
             [1-9]

<octdigit> ::=
             [0-7]

<hexdigit> ::=
             digit / [a-f] / [A-F]

<binarydigit> ::=
              [0-1]

floatnumber ::=
             ("-"?, (exponentfloat / pointfloat)) / (integer, "#"), "!"?

<pointfloat> ::=
             (intpart?, fraction) / (intpart, ".")

<exponentfloat> ::=
             (pointfloat / intpart),
              exponent

<intpart> ::=
             digit+

<fraction> ::=
             ".", digit+

<exponent> ::=
             ("e" / "E"), ("+" / "-")?, digit+