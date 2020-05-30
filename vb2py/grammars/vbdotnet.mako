

region_statement ::=
    "#", wsp*, c"Region", wsp+, stringliteral, line_end,
    region_block,
    "#", wsp*, c"End", wsp+, c"Region"


region_block ::=
    (?-((label_statement, wsp+)?, region_block_terminator), line)*


region_block_terminator ::= "#", wsp*, c"End", wsp+, c"Region"