# Educational platform for distance learning

The application is used to distance learning. It is based on **Django 3**. 
There are three types of users: student, teacher and admin. This platform adapts the teaching to the learning style of the student. First, the student must register.
After that he can enroll in the chosen course, but if he doesn't have a specific style of teaching yet, he must complete a test that will determine his teaching style.
The teacher registers in the same way as the student, and then the admin gives him permissions to create and modify courses. 
The teacher can create course content adapted to different learning styles. The student will see the content that suits his teaching style. 
The teacher can create content such as: text, image, video, files. 
Another function of the teacher is creating tests with closed questions or questions with short answers for a group of students enrolled in a given course.
The tests are checked automatically by comparing the answers with the correct ones. The teacher can view the grades of his students.
Based on the test grades and weights assigned to them, the final grade for the course is calculated.

## How to run:
- instal virtualenv,
- run -> python3 -m venv env,
- activating a virtual environment -> source env/bin/activate,
- installing packages -> pip install -r requirements.txt,
- run -> python manage.py makemigrations,
- run -> python manage.py migrate,
- run -> python manage.py createsuperuser,
- run app -> python manage.py runserver.


