import piece as piece_class
import precompute_movedata
import board
squares_to_edge_lookup = precompute_movedata.squares_to_edge_lookup
knight_movement_lookup = precompute_movedata.knight_movement_lookup
king_movement_lookup = precompute_movedata.king_movement_lookup
pawn_movement_lookup = precompute_movedata.pawn_movement_lookup
castle_range_lookup = precompute_movedata.castle_range_lookup
piece_class_none = piece_class.none

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def sign(x: int):
    return x / abs(x)

def generate_sliding_moves(squares: list, row: int, col: int, piece: int, moves: list):
    piece_type = piece_class.get_piece_type(piece)
    piece_color = piece_class.get_color(piece)

    start_dir_index = 4 if piece_type == piece_class.bishop else 0
    end_dir_index = 4 if piece_type == piece_class.rook else 8
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

def generate_pawn_moves(squares: list, row: int, col: int, piece: int, moves: list, pawn_movement_data: list, move_count: int):
    square_index = row * 8 + col
    single_pawn_push_blocked = False
    color = piece_class.get_color(piece)
    pawn_move_count = pawn_movement_data[square_index][0]

    for target_index in pawn_movement_lookup[square_index][piece_class.convert_to_01_index(color)]:
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
                # Double pawn push
                if not single_pawn_push_blocked and piece_on_target_square == piece_class_none and pawn_move_count == 0:
                    # If single pawn push was not blocked
                    # AND square is not occupied 
                    # AND piece has not moved
                    moves.append((square_index, target_index))
        else:
            # Capture move
            if piece_on_target_square != piece_class_none:
                if piece_class.get_color(piece_on_target_square) != color:
                    moves.append((square_index, target_index))

    # En passant

    if row == 3 or row == 4:
        left_adjacent_square_index = square_index - 1
        right_adjacent_square_index = square_index + 1

        piece_on_left_adjacent_square = squares[left_adjacent_square_index]
        piece_on_right_adjacent_square = squares[right_adjacent_square_index]

        # Left en passant
        if piece_on_left_adjacent_square != piece_class_none:
            if piece_class.is_pawn(piece_on_left_adjacent_square) and piece_class.get_color(piece_on_left_adjacent_square) != color:
                left_pawn_movement_data = pawn_movement_data[left_adjacent_square_index]

                if left_pawn_movement_data[0] == 1 and move_count == left_pawn_movement_data[1]:
                    # If adjacent piece exist
                    # AND piece is a pawn 
                    # AND piece is an enemy 
                    # AND piece only moved once
                    # AND piece moved only a turn ago
                    moves.append((square_index, left_adjacent_square_index + piece_class.dir_top * color))

        # Right en passant
        if piece_on_right_adjacent_square != piece_class_none:
            if piece_class.is_pawn(piece_on_right_adjacent_square) and piece_class.get_color(piece_on_right_adjacent_square) != color:
                right_pawn_movement_data = pawn_movement_data[right_adjacent_square_index]
                
                if right_pawn_movement_data[0] == 1 and move_count == right_pawn_movement_data[1]:
                    # If adjacent piece exist 
                    # AND piece is a pawn 
                    # AND piece is an enemy 
                    # AND piece only moved once
                    # AND piece moved only a turn ago
                    moves.append((square_index, right_adjacent_square_index + piece_class.dir_top * color))

def generate_knight_moves(squares: list, row: int, col: int, piece: int, moves: list):
    square_index = row * 8 + col
    move_target_indices = knight_movement_lookup[square_index]
    color = piece_class.get_color(piece)

    for move_target_index in move_target_indices:
        piece_on_move_target = squares[move_target_index]

        if piece_on_move_target == piece_class_none or piece_class.get_color(piece_on_move_target) != color:
            moves.append((square_index, move_target_index))

