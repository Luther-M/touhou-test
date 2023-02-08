import pygame as py
import random as ran

py.init()

(SCREEN_WIDTH, SCREEN_HEIGHT) = (480, 640)
SCREEN = [SCREEN_WIDTH, SCREEN_HEIGHT]
game_screen = py.display.set_mode(SCREEN)
font_arial = py.font.SysFont('arial', 20)
py.display.set_caption("Touhou Poligon")
clock = py.time.Clock()

(WHITE, BLACK, RED) = ((255, 255, 255), (0, 0, 0), (255, 0, 0))

class render_entitiy:
    def __init__(self, input_position_x, input_position_y):
        self.object_position_x = input_position_x
        self.object_position_y = input_position_y

    def render_square(self, input_length, input_height):
        py.draw.rect(game_screen, BLACK, (self.object_position_x,
                     self.object_position_y, input_length, input_height))

    def render_circle(self, radius):
        py.draw.circle(game_screen, BLACK, (self.object_position_x,
                       self.object_position_y), radius, 2)

def render_laser(init_pos, end_pos):
    py.draw.line(game_screen, RED, init_pos, end_pos)

def display_score(input):
    text = font_arial.render(f"Score : {input}", True, BLACK, None)
    TextRect = text.get_rect()
    TextRect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    game_screen.blit(text, TextRect)

def main():

    (square_velocity) = (6)
    (square_length, square_height) = (30, 30)
    (sqaure_pos_x,square_pos_y) = (SCREEN_WIDTH/2, SCREEN_HEIGHT-60)
    (left_velocity, right_velocity) = (0, 0)
    (up_velocity, down_velocity) = (0, 0)

    circle_radius = 30
    (circle_x_position, circle_y_position) = (
        ran.randint(circle_radius, SCREEN_WIDTH-circle_radius), 0)
    (down_velocity_circle, side_velocity_circle) = (
        ran.randint(1, 3), ran.randint(-4, 4))
    

    score = 0
    shoot = False
    destroy = False

    game_play = False

    while not game_play:

        if destroy:
            destroy = False
            (down_velocity_circle, side_velocity_circle) = (
                ran.randint(1, 3), ran.randint(-4, 4))
            (circle_x_position, circle_y_position) = (
                ran.randint(circle_radius, SCREEN_WIDTH-circle_radius), 0)

        game_screen.fill(WHITE)

        for event in py.event.get():
            if event.type == py.QUIT:
                game_play = True

            if event.type == py.KEYDOWN:
                if event.key == py.K_w:
                    up_velocity = square_velocity
                if event.key == py.K_s:
                    down_velocity = square_velocity
                if event.key == py.K_a:
                    left_velocity = square_velocity
                if event.key == py.K_d:
                    right_velocity = square_velocity
                if event.key == py.K_SPACE:
                    shoot = True

            if event.type == py.KEYUP:
                if event.key == py.K_w:
                    up_velocity = 0
                if event.key == py.K_s:
                    down_velocity = 0
                if event.key == py.K_a:
                    left_velocity = 0
                if event.key == py.K_d:
                    right_velocity = 0
                if event.key == py.K_SPACE:
                    shoot = False


        sqaure_pos_x += (right_velocity - left_velocity)
        square_pos_y += (down_velocity - up_velocity)

        circle_y_position += down_velocity_circle
        circle_x_position += side_velocity_circle

        (laser_x, init_laser_y, end_laser_y) = (
            sqaure_pos_x+square_length/2-1, square_pos_y + square_height/2-1, 0)

        if shoot:
            render_laser((laser_x, init_laser_y),
                         (laser_x, end_laser_y))

        box = render_entitiy(
            sqaure_pos_x, square_pos_y)
        circle = render_entitiy(circle_x_position, circle_y_position)
        box.render_square(square_length, square_height)

        (circle_hitbox_left,circle_hitbox_right) = (circle_x_position - circle_radius,circle_x_position + circle_radius)

        if laser_x > circle_hitbox_left and laser_x < circle_hitbox_right and shoot:
            destroy = True
            score += 1
        if circle_hitbox_left > SCREEN_WIDTH or circle_hitbox_right < 0:
            destroy = True

        display_score(str(score))

        if not destroy:
            circle.render_circle(circle_radius)

        py.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main()
    py.quit()
