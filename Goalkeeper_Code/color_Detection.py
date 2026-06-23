from cvzone.ColorModule import ColorFinder
import cv2
import cvzone

#Creates an instance of the ColorFinder class with trackBar set True
myColorFinder = ColorFinder(trackBar=True)

#Initialize the video capture using OpenCV
#Using the 3rd cam (index 2). Adjust index if you have multiple cameras
cap = cv2.VideoCapture(1)

#Set the dimensions of the camera feed to 640 x 480
cap.set(3, 640)
cap.set(4, 480)

#Custom color values for detecting ball color
# 'hmin', 'smin', 'vmin' are the min values for Hue, Sat, and Value
# 'hmax', 'smax', 'vmax' are the max values for Hue, Sat, and Value

hsvVals = {'hmin': 17, 'smin': 112, 'vmin': 44, 'hmax': 29, 'smax': 255, 'vmax': 255}

#Main loop to continuously get frames from the camera
while True:
    #Read the current frame from the camera
    sucess, img = cap.read()

    #Use the update method from the ColorFinder class to detect the color
    #It returns the masked color image and a binary mask
    imgOrange, mask = myColorFinder.update(img, hsvVals) 

    #Stack the original image, the masked color image, and the binary mask
    imgStack = cvzone.stackImages([img, imgOrange, mask],3,0.5)

    #show the stacked images
    cv2.imshow("imgStack", imgStack)

    #Waits for the user to press the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

