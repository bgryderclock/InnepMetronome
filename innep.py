import pygame
from pygame.locals import *
from sys import exit

instr1 = "Up/Down Arrow = Increase/Decrease Tempo"
instr2 = "Right/Left Arrow = Increase/Decrease Tempo Range "
instr3 = "Space Bar = Start"
instr4 = "Tab Key = Disable/Enable sound"
instr5 = "S-Key/A-Key = Increase/Decrease Tempo Change Rate"
instr6 = "G-Key = Disable/Enable Graphic"

screenwidth = 800
screenheight = 600
bpm = 100.0
orgbpm = bpm
direction = "right"
tempochange = "increase"
showelements = "all"
tempochangerange = 0.05
tempochangerate = 0.02
green = (138,226,52)
blue = (114,159,207)
black = (46,52,54)
white = (238,238,236)
backgroundcolor = (0,0,255)
mute = False
pause = True


pygame.init()
SCREEN_SIZE = (screenwidth, screenheight)
linestart = (0,0)
lineend = (0,screenheight)
screen = pygame.display.set_mode(SCREEN_SIZE, RESIZABLE, 32)
pygame.display.set_caption("Innep Metronome ~ (Penni Spelled Backwards)")

font = pygame.font.SysFont("arial",16);

distance_moved = 0.0

clock = pygame.time.Clock()

# pygame.mixer.music.load('metronome.wav') #if you want a wav

# X coordinate of our sprite
x = 0.0

# Speed in pixels per second  screenwidth = 1 bps or 60 bpm
#speed = screenwidth * bpm / 60
timer_seconds = 0.0

while True:

	for event in pygame.event.get():
		if event.type == QUIT:
			exit()
		if event.type == VIDEORESIZE:
			SCREEN_SIZE = event.size
			screenwidth,screenheight = SCREEN_SIZE
			screen = pygame.display.set_mode(SCREEN_SIZE, RESIZABLE, 32)
		if event.type == KEYDOWN:
			if event.key == K_UP:
				orgbpm = orgbpm + 1.
				if pause:
					bpm = orgbpm
				print "increasing orgbpm" 
			if event.key == K_DOWN:
				orgbpm = orgbpm - 1.
				if pause:
					bpm = orgbpm
				print "decreasing orgbpm" 
			if event.key == K_LEFT and tempochangerange > .05:
				tempochangerange = tempochangerange - .05
				print "decreasing tempochangerange" 
			if event.key == K_RIGHT:
				tempochangerange = tempochangerange + .05
				print "increasing tempochangerange" 
			if event.key == K_a and tempochangerate > .01:
				tempochangerate = tempochangerate - .01
				print "decreasing tempochangerate" 
			if event.key == K_s:
				tempochangerate = tempochangerate + .01
				print "increasing tempochangerate"
			if event.key == K_g:
				if showelements == "all":
					showelements = "none"
					print "showelements = none"
				elif showelements == "none":
					showelements = "all"
					print "showelements = all"
			if event.key == K_TAB:
				if mute == False:
					mute = True
					print "muted"
				elif mute == True:
					mute = False
					print "unmuted"
			if event.key == K_SPACE:
				pause = not pause
				if not pause:
					x = 0.0
					distance_moved = 0.0
					direction = "right"
					instr3 = "Space Bar = Pause"
				else:
					instr3 = "Space Bar = Continue"
				
				
	speed = screenwidth * (bpm / 60)
	time_passed = clock.tick(30)
	if pause:
		time_passed = 0.0
	else:
		time_passed_seconds = time_passed / 1000.0
		timer_seconds = timer_seconds + time_passed_seconds
		
		if direction == "right" and x >= screenwidth:
			if mute == False:
				pygame.mixer.music.play()
			direction = "left"
		if direction == "left" and x < 0:
			if mute == False:
				print "\a" # or pygame.mixer.music.play() if you use a wav file
			direction = "right"
			
		if direction == "left":
			distance_moved = time_passed_seconds * speed * -1
			backgroundcolor = green
			linestart = (x,0)
			lineend = (x,(screenheight/2))
			
		if direction == "right":
			distance_moved = time_passed_seconds * speed * 1
			backgroundcolor = blue
			linestart = (x,(screenheight/2))
			lineend = (x,screenheight)
		x = x + distance_moved
		
	if bpm > (orgbpm + tempochangerange):
		tempochange = "decrease"
	if bpm < (orgbpm - tempochangerange):
		tempochange = "increase"
	if bpm == orgbpm:
		tempochange = "nochange"	
	
	if tempochange == "increase":
		bpm = bpm + tempochangerate
		if bpm > orgbpm:
			bpm = orgbpm
	
	if tempochange == "decrease":
		bpm = bpm - tempochangerate
		if bpm < orgbpm:
			bpm = orgbpm
		
	
	if showelements == "all":
		y_pos = 0
		screen.fill(backgroundcolor)
		screen.blit(font.render(instr3,True,black),(0,y_pos+=20) )
		screen.blit(font.render(instr4,True,black),(0,y_pos+=20) )
		screen.blit(font.render(instr1,True,black),(0,y_pos+=20) )
		screen.blit(font.render(instr2,True,black),(0,y_pos+=20) )
		screen.blit(font.render(instr5,True,black),(0,y_pos+=20) )
		screen.blit(font.render(instr6,True,black),(0,y_pos+=20) )
		screen.blit(font.render("Tempo:"+str(orgbpm),True,black),(0,y_pos+=20) )
		screen.blit(font.render("Varying Tempo:"+str(bpm),True,black),(0,y_pos+=20) )
		screen.blit(font.render("Tempo Range:" + str(tempochangerange),True,black),(0,y_pos+=20) )
		screen.blit(font.render("Tempo Range Rate:" + str(tempochangerate),True,black),(0,y_pos+=20) )
		if not pause:
			pygame.draw.line(screen, white, linestart, lineend, 50)
		#screen.blit
		pygame.display.update()  
