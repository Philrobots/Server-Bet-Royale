from main.service.UserConfirmationService import UserConfirmationService
from flask_restful import Resource
from flask import request

class EmailConfirmationResource(Resource):
    
    def __init__(self, user_confirmation_service: UserConfirmationService):
        self.user_confirmation_service = user_confirmation_service
                            
    def get(self):
        token = request.args.get("token", "")
        return self.user_confirmation_service.confirm_email(token)
    
    def post(self):
        try:
            email = request.json.get("email", "")
            self.user_confirmation_service.send_confirmation_email(email)
            return "Email sent", 200
        except Exception as e:
            return str(e), 400
    
    