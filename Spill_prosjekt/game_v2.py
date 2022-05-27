from ursina import *
import time

  #definerer at vi bruker ursina og vindu farge
app = Ursina()
window.color = color.dark_gray

  #variabler
score1 = score2 = 0
speed_x = speed_y = 0
old_speed_x = old_speed_y = speed_x
anti_speed_stop = 0
anti_winner_spam1 = anti_winner_spam2 = 1
start_timer = speed_timer = winning_display_timer = time.time()
ai_difficulty = 0

  #definerer banen
table = Entity(
  model='cube',
  color=color.black,
  scale=(12,6,1))

  #definerer ballen
ball = Entity(
  model='sphere',
  color=color.red,
  z=-1,
  scale=0.2,
  collider='box')
    
  #definerer spiller 1
player1 = Entity(
  model='cube',
  color=color.white,
  scale=(0.15,0.9,1),
  position=(-5,-1.4,-1),
  collider='box')

  #definerer spiller 2
player2 = duplicate(player1, x=5)


    #definerer poengene
score_p1 = Text(text=str(score1),
            scale=(3,3),
            x=-.15, y=.3)
score_p2 = Text(text=str(score2),
            scale=(3,3),
            x=.15, y=.3)
score_dash = Text(text="-",
            scale=(3,3),
            x=.02, y=.3)

  #definerer konfetti når du vinner
confetti = Animation('assets\Confetti\confetti-', scale=5, position=(0,0,-2),
                fps=30, loop=True, autoplay=True)
confetti.visible=False

  #definerer text på skjermen på siden
how_to_move_line1 = Text(text="Use arrow keys",
                scale=(2,2),
                position=(-.7, .45))
how_to_move_line2 = Text(text="and A-D to move",
                scale=(2,2),
                position=(-.33, .45))

first_to_10_wins = Text(text="First to 10 wins",
                scale=(2,2),
                position=(-.18, .1))

press_r_to_restart = Text(text="Press r to restart",
                scale=(2,2),
                position=(.2, .45))

press_space_to_start = Text(text='Press space to start',
                scale=(2.2,2.2),
                position=(-.25, -.1))
              
pause_icon = Button(texture='assets\Pause_icon', scale=(.08,.08), position=(.75,.45))
play_icon = Button(texture='assets\Play_icon', scale=(.08,.08), position=(1,.45,))
play_icon.visible = False

player1_wins = Text(text="",
                scale=(1.8,1.8),
                position=(-.23,-.2))
player2_wins = Text(text="",
                scale=(1.8,1.8),
                position=(-.23,.2))
ai_set_text = Text(text="Set AI  difficulty:",
                scale=(1.8,1.8),
                position=(-.8,-.4),
                )
ai_difficulty_box = Entity(model='cube', position=(5.6,2.8,-1), scale=(.8,.4), color=color.gray)
ai_difficulty_text = Text(text="", position=(.66,.37), scale=(1.5,1.5), color=color.dark_gray)
ai_difficulty_box.visible = True
ai_difficulty_text.visible = True

  #dette definerer AI vanskelighets knappene
AI_off = Button(text="Off", scale=(.05,.05), position=(-.3, -.43), color=color.gray, highlight_color=color.dark_gray, text_color=color.black)
difficulty_low = Button(text="Low", scale=(.05,.05), position=(-.1, -.43), color=color.green, highlight_color=color.rgb(0, 120, 0), text_color=color.black)
difficulty_medium = Button(text="Medium", scale=(.1,.05), position=(.1,-.43), color=color.yellow, highlight_color=color.rgb(155, 135, 12), text_color=color.black)
difficulty_high = Button(text="High", scale=(.05,.05), position=(.3,-.43), color=color.red, highlight_color=color.rgb(139, 0, 0), text_color=color.black)
AI_off.tooltip = Tooltip(text='You can also press 1', scale=(.75,.75))
difficulty_low.tooltip = Tooltip(text='You can also press 2', scale=(.75,.75))
difficulty_medium.tooltip = Tooltip(text='You can also press 3', scale=(.75,.75))
difficulty_high.tooltip = Tooltip(text='You can also press 4', scale=(.75,.75))

#dette definere boksen som viser ai vanskelighetsgrad
def ai_off_display():
  ai_difficulty_box.color=color.gray
  ai_difficulty_box.visible = False
  ai_difficulty_text.visible = False
def ai_low():
  ai_difficulty_box.visible = True
  ai_difficulty_box.color=color.green
  ai_difficulty_text.visible = True
  ai_difficulty_text.text='Low'
def ai_medium():
  ai_difficulty_box.color=color.yellow
  ai_difficulty_text.text='Mid'
  ai_difficulty_box.visible = True
  ai_difficulty_text.visible = True
def ai_high():
  ai_difficulty_box.color=color.red
  ai_difficulty_text.text='High'
  ai_difficulty_box.visible = True
  ai_difficulty_text.visible = True

  #definerer pause ikonene når du trykker på dem
def pause_click():
  pause_icon.visible = False
  play_icon.visible = True
  pause_icon.position=(1,.45)
  play_icon.position=(.75,.45)
def play_click():
  play_icon.visible = False
  pause_icon.visible = True
  play_icon.position=(1,.45)
  pause_icon.position=(.75,.45)

  #dette er forever loopen
