import pygame
import random
import enum
from highscore import HighscoreAction, HighscoreRecorder
from menu import Menu, MenuAction
from obstacle import Obstacle

default_screen_size = (1200, 800)
TEXT_COLOR = (128, 0, 128)
SCORE_TEXT_COLOR = (0, 64, 160)
fps_text_color = (128, 0, 128) # dark blue

DEBUG = 0

def main():
    game = Game()
    game.run()

class ActiveComponent(enum.Enum):
    MENU =  enum.auto()
    HIGHSCORES = enum.auto()
    GAME = enum.auto()

class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.menu = Menu()
        self.highscore_recorder = HighscoreRecorder()
        self.is_fullscreen = False
        self.active_component: ActiveComponent = ActiveComponent.MENU
        self.show_fps = True
        self.screen = pygame.display.set_mode(default_screen_size) 
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.running = False  
        self.font16 = pygame.font.Font('font/SyneMono-Regular.ttf', 16)
        self.init_sounds()
        self.init_graphics()
        self.init_objects()
        self.open_menu()

    def init_sounds(self):
        self.flying_sound = pygame.mixer.Sound("sound/flying_noise.wav")
        self.hit_sound = pygame.mixer.Sound("sound/Shout.wav")

    def init_graphics(self):
        self.menu.set_font_size(int(48 * self.screen_height / 450))
        self.highscore_recorder.set_font_size(int(36 * self.screen_height / 450))
        big_font_size = int(96 * self.screen_height / 450)
        self.font_big = pygame.font.Font("font/SyneMono-Regular.ttf", big_font_size)
        original_bird_imgs = [pygame.image.load(f"images/bird/frame-{i}.png")
        for i in [1, 2, 3, 4, 5, 6, 7, 8]
        ]

        self.bird_imgs = [pygame.transform.rotozoom(x, 0, 1/11).convert_alpha()
        for x in original_bird_imgs]

        original_bg_imgs = [
            pygame.image.load(f"images/background/layer_{i}.png")
            for i in [1, 2, 3]
        ]
        ''' original_bg_altimgs = [
            pygame.image.load(f"images/background/altlayer_{i}.png")
            for i in [1, 2, 3, 4, 5]
        ]'''
        self.bird_radius = self.bird_imgs[0].get_height() / 2 # Likiarvo
        
        self.bg_imgs = [
            pygame.transform.rotozoom(x, 0, self.screen_height / x.get_height()).convert_alpha()
            for x in original_bg_imgs
        ]
        self.bg_widths = [x.get_width() for x in self.bg_imgs]
        self.bg_pos = [0, 0, 0]
        '''self.bg_altwidths = [x.get_width() for x in self.bg_altimgs]'''

    def init_objects(self):
        self.score = 0
        self.bird_alive = True
        self.bird_y_speed = 0
        self.bird_pos = (self.screen_width/6, self.screen_height/8)
        self.bird_angle = 0
        self.bird_frame = 0
        self.bird_lift = False
        self.obstacles: list[Obstacle] = []
        self.next_obstacle_at = self.screen_width / 2
        self.add_obstacle()

        '''self.altbg_pos = [0, 0, 0, 0, 0]'''
    def add_obstacle(self):
        obstacle = Obstacle.make_random(self.screen_width, self.screen_height)
        self.obstacles.append(obstacle)

    def remove_oldest_obstacle(self):
        self.obstacles.pop(0) 

    def scale_positions_and_sizes(self, scale_x, scale_y):
        self.bird_pos = (self.bird_pos[0] * scale_x, self.bird_pos[1] * scale_y)
        for i in range(len(self.bg_pos)):
            self.bg_pos[i] = self.bg_pos[i] * scale_x
        for obstacle in self.obstacles:
            obstacle.width *= scale_x
            obstacle.position *= scale_x
            obstacle.upper_height *= scale_y
            obstacle.hole_size *= scale_y
            obstacle.lower_height *= scale_y

    def run(self):    
        self.running = True
        while self.running:
            self.handle_events() # Käsittelee tapathumat (eventit)
            
            if self.active_component == ActiveComponent.GAME:
                self.handle_game_logic() # Pelin ligiikka(liikkumiset, painovoima, yms.)
            self.update_screen() # Päivitä näyttö
            pygame.display.flip() # Päivittää näytölle piirtyt asiat näkyviin
            self.clock.tick(60) # Odota niin kauan, että ruudun päivitysnopeus on 60fps
            
        pygame.quit()    
            
    def handle_events(self):        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYUP and event.key == pygame.K_F11:
                self.toggle_fullscreen()
            elif self.active_component == ActiveComponent.GAME:
                self.handle_event(event)
            elif self.active_component == ActiveComponent.MENU:
                action = self.menu.handle_event(event)
                if action:
                    self.handle_menu_action(action)
            elif self.active_component == ActiveComponent.HIGHSCORES:
                action = self.highscore_recorder.handle_event(event)
                if action:
                    self.handle_highsore_action(action)

    def handle_event(self, event): 
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_UP):  
                self.bird_lift = True 
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_SPACE, pygame.K_UP):
                self.bird_lift = False
            elif event.key == pygame.K_ESCAPE or not self.bird_alive:
                if self.active_component == ActiveComponent.GAME:
                    self.record_highscore()
                else:
                    self.open_menu()

    def handle_menu_action(self, action: MenuAction):
        if action == MenuAction.NEW_GAME:
            self.start_game()
        elif action == MenuAction.HIGHSCORES:
            pass
        elif action == MenuAction.ABOUT:
            pass
        elif action == MenuAction.QUIT:
            self.running = False

    def handle_highscore_action(self, action):
        if action == HighscoreAction.CLOSE:
            self.active_component = ActiveComponent.MENU

    def start_game(self):
        self.active_component = ActiveComponent.GAME
        self.play_game_music()
        self.init_objects()
        self.flying_sound.play(-1)

    def open_menu(self):
        self.active_component = ActiveComponent.MENU
        self.play_menu_music()
        self.flying_sound.stop()

    def kill_bird(self):
        if self.bird_alive:
            self.bird_alive = False
            self.flying_sound.stop()
            self.hit_sound.play()
            pygame.mixer.music.fadeout(2500)
            

    def record_highscore(self):
        self.active_component = ActiveComponent.HIGHSCORES
        self.highscore_recorder.record_highscore(self.score)

    def play_menu_music(self):
        pygame.mixer.music.load("sound/Sky Game Menu.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play(loops=-1)

    def play_game_music(self):
        pygame.mixer.music.load("sound/Memoraphile - Up in the Sky.wav")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(loops=-1)

    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        old_width = self.screen_width
        old_height = self.screen_height
        if self.is_fullscreen:
            pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            pygame.display.set_mode(default_screen_size)
        screen = pygame.display.get_surface()
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.init_graphics()
        self.scale_positions_and_sizes(
            scale_x=(self.screen_width / old_width),
            scale_y=(self.screen_height / old_height)
        )

    def handle_game_logic(self):
        if self.bird_alive:
            self.bg_pos[0] -= 0.45
            self.bg_pos[1] -= 0.75
            self.bg_pos[2] -= 2.4

        bird_y = self.bird_pos[1]
        #Painovoima
        if self.bird_alive and self.bird_lift:
            self.bird_y_speed -= 0.5
        else:
            self.bird_y_speed += 0.2
        
        if self.bird_lift or not self.bird_alive:
            self.bird_frame += 1

        bird_y += self.bird_y_speed

        if self.bird_alive:
            self.bird_angle = -90 * 0.04 * self.bird_y_speed
            self.bird_angle = max(min(self.bird_angle, 75), -75)

        # Tarkista onko lintu pudonnut maahan
        if bird_y > self.screen_height * 0.80:
            bird_y = self.screen_height * 0.80
            self.bird_y_speed = -1
            self.kill_bird()

        # Aseta linnun x-y-koordinaatit self.bird_pos-muuttujaan
        self.bird_pos = (self.bird_pos[0], bird_y)
        
        if self.obstacles[-1].position < self.next_obstacle_at:
            self.add_obstacle()
            self.next_obstacle_at = random.randint(
                int(self.screen_width * 0.35),
                int(self.screen_width * 0.65)
            )

        if not self.obstacles[0].is_visible():
            self.remove_oldest_obstacle()
            self.score += 1

            
        self.bird_collides_with_obstacle = False
        for obstacle in self.obstacles:
            if self.bird_alive:
                obstacle.move(self.screen_width * 0.005)
            if obstacle.collides_with_circle(self.bird_pos, self.bird_radius):
                self.bird_collides_with_obstacle = True

        if self.bird_collides_with_obstacle:
            self.kill_bird()

    def update_screen(self):
        '''self.screen.fill("light blue")'''
        for i in range(len(self.bg_imgs)):
            if self.active_component != ActiveComponent.GAME and i == 1:
                break
            self.screen.blit(self.bg_imgs[i], (self.bg_pos[i], 0))
        
            if self.bg_pos[i] + self.bg_widths[i] < self.screen_width:
                self.screen.blit(
                self.bg_imgs[i], 
                (self.bg_pos[i] + self.bg_widths[i], 0))
            if self.bg_pos[i] < -self.bg_widths[i]:
                self.bg_pos[i] += self.bg_widths[i]
        
        if self.active_component == ActiveComponent.MENU:
            self.menu.render(self.screen)
            return
        
        if self.active_component == ActiveComponent.HIGHSCORES:
            self.highscore_recorder.render(self.screen)
            return

        for obstacle in self.obstacles:
            obstacle.render(self.screen)

        # piirä lintu
        if self.bird_alive:
            bird_img_i = self.bird_imgs[(self.bird_frame // 2) % 8]
        else:
            bird_img_i = self.bird_imgs[(self.bird_frame // 35) % 2]

        bird_img = pygame.transform.rotozoom(bird_img_i, self.bird_angle, 1)
        bird_x = self.bird_pos[0] - bird_img.get_width() / 2 * 1.25
        bird_y = self.bird_pos[1] - bird_img.get_height() / 2
        self.screen.blit(bird_img, (bird_x, bird_y))

        score_text = f"{self.score}"
        score_img = self.font_big.render(score_text, True, SCORE_TEXT_COLOR)
        score_pos = (self.screen_width * 0.95 - score_img.get_width(), 
                     self.screen_height - score_img.get_height())
        self.screen.blit(score_img, score_pos)

        if not self.bird_alive:
            game_over_img = self.font_big.render("GAME OVER", True, TEXT_COLOR)
            x = self.screen_width / 2 - game_over_img.get_width() / 2
            y = self.screen_height / 2 - game_over_img.get_height() / 2
            self.screen.blit(game_over_img, (x, y))

        if DEBUG:
            color = (0, 0, 0) if not self.bird_collides_with_obstacle else (255, 0, 0)
            pygame.draw.circle(self.screen, color, self.bird_pos, self.bird_radius)

        if self.show_fps:
            fps_text = f"{self.clock.get_fps():.1f} fps"
            fps_img = self.font16.render(fps_text, True, fps_text_color)
            self.screen.blit(fps_img, (0, 0))

if __name__ == "__main__":
    main()