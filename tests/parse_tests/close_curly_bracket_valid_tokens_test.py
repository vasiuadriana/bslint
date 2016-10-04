import unittest
from bslint import constants as const
from bslint.parser.parser import Parser


class TestCloseCurlyBracketValidTokens(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.preceding_token_type = const.CLOSE_CURLY_BRACKET

    def testComma(self):
        current_token_type = const.COMMA
        result = Parser.is_valid_token(self.preceding_token_type, current_token_type)
        self.assertTrue(result)

    def testColon(self):
        current_token_type = const.COLON
        result = Parser.is_valid_token(self.preceding_token_type, current_token_type)
        self.assertTrue(result)

    def testCloseCurlyBracket(self):
        current_token_type = const.CLOSE_CURLY_BRACKET
        result = Parser.is_valid_token(self.preceding_token_type, current_token_type)
        self.assertTrue(result)

    def testAs(self):
        current_token_type = const.AS
        result = Parser.is_valid_token(self.preceding_token_type, current_token_type)
        self.assertFalse(result)

    def testOpenCurlyBracket(self):
        current_token_type = const.OPEN_CURLY_BRACKET
        result = Parser.is_valid_token(self.preceding_token_type, current_token_type)
        self.assertFalse(result)

    def testFor(self):
        current_token_type = const.FOR
        result = Parser.is_valid_token(self.preceding_token_type, current_token_type)
        self.assertFalse(result)
