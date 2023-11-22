# HAND TRACKING PAINT
#### Video Demo: https://www.youtube.com/watch?v=UiuuyxSREoY
#### Description:
This is a program written in Python that allows user to make simple drawings using hand movement to control the cursor.
It uses three Python libraries:
- OpenCV - to access view from a webcam
- MediaPipe - to track the movement of the user's hand
- Pygame - to actually "draw". <br>
To control the movement of the cursor you wave your hand in front of your camera, it keeps track of the tip of your index finger.
To start and stop drawing press "space" on your keyboard.<br>
Other features:
- To change color of the paintbrush press "c".
- To make paintbrush larger press "z".
- To make paintbrush smaller press "x".
- To clear the screen press "n".
- If you want to save your drawing to a .png file you press "s" and then type the filename followed by "enter".
##### Files:
- [project.py](/project.py) - the main part of the program, the most difficult part was to display the cursor position when you are not drawing. To achive this I choosed to save the drawing sessions in a variable instead of drawing them directly to a display window and then draw them again and again with every frame.<br>
In details:<br>
Initialize Pygame and set up the window.<br>
Then initialize some variables used as parameters.<br>
Use OpenCV to open webcam.
Use while loop to run code with every frame:<br>
Capture the frame from webcam.<br>
Get position of tip of index finger with MediaPipe.<br>
If the position has changed add it to a session variable.<br>
Clear the screen and fill it with text instructions and color indicator.<br>
Draw all the points from the drawing sessions and cursor if not currently drawing.<br>
Handle the text input for saving drawing to a file.<br>
Display Pygame window.<br>
Next few lines of code handles the events in Pygame: quitting the game and keybord input used to control features.<br>
In the saving part (when user press "enter" key) it clears the screen and draws only drawing sessions without text instructions, color indicator and cursor and then saves image of the screen.
- [hand_tracking.py](/hand_tracking.py) - contains the function to track the position of the tip of index finger.<br>
In details:<br>
Initialize MediaPipe Hand module.<br>
Change the frame to RGB and process it with Mediapipe Hand Tracking.<br>
Check for hand presence and if found get the coordinates of the tip of the index finger.<br>
If it is different from the last one return the coordinates.
- [drawing.py](/drawing.py) - contains all the functions used to draw on the display window.<br>
In details:<br>
draw_sessions - uses pygame draw.circle function to draw circle on the screen for every point stored in drawing sessions with associated color and size.<br>
draw_cursor - draws gray circle in position of the tip of index finger with current size of paintbrush.<br>
draw_color_indicator - draws circle in the right up corner of the screen with current size and color of the paintbrush.<br>
draw_text_input - fill the screen with black color and render the label and user's input text.<br>
draw_text_instructions - display the text instructions on the screen.
- [helpers.py](/helpers.py) - contains helper function to save the drawing to a file.
