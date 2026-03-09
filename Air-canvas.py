import cv2
import numpy as np
from collections import deque

# Trackbar callback
def nothing(x):
    pass

# Create HSV control window
cv2.namedWindow("Color Detectors")

cv2.createTrackbar("Upper Hue", "Color Detectors", 153, 180, nothing)
cv2.createTrackbar("Upper Saturation", "Color Detectors", 255, 255, nothing)
cv2.createTrackbar("Upper Value", "Color Detectors", 255, 255, nothing)

cv2.createTrackbar("Lower Hue", "Color Detectors", 64, 180, nothing)
cv2.createTrackbar("Lower Saturation", "Color Detectors", 72, 255, nothing)
cv2.createTrackbar("Lower Value", "Color Detectors", 49, 255, nothing)

# Store drawing points
bpoints = [deque(maxlen=1024)]
gpoints = [deque(maxlen=1024)]
rpoints = [deque(maxlen=1024)]
ypoints = [deque(maxlen=1024)]

blue_index = 0
green_index = 0
red_index = 0
yellow_index = 0

# Kernel for image processing
kernel = np.ones((5,5),np.uint8)

# Colors
colors = [(255,0,0),(0,255,0),(0,0,255),(0,255,255)]
colorIndex = 0

# Create white canvas
paintWindow = np.zeros((471,636,3)) + 255

paintWindow = cv2.rectangle(paintWindow,(40,1),(140,65),(0,0,0),2)
paintWindow = cv2.rectangle(paintWindow,(160,1),(255,65),colors[0],-1)
paintWindow = cv2.rectangle(paintWindow,(275,1),(370,65),colors[1],-1)
paintWindow = cv2.rectangle(paintWindow,(390,1),(485,65),colors[2],-1)
paintWindow = cv2.rectangle(paintWindow,(505,1),(600,65),colors[3],-1)

cv2.putText(paintWindow,"CLEAR",(49,33),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),2)
cv2.putText(paintWindow,"BLUE",(185,33),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2)
cv2.putText(paintWindow,"GREEN",(298,33),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2)
cv2.putText(paintWindow,"RED",(420,33),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2)
cv2.putText(paintWindow,"YELLOW",(520,33),cv2.FONT_HERSHEY_SIMPLEX,0.5,(150,150,150),2)

cv2.namedWindow("Paint")

# Camera (Mac compatible)
cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)

while True:

    ret, frame = cap.read()

    if not ret:
        print("Camera not detected")
        break

    frame = cv2.flip(frame,1)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Get HSV values
    u_hue = cv2.getTrackbarPos("Upper Hue","Color Detectors")
    u_sat = cv2.getTrackbarPos("Upper Saturation","Color Detectors")
    u_val = cv2.getTrackbarPos("Upper Value","Color Detectors")

    l_hue = cv2.getTrackbarPos("Lower Hue","Color Detectors")
    l_sat = cv2.getTrackbarPos("Lower Saturation","Color Detectors")
    l_val = cv2.getTrackbarPos("Lower Value","Color Detectors")

    Upper_hsv = np.array([u_hue,u_sat,u_val])
    Lower_hsv = np.array([l_hue,l_sat,l_val])

    # Draw buttons
    frame = cv2.rectangle(frame,(40,1),(140,65),(122,122,122),-1)
    frame = cv2.rectangle(frame,(160,1),(255,65),colors[0],-1)
    frame = cv2.rectangle(frame,(275,1),(370,65),colors[1],-1)
    frame = cv2.rectangle(frame,(390,1),(485,65),colors[2],-1)
    frame = cv2.rectangle(frame,(505,1),(600,65),colors[3],-1)

    cv2.putText(frame,"CLEAR",(49,33),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2)
    cv2.putText(frame,"BLUE",(185,33),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2)
    cv2.putText(frame,"GREEN",(298,33),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2)
    cv2.putText(frame,"RED",(420,33),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2)
    cv2.putText(frame,"YELLOW",(520,33),cv2.FONT_HERSHEY_SIMPLEX,0.5,(150,150,150),2)

    # Mask creation
    mask = cv2.inRange(hsv, Lower_hsv, Upper_hsv)

    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.dilate(mask, kernel, iterations=1)

    # Find contours
    cnts,_ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    center = None

    if len(cnts) > 0:

        cnt = sorted(cnts, key=cv2.contourArea, reverse=True)[0]

        ((x,y),radius) = cv2.minEnclosingCircle(cnt)

        # Ignore small noise
        if radius > 10:

            cv2.circle(frame,(int(x),int(y)),int(radius),(0,255,255),2)

            M = cv2.moments(cnt)

            if M["m00"] != 0:
                center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))

            if center:

                if center[1] <= 65:

                    if 40 <= center[0] <= 140:
                        bpoints=[deque(maxlen=512)]
                        gpoints=[deque(maxlen=512)]
                        rpoints=[deque(maxlen=512)]
                        ypoints=[deque(maxlen=512)]

                        blue_index=green_index=red_index=yellow_index=0

                        paintWindow[67:,:,:]=255

                    elif 160 <= center[0] <= 255:
                        colorIndex = 0

                    elif 275 <= center[0] <= 370:
                        colorIndex = 1

                    elif 390 <= center[0] <= 485:
                        colorIndex = 2

                    elif 505 <= center[0] <= 600:
                        colorIndex = 3

                else:

                    if colorIndex == 0:
                        bpoints[blue_index].appendleft(center)

                    elif colorIndex == 1:
                        gpoints[green_index].appendleft(center)

                    elif colorIndex == 2:
                        rpoints[red_index].appendleft(center)

                    elif colorIndex == 3:
                        ypoints[yellow_index].appendleft(center)

    else:

        bpoints.append(deque(maxlen=512))
        blue_index += 1

        gpoints.append(deque(maxlen=512))
        green_index += 1

        rpoints.append(deque(maxlen=512))
        red_index += 1

        ypoints.append(deque(maxlen=512))
        yellow_index += 1

    # Draw lines
    points = [bpoints,gpoints,rpoints,ypoints]

    for i in range(len(points)):
        for j in range(len(points[i])):
            for k in range(1,len(points[i][j])):

                if points[i][j][k-1] is None or points[i][j][k] is None:
                    continue

                cv2.line(frame, points[i][j][k-1], points[i][j][k], colors[i],2)
                cv2.line(paintWindow, points[i][j][k-1], points[i][j][k], colors[i],2)

    # Show windows
    cv2.imshow("Tracking",frame)
    cv2.imshow("Paint",paintWindow)
    cv2.imshow("Mask",mask)

    # Quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()