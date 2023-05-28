import threading
import subprocess

class OpenCVThread(threading.Thread):
    def run(self):
        # Run the OpenCV program and capture its stdout
        opencv_process = subprocess.Popen(["python3", "vision_app.py"], stdout=subprocess.PIPE)

        # Continuously read the output from the OpenCV program
        while True:
            output_str = opencv_process.stdout.readline().decode()
            if not output_str:
                # End the loop if there is no more output
                print("probleem")
                break
            try:
                # Split the output string into distance and position parts
                distance_str, position_str = output_str.strip().split(" ")
                # Parse the distance and position values
                distance = float(distance_str)
                position = position_str
                # Do something with the distance and position values
                print("Distance: " + str(distance))
            except ValueError:
                # Do something with the distance and position values
                print("read probleem")

class WebserverThread(threading.Thread):
    webserver_process = subprocess.Popen(["python3", "webserver.py"], stdout=subprocess.PIPE)

    while True:
        output = webserver_process.stdout.readline().decode()
        if not output: break
        try:
            command_str, value_str = output.strip().split(" ")
            value = int(value_str)
            print("command: " + command_str + " value: " + str(value))
        except ValueError:
            print("read probleem")

# Create and start the OpenCV thread
# opencv_thread = OpenCVThread()
# opencv_thread.start()

webserver_thread = WebserverThread()
webserver_thread.start()

# The rest of your program can continue running in the main thread

print("started")