from bslint import constants as const
from bslint.messages import handler as msg_handler
from bslint.lexer import commands as commands
from bslint.lexer.token import Token


class StylingHandler:
    # pylint: disable=too-many-instance-attributes
    def __init__(self, characters, lexer):
        self._is_empty_line = True
        self._skip_styling_on_file = False
        self._line_not_to_style_check = -1
        self._current_indentation_level = 0
        self._indentation_level = 0
        self._token_lexer_type = None
        self._match = None
        self._consecutive_empty_lines = 0
        self.line_number = 1
        self.line_length = 0
        self.characters = characters
        self.current_char_index = 0
        self.warnings = []
        self.end_of_statement = False
        self.open_curly_braces = 0
        self.applied_common_styling = False
        self.dispatcher = None
        self.lexer = lexer

    def _get_last_line(self):
        last_line = self.characters[:self.current_char_index - 1].split("\n")
        return last_line[-1]

    def skip_line(self):
        self._line_not_to_style_check = commands.check_skip_line(self.line_number)

    def skip_file(self):
        self._skip_styling_on_file = commands.check_skip_file()

    def apply_bslint_command(self):
        command_type = self._match.group(const.COMMAND)
        self.dispatcher.bslint_command_dispatcher[command_type]()

    def apply_styling(self, regex_match):
        self._match = regex_match[const.MATCH]
        self._token_lexer_type = regex_match[const.TOKEN_LEXER_TYPE]
        if regex_match[const.INDENTATION_LEVEL] != const.NO_INDENTATION:
            self._indentation_level += regex_match[const.INDENTATION_LEVEL]

        self.applied_common_styling = False
        if self._token_lexer_type in self.dispatcher.styling_dispatcher.keys():
            self.dispatcher.styling_dispatcher[self._token_lexer_type]()
        else:
            self.apply_common_styling()
        return self.applied_common_styling

    def handle_new_line(self):
        self.end_of_statement = True
        self.apply_new_line_styling()
        self._check_add_object_commas()
        self.line_number += 1
        self.line_length = 0

    def style_checking_is_active(self):
        return self.line_number != self._line_not_to_style_check and not self._skip_styling_on_file

    def check_trace_free(self):
        is_trace_free = commands.check_trace_free()
        self._warning_filter(is_trace_free)

    def apply_common_styling(self):
        self.applied_common_styling = True
        if not self.style_checking_is_active():
            return
        self._is_empty_line = False
        if self._token_lexer_type in self.dispatcher.common_styling_dispatcher.keys():
            self.dispatcher.common_styling_dispatcher[self._token_lexer_type]()

    def check_method_dec_spacing(self):
        is_correct_method_dec_spacing = commands.check_method_dec_spacing(self.characters)
        self._warning_filter(is_correct_method_dec_spacing)

    def check_spelling(self):
        is_spelt_correctly = commands.check_spelling(self._match.group(), self._token_lexer_type)
        self._warning_filter(is_spelt_correctly)

    def check_operator_spacing(self):
        correct_spacing = commands.check_spaces_around_operators(self.characters, self.current_char_index)
        self._warning_filter(correct_spacing)

    def check_comment_styling(self):
        is_correct_comment = commands.check_comment(self._match.group())
        self._warning_filter(is_correct_comment)
        self.check_spelling()

    def apply_new_line_styling(self):
        if not self.style_checking_is_active():
            return
        self._count_consecutive_new_lines()
        is_correct_line_length = commands.check_max_line_length(self.line_length)
        self._warning_filter(is_correct_line_length)

        is_consecutive_empty_lines = commands.check_consecutive_empty_lines(self._consecutive_empty_lines)
        self._warning_filter(is_consecutive_empty_lines)

        last_read_line = self._get_last_line()
        self._apply_indentation_styling(last_read_line)

    def _apply_indentation_styling(self, last_read_line):
        is_correct_indentation = commands.check_indentation(self._current_indentation_level, last_read_line,
                                                            self._indentation_level)
        if is_correct_indentation:
            self._warning_filter(is_correct_indentation[0])
            self._current_indentation_level = is_correct_indentation[1]
            self._indentation_level = 0

    def _count_consecutive_new_lines(self):
        if self._is_empty_line:
            self._consecutive_empty_lines += 1
        else:
            self._is_empty_line = True
            self._consecutive_empty_lines = 0

    def check_end_of_statement(self):
        if self._token_lexer_type in self.dispatcher.end_of_statement_dispatcher.keys():
            self.dispatcher.end_of_statement_dispatcher[self._token_lexer_type]()

        if self.open_curly_braces != 0:
            self.end_of_statement = False

    def close_curly_bracket(self):
        if self.lexer.tokens[-2].parser_type == const.COMMA:
            has_trailing_comma = commands.check_trailing_comma_in_objects()
            self._warning_filter(has_trailing_comma)
            self.lexer.tokens.pop(-2)
        self.open_curly_braces -= 1

    def open_curly_bracket(self):
        self.open_curly_braces += 1

    def set_end_of_statement(self):
        self.end_of_statement = True

    def _warning_filter(self, result):
        if result is not None:
            result[const.ERROR_PARAMS].append(str(self.line_number))
            warning = msg_handler.get_error_msg(result[const.ERROR_KEY], result[const.ERROR_PARAMS])
            self.warnings += [warning]

    def _check_add_object_commas(self):
        if self.open_curly_braces != 0:
            if self.lexer.tokens[-1].lexer_type != const.OPEN_CURLY_BRACKET and \
                            self.lexer.tokens[-1].parser_type != const.COMMA:
                comma_token = Token(",", const.SPECIAL_OPERATOR, const.COMMA, None)
                comma_token.line_number = self.line_number
                self.lexer.tokens.append(comma_token)
                has_no_commas = commands.check_commas_in_objects()
                self._warning_filter(has_no_commas)

