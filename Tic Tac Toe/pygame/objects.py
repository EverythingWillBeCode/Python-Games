import pygame  # Importa la librería pygame

class Rect():
    def __init__(self, x, y, index):
        self.rect = pygame.Rect(x, y, 70, 70)  # Crea un rectángulo de 70x70 en la posición (x, y)
        self.index = index                     # Índice de la casilla en el tablero
        self.active = True                     # Indica si la casilla está activa (puede ser jugada)

        self.bgcolor = (32, 33, 36)            # Color de fondo de la casilla (gris oscuro)
        self.color = (255, 255, 255)           # Color del borde y texto (blanco)
        self.text = ''                         # Texto a mostrar en la casilla ('X', 'O' o vacío)
        self.font = pygame.font.Font('c:/GitHub/Python-Games/Tic Tac Toe/pygame/Fonts/PAPYRUS.TTF', 25)  # Fuente del texto
        self.image = self.font.render(self.text, True, self.color)  # Imagen renderizada del texto

    def update(self, win):
        if self.active:
            pygame.draw.rect(win, self.color, self.rect, 2, border_radius=5)  # Dibuja solo el borde si está activa
        else:
            pygame.draw.rect(win, self.bgcolor, self.rect, border_radius=5)   # Dibuja el fondo si está inactiva
            pygame.draw.rect(win, self.color, self.rect, 2, border_radius=5)  # Dibuja el borde

        self.image = self.font.render(self.text, True, self.color)            # Renderiza el texto actualizado
        x = self.rect.centerx - self.image.get_width() // 2                   # Calcula posición X centrada
        y = self.rect.centery - self.image.get_height() // 2                  # Calcula posición Y centrada
        win.blit(self.image, (x, y))                                          # Dibuja el texto en la casilla

def create_board():
    return ['#'] + [' ' for i in range(9)]  # Crea una lista con 10 elementos: el primero es '#' y los demás espacios vacíos

def generate_boxes():
    box_list = []                           # Lista para guardar las casillas
    for i in range(9):                      # Para cada casilla del tablero (9 en total)
        r = i // 3                          # Fila (0, 1, 2)
        c = i % 3                           # Columna (0, 1, 2)
        x = 20 + 70 * c + 16                # Calcula la posición X de la casilla
        y = 220 + 70 * r + 16               # Calcula la posición Y de la casilla
        box = Rect(x, y, i)                 # Crea una instancia de Rect para la casilla
        box_list.append(box)                # Añade la casilla a la lista

    return box_list                         # Devuelve la lista de casillas