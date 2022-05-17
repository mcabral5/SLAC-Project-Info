from vimba import *
import cv2
import os

def print_welcome():
    print("Hello World. This is Mako")

def main(imgcount):
    path = r'C:\Users\PoThe\OneDrive\Desktop\VimbaPython_Source\Calibration Images'
    #imgcount #counter to notify how many images have been captured
    #for imgcount in range (0,5): #will iterate through range. Num of photos captured will be 5 as it iterated through (0, 1, 2, 3, 4). 
    with Vimba.get_instance() as vimba:#Vimba code
            cams = vimba.get_all_cameras()#get cam
            with cams[0] as cam:
                fmts = cam.get_pixel_formats()
                fmts = intersect_pixel_formats(fmts, OPENCV_PIXEL_FORMATS)
                cam.set_pixel_format(fmts[0])
                #fmts = intersect_pixel_formats(fmts, OPENCV_PIXEL_FORMATS)
                frame = cam.get_frame()#capture single frame
                #frame._frame.width = 600 #Set frame width
                #frame._frame.height = 900 #set frame height
                img = frame.as_opencv_image()
                
                #resize the image
                scale_percent = 20 # percent of original size
                width = int(img.shape[1] * scale_percent / 100)
                height = int(img.shape[0] * scale_percent / 100)
                dim = (width, height)
                resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
                
                cv2.imshow("frame",resized)#display frame as cv image
                frame.convert_pixel_format(PixelFormat.Mono8)#image conversion
                #imgcount=imgcount+1#counter to notify which num of photo we are on.
                cv2.waitKey(2000)#displays image for 10 seconds before destorying window
                cv2.destroyAllWindows()
                cv2.imwrite(os.path.join(path,"frame"+str(imgcount)+".jpg"), frame.as_opencv_image())#saves images in same path as code
                print("saved "+str(imgcount)+" image(s)")#indicator that picture has been saved
        
if __name__ == "__main__":
    print_welcome()
    main(imgcount)
    


    
