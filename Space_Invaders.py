# Space Invaders - Part 1  #######################################
# Setup the screen
import turtle
import os
import math
import random
import subprocess
# BGM
os.system("afplay BGM.mp3 &" )
# Setup the screen
wn = turtle.Screen()
wn.bgcolor("white")  #set background color
wn.title("Space Invaders")
wn.bgpic("buddy_background.gif")

#register the shapes
turtle.register_shape("buddy_angry.gif")
turtle.register_shape("heart2.gif")
turtle.register_shape("jia2.gif")
turtle.register_shape("paw2.gif")

#Draw border
border_pen = turtle.Turtle()
border_pen.speed(0)  #0 is for the fastest speed drawing border
border_pen.color("black")
border_pen.penup()   #shows the pen in the middle (pen for border drawing), after pen up, the route of the pen will not be shown.
border_pen.setposition(-300,-300) #pen initial position
border_pen.pensize(3)
border_pen.pendown()  #put the pen down to draw lines
for side in range(4):
	border_pen.fd(600)   ## pen go forward
	border_pen.lt(90)    ## pen turn left 90deg
border_pen.hideturtle()

# Set score to 0
score = 0

# Draw the score  #############################################
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("black")
score_pen.penup()
score_pen.setposition(-290,270)
scorestring = "Score: %s" %score   ###########fill in the score
score_pen.write(scorestring, False, align="left", font= ("Arial", 24, "normal"))
score_pen.hideturtle()

#Create the player turtle
player = turtle.Turtle()
player.color("blue")
player.shape("jia2.gif")
player.penup()
player.speed(0)
player.setposition(0, -250)
player.setheading(90)   ## heading rotate anticlockwise

playerspeed = 15

enemyspeed = 4

# Choose a number of enemies
number_of_enemies = 4
# Create an empty list of enemies
enemies = []
bulletes = []
# Add enemies to the list
for i in range(number_of_enemies):
	enemies.append(turtle.Turtle())
	bulletes.append(turtle.Turtle())

for enemy in enemies:
	# Create the enemy
	enemy.color("red")
	enemy.shape("buddy_angry.gif")
	enemy.penup()
	enemy.speed(0)
	x = random.randint(-200,200)
	y = random.randint(100,250)
	enemy.setposition(x,y)	
	# Create the enemy's bullet
for bullete in bulletes:
	# bullete = turtle.Turtle()
	bullete.color("purple")
	bullete.shape("paw2.gif")
	bullete.penup()
	bullete.speed(0)
	bullete.setheading(270)
	bullete.shapesize(0.5,0.5)
	bullete.hideturtle()
	bulletespeed = 20

# Create the player's bullet
bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("heart2.gif")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5,0.5)
bullet.hideturtle()
bulletspeed = 20
		
# # Create the enemy's bullet
# bullete = turtle.Turtle()
# bullete.color("purple")
# bullete.shape("paw2.gif")
# bullete.penup()
# bullete.speed(0)
# bullete.setheading(270)
# bullete.shapesize(0.5,0.5)
# bullete.hideturtle()
# bulletespeed = 20

# Define bullet state
# ready - ready to fire
# fire- bullet is firing
bulletstate = "ready"

# Move the player left and right
def move_left():
	x = player.xcor()  # findout players x coordinate
	x -= playerspeed
	if x < -280:       #### boundary check
		x = -280
	player.setx(x)
def move_right():
	x = player.xcor()  # findout players x coordinate
	x += playerspeed
	if x > 280:        #### boundary check
		x = 280
	player.setx(x)
def fire_bullet():
	# Declare bulletstate as a glocbal if it needs changed.
	global bulletstate  ##by adding global, all changes inside this function will affect everywhere.
	# Move the bullet to just above the player
	if bulletstate == "ready":
		os.system("afplay laser.wav &")
		bulletstate = "fire"     ## after click space, bullelstate change to fire, to prevent refire. untill reach boundary.
		x = player.xcor()
		y = player.ycor() + 10
		bullet.setposition(x,y)
		bullet.showturtle()

