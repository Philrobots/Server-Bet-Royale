from main.domain.identifiers.DomainId import DomainId
from main.infra.authentication.UserAuth import UserAuth
from main.infra.db.repository.BetterRepository import BetterRepository
from main.domain.bet.BetterFactory import BetterFactory
from main.infra.authentication.Token import Token
from main.infra.authentication.UserAuthFactory import UserAuthFactory
from main.infra.db.repository.UserAuthRepository import UserAuthRepository
from main.infra.exception.FailedLoginException import FailedLoginException
from main.infra.exception.NonExistingEmailException import NonExistingEmailException
from main.infra.exception.NonExistingUserException import NonExistingUserException


class UserService:

    def __init__(self, user_repo: UserAuthRepository, user_auth_factory: UserAuthFactory, better_repo: BetterRepository,
                 better_factory: BetterFactory):
        self.user_repo = user_repo
        self.user_auth_factory = user_auth_factory
        self.better_repo = better_repo
        self.better_factory = better_factory

    def login(self, username, password) -> Token:
        try:
            user = self.user_repo.get_by_username(username)
        except NonExistingUserException:
            try:
                user = self.user_repo.get_by_email(username)
            except NonExistingEmailException:
                raise FailedLoginException

        if user.authenticate(password):
            return user.create_auth_token()
        raise FailedLoginException

    def register(self, username, password, email, birth_date) -> Token:
        user = self.user_auth_factory.create(username, password, email)
        better = self.better_factory.create(user.user_id, birth_date)

        self.user_repo.add_user(user)
        self.better_repo.add_better(better)

        return user.create_auth_token()

    
    def get_by_id(self, user_id: DomainId) -> UserAuth:
        return self.user_repo.get_by_id(user_id)

    
    def get_leaders(self) -> list[UserAuth]:
        leaders_better = self.better_repo.get_leaders()
        
        users = []
        for better in leaders_better:
            user_auth = self.user_repo.get_by_id(better.user_id)
            users.append({
                "username": user_auth.username,
                "bank_balance": better.bank_balance.amount,
            })
            
        return users