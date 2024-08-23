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
            pawn_movement_data=self.pawn_movement_data
        )

    def make_move(self, move: tuple):
        squares = self.squares

        starting_index = move[0]
        ending_index = move[1]
        delta_move = ending_index - starting_index

        piece_on_starting_index = squares[starting_index]
        piece_on_ending_index = squares[ending_index]

        starting_piece_color = piece_class.get_color(piece_on_starting_index) 

        ###
        ### Moving the piece from starting_index to ending_index
        ###
        
        if piece_on_ending_index != piece_class.none:
            # If the captured piece was a pawn, reset the pawn's data
            self.pawn_movement_data[ending_index] = 0
        
        # Handles en passant move
        if piece_class.is_pawn(piece_on_starting_index):
            abs_delta_move = abs(delta_move)

            # If move is a diagonal move
            if abs_delta_move == piece_class.dir_topleft or abs_delta_move == piece_class.dir_topright:
                # Makes sure it is an en passant move
                if piece_on_ending_index == piece_class.none and piece_class.is_pawn(squares[ending_index + piece_class.dir_bottom * starting_piece_color]):
                    squares[ending_index + piece_class.dir_bottom * starting_piece_color] = piece_class.none


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