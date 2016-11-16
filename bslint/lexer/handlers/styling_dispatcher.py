# pylint: disable=too-few-public-methods
import bslint.constants as const


class Dispatcher:
    def __init__(self, styling_handler):
        self.bslint_command_dispatcher = {
            const.SKIP_LINE: styling_handler.skip_line,
            const.SKIP_FILE: styling_handler.skip_file,
        }
        self.common_styling_dispatcher = {
            const.COMMENT: styling_handler.check_comment_styling,
            const.OPERATOR: styling_handler.check_operator_spacing,
            const.ID: styling_handler.check_spelling,
            const.PRINT_KEYWORD: styling_handler.check_trace_free,
            const.FUNCTION: styling_handler.check_method_dec_spacing,
            const.SUB: styling_handler.check_method_dec_spacing,
        }
        self.end_of_statement_dispatcher = {
            const.COLON: styling_handler.set_end_of_statement,
            const.OPEN_CURLY_BRACKET: styling_handler.open_curly_bracket,
            const.CLOSE_CURLY_BRACKET: styling_handler.close_curly_bracket,
        }
        self.styling_dispatcher = {
            const.NEW_LINE: styling_handler.handle_new_line,
            const.BSLINT_COMMAND: styling_handler.apply_bslint_command
        }
