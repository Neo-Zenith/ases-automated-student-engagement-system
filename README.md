# Automated Student Engagement System (aSES)

[COOL BANNER]

## Background
>   *"The Smart Nation is an initiative by the Government of Singapore to harness Infocomm technologies, networks and big data to create tech-enabled solutions."* In this Hackathon, we aim to develop AI models that help to solve industrial or social problems in the new stage of social development.
>
>   In line with the seven National AI Projects that address Key Challenges in Singapore, we decided to focus on the Education section. Our objective is to provide personalised education for students by enhancing the learning experience for both teachers and students.
>
>   A study showed that `64%` of students struggle to maintain **focus and discipline** over online learning.
>   Due to the Covid Pandemic, the trend of class settings shift to online mode aligning with the advancement of technology. While students trying to adapt to the new learning style, teachers are also struggling to track the level of engagement of all students.
>
>   If teachers knew how engaged and focused their students are in class, they can improve their teaching methods by:
>   * Adjusting their teaching pace
>   * Putting more emphasis on harder topics

## Problem Statement
What is the problem we are trying to solve?
<pre>
How might we harness AI to help teachers determine the level of engagement of students in online learning?
</pre>

## Solution
What is the AI-based solution we are offering?
<pre>
A Computer-Vision-based-system that tracks and generates report on students level of engagement 
in real-time during online class sessions.
</pre>
Comparing to the **traditional image processing method** which is *complex* and required certain combinations of models trainings, our solution using `Eye Aspect Ratio (EAR)` is much more *elegant,efficient and easy to implement* as it just requires simple calculation based on the ratio of distances between Facial Landmarks of eyes.


## Technology of Our Solution
What is the underlying technology behind our solution?
>   **(A) Method:**
>   * [OpenCV](https://opencv.org/) with [dlib](https://pypi.org/project/dlib/) in Python
>   * Detect face using "HOG-based" face detector from [dlib](https://pypi.org/project/dlib/)
>   * Predict Facial Landmarks using [dlib](https://pypi.org/project/dlib/) and obtain Facial Landmarks index for both eyes using module `face_utils`
>   * Live video streamming through USB/webcam/Raspberry Pi camera using module `VideoStream` in library [imutils](https://pypi.org/project/imutils/)
>
>   **Note:** Due to shortage of dataset and time, we use pre-trained model in [dlib](https://pypi.org/project/dlib/) and [imutils](https://pypi.org/project/imutils/) to detect face and predict Facial Landmarks.
>
>   **(B) Calculation of Eye Aspect Ratio (EAR):** <br>
>   * The 2D facial landmark locations of each eye is represented by 6 $(x,y)$-coordinates starting from the left-corner of eyes (from the perspective of 3rd party), and ploting it clockwise evenly for the remaining region.
>   * **The Eye Aspect Ratio (EAR) equation:**
>   $$EAR = \frac{\parallel{p_2-p_6}\parallel + \parallel{p_3-p_5}\parallel}{2\parallel{p_1-p_4}\parallel}$$
>       * **Numerator:** Distance between the vertical eye landmarks <br>
>         **Denominator:** Distance between the horizontal eye landmarks <br>
>           (tiwce the Denominator because there is only one set of horizontal points but two sets of vertical points)
>   * Eyes open:    $\text{EAR} \approx \text{constant}$ <br>
>     Eyes closed:  $\text{EAR} = 0$
>   * For the first 5 seconds, we calibrate the average of EAR of the student.
>   * Sets a threshold of `90%` of average EAR to signify closed eyes.


## How It Woks
How does our solution work?
>   **Student:** 
>   * Key in relevent info via [Welcome to aSES](https://github.com/Neo-Zenith/MLDA-Deep-Learning-Week/blob/main/client.ps1) page, the system will run on the students devices via USB/webcam/Raspberry Pi camera and track their engagements during online classes. <br>
>       <sub> ( ```diff - **Disclaimer:** ``` The videos are not being recorded, only data such as *"Engagement of student"* in binary form will be saved into database) </sub> <br>
>   * After class, the results will be uploaded to cloud database.
>   
>   **Based on Eye Aspect Ratio measurement and face detection:** <br>
>   * Every *second*, the student is categorised as engaged (recorded as binary $1$) or disengaged (recorded as binary $0$) based on their eye movements </sub>
>       >   `Disengaged` => When the student’s face is undetected OR their eyes are closed/ partially closed for a fixed period of time. (ie. 2 seconds)
>
>   **Teachers:** Receive information regarding student engagement via `Automated Student Engagement System (aSES)` , where they get feedback on the amount of time students spent disengaged and the engagement level over time in the form of a graph.


## Challenges
What are the challenges we faced when developing the solution?
>   * Cloud-based database is not free for this Hackathon. =)

## Accomplishments
What are our accomplishments from building our solution?

## Future Ahead
What are the future plans for our solution?
>   * Eye detection algorithm can be improved for greater accuracy
>   * Presentation of live statistic to teachers when class ongoing, and use AI for recommendation on how teachers should react 
>   * Dependencies can be built into a client program for easier installation
>   * Solution can be expanded to include facial recognition with multiple users in the field of vision
>       - Applicable to in-person learning in lecture theatres/ classrooms

## Authors
Who are the authors?

## Acknowledgements
Credits

## Reference
Below are some links that we have used as references throughout the project:
* https://iblnews.org/a-survey-shows-that-many-college-students-struggle-to-maintain-focus-and-discipline-in-distance-learning/
* https://pyimagesearch.com/2017/04/24/eye-blink-detection-opencv-python-dlib/
* 
