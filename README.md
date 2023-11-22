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
- [project.py](/project.py) - the main part of the program, the most difficult part was to display the cursor position when you are not drawing. To achive this I choosed to save the drawing sessions in a variable instead of drawing them directly to a display window and then draw them again and again with every frame.
- [hand_tracking.py](/hand_tracking.py) - contains the function to track the position of the tip of index finger.
- [drawing.py](/drawing.py) - contains all the functions used to draw on the display window.
- [helpers.py](/helpers.py) - contains helper function to save the drawing to a file.
