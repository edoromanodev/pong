import pygame
from pygame.locals import *

pygame.init()


# pygame.font.get_fonts()

# screen_width = 600
# screen_height = 500

screen_width = 600
screen_height = 500

#definizione del font
# font = pygame.font.SysFont('Helvetica', 30, bold = pygame.font.Font.bold)
font = pygame.font.SysFont('Helvetica', 30)


tempoEdoJump = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('edoPong')

#colori
bg = (255, 204, 153)   #background
black = (0, 0, 0)  #definizione di bianco


#variabili di gioco
cpu_score = 0
player_score = 0
fps = 60
live_ball = False
winner = 0
speed_increase = 0
margin = 50



def draw_board():
	screen.fill(bg)
	pygame.draw.line(screen, black, (0, margin), (screen_width, margin), 2)



def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))



    

    	#def move(self):
#    
#            
#            if self.rect.top < margin:
#                self.speed_y *= -1
#                   
#                   if self.rect.bottom > screen_height:
#                       self.speed_y *= -1
#                   if self.rect.colliderect(player_paddle) or self.rect.colliderect(cpu_paddle):
#                       self.speed_x *= -1
#       
#                   
#                  if self.rect.left < 0:
#                      self.winner = 1
#                   if self.rect.left > screen_width:
 #                      self.winner = -1
 #   
  #              
  #              self.rect.x += self.speed_x
  #              self.rect.y += self.speed_y
 #   
    #            return self.winner



    


class paddle():
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.rect = Rect(x, y, 20, 100)
		self.speed = 5
		self.ai_speed = 5

	def move(self):
		key = pygame.key.get_pressed()
		if key[pygame.K_UP] and self.rect.top > margin:
			self.rect.move_ip(0, -1 * self.speed)
		if key[pygame.K_DOWN] and self.rect.bottom < screen_height:
			self.rect.move_ip(0, self.speed)

	def draw(self):
		pygame.draw.rect(screen, black, self.rect)

	def ai(self):
		#ai per muovere il cpu paddle


        #muovi su
		if self.rect.centery > pong.rect.bottom and self.rect.top > margin:
			self.rect.move_ip(0, -2 * self.ai_speed)

		#muovi giù
		if self.rect.centery < pong.rect.top and self.rect.bottom < screen_height:
			self.rect.move_ip(0, 4 * self.ai_speed)



class ball():
	def __init__(self, x, y):
		self.reset(x, y)


	def move(self):

		#controllo collisioni margini e schermo 

		if self.rect.top < margin:
			self.speed_y *= -1
		
		if self.rect.bottom > screen_height:
			self.speed_y *= -1
		if self.rect.colliderect(player_paddle) or self.rect.colliderect(cpu_paddle):
			self.speed_x *= -1

		
		if self.rect.left < 0:
			self.winner = 1
		if self.rect.left > screen_width:
			self.winner = -1

		#update della posizione della palla
		self.rect.x += self.speed_x
		self.rect.y += self.speed_y

		return self.winner


	def draw(self):
		pygame.draw.circle(screen, black, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad)


	def reset(self, x, y):
		self.x = x
		self.y = y
		self.ball_rad = 8
		self.rect = Rect(x, y, self.ball_rad * 2, self.ball_rad * 2)
		self.speed_x = -4
		self.speed_y = 4
		self.winner = 0 
        
        # 1 = utente / -1 = cpu


#paddles
player_paddle = paddle(screen_width - 40, screen_height // 2)
cpu_paddle = paddle(20, screen_height // 2)

#pallina
pong = ball(screen_width - 60, screen_height // 2 + 50)


#game loop
run = True

while run:

	tempoEdoJump.tick(fps)

	draw_board()
	draw_text('Cpu: ' + str(cpu_score), font, black, 20, 7)
	draw_text('Utente: ' + str(player_score), font, black, screen_width - 115, 7)
	draw_text('Velocità: ' + str(abs(pong.speed_x)), font, black, screen_width // 2 - 60 , 7)


	#draw paddles
	player_paddle.draw()
	cpu_paddle.draw()

	if live_ball == True:
		speed_increase += 1
		winner = pong.move()
		if winner == 0:
            #muovere pallina : si
			pong.draw()
			#muovere paddles : si
			player_paddle.move()
			cpu_paddle.ai()
		else:
			live_ball = False
			if winner == 1:
				player_score += 1
			elif winner == -1:
				cpu_score += 1


	#print player instructions
	if live_ball == False:
		if winner == 0:
			draw_text('Premi per iniziare', font, black, 200, screen_height //1 - 400)
		if winner == 1:
			draw_text('Hai vinto!', font, black, 240, screen_height //1 - 330)
			draw_text('Premi per iniziare', font, black, 200, screen_height //1 - 400)
		if winner == -1:
			draw_text('Hai perso!', font, black, 240, screen_height //1 - 330)
			draw_text('Premi per iniziare', font, black, 200, screen_height //1 - 400)



	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONDOWN and live_ball == False:
			live_ball = True
			pong.reset(screen_width - 60, screen_height // 2 + 50)



	if speed_increase > 500:
		speed_increase = 0
		if pong.speed_x < 0:
			pong.speed_x -= 2
		if pong.speed_x > 0:
			pong.speed_x += 2
		if pong.speed_y < 0:
			pong.speed_y -= 2
		if pong.speed_y > 0:
			pong.speed_y += 2


	pygame.display.update()

pygame.quit()