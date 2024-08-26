import piece as piece_class
import fen as fen_class
import movegen

class board():
    def __init__(self):
        squares = [0] * 64
        self.squares = squares

        # Gamestate
        self.moves = []
        self.piece_indices = []
        self.pawn_movement_data = [0]*64
        self.castling_allowed = [
            [True, True], 
            [True, True]
        ]
        
    ###
    ###
    ###

    def load_position(self, FEN: str):
        fen_class.overwrite_position(
            squares=self.squares, 
            FEN=FEN, 
            piece_indices=self.piece_indices,
            pawn_movement_data=self.pawn_movement_data
        )

    def generate_moves(self):
        self.moves.clear()
        movegen.generate_moves(
            squares=self.squares, 
            piece_indices=self.piece_indices, 
            moves=self.moves,
            pawn_movement_data=self.pawn_movement_data,
            castling_allowed=self.castling_allowed
        )

    def make_move(self, move: tuple):
        squares = self.squares

        starting_index = move[0]
        ending_index = move[1]
        delta_move = ending_index - starting_index

        piece_on_starting_index = squares[starting_index]
        piece_on_ending_index = squares[ending_index]

        starting_piece_color = piece_class.get_color(piece_on_starting_index) 
        ending_piece_color = piece_class.get_color(piece_on_ending_index)

        ###
        ### Moving the piece from starting_index to ending_index
        ###
        
        if piece_class.is_pawn(piece_on_ending_index):
            # If the captured piece was a pawn, reset the pawn's data
            self.pawn_movement_data[ending_index] = 0

        elif piece_class.is_rook(piece_on_ending_index):
            # If the captured piece was a rook, it's color castling right is taken away
            rook_01_index = piece_class.convert_to_01_index(ending_piece_color)
            rook_col = ending_index % 8
            is_left_index = 0 if rook_col < 5 else 1
            
            self.castling_allowed[rook_01_index][is_left_index] = False
        
        # Handles en passant move
        if piece_class.is_pawn(piece_on_starting_index):
            abs_delta_move = abs(delta_move)

            # If move is a diagonal move
            if abs_delta_move == piece_class.dir_topleft or abs_delta_move == piece_class.dir_topright:
                # Makes sure it is an en passant move
                if piece_on_ending_index == piece_class.none and piece_class.is_pawn(squares[ending_index + piece_class.dir_bottom * starting_piece_color]):
                    squares[ending_index + piece_class.dir_bottom * starting_piece_color] = piece_class.none

        # Handles castling
        if piece_class.is_king(piece_on_starting_index) or piece_class.is_rook(piece_on_starting_index):
            # Left
            if piece_class.is_king(piece_on_starting_index):
                if delta_move == -2:
                    # White
                    if starting_piece_color > 0:
                        squares[3] = piece_class.rook
                        squares[0] = piece_class.none
                        
                        self.piece_indices.remove(0)
                        self.piece_indices.append(3)

                        # When a king or a rook moves, castling is disabled
                        self.castling_allowed[0][0] = False
                        self.castling_allowed[0][1] = False
                    # Black
                    else:
                        squares[59] = -piece_class.rook
                        squares[56] = piece_class.none

                        self.piece_indices.remove(56)
                        self.piece_indices.append(59)

                        # When a king or a rook moves, castling is disabled
                        self.castling_allowed[1][0] = False
                        self.castling_allowed[1][1] = False

                #  Right
                elif delta_move == 2:
                    # White
                    if starting_piece_color > 0:
                        squares[5] = piece_class.rook
                        squares[7] = piece_class.none

                        self.piece_indices.remove(7)
                        self.piece_indices.append(5)

                        # When a king or a rook moves, castling is disabled
                        self.castling_allowed[0][0] = False
                        self.castling_allowed[0][1] = False
                    
                    # Black
                    else:
                        squares[61] = -piece_class.rook
                        squares[63] = piece_class.none

                        self.piece_indices.remove(63)
                        self.piece_indices.append(61)
                        
                        #  When a king or a rook moves, castling is disabled
                        self.castling_allowed[1][0] = False
                        self.castling_allowed[1][1] = False
        
        squares[starting_index] = piece_class.none
        squares[ending_index] = piece_on_starting_index

        ###
        ### Update movecount if it is a pawn
        ###
        
        if piece_class.is_pawn(piece_on_starting_index):
            self.pawn_movement_data[ending_index] =  self.pawn_movement_data[starting_index] + 1
            self.pawn_movement_data[starting_index] = 0

        ###
        ### Update the piece indices loopup
        ###

        self.piece_indices.remove(starting_index)

        if ending_index not in self.piece_indices:
            self.piece_indices.append(ending_index)