import piece as piece_class
piecetype_datavalue = piece_class.piecetype_datavalue

def overwrite_position(squares: list, FEN: str, piece_indices: list, pawn_movement_data: list):
    split_FEN: str = FEN.split(" ")[0]
    row, col = 0, 0

    for char in split_FEN:
        if char == r"/":
            row += 1
            col = 0
        else:
            if char.isdigit():
                col += int(char)
            else:
                square_index = row * 8 + col
                piece = piecetype_datavalue[char.lower()] * (char.islower() and 1 or -1)
                squares[square_index] = piece
                piece_indices.append(square_index)
                col += 1

                if piece_class.is_pawn(piece):
                    pawn_movement_data[square_index] = (0, 0)