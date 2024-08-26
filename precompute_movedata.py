import piece as piece_class

squares_to_edge_lookup = []
knight_movement_lookup = []
king_movement_lookup = []
pawn_movement_lookup = []

castle_range_lookup = [
    [range(1, 4), range(5, 7)], 
    [range(57, 60), range(61, 63)]
]

for row in range(8):
    for col in range(8):
        square_index = row * 8 + col
        top, bottom = 7 - row, row
        left, right = col, 7 - col

        # Squares to edge
        squares_to_edge = [
            7 - row,
            row,
            col,
            7 - col,
            min(top, left),
            min(top, right),
            min(bottom, left),
            min(bottom, right)
        ]

        # Knight moves
        knight_moves = []

        for knight_movement_offset in piece_class.knight_movedirection:
            target_index = square_index + knight_movement_offset

            if 0 <= target_index <= 63:
                target_row = target_index // 8
                target_col = target_index % 8
                distance = max(abs(row - target_row), abs(col - target_col))

                if distance == 2:
                    knight_moves.append(target_index)

        # King moves
        king_moves = []
        
        for movement_offset in piece_class.piece_movedirection:
            target_index = square_index + movement_offset

            if 0 <= target_index <= 63:
                target_row = target_index // 8
                target_col = target_index % 8
                distance = max(abs(row - target_row), abs(col - target_col))

                if distance == 1:
                    king_moves.append(target_index)

        # Pawn moves
        pawn_moves = [[], []]
        white_moves = pawn_moves[0]
        black_moves = pawn_moves[1]

        white_pawn_push_index = square_index + piece_class.dir_top
        double_white_pawn_push_index = square_index + piece_class.dir_top * 2
        white_pawn_left_capture_index = square_index + piece_class.dir_topleft
        white_pawn_right_capture_index = square_index + piece_class.dir_topright

        black_pawn_push_index = square_index + piece_class.dir_bottom
        double_black_pawn_push_index = square_index + piece_class.dir_bottom * 2
        black_pawn_left_capture_index = square_index + piece_class.dir_bottomleft
        black_pawn_right_capture_index = square_index + piece_class.dir_bottomright

        # 0
        if 0 <= white_pawn_push_index <= 63:
            white_moves.append(white_pawn_push_index) # White pawn puuh
        if 0 <= black_pawn_push_index <= 63:
            black_moves.append(black_pawn_push_index) # Black pawn push

        # 1
        if 0 <= double_white_pawn_push_index <= 63:
            white_moves.append(square_index + piece_class.dir_top * 2) # White double pawn push
        if 0 <= double_black_pawn_push_index <= 63:
            black_moves.append(square_index + piece_class.dir_bottom * 2) # Black double pawn push

        if col == 0:
            # Leftside of the board
            # 2
            if 0 <= white_pawn_right_capture_index <= 63:
                white_moves.append(white_pawn_right_capture_index) # White right capture move
            if 0 <= black_pawn_right_capture_index <= 63:
                black_moves.append(black_pawn_right_capture_index) # Black right capture move
        elif col == 7:
            # Rightside of the board    
            # 2
            if 0 <= white_pawn_left_capture_index <= 63:
                white_moves.append(white_pawn_left_capture_index) # White left capture move
            if 0 <= black_pawn_left_capture_index <= 63:
                black_moves.append(black_pawn_left_capture_index) # Black left capture move
        else:
            # Inbetween
            # 2
            if 0 <= white_pawn_left_capture_index <= 63:
                white_moves.append(white_pawn_left_capture_index) # White left capture move
            # 3
            if 0 <= white_pawn_right_capture_index <= 63:
                white_moves.append(white_pawn_right_capture_index) # White right capture move
            # 2
            if 0 <= black_pawn_left_capture_index <= 63:
                black_moves.append(black_pawn_left_capture_index) # Black left capture move
            # 3
            if 0 <= black_pawn_right_capture_index <= 63:
                black_moves.append(black_pawn_right_capture_index) # Black right capture move

        # Insertion
        knight_movement_lookup.append(knight_moves)
        squares_to_edge_lookup.append(squares_to_edge)
        king_movement_lookup.append(king_moves)
        pawn_movement_lookup.append(pawn_moves)