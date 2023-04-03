import pygame

def main():
    game = Game()
    game.run()

default_screen_size = (1200, 800)

class Game:
    def __init__(self):
        pygame.init()
        self.is_fullscreen = False
        self.screen = pygame.display.set_mode(default_screen_size) 
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.running = False  
        self.init_graphics()
        self.init_objects()

    def init_graphics(self):
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

        self.bg_imgs = [
            pygame.transform.rotozoom(x, 0, self.screen_height / x.get_height()).convert_alpha()
            for x in original_bg_imgs
        ]
        self.bg_widths = [x.get_width() for x in self.bg_imgs]
        self.bg_pos = [0, 0, 0]
        '''self.bg_altwidths = [x.get_width() for x in self.bg_altimgs]'''

    def init_objects(self):
        self.bird_alive = True
        self.bird_y_speed = 0
        self.bird_pos = (self.screen_width/6, self.screen_height/8)
        self.bird_angle = 0
        self.bird_frame = 0
        self.bird_lift = False

        '''self.altbg_pos = [0, 0, 0, 0, 0]'''

    def scale_positions(self, scale_x, scale_y):
        self.bird_pos = (self.bird_pos[0] * scale_x, self.bird_pos[1] * scale_y)
        self.bg_pos[0] = self.bg_pos[0] * scale_x
        self.bg_pos[1] = self.bg_pos[1] * scale_x
        self.bg_pos[2] = self.bg_pos[2] * scale_x 

    def run(self):    
        clock = pygame.time.Clock()
        self.running = True
        while self.running:
            self.handle_events()
            self.handle_game_logic()
            self.update_screen()
            clock.tick(60) # Odota niin kauan, että ruudun päivitysnopeus on 60fps
            
        pygame.quit()    
            
    def handle_events(self):        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_UP):
                    self.bird_lift = True
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_SPACE, pygame.K_UP):
                    self.bird_lift = False
                elif event.key in (pygame.K_f, pygame.K_F11):
                    self.toggle_fullscreen()
                elif event.key in (pygame.K_r, pygame.K_RETURN):
                    self.init_objects()

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
        self.scale_positions(
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
            self.bitd_angle = max(min(self.bird_angle, 75), -75)

        # Tarkista onko lintu pudonnut maahan
        if bird_y > self.screen_height * 0.80:
            bird_y = self.screen_height * 0.80
            self.bird_y_speed = -1
            self.bird_alive = False

        # Aseta linnun x-y-koordinaatit self.bird_pos-muuttujaan
        self.bird_pos = (self.bird_pos[0], bird_y)

    def update_screen(self):
        '''self.screen.fill("light blue")'''
        for i in [0, 1, 2]:
            self.screen.blit(self.bg_imgs[i], (self.bg_pos[i], 0))
        
            if self.bg_pos[i] + self.bg_widths[i] < self.screen_width:
                self.screen.blit(
                self.bg_imgs[i], 
                (self.bg_pos[i] + self.bg_widths[i], 0))
            if self.bg_pos[i] < -self.bg_widths[i]:
                self.bg_pos[i] += self.bg_widths[i]

        # piirä lintu
        if self.bird_alive:
            bird_img_i = self.bird_imgs[(self.bird_frame // 2) % 8]
        else:
            bird_img_i = self.bird_imgs[(self.bird_frame // 35) % 2]

        bird_img = pygame.transform.rotozoom(bird_img_i, self.bird_angle, 1)
        self.screen.blit(bird_img, self.bird_pos)

        pygame.display.flip()
 
    
    
    
    

        







if __name__ == "__main__":
    main()