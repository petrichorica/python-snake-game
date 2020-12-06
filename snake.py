from turtle import Turtle, Screen
import random

# Global variables
g_screen = Screen()
g_monster = Turtle(shape='square')
g_snake = Turtle(shape='square')
g_tail = dict()   # Store the position of the tails
g_food = []
g_food_num = []   # The number of food at each food storage place
g_introduction = None
g_remaining_food = 0   # The remaining food the snake is eating
g_food_storage_places = 0   # The overall remaining food storage places
g_pause = True
g_body_contact = 0
g_time = -1

# Constants
FOODNUM = 9
BOUNDARY = 240
SNAKE_SPEED = 300   # in millisecond
EATING_SPEED = 500   # in millisecond
SMALLEST_DISTANCE = 10
INITIAL_TAIL = 5


def startup():
    global g_introduction
    g_introduction = Turtle(visible=False)
    g_introduction.up()
    g_introduction.speed(0)
    g_introduction.goto(-215, 100)
    words = 'Welcome to snake!\n\n'\
            + 'You are going to use four arrow keys to move the snake. \n'\
            + 'Try to consume all the food before being caught by the monster. \n\n'\
            + 'Click anywhere to start the game. Have fun!'
    g_introduction.write(words,font=('Arial', 11, 'normal'))


def set_snake():
    global g_snake
    g_snake.pen(pencolor='red', fillcolor='red', pendown=False)
    g_snake.speed(0)


def set_monster():
    global g_monster
    g_monster.pen(pencolor='purple', fillcolor='purple', pendown=False)
    x, y = random_initial_pos()
    g_monster.speed(0)
    g_monster.goto(x, y)


