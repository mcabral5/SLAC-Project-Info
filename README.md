# Table of Contents
## 1. Introduction
## 2. Camera Calibration
## 3. Aruco Marker Measurements
## 4. RoboDK Station
## 5. RoboDK Python

### 1. Introduction
This respository is for the Spatial Alignment with Machine Vision Robot sponsored by the Stanford Linear Accelerator Center, constructed by CSU, Chico Senior Capstone Team.The main components of the project utilize Python, OpenCV, RoboDK, Vimba Python, and Aruco Libraries. There are several protocals that must be followed in order to successfully run the protoype project. 

### 2. Camera Calibration
Camera and lens calibration must be completed whenever any of the following items are altered:
- Camera Lens
- Lens Appeture
- Lens Focal Length
- Camera Model

#### Hardware Required:
- Calibration Board
- Camera
- Lens
- Robot Arm 
- Camera Mount

#### Python Scripts Required:
- calibcapture.py
- cameracalib.py

#### calibcapture.py
'calibcapture.py' is a python script created in order to access an individual Mako camera in order to take calibration images. This script uses real-time calibration methods, however, this caused issues for this project. Therefore, an offline calibration method was created where this script is the first step. Instead of accessing the camera via 'cv2.VideoCapture()', the mako camera frame must be accessed via the Vimba Python libraries. 

At least 9 images are requried to properly calibrate a camera/lens combination, however, it is recommended to take up to 30 images. The images taken will be of the calibration board (7x11 checkerboard) in various orientations that still allow the board to be within the focal distance of the frame. The recommened method of capturing these images is to keep the camera mounted to the robot and create a simple program on the UR tablet to move the camera around the calibration board. The board should be completely flat when taking calibration images. Please see the UR5e manual on how to create a program using the provided tablet (or click [here](github.com)). 
When creating this robot program, it is important to have the 'Vimba Viewer' open so that no movements cut off or blur the calibration boards in the camera's field of view. Once this program is completed, run the program constantly at 3-9% speed.

Open the computer's command prompt and navigate to the location of the 'calibcapture.py' file (C:\Users\PoThe\OneDrive\Desktop\Mako Camera Code). Run the code. 
```
C:\Users\PoThe>
C:\Users\PoThe>cd C:\Users\PoThe\OneDrive\Desktop\Mako Camera Code
C:\Users\PoThe\OneDrive\Desktop\Mako Camera Code>python calibcapture.py
```
The user will be prompted how many images that they would like capture, enter only numeric values. Once the quantity is inputted, press the 'enter' key to move forward. The camera frame will be displayed, then press 'enter' to capture an image. The viewing window will close and the capture framed will be displayed for a short time before the capturing window reopens. 
After all images are captured, they will be stored in 'C:\Users\PoThe\OneDrive\Desktop\Mako Camera Code\Calibration Images', and the user may move onto the second script.

#### cameracalib.py
'cameracalib.py' is a python script created to calibrate the captured images from the previous script. This method is the same as OpenCV's camera calibration documentation found [here](https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html).

Before running the code, ensure that the rows and columns inside the script match the calibration board used. It is important to note that this code utilizes edge detection, so for a 7x11 chessboard pattern there will be 6 rows and 10 columns in terms of the detectable edges. Also verify that the size of the individual chess squares are the correct size. 
In order to run this code, navigate to its location in the command prompt and run. 
```
C:\Users\PoThe>
C:\Users\PoThe>cd C:\Users\PoThe\OneDrive\Desktop\Mako Camera Code
C:\Users\PoThe\OneDrive\Desktop\Mako Camera Code>python cameracalib.py
```
Once the code is ran, the captured images will be shown on the screen with calibration lines drawn at the edges. The code will run through all images and will prompt you to choose to accept or decline the image if it is able to detect all corners or it will display that the image was a 'bad image'. Press 'enter' to accept the image and 'esc' to decline the image if the calibration quality it not good.

After calibration is complete, the camera matrix and distortion matrix will be shown and saved as text files, a bad image will be reimaged and stored as calib result, and the calibration error will be shown. Calibration error should be as low as possible. 
It is recommended to move the camera matrix and distortion matrix into a separate folder so that it will not be accidentally deleted. Once completed, copy and paste both the camera and distortion matrices to the main folder 'Mako Camera Code' so that they can be accessed when using the measurement code.