def isCollision(t1, t2):
	distance = math.sqrt(math.pow(t1.ycor()-t2.ycor(),2) + math.pow(t1.xcor()-t2.xcor(),2))
	if distance < 25:
		return True
	else:
		return False

def create_text(pos, txt):   ####print text on the screen
    pen = turtle.Turtle()
    pen.speed(0)
    pen.color("black")
    pen.penup()
    pen.setposition(pos)
    pen.write(txt, False, align="center", font= ("Arial", 40, "normal"))
    pen.hideturtle()
    return pen

# Create keyboard bindings
turtle.listen()                     ##### library for binding keyboard
turtle.onkey(move_left,"Left")      # capital L
turtle.onkey(move_right,"Right")    # capital R
turtle.onkey(fire_bullet,"space")   ## all lower case for space


bulletestate = ["ready", "ready", "ready", "ready", "ready"]
#Main game loop
while True:
	create_text((0,250), "Happy BDay!! 2019") 

	for enemy in enemies:
		#move the enemy
		x = enemy.xcor()
		x += enemyspeed
		enemy.setx(x)
		# for be in bullet

		enemy_number = enemies.index(enemy)
		bullete2 = bulletes[enemy_number]
		if bulletestate[enemy_number] == "ready":
			bullete2.setposition(enemy.xcor(),enemy.ycor())
			bullete2.showturtle()
			bulletestate[enemy_number] = "fire"	
			# y += bulletespeed
			# bullete.sety(y) 
		# Move the enemy back and down
		if enemy.xcor() > 280:   ## bondary detect
			for e in enemies:
				y = e.ycor()
				y -= 40              ## move towards the player after touching the bondary
				e.sety(y)
			enemyspeed *= -1     ## reverse
		if enemy.xcor() < -280:
			for e in enemies:
				y = e.ycor()
				y -= 40              ## move towards the player after touching the bondary
				e.sety(y)
			enemyspeed *= -1


		# Check for a collision between bullet and enemy
		if isCollision(bullet, enemy):
			# Reset the bullet
			bullet.hideturtle()
			bulletstate = "ready"
			bullet.setposition(0,-400)
			# Reset enemy
			x = random.randint(-200,200)
			y = random.randint(100,250)
			enemy.setposition(x,y)	
		# update the score
			score += 10
			scorestring = "Score: %s" %score   ###########fill in the score
			score_pen.clear()       # remove the old score
			score_pen.write(scorestring, False, align="left", font= ("Arial", 24, "normal"))
		# sound effect
			os.system("afplay Explosion.wav &")
		# Check for a collision between player and enemy
		if isCollision(player,enemy):
			player.hideturtle()
			bullete.hideturtle()			
			for enemy in enemies:
				enemy.hideturtle()
			# print("Game Over")       ##### show in terminal
			wn.bgpic("buddy_background.gif")
			create_text((0,120), "Game Over")    ###show in screen
			break
		for bullete in bulletes:			
			if isCollision(player,bullete):
				player.hideturtle()
				bullete.hideturtle()
				for enemy in enemies:
					enemy.hideturtle()
				for bullete in bulletes:
					bullete.hideturtle()
				# print("Game Over")       ##### show in terminal
				wn.bgpic("buddy_background.gif")
				create_text((0,120), "Game Over")    ###show in screen
				turtle.done()

# Move the bullet
	if bulletstate == "fire":
		y = bullet.ycor()
		y += bulletspeed
		bullet.sety(y)  
# Check to see if the bullet has gone to the top
	if bullet.ycor() > 275:
		bullet.hideturtle()
		bulletstate = "ready"

# Move the enemy's bullet
	for bullete3 in bulletes:
		if bullete3.ycor() >= -250:
			# bulletestate = "fire"
			y = bullete3.ycor()
			y -= bulletespeed
			bullete3.sety(y)  
	# Check to see if the enemy's bullet has gone to the bottom
		if bullete3.ycor() < -250:
			bullete3.hideturtle()
			bullete_number = bulletes.index(bullete3)
			bulletestate[bullete_number] = "ready"		

# these two line are neccessary for stopping screen from closing. w/o screen will be generated and close immidiately.
# wn.exitonclick()
turtle.done()