def update():
  global speed_x, speed_y, score1, score2, anti_winner_spam1, anti_winner_spam2, speed_timer, start_timer, winning_display_timer, ai_difficulty, old_speed_x, old_speed_y, anti_speed_stop
  speed_timer = time.time() - start_timer

  #bevege spillere
  if held_keys['right arrow']:
    player2.y += time.dt * 2
  if held_keys['left arrow']:
    player2.y -= time.dt * 2
  if held_keys['up arrow']:
    player2.y += time.dt * 2
  if held_keys['down arrow']:
    player2.y -= time.dt * 2
  if held_keys['d']:
    player1.y += time.dt * 2
  if held_keys['a']:
    player1.y -= time.dt * 2
  if held_keys['w']:
    player1.y += time.dt * 2
  if held_keys['s']:
    player1.y -= time.dt * 2
  
  #trykk mellomrom for å starte
  if held_keys['space']:
    if press_space_to_start.text=="Press space to start":
      speed_x = speed_y = 2
      press_space_to_start.text=""
      first_to_10_wins.text=""

  #bevege ball
  ball.x += speed_x * time.dt
  ball.y += speed_y * time.dt
  if ball.y > 3:
    speed_y = -speed_y
  if ball.y < -3:
    speed_y = -speed_y
  
  #hvis spillerne bommer på ballen/ poeng system
  #flytter ballen tilbake til start, gir poeng til spiller og setter ned farten litt
  if ball.x > 6:
    ball.x = 0
    ball.y = -1.2
    score1 +=1
    speed_x *= 0.8
    speed_y *= 0.8
    score_p1.text=str(score1)
    player2.y = 0
  if ball.x < -6:
    ball.x = 0
    ball.y = 1.2
    score2 +=1
    score_p2.text=str(score2)
    player1.y = 0

  #hvis spilleren treffer ballen
  #endrer retning og setter opp farten med 2%
  if ball.intersects().hit:
    if speed_timer > 1:
      speed_x *= 1.02
      speed_y *= 1.02
    speed_x = -speed_x
    start_timer = time.time()

  #gjør så spillerne ikke kan gå utenfor banen
  if player1.y > 2.7:
    player1.y = player1.y - time.dt * 1.5
  if player1.y < -2.7:
    player1.y = player1.y + time.dt * 1.5
  if player2.y > 2.7:
    player2.y = player2.y - time.dt * 1.5
  if player2.y < -2.7:
    player2.y = player2.y + time.dt * 1.5

  #når spiller 1 vinner
  if score1 == 10:
    start_timer = time.time()
    if anti_winner_spam1 == 1:
        anti_winner_spam1 = 0
        speed_x = speed_y = 1
        player1_wins.text="Player 1 is the winner!"
        anti_winner_spam1 = 1
        winning_display_timer = 1
        confetti.y=.2
        confetti.visible=True
        
  #når spiller 2 vinner
  if score2 == 10:
    start_timer = time.time()
    if anti_winner_spam2 == 1:
      anti_winner_spam2 = 0
      speed_x = speed_y = 1
      player2_wins.text="Player 2 is the winner!"
      anti_winner_spam2 = 1
      winning_display_timer = 1
      confetti.y=-.2
      confetti.visible=True
      
  #holder ballen stille når noen vinner
  if winning_display_timer == 1:
    ball.x = ball.y = 0
  
  #holder ballen stille når du har trykket pause
  if play_icon.x == .75:
    if anti_speed_stop == 0:
      old_speed_y = speed_y
      old_speed_x = speed_x
      anti_speed_stop = 1
    speed_x = speed_y = 0
  if pause_icon.x == .75:
    if anti_speed_stop == 1:
      speed_x = old_speed_x
      speed_y = old_speed_y
      anti_speed_stop = 0
  
  #pauser når du trykker escape
    if held_keys['escape']:
      if anti_speed_stop == 0:
        pause_click()
        print('hei')
      if anti_speed_stop == 1:
        play_click()
        print('ikke hei')


  #restart funksjon
  if held_keys['r']:
    ball.x = ball.y = 0
    speed_x = speed_y = 1
    winning_display_timer = 0
    score1 = score2 = 0
    score_p1.text = score_p2.text = str(score1)
    player1_wins.text = player2_wins.text = ""
    confetti.visible=False

  #AI styring.
  #Lett vanskelighetsgrad
  if ai_difficulty == 1:
    if ball.y > player2.y:
      player2.y += time.dt * .75
    if ball.y < player2.y.x:
      player2.y -= time.dt * .75
    
  #Medium vanskelighetsgrad
  if ai_difficulty == 2:
    if ball.y > player2.y:
      player2.y += time.dt * 1.2
    if ball.y < player2.y:
      player2.y -= time.dt * 1.2
  
  #Vanskelig vanskelighetsgrad
  if ai_difficulty == 3:
    if ball.y > player2.y:
      player2.y += time.dt * 1.7
    if ball.y < player2.y:
      player2.y -= time.dt * 1.7

  #AI vanskelighetsgrader knapper
  if held_keys['1']:
      ai_difficulty = 0
      ai_off_display()
  if held_keys['2']:
      ai_difficulty = 1
      ai_low()
  if held_keys['3']:
      ai_difficulty = 2
      ai_medium()
  if held_keys['4']:
      ai_difficulty = 3
      ai_high()
  if ai_difficulty_box.color==color.gray:
    ai_difficulty = 0
  if ai_difficulty_box.color==color.green:
    ai_difficulty = 1
  if ai_difficulty_box.color==color.yellow:
    ai_difficulty = 2
  if ai_difficulty_box.color==color.red:
    ai_difficulty = 3
   
  #når du trykker på AI knappene
AI_off.on_click = ai_off_display
difficulty_low.on_click = ai_low
difficulty_medium.on_click = ai_medium
difficulty_high.on_click = ai_high

  #når du trykker på pause knappene
pause_icon.on_click = pause_click
play_icon.on_click = play_click

#kamera innstillinger
camera.orthographic = True
camera.fov = 8
#kjører koden
app.run()