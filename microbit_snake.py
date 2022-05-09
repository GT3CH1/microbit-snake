# This project will attempt to make a snake game using the microbit
import random
from microbit import *


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    # Gets the coordinates of the point
    def get_coordinates(self):
        return self

    # Move the point in the direction of the given direction
    def move(self, direction):
        if direction == "up":
            self.move_up()
        elif direction == "down":
            self.move_down()
        elif direction == "left":
            self.move_left()
        elif direction == "right":
            self.move_right()
        return self

    def move_up(self):
        self.y -= 1
        self.y = self.y % 5

    def move_down(self):
        self.y += 1
        self.y = self.y % 5

    def move_left(self):
        self.x -= 1
        self.x = self.x % 5

    def move_right(self):
        self.x += 1
        self.x = self.x % 5

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Direction:
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


class Snake:
    def __init__(self):
        # Create a snake with a body length of 3
        self.body = [Point(0, 0)]

        # Set the length of the snake.
        self.length = self.get_length()

        # Set the direction of the snake to be moving up
        self.direction = Direction.RIGHT

        # The previous direction of the snake
        self.previous_direction = self.direction

    def set_direction(self, direction):
        self.direction = direction

    def get_direction(self):
        return self.direction

    def get_length(self):
        return len(self.body)

    def get_head(self) -> Point:
        return self.body[0]

    def add_segment(self):
        new_segment_x = self.body[-1].x
        new_segment_y = self.body[-1].y
        # update the snake's body
        self.update()
        self.body.append(Point(new_segment_x, new_segment_y))

    def update(self):
        self.length = self.get_length()
        tmp_list = []
        # update the position of each segment of the snake
        for i in range(1, self.length):
            tmp_list.append(Point(self.body[i-1].x, self.body[i-1].y))
        # set the snake's body to the temporary list
        tmp_list.insert(0, self.body[0].move(self.direction))
        self.body = tmp_list

class Food:
    def __init__(self):
        self.location = Point(0, 0)
        self.spawn()

    def get_location(self):
        return self.location

    def spawn(self):
        self.location = Point(random.randint(0, 4), random.randint(0, 4))


snake = Snake()
direction_count = 1
food_in_game = True
food_timer = 0
food = Food()


def run():
    global direction_count
    global food_in_game
    global food_timer
    while True:
        display.clear()
        snake.update()
        point_brightness = 9
        for point in snake.body:
            if point_brightness > 5:
                point_brightness -= 2
            display.set_pixel(point.x, point.y, point_brightness)
            if food_in_game:
                # check if the snake head is on the food
                if snake.get_head() == food.get_location():
                    food_in_game = False
                    snake.add_segment()
                while food.get_location() == point:
                    # spawn a new food
                    food.spawn()

                display.set_pixel(food.get_location().x, food.get_location().y, 9)
                food_timer += 1
                if food_timer == 30:
                    food_in_game = False
            else:
                if random.randint(0, 100) == 0:
                    food_in_game = True

        # check if the snake has hit itself
        for i in range(1, snake.get_length()):
            if snake.get_head().x == snake.body[i].x and snake.get_head().y == snake.body[i].y:
                display.clear()
                display.scroll("You died!", 150)
                return
        # check if the snake length is 5, if it is, the game is won
        if snake.get_length() == 5:
            display.clear()
            display.scroll("You win!", 150)
            return
        if button_a.is_pressed():
            direction_count = (direction_count - 1) % 4
            update_direction(direction_count)
        if button_b.is_pressed():
            direction_count = (direction_count + 1) % 4
            update_direction(direction_count)
        sleep(150)


def update_direction(direction_count):
    if direction_count == 0:
        snake.set_direction(Direction.UP)
    elif direction_count == 1:
        snake.set_direction(Direction.RIGHT)
    elif direction_count == 2:
        snake.set_direction(Direction.DOWN)
    elif direction_count == 3:
        snake.set_direction(Direction.LEFT)
    sleep(50)


if __name__ == "__main__":
    run()
