import logging
from flask import jsonify, request, redirect, url_for, render_template
from main.domain.identifiers.DomainId import DomainId
from main.infra.authentication.UserAuth import UserAuth
from main.service.UserConfirmationService import UserConfirmationService
from main.service.UserService import UserService
from flask_restful import Resource
from itsdangerous import URLSafeTimedSerializer
import bcrypt
from main import app, mail
from flask_mail import Mail, Message

class RegisterResource(Resource):

    def __init__(self, user_service: UserService, user_confirmation_service: UserConfirmationService):
        self.user_service = user_service
        self.user_confirmation_service = user_confirmation_service

    def post(self):
        username = request.json.get("username", "")
        password = request.json.get("password", "")
        email = request.json.get("email", "")
        birth_date = request.json.get("birthdate", "")
        token = self.user_service.register(username, password, email, birth_date)
        
        self.user_confirmation_service.send_confirmation_email(email)
        
        response = jsonify({"token": token.to_string()})
        response.status_code = 201
        return response