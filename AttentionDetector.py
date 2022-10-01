# import the necessary packages
from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2
import requests

def eye_aspect_ratio(eye):
	# compute the euclidean distances between the two sets of
	# vertical eye landmarks (x, y)-coordinates
	A = dist.euclidean(eye[1], eye[5])
	B = dist.euclidean(eye[2], eye[4])
	# compute the euclidean distance between the horizontal
	# eye landmark (x, y)-coordinates
	C = dist.euclidean(eye[0], eye[3])
	# compute the eye aspect ratio
	ear = (A + B) / (2.0 * C)
	# return the eye aspect ratio
	return ear

global name, email, course, gender

def main():
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    course = input("Enter your course: ")
    gender = input("Enter your gender (0 for Male, 1 for Female): ")

    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--shape-predictor", required=True,
        help="path to facial landmark predictor")
    ap.add_argument("-v", "--video", type=str, default="",
        help="path to input video file")
    args = vars(ap.parse_args())

    fps = getFPS()

    # define two constants, one for the eye aspect ratio to indicate
    # blink and then a second constant for the number of consecutive
    # frames the eye must be below the threshold
    EYE_AR_THRESH = 1
    EYE_AR_CONSEC_FRAMES = 5 * fps
    # initialize the frame counters and the total number of blinks
    COUNTER = 0
    TOTAL = 0
    # initialize dlib's face detector (HOG-based) and then create
    # the facial landmark predictor
    print("[INFO] loading facial landmark predictor...")
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(args["shape_predictor"])
    # grab the indexes of the facial landmarks for the left and
    # right eye, respectively
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
    # start the video stream thread
    print("[INFO] starting video stream thread...")
    vs = FileVideoStream(args["video"]).start()
    fileStream = True
    vs = VideoStream(src=0).start()
    # vs = VideoStream(usePiCamera=True).start()
    fileStream = False
    time.sleep(1.0)

    # loop over frames from the video stream
    # variable for engagement

    _sum = 0
    _counter = int(5 * fps)
    disengaged = False
    LOOKDOWN_COUNTER = 0
    start = 0
    end = 0
    engaged_status = []
    while True:
        # if this is a file video stream, then we need to check if
        # there any more frames left in the buffer to process
        if fileStream and not vs.more():
            break
        # grab the frame from the threaded video file stream, resize
        # it, and convert it to grayscale
        # channels)
        frame = vs.read()
        frame = imutils.resize(frame, width=450)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # detect faces in the grayscale frame
        rects = detector(gray, 0)
        
        # loop over the face detections

        # determine the facial landmarks for the face region, then
        # convert the facial landmark (x, y)-coordinates to a NumPy
        # array

        if len(rects) != 0:
            LOOKDOWN_COUNTER = 0
            shape = predictor(gray, rects[0])
            shape = face_utils.shape_to_np(shape)
            # extract the left and right eye coordinates, then use the
            # coordinates to compute the eye aspect ratio for both eyes
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)
            # average the eye aspect ratio together for both eyes
            ear = (leftEAR + rightEAR) / 2.0

            
            if EYE_AR_THRESH == 1:
                print(_counter)
                if _counter > 0:
                    _sum += ear
                    
                    _counter -= 1
                else:
                    EYE_AR_THRESH = _sum / int(10 * fps) * 0.6
                    start = time.time()
            
            if _counter == 0:       
                # compute the convex hull for the left and right eye, then
                # visualize each of the eyes
                leftEyeHull = cv2.convexHull(leftEye)
                rightEyeHull = cv2.convexHull(rightEye)
                cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
                cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
                # check to see if the eye aspect ratio is below the blink
                # threshold, and if so, increment the blink frame counter
                # print(ear, EYE_AR_THRESH)
                # otherwise, the eye aspect ratio is not below the blink
                # threshold

                # if the eyes were closed for a sufficient number of
                # then increment the total number of blinks
                if COUNTER >= EYE_AR_CONSEC_FRAMES:
                    disengaged = True
                    TOTAL += 1
                    
                    if ear >= EYE_AR_THRESH:
                        COUNTER = 0
                    else:
                        COUNTER += 1

                # reset the eye frame counter
                elif COUNTER < EYE_AR_CONSEC_FRAMES:
                    disengaged = False
                    if ear < EYE_AR_THRESH:
                        COUNTER += 1         
                    else:
                        COUNTER = 0
               
                    
                # draw the total number of blinks on the frame along with
                # the computed eye aspect ratio for the frame
                #cv2.putText(frame, "Blinks: {}".format(TOTAL), (10, 30),
                #    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                # print text if disengagement detected
                if(disengaged):
                    engaged_status.append(0)
                    cv2.putText(frame, "Disengaged",(10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                else:
                    engaged_status.append(1)
                    cv2.putText(frame, "Engaged",(10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                cv2.putText(frame, "Total: {}".format(TOTAL/fps),(10, 300),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        elif EYE_AR_THRESH != 1:
            # if the eyes were closed for a sufficient number of
            # then increment the total number of blinks
            ##TOTAL += 1
            LOOKDOWN_COUNTER += 1
            ear = 0
            
            #print(LOOKDOWN_COUNTER, EYE_AR_CONSEC_FRAMES)
            if LOOKDOWN_COUNTER >= EYE_AR_CONSEC_FRAMES:
                disengaged = True
                TOTAL += 1

            # draw the total number of blinks on the frame along with
            # the computed eye aspect ratio for the frame
            #cv2.putText(frame, "Blinks: {}".format(TOTAL), (10, 30),
            #    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            # print text if disengagement detected
            if(disengaged):
                engaged_status.append(0)
                cv2.putText(frame, "Disengaged",(10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            else:
                engaged_status.append(1)
                cv2.putText(frame, "Engaged",(10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(frame, "Total: {}".format(TOTAL/fps),(10, 300),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # show the frame
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
    
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            end = time.time()
            post(name, course, gender, email, engaged_status, end - start, fps)
            break

    # do a bit of cleanup
    cv2.destroyAllWindows()
    vs.stop()


def getFPS():
    video = cv2.VideoCapture(0)
    num_frames = 60
    start = time.time()
    
    for i in range(0, num_frames):
        rst, frame = video.read()

    end = time.time()
    seconds = end - start
    video.release()
    return float(num_frames / seconds)

def post(name, course, gender, email, engaged_status, time, fps):
    json = {
        "name": name,
        "course": course,
        "gender": int(gender),
        "engaged_status": engaged_status,
        "email": email,
        "time": time,
        "fps": fps,
    }
    r = requests.post('http://127.0.0.1:8000/api/engagement', json=json)

if __name__ == '__main__':
    main()