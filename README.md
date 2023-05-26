# Ubet

Online betting platform

Port 8000

Post /login
```
{
    "username": string,
    "password": string
}
```

Post /register
```
{
    "username": string,
    "email": valid email,
    "password": string
}
```

Get /sports-game

````
[{
    "team_home": "Vancouver Canucks",
    "score": null,
    "game_end": null,
    "game_start": "2023-01-25T03:00:00+00:00",
    "completed": false,
    "id": "63cee53cfa32148ac2be7123",
    "team_away": "Chicago Blackhawks",
    "league": "NHL",
    "sport": "icehockey"
}]
```


Post /bet

```
{
    "sports_game_id": "63cee53cfa32148ac2be7115",
    "is_home_bet": true,
    "bet_amount": 100,
    "odds": 10

}
```

Get /bet

