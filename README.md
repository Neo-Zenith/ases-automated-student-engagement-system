# Automated Student Engagement System (aSES)
![ases-banner](https://user-images.githubusercontent.com/77436548/193458047-a42b20fd-16f5-45e3-8d0c-4aa80e502cd8.gif)

## 🗺️ Background
> *"The Smart Nation is an initiative by the Government of Singapore to harness Infocomm technologies, networks and big data to create tech-enabled solutions."* 
 
In this Hackathon, we aim to develop AI models that help to solve industrial or social problems in the new stage of social development.

In line with the seven National AI Projects that address Key Challenges in Singapore, we decided to focus on the Education section. Our objective is to provide personalised education for students by enhancing the learning experience for both teachers and students.

A study showed that `64%` of students struggle to maintain **focus and discipline** over online learning.
Due to the Covid Pandemic, the trend of class settings shift to online mode aligning with the advancement of technology. While students trying to adapt to the new learning style, teachers are also struggling to track the level of engagement of all students.

If teachers knew how engaged and focused their students are in class, they can improve their teaching methods by:
* Adjusting their teaching pace
* Putting more emphasis on harder topics

## ❓ Problem Statement
<pre>
How might we harness AI to help teachers determine the level of engagement of students in online learning?
</pre>

## 💡 Solution
What is the AI-based solution we are offering?
<pre>
A computer-vision based system that tracks students level of engagement in real-time during an online class session.
</pre>
Comparing to **traditional image processing method** which is *complex* and required certqain combination of models training, our solution using `Eye Aspect Ratio (EAR)` which is more more *elegant, efficient* and *easy* to implement* as it just requires simple calculation based on the ratio of distances between Facial Landmarks of eyes.

## ⚡ Technology of Our Solution
<img src="https://img.shields.io/badge/streamlit-bd4043?style=for-the-badge&logo=streamlit&logoColor=white" /> <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" /> <img src="https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white" /> <img src="https://img.shields.io/badge/dlib-399639?style=for-the-badge&logo=dlib" /> <img src="https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white" /> <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" /> 

#### (A) Method:
* [OpenCV](https://opencv.org/) with [dlib](https://pypi.org/project/dlib/) as our main machine learning libraries.
* Detect face using "HOG-based" face detector from [dlib](https://pypi.org/project/dlib/)
* Predict Facial Landmarks using [dlib](https://pypi.org/project/dlib/) and obtain Facial Landmarks index for both eyes using module `face_utils`
* Live video streamming through USB/webcam/Raspberry Pi camera using module `VideoStream` in library [imutils](https://pypi.org/project/imutils/)

**Note:** As our project requires datasets of people's images (which are mostly inaccessible to protect privacy), we resort to using pre-trained model in [dlib](https://pypi.org/project/dlib/) and [imutils](https://pypi.org/project/imutils/) to detect face and predict Facial Landmarks.

#### (B) Calculation of Eye Aspect Ratio (EAR):
* The 2D facial landmark locations of each eye is represented by 6 $(x,y)$-coordinates starting from the left-corner of eyes (from the perspective of 3rd party), and ploting it clockwise evenly for the remaining region.

> **The Eye Aspect Ratio (EAR) equation:**
> $$EAR = \frac{\parallel{p_2-p_6}\parallel + \parallel{p_3-p_5}\parallel}{2||p_1-p_4||}$$
> * **Numerator:** Distance between the vertical eye landmarks
> * **Denominator:** Distance between the horizontal eye landmarks
(tiwce the Denominator because there is only one set of horizontal points but two sets of vertical points)

* Eyes open:  $\text{EAR} \approx \text{constant}$ <br>
Eyes closed: $\text{EAR} = 0$
* For the first 5 seconds, we calibrate the average of EAR of the student.
* Sets a threshold of **90%** of average EAR to signify closed eyes.

#### (C) API:
* Storing and querying of student's engagement level is done using API built under [Django's REST framework](https://www.django-rest-framework.org)
* Data is stored on an SQLite database.

#### (D) Interface:
* Student-side interface is built using `streamlit`.
* Professor-side interface is built using Django's template engine.

## 👨‍🎓 How It Woks for Students
Key in relevent info via `Welcome to aSES` page, the system can be run on the students devices via USB/webcame/Raspberry Pi camera and track their engagements during online classes.
![image](https://user-images.githubusercontent.com/77436548/193457711-940e7038-0d65-4e12-aff4-63327be6cf06.png)
* The videos are not being recorded, only data such as `Engagement of student` in binary form will be saved into database
* After class, the results will be uploaded to cloud database.
    
* Based on Eye Aspect Ratio measurement and face detection 
    * The student is categorised as engaged or disengaged every second based on their eye movements
    ![image](https://user-images.githubusercontent.com/77436548/193460332-eca38717-5c85-4b14-a692-ca8125a2e34d.png)

    * `Disengaged` —— when the student’s face is undetected OR their eyes are closed/ partially closed for a fixed period of time (2 seconds).
    ![image](https://user-images.githubusercontent.com/77436548/193460299-2d887644-c463-4606-b676-c9ec7506021a.png)

## 👨‍🏫 How It Woks for Professor
Receive information regarding student engagement via `Automated Student Engagement System (aSES)` , where they get feedback on the amount of time students spent disengaged and the engagement level over time by querying their names, course, module, group.
* Category:
    * Individual student (by querying the student's matriculation number)
    * The entire class (by leaving matriculation number section blank)
        
![image](https://user-images.githubusercontent.com/77436548/193457776-23ec4986-d287-4a6d-9f6f-f019a73536b7.png) ![image](https://user-images.githubusercontent.com/77436548/193457791-ed37115d-c3af-4c38-88a2-ff7eb0e5edcd.png)


## 🚫 Challenges
* Cloud-based database is not free for this Hackathon.
* Public datasets specific to our project's aim is not accessible due to privacy concerns.

## 🥇 Accomplishments
* Successfully developed a computer-vision based AI model under 72 hours using [OpenCV](https://opencv.org/) and [dlib](https://pypi.org/project/dlib/).
* Successfully developed a simple fullstack application for our system using Django and JavaScript.

## 🔮 Future Ahead
* Eye detection algorithm can be improved for greater accuracy
* Presentation of live statistic to teachers when class ongoing, and use AI for recommendation on how teachers should react 
* Dependencies can be built into a client program for easier installation
* Solution can be expanded to include facial recognition with multiple users in the field of vision
     - Applicable to in-person learning in lecture theatres/ classrooms

## 🖊️ Authors
* Lee Juin [@Neo-Zenith](https://github.com/Neo-Zenith)
* Daniel Tan Teck Wee [@DanielTanTWOfficial](https://github.com/DanielTanTWOfficial)
* Ng Woon Yee [@woonyee28](https://github.com/woonyee28)
* Lee Ci Hui [@perfectsquare123](https://github.com/DanielTanTWOfficial)
* Weng Pei He [@wph12](https://github.com/wph12)
* Bernice Koh Jun Yan [@bernicekjy](https://github.com/bernicekjy)

## ⭐ Acknowledgements
* This project uses Django which is licensed under [BSD-3 license](https://github.com/django/django/blob/main/LICENSE) for all backend programming logic and frontend template rendering. 
* This project uses Charts.js which is licensed under [MIT license](https://github.com/chartjs/Chart.js/blob/master/LICENSE.md) for the visual display of charts on frontend.
* This project uses OpenCV which is licensed under [Apache 2 license](https://github.com/opencv/opencv/blob/4.x/LICENSE) for the machine learning logic.

## 📖 Reference
Below are some links that we have used as references throughout the project:
* https://iblnews.org/a-survey-shows-that-many-college-students-struggle-to-maintain-focus-and-discipline-in-distance-learning/
* https://pyimagesearch.com/2017/04/24/eye-blink-detection-opencv-python-dlib/

<hr />

## 💥 How to Use

1.   Begin by cloning this repository to your working directory:
```
git clone https://github.com/Neo-Zenith/MLDA-Deep-Learning-Week.git
```

2.   Run `setup.bat`. This will install Python virtual environment and all the dependcies required.
     * Note that installation of `dlib` will take some time. It is normal that your CPU and/or RAM usage will spike to 100% during this period.

3.   Run `server.bat` to initialize the server.

4.   Run `client.bat` to initialize the client application.
