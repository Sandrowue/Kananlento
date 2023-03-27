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

    def init_graphics(self):
        img_bird1 = pygame.image.load("images/bird/frame-1.png")
        self.img_bird1 = pygame.transform. rotozoom(img_bird1, 0, 1/12)

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

    def handle_game_logic(self):
        pass

    def update_screen(self):
        self.screen.fill("light blue")
        

        # piirä lintu
        self.screen.blit(self.img_bird1, (100, 100))

        pygame.display.flip()
 
    
    
    
    

        







if __name__ == "__main__":
    main()