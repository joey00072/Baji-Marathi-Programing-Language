from Errors.base_error import Error


class IllegalCharacterError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(
            "चुकीचे अक्षर (Illegal Character)", pos_start, pos_end, details
        )


class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__("अवैध वाक्यरचना (InvalidSyntax)", pos_start, pos_end, details)


class ExpectedCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__("Expected Character", pos_start, pos_end, details)


class RTError(Error):
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__("Runtime Error", pos_start, pos_end, details)
        self.context = context

    def as_string(self):
        result = self.generate_traceback()
        result += f"{self.error_name}: {self.details}"
        result += "\n\n" + self.string_with_arrows(
            self.pos_start.ftxt, self.pos_start, self.pos_end
        )
        return result

    def generate_traceback(self):
        result = ""
        pos = self.pos_start
        ctx = self.context

        while ctx:
            result = (
                f"  File {pos.fn}, line {str(pos.ln + 1)}, in {ctx.display_name}\n"
                + result
            )
            pos = ctx.parent_entry_pos
            ctx = ctx.parent

        return "Traceback (most recent call last):\n" + result
