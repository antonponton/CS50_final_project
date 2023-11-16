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
filename = "drawing.png"

# Define a list of colors to cycle through
color_cycle = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
current_color_index = 0

# Initialize MediaPipe Hand module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Open webcam
cap = cv2.VideoCapture(0)

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
            elif event.key == pygame.K_s:
                # Prompt the user for a filename and save the drawing
                filename = input("Enter filename: ")
                filename = filename + ".png"
                pygame.image.save(screen, filename)
                print(f"Drawing saved to {filename}")

# Release resources
cap.release()
cv2.destroyAllWindows()
pygame.quit()