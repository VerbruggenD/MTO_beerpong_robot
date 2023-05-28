import threading
import subprocess
import time
import os
import queue
import cv2
import numpy as np

# Global variables
# global auto_update
# global distUpdate
# global posUpdate

# auto_update = False
# distUpdate = True
# posUpdate = True

# Queue to communicate between threads
command_queue = queue.Queue()
vision_queue = queue.Queue()

# FIFO for serial communication
fifo_path = "my_pipe"

# Create the FIFO if it doesn't exist
if not os.path.exists(fifo_path):
    os.mkfifo(fifo_path)

# Function to handle commands
def process_command(command, value):
    if command == "left":
        # Move left
        #print(command, value)

        command = 'l'  # Example command
        data = f"{command},{value}".encode()  # Convert data to bytes

        sendFifo(data)

        return False

    elif command == "right":
        # move right
        #print(command, value)

        command = 'r'  # Example command
        data = f"{command},{value}".encode()  # Convert data to bytes

        sendFifo(data)

        return False

    elif command == "dist":
        # set distance
        #print(command, value)
        return False

    elif command == "shoot":
        # shoot
        #print(command, value)

        command = 's'  # Example command
        value = 0    # Example value
        data = f"{command},{value}".encode()  # Convert data to bytes

        sendFifo(data)

        return True

    elif command == "auto":
        # shoot
        #print(command, value)
        return True

    else:
        print("Invalid command")


print("started")

def sendFifo(data):
    # Open the FIFO for writing
    fifo = open(fifo_path, 'wb')

    time.sleep(0.001)
    
    # Write data to the FIFO
    fifo.write(data)
    fifo.flush()
    # print("done!")

    time.sleep(0.001)
    
    # Close the FIFO
    fifo.close()

def updateDist(distNow, distPast, distUpdate):
    if distNow == distPast:
        if distUpdate:
            # calculate parameter (angle and retraction)
            # send parameters
            distUpdate = False
    else: distUpdate = True

    return distUpdate

def updatePos(posNow, posPast, posUpdate):
    # if posNow == posPast:
    #     if posUpdate:
    #         # send position
    #         command = 'c'
    #         value = posNow
    #         data = f"{command},{value}".encode()  # Convert data to bytes
    #         sendFifo(data)
    #         posUpdate = False
    if (posNow - posPast < 5) and (posNow - posPast > -5):
        if posUpdate:
            # send position
            command = 'c'
            value = posNow
            data = f"{command},{value}".encode()  # Convert data to bytes
            sendFifo(data)
            posUpdate = False
    else: posUpdate = True
    return posUpdate

# Function to handle user input
def handle_input():
    while True:
        user_input = input("Enter a command and a value: ")
        command_queue.put(user_input)

# Function to handle program logic
def program_logic():
    distNow = 0
    distPast = 0
    posNow = 0
    posPast = 0

    auto_update = False
    distUpdate = True
    posUpdate = True

    while True:
        # Check if there are any commands in the queue
        if not command_queue.empty():
            command = command_queue.get()
            # Split the command and value
            parts = command.split()
            if len(parts) >= 2:
                cmd = parts[0]
                value = int(parts[1])
                # Process the command and value as needed
                auto_update = process_command(cmd, value)
            elif len(parts) == 1:
                cmd = parts[0]
                auto_update = process_command(cmd, 0)
            else:
                print('Invalid command format.')
        
        ####### Main code here #########

        if not vision_queue.empty():
            distPast = distNow
            posPast = posNow
            queue_data = vision_queue.get()

            if isinstance(queue_data, tuple) and len(queue_data) == 2:
                distNow, posNow = queue_data

                if auto_update:
                    distUpdate = updateDist(distNow, distPast, distUpdate)
                    posUpdate = updatePos(posNow, posPast, posUpdate)
            #else:
                # Handle the case when the queue data is not in the expected format
                #print("Error: Invalid queue data format")
        #else:
            # Handle the case when the queue is empty
            #print("Error: vision_queue is empty")

        # if auto_update:     # code for auto mode
        #     distUpdate = updateDist(distNow, distPast, distUpdate)
        #     posUpdate = updatePos(posNow, posPast, posUpdate)

        time.sleep(0.1)

        ################################

def vision_app():

    marker_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
    param_markers = cv2.aruco.DetectorParameters_create()
    calib_ls = []

    calibrated = False
    eq = [0, 0, 0]

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        ret, dilated = cap.read()
        if not ret:
            break
        
        ###

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
            corners = corners.reshape(4, 2)
            corners = corners.astype(int)
            top_right = corners[0].ravel()

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
                vision_queue.put((dist, y))


        ###

        key = cv2.waitKey(1)
        if key == ord("q"):
            break
        time.sleep(0.1)

    cap.release()
    cv2.destroyAllWindows()
    

# Create and start the threads
input_thread = threading.Thread(target=handle_input)
logic_thread = threading.Thread(target=program_logic)
vision_thread = threading.Thread(target=vision_app)

input_thread.start()
logic_thread.start()
vision_thread.start()

# Wait for both threads to finish
input_thread.join()
logic_thread.join()
vision_thread.join()