import cv2
import mediapipe as mp
import pygame

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
drawing = False
current_session = []
drawing_sessions = []
last_tip_position = (0, 0)

# Initialize the filename variable
font = pygame.font.SysFont("Verdana", 20)
filename = ""
text = font.render(filename, True, (0, 0, 0))
text_label = font.render("Enter filename:", True, (0, 0, 0))
input_text = False
input_rect = pygame.Rect((width / 2) - 70, (height / 2) - 16, 140, 32)

# Define a list of colors to cycle through
color_cycle = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
current_color_index = 0

# Initialize MediaPipe Hand module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Open webcam
cap = cv2.VideoCapture(0)

def get_painting():
    screen.fill((255, 255, 255))
    for session in drawing_sessions:
        for i in range(1, len(session)):
            pygame.draw.line(screen, session[i][1], session[i - 1][0], session[i][0], line_thickness)
    for i in range(1, len(current_session)):
        pygame.draw.line(screen, current_session[i][1], current_session[i - 1][0], current_session[i][0], line_thickness)
    pygame.display.update()

while True:
    # Capture frame from webcam
    ret, frame = cap.read()

    # Process the frame with MediaPipe Hand Tracking
    rgb_frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    

    # Check for hand presence
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Extract the coordinates of the tip of the index finger (landmark point 8)
            tip_of_index_finger_pygame = (
                int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * width),
                int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * height)
            )

            # Check for changes in the tip of the index finger position
            if tip_of_index_finger_pygame != last_tip_position:
                if drawing:
                    current_session.append((tip_of_index_finger_pygame, color_cycle[current_color_index]))
                last_tip_position = tip_of_index_finger_pygame

    # Display the Pygame window
    screen.fill((255, 255, 255))  # Clear the screen

    # Draw all previous drawing sessions
    for session in drawing_sessions:
        for i in range(1, len(session)):
            pygame.draw.line(screen, session[i][1], session[i - 1][0], session[i][0], line_thickness)

    # Draw the current drawing session
    for i in range(1, len(current_session)):
        pygame.draw.line(screen, current_session[i][1], current_session[i - 1][0], current_session[i][0], line_thickness)

    # Draw the cursor when not drawing
    if not drawing:
        pygame.draw.circle(screen, cursor_color, last_tip_position, cursor_radius)
    
    # Draw the color indicator circle in the right upper corner
    pygame.draw.circle(screen, color_cycle[current_color_index], (width - 20, 20), 15)

    if input_text:
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (0, 0, 0), input_rect)
        screen.blit(text_label, ((width / 2) - 100, (height / 2) - 40))
        text_surface = font.render(filename, True, (255, 255, 255))
        screen.blit(text_surface, (input_rect.x+5, input_rect.y+5))
        input_rect.w = max(100, text_surface.get_width()+10)

    pygame.display.flip()

    # Draw on Pygame window
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
                filename = filename[:-1]
                text = font.render(filename, True, (255, 255, 255))
            elif event.key == pygame.K_RETURN:
                input_text = False
                get_painting()
                filename = filename + ".png"
                pygame.image.save(screen, filename)
                print(f"Drawing saved to {filename}")
                filename = ""
            elif event.unicode.isprintable() and input_text:
                filename += event.unicode
                text = font.render(filename, True, (255, 255, 255))
            elif event.key == pygame.K_n:
                # New sheet
                current_session = []
                drawing_sessions = []

# Release resources
cap.release()
cv2.destroyAllWindows()
pygame.quit()