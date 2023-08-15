from datetime import datetime
from flask import request
from main import API, app
from main.api.resources.AcceptBetResource import AcceptBetResource
from main.api.resources.BaseballSportsGameResource import BaseballSportsGameResource
from main.api.resources.BasketballSportsGameResource import BasketballSportsGameResource
from main.api.resources.BetWithIdResource import BetWithIdResource
from main.api.resources.LeaderBordResource import LeaderboardResource
from main.api.resources.BetResource import BetResource
from main.api.resources.BetterFundsResource import BetterFundsResource
from main.api.resources.LoginResource import LoginResource
from main.api.resources.MMASportsGameResource import MMASportsGameResource
from main.api.resources.PingResource import PingResource
from main.api.resources.RegisterResource import RegisterResource
from main.api.resources.HockeySportsGameResource import HockeySportsGameResource
from main.api.resources.SportsKey import SportsKey
from main.api.resources.TransactionResource import TransactionResource
from main.api.resources.UserBetResource import UserBetResource
from main.api.resources.UserResource import UserResource
from main.api.resources.ChatResource import ChatResource
from main.api.resources.SportsGameResource import SportsGameResource
from main.api.resources.payment.CreatePurchaseRequestSchema import CreatePurchaseRequestSchema
from main.api.resources.payment.PaymentResource import PaymentResource
from main.api.resources.payment.PurchaseResponseSchema import PurchaseResponseSchema

from main.api.schemas.response.BetterStatsResponseSchema import BetterStatsResponseSchema
from main.domain.better_stats.BetterStatsFactory import BetterStatsFactory
from main.domain.purchase.PurchaseFactory import PurchaseFactory
from main.domain.transaction.TransactionInfoFactory import TransactionInfoFactory
from main.infra.db.repository.AppSettingRepository import AppSettingRepository
from main.infra.db.repository.PurchaseRepository import PurchaseRepository
from main.infra.schemas.mongo.MongoAppSettingSchema import MongoAppSettingSchema
from main.infra.schemas.mongo.MongoPurchaseSchema import MongoPurchaseSchema
from main.schedulers.BetScheduler import BetScheduler
from main.service.BetterFundsService import BetterFundsService
from main.domain.sports_game.bookmakers.BookMakersFactory import BookMakersFactory
from main.schedulers.SportsGameScheduler import SportsGameScheduler
from main.service.PaymentService import PaymentService
from main.service.PaypalService import PaypalService
from main.service.UserConfirmationService import UserConfirmationService
from pymongo import errors
from main.api.schemas.request.CreateBetRequestSchema import CreateBetRequestSchema
from main.api.schemas.response.BetResponseSchema import BetResponseSchema
from main.api.schemas.response.SportsGameResponseSchema import SportsGameResponseSchema
from main.domain.bet.BetAmountFactory import BetAmountFactory
from main.domain.bet.BetFactory import BetFactory
from main.domain.bet.BetterFactory import BetterFactory
from main.domain.date.DateTimeHelper import DateTimeHelper
from main.domain.sports_game.SportsGameFactory import SportsGameFactory
from main.infra.db.connector.MongoConnector import MongoConnector
from main.infra.db.repository.BetRepository import BetRepository
from main.infra.db.repository.BetterRepository import BetterRepository
from main.infra.db.repository.SportsGameRepository import SportsGameRepository
from main.infra.db.repository.UserAuthRepository import UserAuthRepository
from main.infra.external_api.odds_api.OddsApiEngine import OddsApiEngine
from main.infra.schemas.mongo.MongoBetSchema import MongoBetSchema
from main.infra.schemas.mongo.MongoBetterSchema import MongoBetterSchema
from main.infra.schemas.mongo.MongoSportsGameSchema import MongoSportsGameSchema
from main.infra.schemas.mongo.MongoUserAuthSchema import MongoUserAuthSchema
from main.infra.schemas.mongo.MongoTransactionSchema import MongoTransactionSchema
from main.infra.db.repository.TransactionRepository import TransactionRepository
from main.api.schemas.request.AddBetterFundsRequestSchema import AddBetterFundsRequestSchema
from main.domain.transaction.TransactionHandler import TransactionHandler

