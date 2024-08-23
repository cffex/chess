import piece as piece_class
import precompute_movedata
squares_to_edge_lookup = precompute_movedata.squares_to_edge_lookup
knight_movement_lookup = precompute_movedata.knight_movement_lookup
king_movement_lookup = precompute_movedata.king_movement_lookup
pawn_movement_lookup = precompute_movedata.pawn_movement_lookup
piece_class_none = piece_class.none

def generate_sliding_moves(squares: list, row: int, col: int, piece: int, moves: list):
    piece_type = piece_class.get_piece_type(piece)
    piece_color = piece_class.get_color(piece)

    start_dir_index = (piece_type == piece_class.bishop and 4) or 0
    end_dir_index = (piece_type == piece_class.rook and 4) or 8
    square_index = row * 8 + col

    for dir_index in range(start_dir_index, end_dir_index):
        movement_dir = piece_class.piece_movedirection[dir_index]
        squares_to_edge = squares_to_edge_lookup[square_index][dir_index]

        for n in range(1, squares_to_edge + 1):
            target_square_index = square_index + movement_dir * n
            piece_on_target_square = squares[target_square_index]
            piece_on_target_square_exist = piece_on_target_square != piece_class_none
            piece_on_target_square_is_friendly = piece_class.get_color(piece_on_target_square) == piece_color

            # Blocked by friendly piece
            if piece_on_target_square_exist and piece_on_target_square_is_friendly:
                break

            moves.append((square_index, target_square_index))

            # Blocked by enemy piece
            if piece_on_target_square_exist and not piece_on_target_square_is_friendly:
                break

def generate_pawn_moves(squares: list, row: int, col: int, piece: int, moves: list, pawn_movement_data: list):
    square_index = row * 8 + col
    move_count = pawn_movement_data[square_index]
    color = piece_class.get_color(piece)
    pawn_moves = pawn_movement_lookup[square_index][1 - int(0.5 * (color + 1))]
    single_pawn_push_blocked = False

    for target_index in pawn_moves:
        delta_move = abs(target_index - square_index)
        is_push_move = delta_move == 8 or delta_move == 16
        piece_on_target_square = squares[target_index]

        # Push move
        if is_push_move:
            if delta_move == 8:
                # Single pawn push
                if piece_on_target_square == piece_class_none:
                    # If square is not occupied
                    moves.append((square_index, target_index))
                else:
                    single_pawn_push_blocked = True
                    continue
            elif delta_move == 16:
                # Double pawn push:
                if not single_pawn_push_blocked and piece_on_target_square == piece_class_none and move_count == 0:
                    # If single pawn push was not blocked and square is not occupied and piece has not moved
                    moves.append((square_index, target_index))
        else:
            # Capture move
            if piece_on_target_square != piece_class_none:
                if piece_class.get_color(piece_on_target_square) != color:
                    moves.append((square_index, target_index))

    # En passant
        

def generate_knight_moves(squares: list, row: int, col: int, piece: int, moves: list):
    square_index = row * 8 + col
    move_target_indices = knight_movement_lookup[square_index]
    color = piece_class.get_color(piece)

    for move_target_index in move_target_indices:
        piece_on_move_target = squares[move_target_index]

        if piece_on_move_target == piece_class_none or piece_class.get_color(piece_on_move_target) != color:
            moves.append((square_index, move_target_index))

def generate_king_moves(squares: list, row: int, col: int, piece: int, moves: list):
    square_index = row * 8 + col
    color = piece_class.get_color(piece)

    for target_square_index in king_movement_lookup[square_index]:
        piece_on_target_square = squares[target_square_index]
        piece_on_target_square_exist = piece_on_target_square == piece_class_none
        piece_on_target_square_is_enemy = piece_class.get_color(piece_on_target_square)!= color 

        if (piece_on_target_square_exist or piece_on_target_square_is_enemy) and not piece_class.is_king(piece_on_target_square):
            moves.append((square_index, target_square_index))

def generate_moves(squares: list, piece_indices: list, moves: list, pawn_movement_data: list):
    for square_index in piece_indices:
        piece = squares[square_index]
        row, col = square_index // 8, square_index % 8

        if piece_class.is_sliding_move(piece):
            generate_sliding_moves(
                squares=squares, 
                row=row, 
                col=col,
                piece=piece, 
                moves=moves
            )
        else:
            if piece_class.is_pawn(piece):
                generate_pawn_moves(
                    squares=squares,
                    row=row,
                    col=col,
                    piece=piece,
                    moves=moves,
                    pawn_movement_data=pawn_movement_data
                )
            elif piece_class.is_knight(piece):
                generate_knight_moves(
                    squares=squares,
                    row=row,
                    col=col,
                    piece=piece,
                    moves=moves
                )
            elif piece_class.is_king(piece):
                generate_king_moves(
                    squares=squares,
                    row=row,
                    col=col,
                    piece=piece,
                    moves=moves
                )