import serial
import threading
from imutils.video import VideoStream
import face_recognition
import imutils
import pickle
import time
import os
import cv2
from mail import *
from headshots import *
from train_model import *

target_email = None
source_email = None
password = None

#File path which includes email credentials
file_path = "email_credentials.txt"
# Specify the serial port and baud rate (2000000) the Arduino is connected to
ser = serial.Serial('/dev/ttyACM0', 2000000)
#Determine faces from encodings.pickle file model created from train_model.py
encodingsP = "encodings.pickle"

def camera():
    camera_time = time.time()
    while time.time() - camera_time < 5:
        # grab the frame from the threaded video stream and resize it
        # to 500px (to speedup processing)
        frame = vs.read()
        frame = imutils.resize(frame, width=500)
        # Detect the fce boxes
        boxes = face_recognition.face_locations(frame)
        # compute the facial embeddings for each face bounding box
        encodings = face_recognition.face_encodings(frame, boxes)
        names = []

        # loop over the facial embeddings
        for encoding in encodings:
            # attempt to match each face in the input image to our known
            # encodings
            matches = face_recognition.compare_faces(data["encodings"],
                                                     encoding)
            name = "Unknown"  # if face is not recognized, then print Unknown

            # check to see if we have found a match
            if True in matches:
                # find the indexes of all matched faces then initialize a
                # dictionary to count the total number of times each face
                # was matched
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}

                # loop over the matched indexes and maintain a count for
                # each recognized face face
                for i in matchedIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1

                # determine the recognized face with the largest number
                # of votes (note: in the event of an unlikely tie Python
                # will select first entry in the dictionary)
                name = max(counts, key=counts.get)

                # If someone in your dataset is identified, print their name on the screen
                """
                if "Unknown" != name:
                    print(name)
                """

                # update the list of names
            names.append(name)
        count = names.count("Unknown")
        try:
            if float(count) / len(names) >= 0.3:
                cv2.imwrite("frame.jpg", frame)
                print("Picture saved")
                try:
                    mail(target_email, source_email, password)
                    print("Mail is sent.")
                except:
                    print("Mail could not be sent.")
        except ZeroDivisionError:
            pass
class SensorThread(threading.Thread):
    def __init__(self):
        super(SensorThread, self).__init__()
        self.sensor_thr_status = True
    
    def run(self):
        values = []
        val = 0
        start_time = time.time()

        while self.sensor_thr_status:
            #if there is any waiting data
            if ser.inWaiting() > 0:
                #Read data and clean unnecessary line break character
                data = ser.readline().decode().rstrip()
                try:
                    val = int(float(data))
                except:
                    pass

                if time.time() - start_time < 10:
                    if val > 5:
                        #print(val)
                        #Add values to list
                        values.append(val)
                else:
                    average = sum(values)# / (len(values) + 1)
                    print("average: ", average)
                    if average > 5000:
                        camera_thread = threading.Thread(target=camera)
                        camera_thread.start()
                        camera_thread.join()
                    else:
                        start_time = time.time()
                    values = []

    def get_sensor_thr_status(self):
        return self.sensor_thr_status

    def stop_app(self):
        self.sensor_thr_status = False
        vs.stop()

def read_email_credentials(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        if len(lines) >= 3:
            target_email = lines[0].strip()
            source_email = lines[1].strip()
            password = lines[2].strip()
            return target_email, source_email, password
        else:
            print("There is no enough lines in configuration.")
            return None, None, None
def register_person():
    Flag = True
    while Flag:
        name = input(
            "Enter name and press space to take picture. Min 10 Pictures is required. Press 'ESC' to exit\n").strip()

        if os.path.isdir(os.path.join("dataset", name)):
            os.system("rm -rf {}".format(os.path.join("dataset", name)))

        os.makedirs(os.path.join("dataset", name))
        headshot(name)
        answer = int(input("Do you want to add a more person? Press 1 if yes, Press 2 if no\n").strip())
        if 1 == answer:
            Flag = True
        else:
            Flag = False
            train_model()
            print("Please restart application.")

def first_registration():
    input("To add person to database, press any key...\n")
    register_person()

if __name__ == "__main__":
    #print("To add person to database, press any key...")
    #reg_thread = threading.Thread(target=first_registration)  #
    #reg_thread.start()
    #time.sleep(5)
    #reg_thread.join()
    # load the known faces and embeddings along with OpenCV's Haar
    # cascade for face detection
    print("[INFO] loading encodings + face detector...")
    try:
        data = pickle.loads(open(encodingsP, "rb").read())
        # src = 0 : for the build in single web cam, could be your laptop webcam
        # src = 2 : I had to set it to 2 inorder to use the USB webcam attached to my laptop
        print("Application starts")
        # initialize the video stream and allow the camera sensor to warm up
        vs = VideoStream(src=0, framerate=25).start()
        # vs = VideoStream(src=0).start()
        # vs = VideoStream(usePiCamera=True).start()
        time.sleep(2.0)

        # Read email credentials
        target_email, source_email, password = read_email_credentials(file_path)

        sensor_thread = SensorThread()
        # thread başlar
        sensor_thread.start()
        # Thread'in tamamlanmasını bekle
        sensor_thread.join()
    except FileNotFoundError:
        print("Nobody is found in database. Please add yourself to database.")
        register_person()
