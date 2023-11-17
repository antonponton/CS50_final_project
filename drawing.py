import pygame

def draw_sessions(screen, drawing_sessions, current_session, line_thickness):
    # Draw all previous drawing sessions
    for session in drawing_sessions:
        for i in range(1, len(session)):
            pygame.draw.line(screen, session[i][1], session[i - 1][0], session[i][0], line_thickness)

    # Draw the current drawing session
    for i in range(1, len(current_session)):
        pygame.draw.line(screen, current_session[i][1], current_session[i - 1][0], current_session[i][0], line_thickness)

def draw_cursor(screen, cursor_color, last_tip_position, cursor_radius):
    pygame.draw.circle(screen, cursor_color, last_tip_position, cursor_radius)

def draw_color_indicator(screen, color_cycle, current_color_index, width):
    pygame.draw.circle(screen, color_cycle[current_color_index], (width - 20, 20), 15)

def draw_text_input(screen, text_label, text_input, width, height):
    screen.fill((255, 255, 255))
    font = pygame.font.SysFont("Verdana", 20)
    input_box = pygame.Rect((width / 2) - 70, (height / 2) - 16, 140, 32)
    pygame.draw.rect(screen, (0, 0, 0), input_box)
    screen.blit(text_label, ((width / 2) - 100, (height / 2) - 40))
    text_surface = font.render(text_input, True, (255, 255, 255))
    screen.blit(text_surface, (input_box.x+5, input_box.y+5))
    input_box.w = max(100, text_surface.get_width()+10)
    