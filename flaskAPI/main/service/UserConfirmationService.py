import logging
from flask import  redirect, render_template, url_for
from main.domain.identifiers.DomainId import DomainId
from main.infra.authentication.UserAuth import UserAuth
from main.service.UserService import UserService
from itsdangerous import URLSafeTimedSerializer
import bcrypt
from main import mail
from flask_mail import Message

class UserConfirmationService:

    def __init__(self, user_service: UserService, secret_key: str, client_domain: str):
        self.user_service = user_service
        self.secret_key = secret_key
        self.salt = bcrypt.gensalt()
        self.client_domain = client_domain
        self.mail = mail
    
    def confirm_email(self, token: str):
        email = self.confirm_token(token)
        
        if email is False:
            return "The confirmation link is invalid or has expired.", 404
        
        try: 
            user: UserAuth = self.user_service.get_by_email(email)
        except:
            return "The confirmation link is invalid or has expired.", 404
        
        if user.confirmed:
            return redirect("{}/authentication/sign-in?email={}".format(self.client_domain, email))
        
        user.confirm_user()
        self.user_service.update_user(user)
        
        return redirect("{}/authentication/sign-in?email={}".format(self.client_domain, email))
        
    def send_confirmation_email(self, email: str): 
        verification_token = self.get_verification_code(email)
        
        confirm_url = url_for('confirm_email', token=verification_token, _external=True)
        html = render_template('ConfirmEmail.html', confirm_url=confirm_url)
        
        message = Message(
            'Please Confirm your Email',
            recipients=[email],
            html=html,
            sender="betroyale1@gmail.com"
        )
        
        self.mail.send(message)
    
    def get_verification_code(self, email: str):
        serializer = URLSafeTimedSerializer(self.secret_key)
        return serializer.dumps(email, salt=self.salt)

    def confirm_token(self, token: str, expiration=3600):
        serializer = URLSafeTimedSerializer(self.secret_key)
        try:
            email = serializer.loads(
                token,
                salt=self.salt,
                max_age=expiration
            )
        except:
            return False
        return email
        
