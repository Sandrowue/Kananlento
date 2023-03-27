import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 750))  
    clock = pygame.time.Clock()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill("light blue")
        pygame.display.flip()

        clock.tick(60) # Odota niin kauan, että ruudun päivitysnopeus on 60fps
    
    pygame.quit()

        







if __name__ == "__main__":
    main()