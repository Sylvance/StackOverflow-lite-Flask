from flask import Flask
from flask_restplus import Api, Resource, fields
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='Question API',
    description='A simple Question API',
)

ns = api.namespace('questions', description='QUESTION operations')

answer = api.model('Answer', {
    'id': fields.Integer(readOnly=True, description='The answer unique identifier'),
    'question_id': fields.Integer(readOnly=True, description='The question unique identifier'),
    'description': fields.String(required=True, description='The answer detail')
})

question = api.model('Question', {
    'id': fields.Integer(readOnly=True, description='The question unique identifier'),
    'title': fields.String(required=True, description='The title detail'),
    'description': fields.String(required=True, description='The question detail')
    # ,'answers': fields.List(fields.Nested(answer))
})

class QuestionDAO(object):
    def __init__(self):
        self.question_counter = 0
        self.questions = []

    def get(self, id):
        for question in self.questions:
            if question['id'] == id:
                return question
        api.abort(404, "question {} doesn't exist".format(id))

    def create(self, data):
        question = data
        question['id'] = self.question_counter = self.question_counter + 1
        self.questions.append(question)
        return question

    def update(self, id, data):
        question = self.get(id)
        question.update(data)
        return question

    def delete(self, id):
        question = self.get(id)
        self.questions.remove(question)

class AnswerDAO(object):
    def __init__(self, question_instance):
        self.question_instance = question_instance
        self.answer_counter = 0
        self.answers = []

    def retrive_answer_by_id(self, question_id, id):
        self.question_instance.get(question_id)
        for answer in self.answers:
            if answer['id'] == id:
                return answer
        api.abort(404, "answer {} doesn't exist".format(id))

    def retrive_answers_by_question_id(self, question_id):
        self.question_instance.get(question_id)
        result = []
        for answer in self.answers:
            if answer['question_id'] == question_id:
                result.append(answer)
        return result

    def create_answer(self, question_id, data):
        answer = data
        answer['id'] = self.answer_counter = self.answer_counter + 1
        answer['question_id'] = question_id
        self.answers.append(answer)
        return answer

    def update_answer(self, question_id, id, data):
        answer = self.retrive_answer_by_id(question_id, id)
        answer.update(data)
        return answer

    def delete_answer(self, question_id, id):
        question = self.question_instance.get(question_id)
        question.answers.remove(id)
        answer = self.retrive_answer_by_id(question_id, id)
        self.answers.remove(answer)


question_dao = QuestionDAO()
question_dao.create({'title': 'Build an API','description':'Write endpoints'})
question_dao.create({'title': 'Test the API','description':'Write Tests'})
question_dao.create({'title': 'Deploy the API','description':'Heroku deployment'})
answer_dao = AnswerDAO(question_dao)


@ns.route('/')
class QuestionList(Resource):
    '''Shows a list of all questions, and lets you POST to add new questions'''
    @ns.doc('list_questions')
    @ns.marshal_list_with(question)
    def get(self):
        '''List all questions'''
        return question_dao.questions

    @ns.doc('create_question')
    @ns.expect(question)
    @ns.marshal_with(question, code=201)
    def post(self):
        '''Create a new question'''
        return question_dao.create(api.payload), 201


@ns.route('/<int:question_id>')
@ns.response(404, 'question not found')
@ns.param('id', 'The title identifier')
class Question(Resource):
    '''Show a single question item and lets you delete them'''
    @ns.doc('get_question')
    @ns.marshal_with(question)
    def get(self, question_id):
        '''Fetch a given question'''
        return question_dao.get(question_id)

    @ns.doc('delete_question')
    @ns.response(204, 'question deleted')
    def delete(self, question_id):
        '''Delete a question given its identifier'''
        question_dao.delete(question_id)
        return '', 204

    @ns.expect(question)
    @ns.marshal_with(question)
    def put(self, question_id):
        '''Update a question given its identifier'''
        return question_dao.update(question_id, api.payload)

@ns.route('/<int:question_id>/answers')
class AnswersList(Resource):
    '''Shows a list of all answers, and lets you POST to add new answers'''
    @ns.doc('list_answers')
    @ns.marshal_list_with(answer)
    def get(self, question_id):
        '''List all answers for particular question'''
        return answer_dao.retrive_answers_by_question_id(question_id)

    @ns.doc('create_answer')
    @ns.expect(answer)
    @ns.marshal_with(answer, code=201)
    def post(self, question_id):
        '''Create a new answer'''
        return answer_dao.create_answer(question_id, api.payload), 201


@ns.route('/<int:question_id>/answers/<int:answer_id>')
@ns.response(404, 'answer not found')
@ns.param('question_id', 'The title identifier')
class Answer(Resource):
    '''Show a single answer item and lets you delete them'''
    @ns.doc('get_answer')
    @ns.marshal_with(answer)
    def get(self, question_id, answer_id):
        '''Fetch a given answer'''
        return answer_dao.retrive_answer_by_id(question_id, answer_id)

    @ns.doc('delete_answer')
    @ns.response(204, 'answer deleted')
    def delete(self, question_id, answer_id):
        '''Delete a answer given its identifier'''
        answer_dao.delete_answer(question_id, answer_id)
        return '', 204

    @ns.expect(answer)
    @ns.marshal_with(answer)
    def put(self, question_id, answer_id):
        '''Update a answer given its identifier'''
        return answer_dao.update_answer(question_id, answer_id, api.payload)
