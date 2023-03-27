import pygame

def main():
    game = Game()
    game.run()

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 750)) 
        self.running = False  
        self.init_graphics()
        self.init_objects()

    def init_graphics(self):
        self.bird_frame = 0
        bird_imgs = [pygame.image.load(f"images/bird/frame-{i}.png")
        for i in [1, 2, 3, 4, 5, 6, 7, 8]
        ]

        self.bird_imgs = [pygame.transform. rotozoom(x, 0, 1/12)
        for x in bird_imgs]

    def init_objects(self):
        self.bird_y_speed = 0
        self.bird_pos = (150, 100)
        self.bird_lift = False

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


    def handle_game_logic(self):

        bird_y = self.bird_pos[1]
        #Painovoima
        if self.bird_lift:
            self.bird_y_speed -= 0.5
            self.bird_frame += 1
        else:
            self.bird_y_speed += 0.2
        
        bird_y += self.bird_y_speed
        self.bird_pos = (self.bird_pos[0], bird_y)

    def update_screen(self):
        self.screen.fill("light blue")
        

        # piirä lintu
        angle = -90 * 0.04 * self.bird_y_speed
        angle = max(min(angle, 75), -75)
        
        bird_img_i = self.bird_imgs[(self.bird_frame // 2) % 8]

        bird_img = pygame.transform.rotozoom(bird_img_i, angle, 1)
        self.screen.blit(bird_img, self.bird_pos)

        pygame.display.flip()
 
    
    
    
    

        







if __name__ == "__main__":
    main()