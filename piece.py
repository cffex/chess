###
### Datavalues / enums
###

none = 0
white = 1
black = -1

pawn = 1
rook = 2
bishop = 3
knight = 4
queen = 5
king = 6

dir_top = 8
dir_bottom = -8
dir_left = -1
dir_right = 1
dir_topleft = 7
dir_topright = 9
dir_bottomleft = -9
dir_bottomright = -7

dir_knight_topleft_top = 15
dir_knight_topleft_bottom = 6
dir_knight_topright_top = 17
dir_knight_topright_bottom = 10
dir_knight_bottomleft_top = -10
dir_knight_bottomleft_bottom = -17
dir_knight_bottomright_top = -6
dir_knight_bottomright_bottom = -15

piecetype_datavalue = {
    "p": pawn,
    "r": rook,
    "b": bishop,
    "n": knight,
    "q": queen,
    "k": king
}

movetype_datavalue = {
    "normal": 1,
    "castle_ks": 2,
    "castle_qs": 3,
    "double_pawn": 4,
    "en_passant": 5,
    "pawn_promotion": 6 
}

piece_movedirection = [
    dir_top,
    dir_bottom,
    dir_left,
    dir_right,
    dir_topleft,
    dir_topright,
    dir_bottomleft,
    dir_bottomright
]

knight_movedirection = [
    dir_knight_topleft_top,
    dir_knight_topleft_bottom,
    dir_knight_topright_top,
    dir_knight_topright_bottom,
    dir_knight_bottomleft_top,
    dir_knight_bottomleft_bottom,
    dir_knight_bottomright_top,
    dir_knight_bottomright_bottom
]

###
### Utilities
###

def is_white(piece: int):
    return piece > 0

def is_black(piece: int):
    return piece < 0

##############################################################

def is_sliding_piece(piece: int):
    piecetype = abs(piece)
    return piecetype == rook or piecetype == queen or piecetype == bishop

def is_nonsliding_piece(piece: int):
    piecetype = abs(piece)
    return piecetype == pawn or piecetype == knight or piecetype == king

##############################################################

def is_pawn(piece: int):
    return get_piece_type(piece) == pawn

def is_rook(piece: int):
    return get_piece_type(piece) == rook

def is_knight(piece: int):
    return get_piece_type(piece) == knight

def is_bishop(piece: int):
    return get_piece_type(piece) == bishop

def is_queen(piece: int):
    return get_piece_type(piece) == queen

def is_king(piece: int):
    return get_piece_type(piece) == king

##############################################################

def get_color(piece: int):
    return (is_white(piece) and white) or black

def get_opposite_color(color: int):
    return -color

def get_piece_type(piece: int):
    return abs(piece)

def get_enum(piece: int):
    piecetype = abs(piece)

    if piecetype == pawn:
        return "p"
    elif piecetype == rook:
        return "r"
    elif piecetype == bishop:
        return "b"
    elif piecetype == knight:
        return "n"
    elif piecetype == queen:
        return "q"
    elif piecetype == king:
        return "k"
    elif piecetype == none:
        return "none"
    
##############################################################

# Translates [-1, 1] -> [0, 1] by -1 -> 0 and 1 -> 1 
def convert_to_01_index(color: int):
    return 1 - int(0.5 * (color + 1))