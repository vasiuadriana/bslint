# pylint: disable=too-many-instance-attributes

import bslint.messages.error_constants as err_const
import bslint.messages.handler as err
import bslint.lexer.handlers.match_handler as match_handler
import bslint.lexer.handlers.regex_handler as regex_handler
import bslint.lexer.handlers.styling_handler as styling_handler
import bslint.utilities.custom_exceptions as custom_exception
from bslint.lexer.token import Token
import bslint.constants as const
import bslint.lexer.handlers.styling_dispatcher as styling_dispatcher

MATCH = "match"


class Lexer:
    def __init__(self):
        self.tokens = []
        self.errors = []
        self.handle_match = match_handler.MatchHandler()
        self.characters = ""
        self.handle_style = None
        self.preceding_token = None
        self.is_valid_token = True
        self.current_token_index = 0
        self.statements_counter = 0

    def lex(self, characters):
        self.characters = characters
        self.handle_style = styling_handler.StylingHandler(characters)
        self.handle_style.dispatcher = styling_dispatcher.Dispatcher(self.handle_style)
        while self.handle_style.current_char_index < len(self.characters):
            try:
                self.create_token_and_handle_styling()
            except custom_exception.UnexpectedTokenException:
                self.handle_unexpected_token()
                break

        self.handle_style.apply_new_line_styling()
        self.statements_counter += 1
        return self.build_return_message()

    def build_return_message(self):
        if len(self.errors) != 0:
            return {const.STATUS: const.ERROR, const.TOKENS: self.errors, const.WARNINGS: self.handle_style.warnings}
        else:
            return {const.STATUS: const.SUCCESS, const.TOKENS: self.tokens, const.WARNINGS: self.handle_style.warnings}

    def create_token_and_handle_styling(self):
        regex_match = regex_handler.find_match(self.characters[self.handle_style.current_char_index:])
        self.handle_style.line_length += len(regex_match[MATCH].group())
        self.handle_style.current_char_index += len(regex_match[MATCH].group())
        if regex_match["token_lexer_type"] is not None:
            applied_common_styling = self.handle_style.apply_styling(regex_match)
            if applied_common_styling:
                token = self.handle_match.match_handler(regex_match)
                if token is not None:
                    token.line_number = self.handle_style.line_number
                    self.tokens.append(token)
            self.add_commas_to_object()
            self.handle_style.check_end_of_statement()
            self.remove_trailing_comma()
            self.handle_end_of_statement()

    def handle_end_of_statement(self):
        if self.handle_style.end_of_statement:
            self.check_statement_validity(self.tokens[self.current_token_index:])
            self.handle_style.end_of_statement = False
            self.current_token_index = len(self.tokens)

    def remove_trailing_comma(self):
        if self.handle_style.check_remove_trailing_comma:
            if self.tokens[-2].parser_type == const.COMMA:
                self.tokens.pop(-2)

    def add_commas_to_object(self):
        if self.handle_style.add_object_commas:
            if self.tokens[-1].lexer_type != const.OPEN_CURLY_BRACKET and \
                            self.tokens[-1].parser_type != const.COMMA:
                comma_token = Token(",", const.SPECIAL_OPERATOR, const.COMMA, None)
                comma_token.line_number = self.handle_style.line_number
                self.tokens.append(comma_token)

    def handle_unexpected_token(self):
        end_of_line = self.characters[self.handle_style.current_char_index:].split("\n")[0]
        self.errors.append(err.get_error_msg(err_const.UNMATCHED_QUOTATION_MARK, [end_of_line,
                                                                                  self.handle_style.line_number]))

    # pylint: disable=unused-argument
    def check_statement_validity(self, statement):
        self.statements_counter += 1