def generate_king_moves(squares: list, row: int, col: int, piece: int, moves: list, castling_allowed: list, legal_move_search: bool):
    square_index = row * 8 + col
    color = piece_class.get_color(piece)

    for target_square_index in king_movement_lookup[square_index]:
        piece_on_target_square = squares[target_square_index]
        piece_on_target_square_exist = piece_on_target_square == piece_class_none
        piece_on_target_square_is_enemy = piece_class.get_color(piece_on_target_square)!= color 

        if (piece_on_target_square_exist or piece_on_target_square_is_enemy): #and not piece_class.is_king(piece_on_target_square):
            moves.append((square_index, target_square_index))

    # Castling
    #print("white king" if color == piece_class.white else "black")
    #print("square_index:", square_index)
    #print("is searching legal move:", legal_move_search)

    # Positional condition
    if col == 4 and (row == 0 or row == 7):
        is_white = color > 0
        left_range = castle_range_lookup[0][0] if is_white else castle_range_lookup[1][0]
        right_range = castle_range_lookup[0][1] if is_white else castle_range_lookup[1][1]

        left_castle_allowed = castling_allowed[piece_class.convert_to_01_index(color)][0]
        right_castle_allowed = castling_allowed[piece_class.convert_to_01_index(color)][1]
        left_rook_exist = squares[0 if is_white else 56] != piece_class_none
        right_rook_exist = squares[7 if is_white else 63] != piece_class_none

        #print(f"left_range, initially: {left_castle_allowed}")
        for target_index in left_range:
            #print(f"target_index: {target_index} exist: {squares[target_index] != piece_class_none}")
            if squares[target_index] != piece_class_none:
                left_castle_allowed = False
        #print(f"left_range, after: {left_castle_allowed}")

        #print(f"right_range, initially: {right_castle_allowed}")
        for target_index in right_range:
            #print(f"target_index: {target_index} exist: {squares[target_index] != piece_class_none}")
            if squares[target_index] != piece_class_none:
                right_castle_allowed = False
        #print(f"right range, after: {right_castle_allowed}")

        #print("left castle allowed" if left_castle_allowed and left_rook_exist else "left castle not allowed", f"because left_castle_allowed: {left_castle_allowed} and left_rook_exist: {left_rook_exist}")
        #print("right castle allowed" if right_castle_allowed and right_rook_exist else "right castle not allowed", f"because right_castle_allowed: {right_castle_allowed} and right_rook_exist: {right_rook_exist}")

        if left_castle_allowed and left_rook_exist:
            moves.append((square_index, square_index - 2))

        if right_castle_allowed and right_rook_exist:
            moves.append((square_index, square_index + 2))

        #print("\n")

def generate_moves(squares: list, piece_indices: list, pawn_movement_data: list, castling_allowed: list, move_count: int, color: int, legal_move_search: bool):
    moves = []
    
    for square_index in piece_indices:
        piece = squares[square_index]
        row, col = square_index // 8, square_index % 8

        if piece_class.get_color(piece) != color:
            continue

        if piece_class.is_sliding_piece(piece):
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
                    pawn_movement_data=pawn_movement_data,
                    move_count=move_count
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
                    moves=moves,
                    castling_allowed=castling_allowed,
                    legal_move_search=legal_move_search
                )
    return moves

def generate_legal_moves(squares: list, piece_indices: list, pawn_movement_data: list, castling_allowed: list, move_count: int):
    white_moves = generate_moves(
        squares=squares,
        piece_indices=piece_indices,
        pawn_movement_data=pawn_movement_data,
        castling_allowed=castling_allowed,
        move_count=move_count,
        color=piece_class.white,
        legal_move_search=True
    )

    black_moves = generate_moves(
        squares=squares,
        piece_indices=piece_indices,
        pawn_movement_data=pawn_movement_data,
        castling_allowed=castling_allowed,
        move_count=move_count,
        color=piece_class.black,
        legal_move_search=False
    )

    # Filter white's moves
    eliminated_white_moves = filter_illegal_moves(
        squares, piece_indices, pawn_movement_data, castling_allowed, move_count, 
        white_moves, piece_class.white, piece_class.black
    )
    # Filter black's moves
    eliminated_black_moves = filter_illegal_moves(
        squares, piece_indices, pawn_movement_data, castling_allowed, move_count,
        black_moves, piece_class.black, piece_class.white
    )

    return [item for item in white_moves if item not in eliminated_white_moves], [item for item in black_moves if item not in eliminated_black_moves]

#* Bruteforce method. An incredibly slow method.
def filter_illegal_moves(squares: list[int], piece_indices: list[int], pawn_movement_data: list[int], castling_allowed: list[list[bool]], move_count: int, my_moves: list[tuple], my_color: int, enemy_color: int):
    eliminated_moves = []
    board_copy = board.board()

    for my_move in my_moves:
        #print("move:", my_move)
        #print("color:", "white" if my_color == piece_class.white else "black")
        
        board_copy.load_position_list(
            squares.copy(), 
            piece_indices.copy(), 
            pawn_movement_data.copy(), 
            [castling_allowed[0].copy(), castling_allowed[1].copy()], 
            move_count
        )
        board_copy.make_move(my_move)
        board_copy.generate_moves(get_legal_moves=False, color=enemy_color)

        is_move_castle = False

        if piece_class.is_king(board_copy.squares[my_move[1]]) and abs(my_move[1] - my_move[0]) == 2:
            is_move_castle = True

        for enemy_move in board_copy.moves:
            enemy_move_target = enemy_move[1]
            piece_on_enemy_move_target = board_copy.squares[enemy_move_target]

            if is_move_castle:
                if piece_class.is_rook(board_copy.squares[enemy_move_target]):
                    if enemy_move_target == 3 or enemy_move_target == 5 or enemy_move_target == 59 or enemy_move_target == 61:
                        eliminated_moves.append(my_move)
                        #print("castling dismissed")
                        break

            if piece_class.is_king(piece_on_enemy_move_target) and piece_class.get_color(piece_on_enemy_move_target) == my_color:
                eliminated_moves.append(my_move)
                break
        
        #print("\n")

    #print(eliminated_moves)

    return eliminated_moves

