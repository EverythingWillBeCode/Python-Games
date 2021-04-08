import json
import pygame
from objects import Board, Button, message_box

### SETUP *********************************************************************
pygame.init()
SCREEN = WIDTH, HEIGHT = 890, 480
win = pygame.display.set_mode(SCREEN, pygame.NOFRAME)
pygame.display.set_caption('Memory Puzzle')

clock = pygame.time.Clock()
FPS = 30

ROWS, COLS = 8, 10
TILESIZE = 45

### COLORS ********************************************************************
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 25, 25)
WHITE = (255, 255, 255)

### LOADING IMAGES ************************************************************
img_list = []
for img in range(1,21):
	image = pygame.image.load(f"Assets/icons/{img}.jpeg")
	image = pygame.transform.scale(image, (TILESIZE,TILESIZE))
	img_list.append(image)

bg = pygame.image.load('Assets/bg.jpg')
rightbar = pygame.image.load('Assets/image.jpg')
rightbar = pygame.transform.scale(rightbar, (280, HEIGHT - 47))

### Buttons *******************************************************************
restart_img = pygame.image.load('Assets/restart.png')
restart_btn = Button(restart_img, (40,40), 720, 230)

info_img = pygame.image.load('Assets/info.png')
info_btn = Button(info_img, (40,40), 720, 280)

close_img = pygame.image.load('Assets/close.png')
close_btn = Button(close_img, (40,40), 720, 330)

### LOADING FRUITS INFORMATION ************************************************
with open('Info/info.json') as f:
	dct = json.load(f)

### LOADING FONTS *************************************************************
sys_font = pygame.font.SysFont(("Times New Roman"),20)

### CREATING BOARD ************************************************************
board = Board(img_list)
board.randomize_images()

### GAME VARIABLES ************************************************************
game_screen = True
first_card = None
second_card = None
first_click_time = None
second_click_time = None

running = True

while running:
	win.blit(bg, (0,0), (400, 100,WIDTH,HEIGHT))
	win.blit(rightbar, (595, 20))
	pygame.draw.rect(win, BLUE, (5, 10, 580, HEIGHT - 20), 2)
	pygame.draw.rect(win, BLUE, (585, 10, 300, HEIGHT - 20), 2)

	if restart_btn.draw(win):
		game_screen = True
		show_text = False
		first_card = None
		second_card = None
		first_click_time = None
		second_click_time = None

		board.randomize_images()

	if info_btn.draw(win):
		game_screen = False
		show_text = False

	if close_btn.draw(win):
		running = False

	clicked = False

	x, y = pygame.mouse.get_pos()

	for event in pygame.event.get():
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				clicked = True
				x, y = pygame.mouse.get_pos()

	if game_screen:
		### Game is on

		### Polling time to hide cards
		if second_click_time:
			current_time = pygame.time.get_ticks()

			delta = current_time - second_click_time
			if delta >= 1000:
				if first_card.value == second_card.value:
					first_card.is_alive = False
					second_card.is_alive = False

				index = first_card.index
				fcard = board.board[index[0]][index[1]]
				fcard.animate = True
				fcard.slide_left = False
				first_card = None

				index = second_card.index
				scard = board.board[index[0]][index[1]]
				scard.animate = True
				scard.slide_left = False
				second_card = None

				first_click_time = None
				second_click_time = None
			else:
				clicked = False

		### Displaying cards
		for r in range(ROWS):
			for c in range(COLS):
				border = False
				card = board.board[r][c]
				if card.is_alive:
					xcord = card.rect.x
					ycord = card.rect.y

					if card.rect.collidepoint((x,y)):
						border = True
						if clicked:
							card.visible = True
							card.animate = True
							card.slide_left = True

							if not first_card:
								first_card = card
							else:
								second_card = card
								if second_card != first_card:
									second_click_time = pygame.time.get_ticks()
								else:
									second_card = None

					pygame.draw.rect(win, BLACK, (xcord+5, ycord+5,TILESIZE, TILESIZE))

					if not card.animate:
						if card.visible:
							win.blit(card.image, card.rect)
						else:
							pygame.draw.rect(win, WHITE, (xcord, ycord,TILESIZE, TILESIZE))

						if border:
							pygame.draw.rect(win, RED, (xcord, ycord,TILESIZE, TILESIZE), 2)
					else:
						card.on_click(win)
	else:
		for r in range(2):
			for c in range(COLS):
				card = board.info_board[r][c]
				xcord = card.rect.x
				ycord = card.rect.y

				pygame.draw.rect(win, BLACK, (xcord+5, ycord+5,TILESIZE, TILESIZE))
				win.blit(card.image, card.rect)

				if card.rect.collidepoint((x,y)):
					pygame.draw.rect(win, RED, (xcord, ycord,TILESIZE, TILESIZE), 2)

					if clicked:
						show_text = True
						data = dct[str(card.value)]
						name = data['Name']
						info = data['Info']

						border = True
						pos = (xcord, ycord)

		if border:
			pygame.draw.rect(win, BLUE, (pos[0], pos[1],TILESIZE, TILESIZE), 2)
		if show_text:
			message_box(win, sys_font, info)

	pygame.display.flip()
	clock.tick(FPS)

pygame.quit()