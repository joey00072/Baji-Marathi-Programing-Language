# -----------ERROR--------------
class Error:
    def __init__(self, error_name, pos_start, pos_end, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name} : {self.details} \n'
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln+1}'
        result += '\n\n' + \
            self.string_with_arrows(
                self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result

    def string_with_arrows(self, text, pos_start, pos_end):
        result = ''

        # Calculate indices
        idx_start = max(text.rfind('\n', 0, pos_start.idx), 0)
        idx_end = text.find('\n', idx_start + 1)
        if idx_end < 0:
            idx_end = len(text)

        # Generate each line
        line_count = pos_end.ln - pos_start.ln + 1
        for i in range(line_count):
            # Calculate line columns
            line = text[idx_start:idx_end]
            col_start = pos_start.col if i == 0 else 0
            col_end = pos_end.col if i == line_count - 1 else len(line) - 1

            # Append to result
            result += line + '\n'
            result += ' ' * col_start + '^' * (col_end - col_start)

            # Re-calculate indices
            idx_start = idx_end
            idx_end = text.find('\n', idx_start + 1)
            if idx_end < 0:
                idx_end = len(text)

        return result.replace('\t', '')