## GRAMMAR

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
                        : power

---

        power           : atom(POWER factor)*

---

        atom            : INT | FLOAT | IDENTIFIER
                        : LPARAN expr RPARAN
---
        if-expr	        : KEYWORD:IF expr KEYWORD:THEN expr
                          (KEYWORD:ELIF expr KEYWORD:THEN expr)*
                          (KEYWORD:ELSE expr)?
---
        for-expr	: KEYWORD:FOR IDENTIFIER EQ expr KEYWORD:TO expr 
                          (KEYWORD:STEP expr)? KEYWORD:THEN expr
---     
        while-expr	: KEYWORD:WHILE expr KEYWORD:THEN expr