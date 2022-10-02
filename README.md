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
```
***How might we harness AI to help teachers determine the level of engagement of students in online learning?***
```

## Solution
What is the AI-based solution we are offering?
```
A computer vision based system that tracks students level of engagement in real-time during an online class session.
```

## Technology of Our Solution
What is the underlying technology behind our solution?
>   **Method:**
>   * [OpenCV](https://opencv.org/) with [dlib](https://pypi.org/project/dlib/) in Python
>   * Detect face using "HOG-based" face detector from [dlib](https://pypi.org/project/dlib/)
>   * Predict Facial Landmarks using [dlib](https://pypi.org/project/dlib/) and obtain Facial Landmarks index for both eyes using module `face_utils`
>   * Live video streamming through USB/webcam/Raspberry Pi camera using module `VideoStream` in library [imutils](https://pypi.org/project/imutils/)
>
>   **Note:** Due to shortage of dataset 
>
>   **Calculate the average Eye Aspect Ratio (EAR) of each student:**
>   <sub> Sets a threshold of `60%` of *average EAR* to signify closed eyes </sub>
>   $$EAR = \frac{\|p_2-p_6\| + \|p_3-p_5\|}{2\|p_1-p_4\|}$$


## How It Woks
How does our solution work?
>   * Based on Eye Aspect Ratio measurement and face detection 
>       <sub> The student is categorised as engaged or disengaged based on their eye movements </sub>
>       >   `Disengaged` => when the student’s face is undetected OR their eyes are closed/ partially closed for a fixed period of time
>
>   * **Student:** Key in relevent info via `Welcome to aSES` page, the system can be run on the students devices during online classes. 
>       <sub> *(The videos are not being recorded, only data such as `Engagement of student` in binary form will be saved into database) </sub>
>
>   * **Teachers:** Receive information regarding student engagement via `Automated Student Engagement System (aSES)` , where they get feedback on the amount of time students spent disengaged and the engagement level over time in the form of a graph.


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
