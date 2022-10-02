# import the necessary packages
from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
import argparse
import imutils
import time
import dlib
import cv2
import streamlit as st
import requests

global name, course, group, module, duration


def main():
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--shape-predictor", required=True,
        help="path to facial landmark predictor")
    ap.add_argument("-v", "--video", type=str, default="",
        help="path to input video file")
    args = vars(ap.parse_args())

    fps = getFPS()                      # get the frames per second of the video device
    EYE_AR_THRESH = 1                   # threshold for which the eye aspect ratio is counted as disengaged
    EYE_AR_CONSEC_FRAMES = 5 * fps      # number of consecutive frames before user is counted as disengaged

    # counter counts the number of consecutive frames not meeting EAR threshold
    # counter resets to 0 when current fram meets EAR threshold
    COUNTER = 0         
    TOTAL = 0                           # total number of frames counted as disengaged

    print("Intiating facial landmark predictor...")                 # for debug purpose
    detector = dlib.get_frontal_face_detector()                     # dlib's face detector (HOG-based)
    predictor = dlib.shape_predictor(args["shape_predictor"])       # facial landmark predictor

    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]   # facial landmark index for left eye
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]  # facial landmark index for right eye

    print("Initiating video stream thread...")
    vs = FileVideoStream(args["video"]).start()         # Start video stream thread
    fileStream = True
    vs = VideoStream(src=0).start()
    fileStream = False
    time.sleep(1.0)

    _sum = 0                            # sum variable for initial calibration for EAR threshold
    _counter = int(5 * fps)             # number of frames for calibration (5 seconds) 
    disengaged = False                  # initiate engagement state to be 'engaged'
    # LOOKDOWN_COUNTER counts the number of consecutive frames where eyes cannot be detected
    # resets to 0 when current fram meets EAR threshold
    LOOKDOWN_COUNTER = 0                
    start = 0                           # time since epoch for when calibration completes (and recording starts)
    # list of binary classification of engagement status
    # each entry in the list represents engagement status on 1 frame
    engaged_status = []   

    # iterate through all frames until video stops              
    while True:
        # if this is a file video stream, then we need to check if
        # there any more frames left in the buffer to process
        if fileStream and not vs.more():
            break

        # grab the frame from the threaded video file stream, resize
        # it, and convert it to grayscale
        frame = vs.read()
        frame = imutils.resize(frame, width=450)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rects = detector(gray, 0)       # detect faces in the grayscale frame
        
        if len(rects) != 0:
            LOOKDOWN_COUNTER = 0
            # determine the facial landmarks for the face region, then
            # convert the facial landmark (x, y)-coordinates to a NumPy array
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

            # run this section if calibration has not been done
            if EYE_AR_THRESH == 1:
                if _counter > 0:
                    _sum += ear
                    
                    _counter -= 1
                else:
                    # calibrated the user specific EAR threshold 
                    EYE_AR_THRESH = _sum / int(10 * fps) * 0.6
                    start = int(time.time())
            
            # only run this section once calibration completes
            if _counter == 0:       
                # compute the convex hull for the left and right eye, then
                # visualize each of the eyes
                leftEyeHull = cv2.convexHull(leftEye)
                rightEyeHull = cv2.convexHull(rightEye)
                cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
                cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
                
                # if more than the set threshold frames
                # classify as disengaged
                # check current frame whether user EAR meets the threshold
                if COUNTER >= EYE_AR_CONSEC_FRAMES:
                    disengaged = True
                    TOTAL += 1
                    
                    if ear >= EYE_AR_THRESH:
                        COUNTER = 0         # resets counter if meets EAR threshold
                    else:
                        COUNTER += 1        # incremets counter otherwise

                # if less than the set threshold frames
                # classify as still engaged
                # check if current frame meets EAR threshold
                elif COUNTER < EYE_AR_CONSEC_FRAMES:
                    disengaged = False
                    if ear < EYE_AR_THRESH:
                        COUNTER += 1         # increments counter if does not meet EAR threshold
                    else:
                        COUNTER = 0          # resets counter otherwise
               
                # classify current frame as engaged or disengaged
                if disengaged:
                    engaged_status.append(0)                            # 0 as disengaged
                    cv2.putText(frame, "Disengaged",(10, 30),           # visual output
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                else:
                    engaged_status.append(1)                            # 1 as engaged
                    cv2.putText(frame, "Engaged",(10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                # visual output for current frame EAR and total number of disengaged frames
                cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                cv2.putText(frame, "Total: {:.2f}".format(TOTAL/fps),(300, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        # execution will only run this when eyes are not detected
        elif EYE_AR_THRESH != 1:
            LOOKDOWN_COUNTER += 1           # increment counter by 1
            ear = 0                         # set EAR to 0
            
            # if more than set threshold number of frames
            if LOOKDOWN_COUNTER >= EYE_AR_CONSEC_FRAMES:
                disengaged = True           # set state to disengaged
                TOTAL += 1


            if disengaged:
                engaged_status.append(0)
                cv2.putText(frame, "Disengaged",(10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            else:
                engaged_status.append(1)
                cv2.putText(frame, "Engaged",(10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            cv2.putText(frame, "Total: {:.2f}".format(TOTAL/fps),(300, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        cv2.imshow("Frame", frame)      # show the frame
        cv2.waitKey(1) & 0xFF

        # check if time is up
        if int(time.time()) - start == duration * 60:
            # send a POST request to server to update data
            post(name, course, engaged_status, duration * 60, fps, module, group)
            break

    # cleaning up
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


def post(name, course, engaged_status, time, fps, module, group):
    json = {
        "name": name,
        "course": course,
        "module": module,
        "group": group,
        "engaged_status": engaged_status,
        "time": time,
        "fps": fps,
    }
    requests.post('http://127.0.0.1:8000/api/v1/engagement/upload', json=json)


def eye_aspect_ratio(eye):
	A = dist.euclidean(eye[1], eye[5])  # compute the euclidean distances between the two sets of
	B = dist.euclidean(eye[2], eye[4])  # vertical eye landmarks (x, y)-coordinates
	C = dist.euclidean(eye[0], eye[3])  # horizontal eye landmark (x, y)-coordinates
	
	ear = (A + B) / (2.0 * C)           # compute the eye aspect ratio
	return ear



html_string = """
<h1> Welcome to Engageder </h1>
"""
st.markdown(html_string, unsafe_allow_html=True)
name = st.text_input("Name: ")
course = st.text_input("Course: ")
group = st.text_input("Group: ")
module = st.text_input("Module: ")
duration = st.slider("Duration in minutes: ", 1, 120, 1)
submit = st.button("Submit")

if submit:
    main()
    
st.stop()