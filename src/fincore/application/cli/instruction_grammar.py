"""
Grammar:
<path> ":" <expr>
<path> "->" <name>
<path> "/del"
<path> OR <path> "/show" (implicit | explicit)
"""

ADD: str = "+" # <value> + <value>
SUB: str = "-" # <value> - <value>
REKEY: str = "->" # <path> "->" <name>
DELETE: str = "/del" # <path> "/del"
ASSIGN: str = ":" # <path> ":" <expr>
SELECT: str = "/show" # <path> OR <path> "/show"