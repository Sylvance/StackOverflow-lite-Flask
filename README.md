# StackOverflow-lite
StackOverflow-lite is a platform where people can ask questions and provide answers.

## Heroku deployment
- Check it out [here](https://so-flask-retplus-api.herokuapp.com/)

## Required Features
- Users can create an account and log in.
- Users can post questions.
- Users can delete the questions they post.
- Users can post answers.
- Users can view the answers to questions.
- Users can accept an answer out of all the answers to his/her question as the preferred answer. 


## Optional Features
- Users can upvote or downvote an answer.
- Users can comment on an answer.
- Users can fetch all questions he/she has ever asked on the platform
- Users can search for questions on the platform
- Users can view questions with the most answers.

## API
### Installation
- Change directory to api
```cd api```
- Depending on your os open your virtual enviroment
- Run on your terminal
```pip install -r requirements.txt```

### Run the server
- Then run
```python api.py```
- In your browser go to 
```http://localhost:5000```

### Dependencies used
- In this project `Flask` and `Flask-restplus` have been used.

### Endpoints
#### Questions Endpoints

Method | Endpoint | Functionality
--- | --- | ---
POST | `/api/v1/questions` | Add a question
GET | `/api/v1/questions` | Lists all questions 
GET | `/api/v1/questions/question_id` | Retrieve a question 
PUT | `/api/v1/questions/question_id` | Edit a question of a logged in user
DELETE | `/api/v1/questions/question_id` | Delete a request of a logged in user
:smile:|:pray:|:heart:

#### Answers Endpoints

Method | Endpoint | Functionality
--- | --- | ---
POST | `/api/v1/questions/question_id/answers` | Add an answer
GET | `/api/v1/questions/question_id/answers` | Lists all answers 
GET | `/api/v1/questions/question_id/answers/answerID` | Retrieve an answers 
PUT | `/api/v1/questions/question_id/answer/answerID` | Edit an answer 
DELETE | `/api/v1/questions/question_id/answer/answerID` | Delete an answer
:smile:|:pray:|:heart:

## Credits
This challenge was part of the Bootcamp 31 NBO Andela cp. Learning Team.

## Author
Sylvance Mbaka.
