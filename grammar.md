## GRAMMAR
---
        statements      : NEWLINE* statement (NEWLINE+ statement)* NEWLINE*
---
        statement       : KEYWORD:RETURN expr?
                        : KEYWORD:CONTINUE
                        : KEYWORD:BREAK
                        : expr
---

        expr            : KEYWORD var|चल IDENTIFIER EQ expr
                        : comp-expr ((KEYWORD:AND|KEYWORD:OR) comp-expr)*

---

        comp-expr       : NOT comp-expr
                        : arith-expr ((EE|LT|GT|LTE|GTE) arith-expr)*

---

        arith-expr      : term ((PLUS|MINUS) term)*

---

        term            : factor((MUL|DIV) factor)*

---

        factor          : (PLUS|MINUS) factor
                        : mod
---
        mod             : expr MOD expr
                        : power
---

        power           : call(POWER factor)*
---
        call            : atom (LPAREN (expr (COMMA expr)*)? RPAREN)?
                        : atom (LSQUARE (expr) LSQUARE)? EQ expr
                        : atom (LSQUARE (expr) LSQUARE)? 

---

        atom            : INT | FLOAT | STRING | IDENTIFIER
                        : LPARAN expr RPARAN
                        : list-expr
                        : if-expr
                        : for-expr
                        : while-expr
                        : func-def
---
        list-expr       : LSQUARE (expr (COMMA expr)*)? RSQUARE
---
        if-expr         : KEYWORD:IF expr KEYWORD:THEN
                          (statement if-expr-b|if-expr-c?)
                        | (NEWLINE statements KEYWORD:END|if-expr-b|if-expr-c)
---
        if-expr-b       : KEYWORD:ELIF expr KEYWORD:THEN
                          (statement if-expr-b|if-expr-c?)
                        | (NEWLINE statements KEYWORD:END|if-expr-b|if-expr-c)
---
        if-expr-c       : KEYWORD:ELSE
                          statement
                        | (NEWLINE statements KEYWORD:END)

---
        for-expr        : KEYWORD:FOR IDENTIFIER EQ expr KEYWORD:TO 
                          statement
                        | (NEWLINE statements KEYWORD:END)expr
                        
---     
        while-expr      : KEYWORD:WHILE expr KEYWORD:THEN 
                          statement
                        | (NEWLINE statements KEYWORD:END)
---
        func-def        : KEYWORD:FUN IDENTIFIER?
                          LPAREN (IDENTIFIER (COMMA IDENTIFIER)*)? RPAREN
                          (ARROW expr)
                        | (NEWLINE statements KEYWORD:END)