from main.infra.authentication.TokenDecoder import TokenDecoder
from main.service.BetService import BetService
from main.service.BetterStatsService import BetterStatsService
from main.service.SportsGameService import SportsGameService
from main.service.UserService import UserService
from main.infra.authentication.UserAuthFactory import UserAuthFactory
from main.api.schemas.request.AcceptBetRequestSchema import AcceptBetRequestSchema
from apscheduler.schedulers.background import BackgroundScheduler

import os
import logging


class Context:

    def __init__(self):
        logging.info(app.config)
        self.mongo_connector = MongoConnector()
        self.sports_key = SportsKey()
        self.create_purchase_request_schema = CreatePurchaseRequestSchema()
        self.purchase_schema = MongoPurchaseSchema()
        self.user_auth_schema = MongoUserAuthSchema(app.config["SECRET_KEY"])
        self.mongo_sports_game_schema = MongoSportsGameSchema()
        self.sports_game_response_schema = SportsGameResponseSchema()
        self.bet_request_schema = CreateBetRequestSchema()
        self.accept_bet_request_schema = AcceptBetRequestSchema()
        self.app_setting_schema = MongoAppSettingSchema()
        self.better_stats_response_schema = BetterStatsResponseSchema()
        self.chat_resource = ChatResource()
        self.purchase_response_schema = PurchaseResponseSchema()
        
        self.transaction_schema = MongoTransactionSchema()
        self.add_better_funds_schema = AddBetterFundsRequestSchema()
        
        self.sports_game_repo = SportsGameRepository(self.mongo_sports_game_schema, self.mongo_connector, self.sports_key)
        self.transaction_repo = TransactionRepository(transaction_schema=self.transaction_schema,
                                                      connector=self.mongo_connector)

        self.transaction_handler = TransactionHandler(self.transaction_repo)

        self.better_schema = MongoBetterSchema(self.transaction_handler)
        self.mongo_bet_schema = MongoBetSchema(self.sports_game_repo)

        self.user_repo = UserAuthRepository(self.user_auth_schema, self.mongo_connector)
        self.bet_response_schema = BetResponseSchema(self.user_repo)
        self.better_repo = BetterRepository(self.better_schema, self.mongo_connector)
        
        self.token_decoder = TokenDecoder(app.config["SECRET_KEY"])
        self.datetime_helper = DateTimeHelper()
        self.odds_api_engine = OddsApiEngine(app.config["ODDS_API_KEY"], self.sports_key)
        
        self.purchase_factory = PurchaseFactory()
        self.better_factory = BetterFactory(self.datetime_helper, self.transaction_handler)
        self.user_factory = UserAuthFactory(self.user_repo, app.config["SECRET_KEY"])
        self.book_makers_factory = BookMakersFactory()
        self.sports_game_factory = SportsGameFactory(self.datetime_helper, self.book_makers_factory)
        self.bet_amount_factory  = BetAmountFactory()
        self.bet_factory = BetFactory(self.bet_amount_factory)
        self.bet_repository = BetRepository(self.mongo_bet_schema, self.mongo_connector)
        self.transaction_info_factory = TransactionInfoFactory(self.bet_repository)
        self.better_stats_factory = BetterStatsFactory(self.transaction_info_factory)
        self.app_setting_repo = AppSettingRepository(self.app_setting_schema, self.mongo_connector)
        self.purchase_repository = PurchaseRepository(self.purchase_schema, self.mongo_connector)

        self.paypal_service = PaypalService(app.config["PAYPAL_API_URL"], app.config["PAYPAL_CLIENT_ID"], app.config["PAYPAL_SECRET"])
        self.user_service = UserService(self.user_repo, self.user_factory, self.better_repo, self.better_factory)
        self.user_confirmation_service = UserConfirmationService(user_service=self.user_service, secret_key=app.config["SECRET_KEY"], client_domain=app.config["CLIENT_DOMAIN"])
        self.sports_game_service = SportsGameService(self.sports_game_repo)
        self.bet_service = BetService(self.better_repo, self.sports_game_repo, self.bet_factory, self.bet_repository, self.bet_amount_factory)
        self.better_stats_service = BetterStatsService(self.transaction_repo, self.better_stats_factory)
        self.payment_service = PaymentService(purchase_repository=self.purchase_repository,
                                              better_repository=self.better_repo, 
                                              purchase_factory=self.purchase_factory, 
                                              paypalService=self.paypal_service)
        
        self.sports_game_scheduler = SportsGameScheduler(odds_api_engine=self.odds_api_engine, sports_game_factory=self.sports_game_factory,
                                                         sports_game_repo=self.sports_game_repo, sports_game_service=self.sports_game_service, bet_service=self.bet_service, better_stats_service=self.better_stats_service, sports_key=self.sports_key)
        self.bet_scheduler = BetScheduler(bet_service=self.bet_service, bet_repo=self.bet_repository, better_repo=self.better_repo)
        self.all_schedulers = [self.sports_game_scheduler, self.bet_scheduler]
        self.better_funds_service = BetterFundsService(self.better_repo)
        self.scheduler = BackgroundScheduler()

    def create_context_login_resource_class_kwargs(self):
        return {"user_service": self.user_service}
    
    def create_context_chat_resource_class_kwargs(self):
        return {}

    def create_context_register_resource_class_kwargs(self):
        return {"user_service": self.user_service, "user_confirmation_service": self.user_confirmation_service}
    
    def create_context_leaderboard_resource_class_kwargs(self):
        return {"user_service": self.user_service, "token_decoder": self.token_decoder}
    
    def create_context_user_resource_class_kwargs(self):
        return {"user_service": self.user_service, "token_decoder": self.token_decoder}

    def create_context_hockey_sports_game_resource_class_kwargs(self):
        return {"sports_game_service": self.sports_game_service, "sports_game_response_schema" : self.sports_game_response_schema}
    
    def create_context_sports_game_resource_class_kwargs(self):
        return {"sports_game_service": self.sports_game_service, "sports_game_response_schema" : self.sports_game_response_schema, "sports_key": self.sports_key}

    def create_context_payment_resource_class_krwargs(self):
        return { "payment_service": self.payment_service, "token_decoder": self.token_decoder,  "create_purchase_request_schema": self.create_purchase_request_schema, "purchase_response_schema": self.purchase_response_schema}

    def create_context_basketball_sports_game_resource_class_kwargs(self):
        return {"sports_game_service": self.sports_game_service, "sports_game_response_schema" : self.sports_game_response_schema}

    def create_context_baseball_sports_game_resource_class_kwargs(self):
        return {"sports_game_service": self.sports_game_service, "sports_game_response_schema" : self.sports_game_response_schema}

    def create_context_mma_sports_game_resource_class_kwargs(self):
        return {"sports_game_service": self.sports_game_service, "sports_game_response_schema" : self.sports_game_response_schema}

    def create_context_bet_resource_class_kwargs(self):
        return {"token_decoder": self.token_decoder, "bet_service" : self.bet_service, "create_bet_request_schema": self.bet_request_schema, "bet_response_schema": self.bet_response_schema}
    
    def create_context_user_bet_resource_class_kwargs(self):
        return {"token_decoder": self.token_decoder, "bet_service" : self.bet_service, "bet_response_schema": self.bet_response_schema}
    
    def create_context_accept_bet_resource_class_kwargs(self):
        return {"token_decoder": self.token_decoder, "bet_service" : self.bet_service, "bet_response_schema": self.bet_response_schema, "accept_bet_request_schema": self.accept_bet_request_schema}

    def create_context_better_funds_resource_class_kwargs(self):
        return {"token_decoder": self.token_decoder, "better_funds_service" : self.better_funds_service, "add_better_funds_request_schema": self.add_better_funds_schema}

    def create_context_transaction_resource_class_kwargs(self):
        return {"token_decoder": self.token_decoder, "better_stats_service": self.better_stats_service, "better_stats_response_schema": self.better_stats_response_schema}
        
    def create_context_bet_with_id_resource_class_kwargs(self):
        return {"token_decoder": self.token_decoder, "bet_service" : self.bet_service}
            

    def initialize_jobs(self):
        try:
            self.mongo_connector.server_info()
            for app_setting in self.app_setting_repo.get_jobs():
                for scheduler in self.all_schedulers:
                    setting_class_name, setting_method_name = app_setting.value.split(".")
                    class_name = scheduler.__class__.__name__
                    method_names = [method for method in dir(scheduler.__class__) if method.startswith('__') is False]

                    if setting_class_name == class_name and setting_method_name in method_names:
                        logging.warning("Adding job: %s", app_setting.value)
                        self.scheduler.add_job(getattr(scheduler, setting_method_name), next_run_time=datetime.now(), **app_setting.kwargs)
            self.scheduler.start()
        except errors.ServerSelectionTimeoutError:
            logging.warning("Mongodb is not running!")





logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

context = Context()
context.initialize_jobs()

API.add_resource(PingResource, "/ping")
API.add_resource(LoginResource, "/login", resource_class_kwargs=context.create_context_login_resource_class_kwargs())
API.add_resource(RegisterResource, "/register", resource_class_kwargs=context.create_context_register_resource_class_kwargs())
API.add_resource(HockeySportsGameResource, "/sports-game/hockey", resource_class_kwargs=context.create_context_hockey_sports_game_resource_class_kwargs())
API.add_resource(BasketballSportsGameResource, "/sports-game/basketball", resource_class_kwargs=context.create_context_basketball_sports_game_resource_class_kwargs())
API.add_resource(BaseballSportsGameResource, "/sports-game/baseball", resource_class_kwargs=context.create_context_baseball_sports_game_resource_class_kwargs())
API.add_resource(MMASportsGameResource, "/sports-game/mma", resource_class_kwargs=context.create_context_mma_sports_game_resource_class_kwargs())
API.add_resource(BetResource, "/bet", resource_class_kwargs=context.create_context_bet_resource_class_kwargs())
API.add_resource(BetWithIdResource, "/bet/<string:id>", resource_class_kwargs=context.create_context_bet_with_id_resource_class_kwargs())
API.add_resource(BetterFundsResource, "/better-funds", resource_class_kwargs=context.create_context_better_funds_resource_class_kwargs())
API.add_resource(AcceptBetResource, "/accept-bet", resource_class_kwargs=context.create_context_accept_bet_resource_class_kwargs())
API.add_resource(UserResource, "/user", resource_class_kwargs=context.create_context_user_resource_class_kwargs())
API.add_resource(UserBetResource, "/user/bet", resource_class_kwargs=context.create_context_user_bet_resource_class_kwargs())
API.add_resource(TransactionResource, "/transactions", resource_class_kwargs=context.create_context_transaction_resource_class_kwargs())
API.add_resource(LeaderboardResource, "/leaderboard", resource_class_kwargs=context.create_context_leaderboard_resource_class_kwargs())
API.add_resource(ChatResource, "/chat", resource_class_kwargs=context.create_context_chat_resource_class_kwargs())
API.add_resource(SportsGameResource, "/sports", resource_class_kwargs=context.create_context_sports_game_resource_class_kwargs())
API.add_resource(PaymentResource, "/payment", resource_class_kwargs=context.create_context_payment_resource_class_krwargs())

if __name__ == "__main__":    
    
    @app.route("/send_confirmation/<email>", methods = ['POST'])
    def send_confirmation_email(email: str):
        try:
            context.user_confirmation_service.send_confirmation_email(email)
            return "Email sent", 200
        except Exception as e:
            return str(e), 400
            
    @app.route("/confirm_email/<token>", methods = ['GET'])
    def confirm_email(token: str):
        return context.user_confirmation_service.confirm_email(token)
    
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)), threaded=True)
    
    
