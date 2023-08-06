from main.api.schemas.response.SportsGameResponseSchema import SportsGameResponseSchema
from main.domain.sports_game.SportsGame import SportsGame


class SportsGameResponse:

    def __init__(self, all_sports_game: list[SportsGame], sports_game_response_schema: SportsGameResponseSchema):
        self.sports_game_response_schema = sports_game_response_schema
        self.add_sports_game(all_sports_game)

    def add_sports_game(self, all_sports_game: list[SportsGame]):
        for sport_game in all_sports_game:
            try:
                sport_key_attribute = getattr(self, sport_game.sport)
            except AttributeError:
                setattr(self, sport_game.sport, [])
                sport_key_attribute = getattr(self, sport_game.sport)



            if len(sport_key_attribute) <= 10:
                sport_key_attribute.append(
                    self.sports_game_response_schema.dump(sport_game))

    def get_games(self):
        return self.__str__()

    def __str__(self):
        return {k: val for k, val in self.__dict__.items() if not str(hex(id(val))) in str(val) and k != "sports_game_response_schema"}
