# Table of Contents
## [1. Introduction](#1.-introduction)
## [2. Camera Calibration](#camera-calibration)
## [3. Aruco Marker Measurements](#3.-aruco-marker-measurements)
## 4. RoboDK Station
## 5. RoboDK Python

### 1. Introduction
This respository is for the Spatial Alignment with Machine Vision Robot sponsored by the Stanford Linear Accelerator Center, constructed by CSU, Chico Senior Capstone Team.The main components of the project utilize Python, OpenCV, RoboDK, Vimba Python, and Aruco Libraries. There are several protocals that must be followed in order to successfully run the protoype project. 

### Camera Calibration
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

At least 9 images are requried to properly calibrate a camera/lens combination, however, it is recommended to take up to 30 images. The images taken will be of the calibration board (7x11 checkerboard) in various orientations that still allow the board to be within the focal distance of the frame. The recommened method of capturing these images is to keep the camera mounted to the robot and create a simple program on the UR tablet to move the camera around the calibration board. The board should be completely flat when taking calibration images. Please see the UR5e manual on how to create a program using the provided tablet (or click [here](https://github.com/mcabral5/SLAC-Project-Info/blob/main/UR5e_User_Manual.pdf)). 
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

##### Example of [CameraDistortion File](https://github.com/mcabral5/SLAC-Project-Info/blob/main/cameraDistortion.txt). Example of [CameraMatrix](https://github.com/mcabral5/SLAC-Project-Info/blob/main/cameraMatrix.txt)

### [3. ArUco Marker Measurements]
Marker measurements are done inside the RoboDK script, however it is important to note the size of the marker. Insert the size of the marker in mm as the 'actual_size' variable in the roboDk python script. 

Two sets of marker measurements are provided. The first is the xyz rpy of the marker with respect to the camera frame. The second set is derived from the marker's eurler angles to get the camera's position with respect to the marker frame. This is the set of coordinates use in the transformation to get the marker's xyz coordinates with respect to the robot base. In order to properly utilize these measurements in the transformation, the x coordinate of the camera with respect to the marker must be flipped to retrieve the marker's position with repsect to the camera. So, from the displayed coordinates, the coordinates of interest are the third from the top 'Camera Position'. 

### 4. RoboDK Station
RoboDK is a very user-friendly robot software that is used to accurately place various robot target positions throughout a 3D space. In order to fully utilize this project, all objects must be percisly placed inside of a RoboDK station as they are in the physical world. Any deviation will result in inaccurate results. RoboDK has some excellent documentation for beginning with the program [here](https://www.youtube.com/c/RoboDK3D/playlists).

For ease of the user, it is benificial to import all fiducial markers to roboDK and create the targets in the area. This way, simulated programs can be run to view the robot's path without running the actual python script. Creating targets prior to the python script will also make the robot movements simpiler as well. 

##### Example of RoboDK station from CSU, Chico Expo Demo [here](https://github.com/mcabral5/SLAC-Project-Info/blob/main/CSU%20Expo%20Station.rdk).

### 5. RoboDK Python
In order to run a python script with robodk, add a python script and edit it inside robodk. All items in the RoboDK station can be defined using the following code, depending on item type ([Source](https://robodk.com/doc/en/PythonAPI/robodk.html#robolink-py)):

```
ITEM_TYPE_STATION=1             # station item (.rdk files)
ITEM_TYPE_ROBOT=2               # robot item (.robot files)
ITEM_TYPE_FRAME=3               # reference frame item
ITEM_TYPE_TOOL=4                # tool item (.tool files or tools without geometry)
ITEM_TYPE_OBJECT=5              # object item (.stl, .step, .iges, ...)
ITEM_TYPE_TARGET=6              # target item
ITEM_TYPE_PROGRAM=8             # program item (made using the GUI)
ITEM_TYPE_PROGRAM_PYTHON=10     # Python program or macro
```
If all targets are exisiting in the station, then robot moves will be simple:
```
MoveL(target)                   # linear move
MoveJ(target)                   # joint move
```

Each fiducial marker is assigned as a class of type measure_class() such as the following code:
```
marker1 = measure_class.measure(0,0,0,0)    # arguments are marker id, x pos, y pos, z pos
```
In order measure the function 'measure()' is called within the measure_class() class.

```
marker1.measuring(marker_size, calib_path, camera_matrix, camera_distortion)
cv2.destroyAllWindows()
```
The x, y, z coordinates are then saved to a variable to be accessed later. 

In order to complete the last transformation to the target source, the known distance between the marker reference frame (corner of marker) and the target must be known. The following transformations can be completed like so:

```
# Set Items
robot = RDK.Item('UR5e', ITEM_TYPE_ROBOT)
O1M1 = RDK.Item('O1-M1', ITEM_TYPE_TARGET)
# Define xyz list
O1_M1_xyz = list()
# Define position vector of target (x-ray or specimen) with respect to the marker
O1M1_Xray = (73, -140.5, 161.00)

# Main Code
robot.MoveL(O1M1) # Move to target
TCP = robot.Pose() # Retrieve TCP of robot. Ensure that the correct TCP is selected 
O1_M1.measuring(marker_size, calib_path, camera_matrix, camera_distortion) #Begin Measuring
cv2.destroyAllWindows() # Close all viewing windows
# x y z coordinates of frame with respect to camera
O1_M1_xyz.append(-O1_M1.x) 
O1_M1_xyz.append(O1_M1.y)
O1_M1_xyz.append(O1_M1.z)
# transformations with respect to robot base
O1M1_Base = TCP*transl(O1_M1_xyz) # Marker with respect to base
O1_X1 = O1M1_Base*transl(O1M1_Xray) # Target with respect to base
```
There are several python examples with RoboDK [here](https://robodk.com/doc/en/PythonAPI/index.html). 
