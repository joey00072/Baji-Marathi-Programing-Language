## GRAMMAR

        expr            : KEYWORD var|चल IDENTIFIER EQ expr
                        : comp-expr ((KEYWORD:AND|KEYWORD:OR) comp-expr)*

---

        comp-expr       : NOT comp-expr
                        : arith-expr ((EE|LT|GT|LTE|GTE) arith-expr)*

---

        arith-expr      :term ((PLUS|MINUS) term)*

---

        term            :factor((MUL|DIV) factor)*

---

        factor          :(PLUS|MINUS) factor
                        :power

---

        power           :atom(POWER factor)*

---

        atom            : INT | FLOAT | IDENTIFIER
                        : LPARAN expr RPARAN