#! I felt too burnt out filtering moves like this. Too many possibilities.
#! This was supposed to be a small project of mine, so I switched to the bruteforce filtering method instead.
#! Function is not fully done written. Maybe when I get motivations to improve performance...
def filter_illegal_moves_not_finished(squares: list[int], my_moves: list[tuple], enemy_moves: list[tuple], my_color: int, enemy_color: int):
    eliminated_moves = []
    enemy_pins = []

    my_king_square_index: int = None
    #enemy_king_square_index: int = None

    i = 0
    for piece in squares:
        if piece_class.is_king(piece):
            if piece_class.get_color(piece) == my_color:
                my_king_square_index = i
                break
        
        #if piece == piece_class.king * enemy_color:
        #   enemy_king_square_index = i

        i += 1

    i = 0
    for piece in squares:
        if piece_class.is_sliding_piece(piece) and piece_class.get_color(piece) == enemy_color:
            start_dir_index = 4 if piece_class.is_bishop(piece) else 0
            end_dir_index = 4 if piece_class.is_rook(piece) else 8

            piece_square_index = i
            delta_piece_my_king_square_index = piece_square_index - my_king_square_index
            piece_attack_direction = None

            for dir_index in range(start_dir_index, end_dir_index):
                dir = piece_class.piece_movedirection[dir_index]
                #print(f"{bcolors.WARNING}delta: {delta_piece_my_king_square_index}, dir: {dir}{bcolors.ENDC}")

                if delta_piece_my_king_square_index % dir == 0 and sign(delta_piece_my_king_square_index) == sign(dir) and delta_piece_my_king_square_index / dir < 8:
                    # King in piece's attack rays
                    piece_attack_direction = dir
                    break

            #print(piece_attack_direction)
            #print(delta_piece_my_king_square_index)

            if piece_attack_direction != None:
                pinned_piece_count = 0
                pinned_piece_square_index = None
                pin_dir = None

                for square_index in range(piece_square_index - piece_attack_direction, my_king_square_index, -piece_attack_direction):
                    if squares[square_index] != piece_class_none:
                        pinned_piece_count += 1
                        pinned_piece_square_index = square_index
                        pin_dir = piece_attack_direction

                if pinned_piece_count == 1:
                    enemy_pins.append((piece_square_index, pinned_piece_square_index, pin_dir))
        i += 1

    #print(enemy_pins, "enemy", enemy_color)
    
    for my_move in my_moves:
        if my_move in eliminated_moves:
            continue

        starting_index = my_move[0]
        ending_index = my_move[1]

        piece_on_starting_index = squares[starting_index]
        piece_on_ending_index = squares[ending_index]

        color_starting_piece = piece_class.get_color(piece_on_starting_index)
        color_ending_piece = piece_class.get_color(piece_on_ending_index)

        move_eliminated = False

        #* Filter 1: King cannot be moved to enemies' attack
        if piece_class.is_king(piece_on_starting_index):
            for enemy_move in enemy_moves:
                if ending_index == enemy_move[1]:
                    #my_moves.remove(my_move)
                    eliminated_moves.append(my_move)
                    move_eliminated = True
                    break
        else:
            #* Filter 2: Pieces pinned to the king cannot be moved
            #? Except for capturing the pinner, if possible
            #? Except for moving inside the pin ray 
            
            for pin_info in enemy_pins:
                pinner_square_index = pin_info[0]
                pinned_square_index = pin_info[1]
                pin_direction = pin_info[2]
                
                #? Capturing the pinner /1/
                #* If piece is pinned and it's move constitute capturing it's pinner => move is preserved
                condition_1 = starting_index == pinned_square_index and ending_index == pinner_square_index

                #? Moving inside the pin ray /2/
                #* If piece target square index is inside the pin ray => move is preserved
                ray = range(my_king_square_index + pin_direction, pinner_square_index, pin_direction)
                condition_2 = ending_index in ray

                #print(condition_1, "c1")
                #print(condition_2, "c2")
                #print(ray, "ray")
                #print(ending_index, "ending_index")
                #print(piece_class.get_enum(piece_on_starting_index), my_color)
                #print("\n")

                if not condition_1 and not condition_2:
                    eliminated_moves.append(my_move)
                    move_eliminated = True
                    break

            #* Filter 3: Kings cannot capture protected pieces
    
    return eliminated_moves