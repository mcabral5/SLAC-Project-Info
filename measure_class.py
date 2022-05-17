import numpy as np
import cv2 as cv
import cv2
from cv2 import VideoCapture, aruco
import sys, time, math
from vimba import *
import logging
import time
import matplotlib.pyplot as plt 


class measure:
    def __init__(self, markerid, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.markerid = markerid
    
    def isRotationMatrix(self, R):
        Rt = np.transpose(R)
        shouldBeIdentity = np.dot(Rt, R)
        I = np.identity(3, dtype=R.dtype)
        n = np.linalg.norm(I - shouldBeIdentity)
        return n < 1e-6
    
    def rotationMatrixToEulerAngles(self,R):
        try:
            assert (self.isRotationMatrix(R))
            logging.debug("successful")
        except:
            logging.error("error with isRotationMatrix")
        sy = math.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])
        singular = sy < 1e-6
        if not singular:
            x = math.atan2(R[2, 1], R[2, 2])
            y = math.atan2(-R[2, 0], sy)
            z = math.atan2(R[1, 0], R[0, 0])
        else:
            x = math.atan2(-R[1, 2], R[1, 1])
            y = math.atan2(-R[2, 0], sy)
            z = 0
        return np.array([x, y, z])
    
    def measuring(self, marker_size, calib_path, camera_matrix, camera_distortion):
        #--- 180 deg rotation matrix around the x axis
        R_flip  = np.zeros((3,3), dtype=np.float32)
        R_flip[0,0] = 1.0
        R_flip[1,1] =-1.0
        R_flip[2,2] =-1.0

        #--- Define the aruco dictionary
        aruco_dict  = aruco.getPredefinedDictionary(aruco.DICT_ARUCO_ORIGINAL)
        parameters  = aruco.DetectorParameters_create()
        logging.debug(parameters)
        logging.debug(camera_distortion)
        logging.debug(camera_matrix)

        #-- Font for the text in the image

        font = cv2.FONT_HERSHEY_TRIPLEX
        #initialize moving sum variables for tag
        xSum=0 
        xavg=0
        ySum=0
        yavg=0
        zSum=0
        zavg=0
        rxSum=0
        rxavg=0
        rySum=0
        ryavg=0
        rzSum=0
        rzavg=0
        xList = list()
        yList = list()
        zList = list()
        rxList = list()
        ryList = list()
        rzList = list()
        bool70 = False
        bool71 = False
        bool72 = False
        bool73 = False
        bool74 = False
        bool75 = False
        bool76 = False
        bool77 = False
        bool78 = False
        bool79 = False
        bool80 = False
        #initialize moving sum variables for cam
        camxSum=0 
        camxavg=0
        camySum=0
        camyavg=0
        camzSum=0
        camzavg=0
        camrxSum=0
        camrxavg=0
        camrySum=0
        camryavg=0
        camrzSum=0
        camrzavg=0
        window_size = 30
        count = 0
        camxList = list()
        camyList = list()
        camzList = list()
        camrxList = list()
        camryList = list()
        camrzList = list()
        id70 = list()
        id71 = list()
        id72 = list()
        id73 = list()
        id74 = list()
        id75 = list()
        id76 = list()
        id77 = list()
        id78 = list()
        id79 = list()
        id80 = list()

        #Access Camera
        with Vimba.get_instance() as vimba:#Vimba code
            cams = vimba.get_all_cameras()#get camera
            with cams[0] as cam:
                while True:
        #try:       
                    fmts = cam.get_pixel_formats() #get pixel format
                    fmts = intersect_pixel_formats(fmts, OPENCV_PIXEL_FORMATS) #set format (fmts) as Mono8
                    cam.set_pixel_format(fmts[0]) #set cam to Mono8 format
                    logging.debug('Camera was successfully accessed.')
            #-- Read the camera frame
                    frame = cam.get_frame() #grab frame from camera
                    
        #             #-- Convert in gray scale
                    img= frame.as_opencv_image()
                    
                    #img is used to read frame as an opencv image which can be used with cv2 commands
                    logging.debug('Frame was successfully accessed and converted to an OpenCV image.')

                    #-- Find all the aruco markers in the image
                    #print("ready to measure")
                    corners, ids, rejected = cv2.aruco.detectMarkers(image=img, dictionary=aruco_dict, parameters=parameters,
                                            cameraMatrix=camera_matrix, distCoeff=camera_distortion)

                    #if ids is not None and ids[0] == id_to_find:
                    if ids is not None:
                    # print("marker detected")
                        #-- ret = [rvec, tvec, ?]
                        #-- array of rotation and position of each marker in camera frame
                        #-- rvec = [[rvec_1], [rvec_2], ...]    attitude of the marker respect to camera frame
                        #-- tvec = [[tvec_1], [tvec_2], ...]    position of the marker in camera frame
                        reading_id = ids[0]
                        #-------- store cam location w/ respect to marker 70 
                        if reading_id == 70:
                            id70 = [camxavg,camyavg,camzavg]
                            bool70 = True

                        #-------- store cam location w/ respect to marker 71
                        elif reading_id == 71:
                            id71 = [camxavg,camyavg,camzavg]
                            bool71 = True

                        #-------- store cam location w/ respect to marker 72
                        elif reading_id == 72:
                            id72 = [camxavg,camyavg,camzavg]
                            bool72 = True

                        #-------- store cam location w/ respect to marker 73
                        elif reading_id == 73:
                            id73 = [camxavg,camyavg,camzavg]
                            bool73 = True

                        #-------- store cam location w/ respect to marker 74
                        elif reading_id == 74:
                            id74 = [camxavg,camyavg,camzavg]
                            bool74 = True

                        #-------- store cam location w/ respect to marker 75
                        elif reading_id == 75:
                            id75 = [camxavg,camyavg,camzavg]
                            bool75 = True

                        #-------- store cam location w/ respect to marker 76
                        elif reading_id == 76:
                            id76 = (camxavg,camyavg,camzavg)
                            #logging.info(type(camxavg))
                            bool76 = True

                        #-------- store cam location w/ respect to marker 77
                        elif reading_id == 77:
                            id77 = [camxavg,camyavg,camzavg]
                            bool77 = True

                        #-------- store cam location w/ respect to marker 78
                        elif reading_id == 78:
                            id78 = [camxavg,camyavg,camzavg]
                            bool78 = True

                        #-------- store cam location w/ respect to marker 79
                        elif reading_id == 79:
                            id79 = [camxavg,camyavg,camzavg]
                            bool79 = True

                        #-------- store cam location w/ respect to marker 80
                        elif reading_id == 80:
                            id80 = [camxavg,camyavg,camzavg]
                            bool80 = True

                        try: 
                            # log different id marker locations
                            pos = aruco.estimatePoseSingleMarkers(corners, marker_size, camera_matrix, camera_distortion)
                            #-- Unpack the output, get only the first
                            rvec, tvec = pos[0][0,0,:], pos[1][0,0,:]
            
                            #-- Draw the detected marker and put a reference frame over it
                            aruco.drawDetectedMarkers(img, corners) #changed frame to img
                            aruco.drawAxis(img, camera_matrix, camera_distortion, rvec, tvec, .3) #changed frame to img
                            
                            tag_pos = [element * 10 for element in tvec]
                            count = count +1
                  
                            #avg x pos for tag
                            xList.append(tag_pos[0])              
                            if count > window_size:
                                xSum = sum(xList[count-window_size:count-1])
                                xavg = xSum/window_size
                            else:
                                xSum = xSum + tag_pos[0]
                                xavg = xSum/count
                      
                        
                            #avg y pos for tag
                            yList.append(tag_pos[1])              
                            if count > window_size:
                                ySum = sum(yList[count-window_size:count-1])
                                yavg = ySum/window_size
                            else:
                                ySum = ySum + tag_pos[1]
                                yavg = ySum/count
                            
                            #avg z pos for tag
                            zList.append(tag_pos[2])              
                            if count > window_size:
                                zSum = sum(zList[count-window_size:count-1])
                                zavg = zSum/window_size
                            else:
                                zSum = zSum + tag_pos[2]
                                zavg = zSum/count

                            #-- Print the tag position in camera frame
                            str_position = "MARKER Position [mm] x=%2.3f  y=%2.3f  z=%2.3f"%(xavg, yavg, zavg)
                            cv2.putText(img, str_position, (0, 100), font, 2, (0, 255, 0), 3, cv2.LINE_AA)#changed frame to img

                            #-- Obtain the rotation matrix tag->camera
                            R_ct    = np.matrix(cv2.Rodrigues(rvec)[0])
                            R_tc    = R_ct.T

                            #-- Get the attitude in terms of euler 321 (Needs to be flipped first)
                            try:
                                roll_marker, pitch_marker, yaw_marker = self.rotationMatrixToEulerAngles(R_flip*R_tc)
                            except: 
                                logging.error("error with rotationMatrixToEulerAngle")
                            #avg rx pos for tag
                            rxList.append(roll_marker)              
                            if count > window_size:
                                rxSum = sum(rxList[count-window_size:count-1])
                                rzavg = rzSum/window_size
                            else:
                                rxSum = rxSum + roll_marker
                                rxavg = rxSum/count

                            #avg ry pos for tag
                            ryList.append(pitch_marker)              
                            if count > window_size:
                                rySum = sum(ryList[count-window_size:count-1])
                                ryavg = rySum/window_size
                            else:
                                rySum = rySum + pitch_marker
                                ryavg = rySum/count

                            #avg rz pos for tag
                            rzList.append(yaw_marker)              
                            if count > window_size:
                                rzSum = sum(rzList[count-window_size:count-1])
                                rzavg = rzSum/window_size
                            else:
                                rzSum = rzSum + yaw_marker
                                rzavg = rzSum/count


                            #-- Print the marker's attitude respect to camera frame
                            str_attitude = "MARKER Attitude [degrees] r=%2.3f  p=%2.3f  y=%2.3f"%(math.degrees(rxavg),math.degrees(ryavg),
                                                math.degrees(rzavg))
                            cv2.putText(img, str_attitude, (0, 200), font, 2, (0, 255, 0), 3, cv2.LINE_AA)#changed frame to img


                            #-- Now get Position and attitude f the camera respect to the marker
                            pos_camera = -R_tc*np.matrix(tvec).T

                            camera_pos = [element * 10 for element in pos_camera]

                            cam_posx = np.asarray(camera_pos[0]).flatten()
                            #avg x pos for cam
                            camxList.append(cam_posx[0])              
                            if count > window_size:
                                camxSum = sum(camxList[count-window_size:count])
                                camxavg = camxSum/window_size
                            else:
                                camxSum = camxSum + cam_posx[0]
                                camxavg = camxSum/count
                            #logging.info(camxavg)
                  
                            cam_posy = np.asarray(camera_pos[1]).flatten()
                            #avg y pos for cam
                            camyList.append(cam_posy[0])              
                            if count > window_size:
                                camySum = sum(camyList[count-window_size:count])
                                camyavg = camySum/window_size
                            else:
                                camySum = camySum + cam_posy[0]
                                camyavg = camySum/count
                            
                            #avg z pos for cam
                            cam_posz = np.asarray(camera_pos[2]).flatten()
                            camzList.append(cam_posz[0])              
                            if count > window_size:
                                camzSum = sum(camzList[count-window_size:count])
                                camzavg = camzSum/window_size
                            else:
                                camzSum = camzSum + cam_posz[0]
                                camzavg = camzSum/count

                            
                            str_position = "CAMERA Position [mm] x=%2.3f  y=%2.3f  z=%2.3f"%(camxavg, camyavg, camzavg)
                            cv2.putText(img, str_position, (0, 300), font, 2, (0, 255, 0), 3, cv2.LINE_AA)#changed frame to img

                            #-- Get the attitude of the camera respect to the frame
                            try:
                                roll_camera, pitch_camera, yaw_camera = self.rotationMatrixToEulerAngles(R_flip*R_tc)
                            except: 
                                logging.error("error with rotationMatrixToEulerAngle again")
                            #avg rx pos for cam
                            camrxList.append(roll_camera)              
                            if count > window_size:
                                camrxSum = sum(camrxList[count-window_size:count-1])
                                camrxavg = camrxSum/window_size
                            else:
                                camrxSum = camrxSum + roll_camera
                                camrxavg = camrxSum/count

                            #avg ry pos for cam
                            camryList.append(pitch_camera)              
                            if count > window_size:
                                camrySum = sum(camryList[count-window_size:count-1])
                                camryavg = camrySum/window_size
                            else:
                                camrySum = camrySum + pitch_camera
                                camryavg = camrySum/count

                            #avg rz pos for cam
                            camrzList.append(yaw_camera)              
                            if count > window_size:
                                camrzSum = sum(camrzList[count-window_size:count-1])
                                camrzavg = camrzSum/window_size
                            else:
                                camrzSum = camrzSum + yaw_camera
                                camrzavg = camrzSum/count


                            str_attitude = "CAMERA Attitude [degrees] r=%2.3f  p=%2.3f  y=%2.3f"%(math.degrees(roll_camera),math.degrees(pitch_camera),
                                                math.degrees(yaw_camera))
                            cv2.putText(img, str_attitude, (0, 400), font, 2, (0, 255, 0), 3, cv2.LINE_AA)#changed frame to img
                            

                        except:
                            logging.error("Error with measurement.")


                        #--- Display the frame
                    scale_percent = 20 # percent of original size
                    width = int(img.shape[1] * scale_percent / 100)
                    height = int(img.shape[0] * scale_percent / 100)
                    dim = (width, height)
                    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
                    cv2.imshow('press q to quit', resized)

        
                    #--- use 'q' to quit
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        cv2.imwrite('expo.jpg',img)
                        self.markerid = reading_id
                        
                        if bool70 == True:
                            self.x = id70[0]
                            self.y = id70[1]
                            self.z = id70[2]
                            
                        if bool71 == True:
                            self.x = id71[0]
                            self.y = id71[1]
                            self.z = id71[2]

                        if bool72 == True:
                            self.x = id72[0]
                            self.y = id72[1]
                            self.z = id72[2]

                        if bool73 == True:
                            self.x = id73[0]
                            self.y = id73[1]
                            self.z = id73[2]

                        if bool74 == True:
                            self.x = id74[0]
                            self.y = id74[1]
                            self.z = id74[2]
                            

                        if bool75 == True:
                            self.x = id75[0]
                            self.y = id75[1]
                            self.z = id75[2]

                        if bool76 == True:
                            self.x = id76[0]
                            self.y = id76[1]
                            self.z = id76[2]

                        if bool77 == True:
                            self.x = id77[0]
                            self.y = id77[1]
                            self.z = id77[2]

                        if bool78 == True:
                            self.x = id78[0]
                            self.y = id78[1]
                            self.z = id78[2]

                        if bool79 == True:
                            self.x = id79[0]
                            self.y = id79[1]
                            self.z = id79[2]

                        if bool80 == True:
                            self.x = id80[0]
                            self.y = id80[1]
                            self.z = id80[2]
                            
                        cv2.destroyAllWindows()
                        break
