import pygame

def save_drawing(screen, filename):
    filename = filename + ".png"
    pygame.image.save(screen, filename)
    print(f"Drawing saved to {filename}")