import bslint.constants as const

valid_token_associations = {
    const.WHILE: [const.ID, const.VALUE, const.NOT],
    const.ID: [const.DOT, const.OPERATOR, const.BRACKET, const.AND, const.AS, const.COLON, const.COMMA, const.OR],
    const.VALUE: [const.COMMA, const.CLOSE_PARENTHESIS, const.AND, const.COLON, const.OPERATOR],
    const.NOT: [const.ID, const.VALUE],
    const.AND: [const.ID, const.VALUE, const.OPEN_PARENTHESIS, const.NOT, const.PLUS, const.MINUS],
    const.OR: [const.ID, const.VALUE, const.OPEN_PARENTHESIS, const.NOT, const.PLUS, const.MINUS],
    const.DOT: [const.ID],
    const.OPEN_PARENTHESIS: [const.ID, const.VALUE, const.CLOSE_PARENTHESIS],
    const.CLOSE_PARENTHESIS: [const.CLOSE_PARENTHESIS, const.CLOSE_SQUARE_BRACKET, const.OPEN_PARENTHESIS,
                              const.OPEN_SQUARE_BRACKET,
                              const.OPEN_CURLY_BRACKET, const.DOT, const.COMMA, const.AS, const.OPERATOR, const.PLUS,
                              const.MINUS, const.COLON],
    const.OPEN_SQUARE_BRACKET: [const.ID, const.VALUE, const.OPEN_PARENTHESIS, const.OPEN_SQUARE_BRACKET,
                                const.CLOSE_SQUARE_BRACKET],
    const.CLOSE_SQUARE_BRACKET: [const.CLOSE_PARENTHESIS, const.CLOSE_SQUARE_BRACKET, const.DOT, const.COMMA,
                                 const.OPERATOR],
    const.OPEN_CURLY_BRACKET: [const.ID, const.VALUE, const.CLOSE_CURLY_BRACKET],
    const.CLOSE_CURLY_BRACKET: [const.COMMA, const.COLON, const.CLOSE_CURLY_BRACKET],
    const.AS: [const.ID]
}
