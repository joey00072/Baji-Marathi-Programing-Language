# -----------CONSTANTS-----------
DIGITS = "0123456789०१२३४५६७८९"
LATTERS = (
    "ऀँंःऄअआइईउऊऋऌऍऎएऐऑऒओऔकखगघङचछजझञटठडढणतथदधनऩपफबभमयरऱलळऴवशषसहऺऻ़ऽािीुूृॄॅॆेैॉॊोौ्ॎॏॐ॒॑॓॔ॕॖॗक़ख़ग़ज़ड़ढ़फ़य़ॠॡॢॣ।॥"
    + "०१२३४५६७८९॰ॱॲॳॴॵॶॷॸॹॺॻॼॽॾॿ"
    + "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
)
LATTERS_DIGITS = LATTERS + DIGITS

# -----------TOKEN---------------
TT_INT = "INT"
TT_FLOAT = "FLOAT"
TT_IDENTIFIER = "IDENTIFIER"
TT_KEYWORD = "KEYWORD"
TT_PLUS = "PLUS"
TT_MINUS = "MINUS"
TT_MUL = "MUL"
TT_DIV = "DIV"
TT_POWER = "POWER"
TT_EQ = "EQ"
TT_LPAREN = "LPAREN"
TT_RPAREN = "RPAREN"
TT_EE = "EE"
TT_NE = "NE"
TT_LT = "LT"
TT_GT = "GT"
TT_LTE = "LTE"
TT_GTE = "GTE"
TT_EOF = "EOF"

KEYWORDS = [
    "var",
    "चल",
    "AND",
    "आणि",
    "OR",
    "किंवा",
    "NOT",
    "नाही",
]