def random_initial_pos():
    x_range = list(range(-BOUNDARY, -BOUNDARY//2)) + list(range(BOUNDARY//2, BOUNDARY))
    y_range = list(range(-BOUNDARY, -BOUNDARY//2))
    x = random.choice(x_range)
    y = random.choice(y_range)
    return x, y


def set_food():
    global g_food
    global g_food_storage_places
    global g_food_num
    g_food_storage_places = FOODNUM + 1
    for count in range(FOODNUM):
        num = count + 1
        num_str = str(num)
        food = Turtle(visible=False)
        x = random.randint(-BOUNDARY, BOUNDARY)
        y = random.randint(-BOUNDARY, BOUNDARY)
        food.pen(pendown=False, speed=0)
        food.goto(x, y)
        food.write(num_str, False, 'center')
        g_food.append(food)
        g_food_num.append(num)
    initial_tail = Turtle(visible=False)
    initial_tail.up()
    g_food.append(initial_tail)
    g_food_num.append(INITIAL_TAIL)


def move_out():
    direction = g_snake.heading()
    x = g_snake.xcor()
    y = g_snake.ycor()
    if direction == 0 and x >= BOUNDARY:
        return True
    elif direction == 90 and y >= BOUNDARY:
        return True
    elif direction == 180 and x <= -BOUNDARY:
        return True
    elif direction == 270 and y <= -BOUNDARY:
        return True
    else:
        return False


def snake_move():
    if end():
        return
    else:
        if is_eating():
            eat()
            if g_pause or move_out():
                g_snake.forward(0)
            else:
                g_snake.forward(20)
            g_screen.update()
            g_screen.ontimer(snake_move, EATING_SPEED)
        else:
            if g_pause or move_out():
                g_snake.forward(0)
            else:
                move_tail()
                g_snake.forward(20)
            g_screen.update()
            g_screen.ontimer(snake_move, SNAKE_SPEED)


def move_towards(angle):
    global g_pause
    g_pause = False
    g_snake.setheading(angle)


def pause():
    global g_pause
    g_pause = not g_pause


def bind_keys():
    g_screen.onkey(lambda: move_towards(180), 'Left')
    g_screen.onkey(lambda: move_towards(0), 'Right')
    g_screen.onkey(lambda: move_towards(90), 'Up')
    g_screen.onkey(lambda: move_towards(270), 'Down')
    g_screen.onkey(pause, 'space')


def check_body_contact():
    global g_body_contact
    for pos in g_tail.values():
        if g_monster.distance(pos) <= SMALLEST_DISTANCE+5:
            g_body_contact += 1
            return
    return


def monster_speed():
    random_speed = random.randint(int(SNAKE_SPEED*0.9), int(SNAKE_SPEED*1.6))
    return random_speed


def monster_move():
    if end():
        return
    else:
        angle = g_monster.towards(g_snake)
        if 45 <= angle <= 135:
            g_monster.setheading(90)
        elif 135 < angle <= 225:
            g_monster.setheading(180)
        elif 225 < angle <= 315:
            g_monster.setheading(270)
        else:
            g_monster.setheading(0)
        g_monster.forward(20)
        
        check_body_contact()
        title = 'Snake Contacted: ' + str(g_body_contact) + ' Time: ' + str(g_time)
        g_screen.title(title)
        g_screen.update()
        g_screen.ontimer(monster_move, monster_speed())


def move_tail():
    global g_tail
    g_snake.pen(pencolor='orange', fillcolor='yellow')
    tail_id = g_snake.stamp()
    pos = g_snake.position()
    g_tail[tail_id] = pos
    tail_id_deleted = g_snake.stampItems[0]
    del g_tail[tail_id_deleted]
    g_snake.clearstamps(1)
    g_snake.pen(pencolor='red', fillcolor='red')


def near_food():
    global g_remaining_food
    global g_food_storage_places
    for i in g_food:
        if i.distance(g_snake) <= SMALLEST_DISTANCE+5:
            i.clear()
            i.goto(BOUNDARY+50,BOUNDARY+50)
            index = g_food.index(i)
            num = g_food_num[index]  # The number of food
            g_remaining_food += num
            g_food_storage_places -= 1
            return
    return


def is_eating():
    near_food()
    if g_remaining_food:
        return True
    else:
        return False


def eat():
    global g_remaining_food
    global g_tail
    g_snake.pen(pencolor='orange', fillcolor='yellow')
    tail_id = g_snake.stamp()
    pos = g_snake.position()
    g_tail[tail_id] = pos
    g_snake.pen(pencolor='red', fillcolor='red')
    g_remaining_food -= 1


def end():
    if g_food_storage_places == 0 and g_remaining_food == 0:
        win()
        return True
    elif g_monster.distance(g_snake) < SMALLEST_DISTANCE:
        lose()
        return True
    else:
        return False


def win():
    win_msg = Turtle(visible=False)
    win_msg.up()
    pos = g_snake.position()
    win_msg.goto(pos)
    win_msg.down()
    win_msg.pencolor('red')
    win_msg.write('Win!', font=('Arial', 16, 'normal'))


def lose():
    lose_msg = Turtle(visible=False)
    lose_msg.up()
    pos = g_snake.position()
    lose_msg.goto(pos)
    lose_msg.down()
    lose_msg.pencolor('red')
    lose_msg.write('Game over.', font=('Arial', 16, 'normal'))


def game_start(x, y):
    global g_introduction
    g_introduction.clear()
    set_food()
    g_screen.update()
    g_screen.onclick(None)   # remove binding
    game_loop()


def record_time():
    global g_time
    if end():
        return
    else:
        g_time += 1
        g_screen.ontimer(record_time, 1000)


def game_loop():
    g_screen.ontimer(snake_move, SNAKE_SPEED)
    g_screen.ontimer(monster_move, monster_speed())
    g_screen.ontimer(record_time, 1000)


def main():
    g_screen.setup(510, 518)
    g_screen.screensize(500, 500)
    set_snake()
    set_monster()
    startup()
    g_screen.tracer(0)
    g_screen.delay(100)
    g_screen.listen()
    bind_keys()
    g_screen.onclick(game_start)
    g_screen.mainloop()


if __name__ == '__main__':
    main()