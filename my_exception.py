# Create an exception from a list of tokens, an error position in the tokens, and an error message
class MyException(Exception):
    def __init__(self, tokens, err_pos, err_msg):
        self.tokens = tokens
        self.err_pos = err_pos
        self.err_msg = err_msg

    # Print the tokens with a cursor indicating where the error is
    def __str__(self):
        cursor = ""
        for i, token in enumerate(self.tokens):
            if i != self.err_pos:
                cursor += " " * len(token)

            else:
                cursor += "^" + " " * (len(token) - 1)

        tokens_str = "".join(self.tokens)
        return "\n".join([tokens_str, cursor, self.err_msg])
