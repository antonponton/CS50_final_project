import pygame

def draw_sessions(screen, drawing_sessions, current_session):
    # Draw all previous drawing sessions
    for session in drawing_sessions:
        for i in range(0, len(session)-1):
            pygame.draw.circle(screen, session[i][1], session[i][0], session[i][2])

    # Draw the current drawing session
    for i in range(0, len(current_session)-1):
        pygame.draw.circle(screen, current_session[i][1], current_session[i][0], current_session[i][2])

def draw_cursor(screen, cursor_color, last_tip_position, line_thickness):
    pygame.draw.circle(screen, cursor_color, last_tip_position, line_thickness)

def draw_color_indicator(screen, color_cycle, current_color_index, line_thickness, width):
    pygame.draw.circle(screen, color_cycle[current_color_index], (width - 20, 20),  line_thickness)

def draw_text_input(screen, text_label, text_input, input_box, font, width, height):
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (0, 0, 0), input_box)
    screen.blit(text_label, ((width / 2) - 70, (height / 2) - 40))
    text_surface = font.render(text_input, True, (255, 255, 255))
    screen.blit(text_surface, (input_box.x+5, input_box.y+5))
    input_box.w = max(150, text_surface.get_width()+10)

def draw_text_instructions(screen, font, width, height):
    text_color = font.render("Current color", True, (0, 0, 0))
    screen.blit(text_color, (width - 115, 15))
    text_instructions1 = font.render(
        "Press: [SPACE] to start/stop drawing | [C] to change the color | [S] to save the image | [N] to erease everything", 
        True, 
        (0, 0, 0,)
        )
    screen.blit(text_instructions1, (20, height - 40))
    text_instructions2 = font.render(
        "[z] to make paintbrush larger | [x] to make paintbrush smaller", 
        True, 
        (0, 0, 0,)
        )
    screen.blit(text_instructions2, (20, height - 20))