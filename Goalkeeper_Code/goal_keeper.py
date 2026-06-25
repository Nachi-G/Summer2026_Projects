import cv2
import cvzone
from cvzone.ColorModule import ColorFinder
import time
from cvzone.Utils import findContours
import serial

pico = serial.Serial("COM9", 115200, timeout=1)
time.sleep(2)

#Creates an instance of the ColorFinder class with trackBar set True
myColorFinder = ColorFinder(trackBar= False)

#Initialize the video capture using OpenCV, using 1st cam (index 1) - adjust index if you have multiple cameras
cap = cv2.VideoCapture(0)

#Set the dimensions of the camera feed to 640 x 480
cap.set(3, 640)
cap.set(4, 480)


#Custom color values for detecting ball color
# 'hmin', 'smin', 'vmin' are the min values for Hue, Sat, and Value
# 'hmax', 'smax', 'vmax' are the max values for Hue, Sat, and Value
hsvVals = {'hmin': 14, 'smin': 100, 'vmin': 21, 'hmax': 61, 'smax': 230, 'vmax': 255}

#List to store tracking points: Each element will be a tuple: ((cx,cy), timestamp)
track_points = []

# Decision line position as a percentage of the image height.
# 0.0 is the top of the camera view, 1.0 is the bottom.
decision_line_ratio = 0.7
decision_hold_seconds = 2.0
last_decision = None
last_decision_time = 0

#Main loop to continuously get frames from the camera
while True:
    #Read the current frame from the camera
    sucess, img = cap.read()
    if not sucess:
        break

    #Use the update method from the ColorFinder class to detect the color
    #It returns the masked color image and a binary mask
    imgOrange, mask = myColorFinder.update(img, hsvVals)

    imgContours, conFound = findContours(img, mask, minArea=1000, sort=True,
                                             filter=None, drawCon=True, c=(255, 0, 0), ct=(255, 0, 255),
                                             retrType=cv2.RETR_EXTERNAL, approxType=cv2.CHAIN_APPROX_NONE)
    #img = where to display results, mask = img we are feeding from our HSV values

    current_time = time.time()

    decision_line_y = int(img.shape[0] * decision_line_ratio)

    #1. Track the ball if a contour is found
    if conFound:
        #Get the center of the largest/only contour
        cx, cy = conFound[0]["center"]

        if track_points and current_time - last_decision_time > decision_hold_seconds:
            previous_x, previous_y = track_points[-1][0]
            crossed_decision_line = (
                previous_y < decision_line_y <= cy
                or previous_y > decision_line_y >= cy
            )

            if crossed_decision_line:
                if cx > previous_x:
                    last_decision = "RIGHT"
                    print(0)   #180 degrees on servo
                    pico.write(b"0\n")
                    pico.flush()

                else:
                    last_decision = "LEFT"
                    print(1)  #0 degrees on servo
                    pico.write(b"1\n")
                    pico.flush()

                last_decision_time = current_time

        #append the center coordinates and current timestamp
        track_points.append(((cx, cy), current_time))

    #2. Remove points older than 3 seconds
    track_points = [ point for point in track_points if current_time - point[1] <= 3.0]

    #3. Draw the tracking line on the contour image
    if len(track_points) > 1:
        for i in range (1, len(track_points)):
            pt1 = track_points[i - 1][0]
            pt2 = track_points[i][0]
            #Draw a thick green tracking line
            cv2.line(imgContours, pt1, pt2, (0, 255, 0), 3)

    cv2.line(imgContours, (0, decision_line_y), (img.shape[1], decision_line_y), (255, 255, 0), 2)

    if last_decision and current_time - last_decision_time <= decision_hold_seconds:
        cv2.putText(
            imgContours,
            last_decision,
            (30, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.5,
            (0, 255, 255),
            3,
        )

    #Stack the original image, the masked color image, and the binary mask
    #imgStack = cvzone.stackImages([img, imgOrange, mask, imgContours], 2, 0.5)

    #show the stacked images
    cv2.imshow("imgStack", imgContours)

    #Waits for the user to press the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()



