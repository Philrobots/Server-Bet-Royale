import logging
from main.domain.sports_game.SportsGameFactory import SportsGameFactory
from main.infra.db.repository.SportsGameRepository import SportsGameRepository
from main.infra.external_api.odds_api.OddsApiEngine import OddsApiEngine
from main.service.BetService import BetService
from main.service.SportsGameService import SportsGameService
from datetime import datetime
from main.service.BetterStatsService import BetterStatsService
import pytz


class SportsGameScheduler:

    def __init__(self, odds_api_engine: OddsApiEngine, sports_game_factory: SportsGameFactory, sports_game_repo: SportsGameRepository, sports_game_service: SportsGameService, bet_service: BetService, better_stats_service: BetterStatsService) -> None:
        self.odds_api_engine = odds_api_engine
        self.sports_game_factory = sports_game_factory
        self.sports_game_repo = sports_game_repo
        self.sports_game_service = sports_game_service
        self.bet_service = bet_service
        self.better_stats_service = better_stats_service

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

        live_hockey_games =  [] #self.odds_api_engine.get_hockey_games_with_scores_and_odds() NO NHL GAMES !!!

        for live_hockey_game in live_hockey_games:
            sport_game = self.sports_game_factory.create(live_hockey_game)
            self.sports_game_repo.insert_or_update_sports_game(
                sports_game=sport_game)

        live_basketball_games = [] #self.odds_api_engine.get_nba_games_with_scores_and_odds() NO NBA GAMES !!!

        for live_basketball_game in live_basketball_games:
            sport_game = self.sports_game_factory.create(live_basketball_game)
            self.sports_game_repo.insert_or_update_sports_game(
                sports_game=sport_game)

        live_mlb_games = self.odds_api_engine.get_mlb_games_with_scores_and_odds()

        for live_mlb_game in live_mlb_games:
            sport_game = self.sports_game_factory.create(live_mlb_game)
            self.sports_game_repo.insert_or_update_sports_game(
                sports_game=sport_game)

        live_mma_games = self.odds_api_engine.get_mma_games_with_scores_and_odds()
        for live_mma_game in live_mma_games:
            sport_game = self.sports_game_factory.create(live_mma_game)
            self.sports_game_repo.insert_or_update_sports_game(
                sports_game=sport_game)

        live_mls_games = self.odds_api_engine.get_mls_games_with_scores_and_odds()
        for live_mls_game in live_mls_games:
            sport_game = self.sports_game_factory.create(live_mls_game)
            self.sports_game_repo.insert_or_update_sports_game(
                sports_game=sport_game)

        logging.info("New live games added to database")
