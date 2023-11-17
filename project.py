import cv2
import pygame
from hand_tracking import track_hand
from drawing import draw_sessions, draw_cursor, draw_color_indicator, draw_text_input
from helpers import save_drawing

# Initialize Pygame
pygame.init()

# Set up the window
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Hand Tracking Paint")

# Set up colors and drawing parameters
cursor_color = (200, 200, 200)
line_thickness = 5
cursor_radius = 10
current_session = []
drawing_sessions = []
last_tip_position = (0, 0)
drawing = False

# Initialize the text input
text_input = ""
input_text = False

# Define a list of colors to cycle through
color_cycle = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
current_color_index = 0

# Open webcam
cap = cv2.VideoCapture(0)

while True:
    # Capture frame from webcam
    ret, frame = cap.read()

    # Get the coordinates of the tip of index finger
    tip_of_index_finger = track_hand(frame, width, height, last_tip_position)
    
    # Check for changes in the tip of index finger position
    if tip_of_index_finger != last_tip_position:
        if drawing:
            current_session.append((tip_of_index_finger, color_cycle[current_color_index]))
        last_tip_position = tip_of_index_finger
    

    # Display the Pygame window
    screen.fill((255, 255, 255))  # Clear the screen

    # Draw on Pygame window
    draw_sessions(screen, drawing_sessions, current_session, line_thickness)
    if not drawing:
        draw_cursor(screen, cursor_color, last_tip_position, cursor_radius)
    draw_color_indicator(screen, color_cycle, current_color_index, width)
    
    # Display the text input for filename to save
    if input_text:
        font = pygame.font.SysFont("Verdana", 20)
        text_label = font.render("Enter filename:", True, (0, 0, 0))
        filename = text_input
        draw_text_input(screen, text_label, text_input, width, height)

    pygame.display.flip()

    # Handle events in Pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cap.release()
            cv2.destroyAllWindows()
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not drawing:
                    # If starting a new drawing session, add the current session to the list
                    if current_session:
                        drawing_sessions.append(current_session)
                    current_session = []
                drawing = not drawing  # Toggle drawing mode
            elif event.key == pygame.K_ESCAPE:
                cap.release()
                cv2.destroyAllWindows()
                pygame.quit()
                exit()
            elif event.key == pygame.K_c:
                # Change color by cycling through the color_cycle list
                current_color_index = (current_color_index + 1) % len(color_cycle)
            elif event.key == pygame.K_s and input_text == False:
                input_text = True
            elif event.key == pygame.K_BACKSPACE:
                text_input = text_input[:-1]
            elif event.key == pygame.K_RETURN:
                input_text = False
                screen.fill((255, 255, 255))
                draw_sessions(screen, drawing_sessions, current_session, line_thickness)
                save_drawing(screen, filename)
                text_input = ""
            elif event.unicode.isprintable() and input_text:
                text_input += event.unicode
            elif event.key == pygame.K_n:
                # New sheet
                current_session = []
                drawing_sessions = []

# Release resources
cap.release()
cv2.destroyAllWindows()
pygame.quit()