import logging
from main.api.resources.SportsKey import SportsKey
from main.domain.sports_game.SportsGameFactory import SportsGameFactory
from main.infra.db.repository.SportsGameRepository import SportsGameRepository
from main.infra.external_api.odds_api.OddsApiEngine import OddsApiEngine
from main.service.BetService import BetService
from main.service.SportsGameService import SportsGameService
from datetime import datetime
from main.service.BetterStatsService import BetterStatsService
import pytz


class SportsGameScheduler:

    def __init__(self, odds_api_engine: OddsApiEngine, sports_game_factory: SportsGameFactory, sports_game_repo: SportsGameRepository, sports_game_service: SportsGameService, bet_service: BetService, better_stats_service: BetterStatsService, sports_key: SportsKey) -> None:
        self.odds_api_engine = odds_api_engine
        self.sports_game_factory = sports_game_factory
        self.sports_game_repo = sports_game_repo
        self.sports_game_service = sports_game_service
        self.bet_service = bet_service
        self.better_stats_service = better_stats_service
        self.sports_key = sports_key

    def is_in_range_to_not_get_new_game(self) -> bool:
        now = datetime.now(tz=pytz.timezone('US/Eastern'))
        current_time = now.strftime("%H:%M:%S")
        start = '01:00:00'
        end = '13:00:00'
        return current_time > start and current_time < end

    def remove_old_games_and_old_transactions(self) -> None:
        sports_games_remove = self.sports_game_service.remove_old_games()
        transactions_remove = self.better_stats_service.remove_old_transactions()

        logging.info(f"Removed {sports_games_remove} old sports games")
        logging.info(f"Removed {transactions_remove} old transactions")

    def get_new_live_games(self) -> None:
        if self.is_in_range_to_not_get_new_game():
            return

        active_sports = self.sports_key.get_active_sports()

        for active_sport in active_sports:
            logging.info(
                "New live game added to database with sport key: " + active_sport)
            live_sports_game = self.odds_api_engine.get_sports_game_with_odds_and_scores(
                sport_key=active_sport)
            for live_sport_game in live_sports_game:
                sport_game = self.sports_game_factory.create(live_sport_game)
                self.sports_game_repo.insert_or_update_sports_game(
                    sports_game=sport_game)

        logging.info("New live games added to database")
