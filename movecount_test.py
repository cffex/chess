import board as board_class
import piece as piece_class
import copy
import time

board = board_class.board()
board.load_position(r"r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R")

def print_pos(squares: list[int], a):
    board = ""

    for row in range(7, -1, -1):
        str = ""

        for col in range(8):
            piece = squares[row*8 + col]
            piece_enum = piece_class.get_enum(piece)
            
            if piece_class.is_white(piece):
                piece_enum = piece_enum.upper()
            elif piece_class.is_black(piece):
                piece_enum = piece_enum.lower()
            
            if piece == piece_class.none:
                str += "|   |"
            else:
                str += f"| {piece_enum} |"
        board += str + '\n'
    board += f"pos_num: {a}\n\n"

    with open("visualize.txt", "w") as vfile: 
        vfile.write(board)
    time.sleep(0.1)

cols_text = ["a", "b", "c", "d", "e", "f", "g", "h"]
def convert_tuple_to_chess_move(tuple: tuple):
    start, end = tuple[0], tuple[1]
    start_row, start_col, end_row, end_col = start // 8 + 1, start % 8 + 1, end // 8 + 1, end % 8 + 1
    return cols_text[start_col-1] + str(start_row) + cols_text[end_col-1] + str(end_row)
debug_move = ["a2a3", "b2b3", "g2g3"]

def perft(last_board: board_class.board, depth: int, last_color: int) -> int:
    if depth == 0:
        return 1

    this_color = -last_color
    this_board = board_class.board()
    this_board.load_position_list(
        last_board.squares.copy(),
        last_board.piece_indices.copy(),
        last_board.pawn_movement_data.copy(),
        copy.deepcopy(last_board.castling_allowed),
        last_board.move_count    
    )
    this_board.generate_moves(True, this_color)

    pos_count = 0
    for move in this_board.moves:
        print("Applying move:", convert_tuple_to_chess_move(move))
        this_board.make_move(move)

        chess_move = convert_tuple_to_chess_move(move)
        if chess_move in debug_move:
            print(chess_move, pos_count + 1)

        pos_count += perft(this_board, depth-1, this_color)

        print("Restoring board state")
        this_board.load_position_list(
            last_board.squares.copy(),
            last_board.piece_indices.copy(),
            last_board.pawn_movement_data.copy(),
            copy.deepcopy(last_board.castling_allowed),
            last_board.move_count    
        )

    return pos_count

for n in range(2, 3):
    a = time.time()
    print(f"perft {n} ply: {perft(board, n, piece_class.black)}")
    print(f"time elapsed: {time.time() - a}")