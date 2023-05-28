import cv2
import numpy as np
import os

marker_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
param_markers = cv2.aruco.DetectorParameters_create()
calib_ls = []

calibrated = False
eq = [0, 0, 0]

def aruco_position_detection():
    global calibrated
    global eq
    ready1 = False
    ready2 = False
    ready3 = False

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    marker_corners, marker_IDs, reject = cv2.aruco.detectMarkers(
        gray_frame, marker_dict, parameters = param_markers
    )

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_range = np.array([164, 144, 0])
    upper_range = np.array([179, 255, 255])

    if calibrated == False:
        if marker_IDs is not None:
            for ids, corners in zip(marker_IDs, marker_corners):
                cv2.polylines(
                    frame, [corners.astype(np.int32)], True, (0, 255, 255), 4, cv2.LINE_AA
                )
                x = (corners[0][0][0] + corners[0][1][0] + corners[0][2][0] + corners[0][3][0]) / 4
                y = (corners[0][0][1] + corners[0][1][1] + corners[0][2][1] + corners[0][3][1]) / 4
                cv2.circle(
                    frame, (x.astype(int),y.astype(int)), radius = 0, color = (0, 0, 255), thickness = 7
                )
                if ids[0] == 0:
                    z1 = y
                    ready1 = True
                elif ids[0] == 1:
                    z2 = y
                    ready2 = True
                elif ids[0] == 3:
                    z3 = y
                    ready3 = True
                but = cv2.waitKey(1)
                if (ready1 == True) and (ready2 == True) and (ready3 == True):
                    print("calibrated")
                    dist_ls = [50, 80, 110]
                    calib_ls.clear()
                    calib_ls.extend((z1, z2, z3))
                    calib_ls.sort(reverse=True)
                    eq = np.polyfit(calib_ls, dist_ls, 2)
                    calibrated = True
                else:
                    print(" ")
        corners = corners.reshape(4, 2)
        corners = corners.astype(int)
        top_right = corners[0].ravel()
        cv2.putText(frame, f"id: {ids[0]}", top_right, cv2.FONT_HERSHEY_PLAIN, 1.3, (0, 255, 0), 2, cv2.LINE_AA )

    if calibrated == True:
        mask = cv2.inRange(hsv, lower_range, upper_range)
        kernel = np.ones((10, 10), np.uint8)
        eroded = cv2.erode(mask, kernel)
        dilated = cv2.dilate(eroded, kernel)

        cnts = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        if len(cnts):
            c = max(cnts, key=cv2.contourArea)
            bottom = tuple(c[c[:, :, 1].argmax()][0])
            z = bottom[1]
            y = bottom[0]
            dist = z**2*eq[0] + z*eq[1] + eq[2] + 3
            cv2.putText(frame, f"distance: {round(dist, 4)}", (0, 50), cv2.FONT_HERSHEY_PLAIN, 1.3, (0, 255, 0), 1, cv2.LINE_AA )
            if y > 335:
                cv2.putText(frame, f"move to the right", (0, 80), cv2.FONT_HERSHEY_PLAIN, 1.3, (0, 255, 0), 1, cv2.LINE_AA )
                position_str = "right"
#                 fifo = open(PIPE_NAME, 'wb')
#                 dist_cm = int(dist)
#                 dist_mm = int((dist - dist_cm) * 10)
#                 fifo.write(bytes([1]+[dist_cm]+[dist_mm]))
#                 fifo.close()
            elif y < 325:
                cv2.putText(frame, f"move to the left", (0, 80), cv2.FONT_HERSHEY_PLAIN, 1.3, (0, 255, 0), 1, cv2.LINE_AA )
                position_str = "left"
#                 fifo = open(PIPE_NAME, 'wb')
#                 dist_cm = int(dist)
#                 dist_mm = int((dist - dist_cm) * 10)
#                 fifo.write(bytes([1]+[dist_cm]+[dist_mm]))                
#                 fifo.close()
            else:
                cv2.putText(frame, f"don't move", (0, 80), cv2.FONT_HERSHEY_PLAIN, 1.3, (0, 255, 0), 1, cv2.LINE_AA )
                position_str = "center"
#                 fifo = open(PIPE_NAME, 'wb')
#                 dist_cm = int(dist)
#                 dist_mm = int((dist - dist_cm) * 10)
#                 fifo.write(bytes([1]+[dist_cm]+[dist_mm]))
#                 fifo.close()
            output_str = f"{dist} {position_str}"
            print(output_str)

        
    cv2.imshow("frame", frame)


cap = cv2.VideoCapture(0)

while True:
    
    ret, frame = cap.read()
    ret, dilated = cap.read()
    if not ret:
        break
    aruco_position_detection()

    key = cv2.waitKey(1)
    if key == ord("q"):
        break
    
cap.release()
cv2.destroyAllWindows()