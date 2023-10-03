#!/usr/bin/env python3

from flask import Flask, make_response,jsonify,request
from flask_migrate import Migrate
from flask_restful import Api,Resource
from flask_jwt_extended import  create_access_token
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField
from wtforms.validators import DataRequired,Email,Length


from models import db, JobApplication,JobListing,User

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact =False

migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=4,max=80)])
    email = StringField('Email', validators=[DataRequired(),Email(),Length(max=120)])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=3)])
    
class UserRegistrationResource(Resource):
    def post(self):
        data=request.get_json()
        form = RegistrationForm(data=data)
        
        if form.validate():
            username = form.username.data
            email=form.email.data
            password = form.password.data

            if User.query.filter_by(username=username).first is not None:
                return {'message':'Email already exists'},400
            
            new_user = User(username=username,email=email,password=password)
            db.session.add(new_user)
            db.session.commit()
            access_token = create_access_token(indentity=new_user.id)

            return {
                'message':"user registered succesfully",
                'access_token': access_token
            },201
        else:
            return {'message':'validation errors','errors':form.errors},400

api.add_resource(UserRegistrationResource,'/register')

class UserLogInResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return{'message':'username and password required'},400
        
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            access_token= create_access_token(indentity=user.id)
            return {'access token':access_token},200
        else:
            return {'message':'Invalid credentials'},401
        
api.add_resource(UserLogInResource,'/log in')
    
class JobListResource(Resource):
    def get(self):
        joblists = [{'id':job.id,'title':job.title,'description':job.description,'location':job.location,'company_name':job.company_name,'datetime':job.posted_at}  for job in JobListing.query.all()]
        response = make_response(jsonify(joblists),200)
        return response

    def post(self):
        data = request.get_json()
        new_job = JobListing(title=data['title'],description=data['description'],location=data['location'],company_name=data['company_name'],posted_at=data['posted_at'])
        db.session.add(new_job)
        db.session.commit()
        response = make_response(new_job.to_dict(),201)
        return response


api.add_resource(JobListResource,'/Available jobs')

class JobListByIdResource(Resource):
    def get(self,id):
        job = JobListing.query.filter_by(JobListing.id == id).first()
        if not job:
            job_dict={'error':'job not found'}
            response = make_response(jsonify(job_dict),404)
            return response
        response = make_response(jsonify(job),200)
        return response
    
api.add_resource(JobListByIdResource,'/Search Job/<int:id>')

class JobApplicationResource(Resource):
    def get(self):
        job_applications = [{'id': app.id, 'job_id': app.job_id, 'applicant_name': app.applicant_name} for app in JobApplication.query.all()]
        response = make_response(jsonify(job_applications), 200)
        return response

    def post(self):
        data = request.get_json()
        job_id = data.get('job_id')
        applicant_name = data.get('applicant_name')

        if not job_id or not applicant_name:
            return {'message': 'job_id and applicant_name are required'}, 400

        job = JobListing.query.get(job_id)
        if not job:
            return {'message': 'Job not found'}, 404

        new_application = JobApplication(job_id=job_id, applicant_name=applicant_name)
        db.session.add(new_application)
        db.session.commit()

        response = make_response(new_application.to_dict(), 201)
        return response

api.add_resource(JobApplicationResource, '/job-applications')


class JobApplicationByIdResource(Resource):
    def get(self, id):
        application = JobApplication.query.get(id)
        if not application:
            return {'error': 'Job application not found'}, 404
        response = make_response(jsonify(application.to_dict()), 200)
        return response

    def delete(self, id):
        application = JobApplication.query.get(id)
        if not application:
            return {'error': 'Job application not found'}, 404
        db.session.delete(application)
        db.session.commit()
        return {'message': 'Job application deleted'}, 200

    def patch(self, id):
        application = JobApplication.query.get(id)
        if not application:
            return {'error': 'Job application not found'}, 404

        data = request.get_json()
        if 'applicant_name' in data:
            application.applicant_name = data['applicant_name']

        db.session.commit()
        response = make_response(application.to_dict(), 200)
        return response

api.add_resource(JobApplicationByIdResource, '/job-application/<int:id>')

    
