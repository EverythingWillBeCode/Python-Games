def check_space(cell):
    return cell == ' '                 # Devuelve True si la celda está vacía (espacio en blanco)

def isBoardFull(board):
    for cell in board:                 # Recorre cada celda del tablero
        if check_space(cell):          # Si encuentra una celda vacía
            return False               # El tablero no está lleno, retorna False

    return True                        # Si no hay celdas vacías, retorna True

def check_win(board, mark):
    # Comprueba todas las combinaciones ganadoras posibles para el jugador 'mark'
    if (board[1] == board[2] == board[3] == mark):           # Fila superior
        value = (True, '123')
    elif (board[4] == board[5] == board[6] == mark):         # Fila del medio
        value = (True, '456')
    elif (board[7] == board[8] == board[9] == mark):         # Fila inferior
        value = (True, '789')
    elif (board[7] == board[4] == board[1] == mark):         # Columna izquierda
        value = (True, '147')
    elif (board[8] == board[5] == board[2] == mark):         # Columna central
        value = (True, '258')
    elif (board[9] == board[6] == board[3] == mark):         # Columna derecha
        value = (True, '369') 
    elif (board[1] == board[5] == board[9] == mark):         # Diagonal principal
        value = (True, '159')
    elif (board[3] == board[5] == board[7] == mark):         # Diagonal secundaria
        value = (True, '357')
    else:
        value = (False, -1)                                  # No hay ganador

    return value                                             # Devuelve tupla (True/False, combinación ganadora o -1)