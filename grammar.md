## GRAMMAR


        expr    :KEYWORD var|चल IDENTIFIER EQ expr
                :term((PLUS|MINUS) term)*
---
        term    :factor((MUL|DIV) power)*
---
        factor  :(PLUS|MINUS) factor
                :power
---
        power   :atom(POWER factor)*
---
        atom    : INT | FLOAT | IDENTIFIER
                : LPARAN expr RPARAN