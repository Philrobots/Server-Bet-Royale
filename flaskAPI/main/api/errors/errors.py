errors = {
    "FailedLoginException": {
        "message": "Invalid username or password",
        "status": 400
    },
    "InvalidUsernameFormatException": {
        "message": "Invalid username format",
        "status": 400
    },
    "InvalidPasswordFormatException": {
        "message": "Password must be length 8-16 with a capital letter a lowercase letter and a number",
        "status": 400
    },
    "InvalidEmailFormatException": {
        "message": "Email must be valid",
        "status": 400
    },
    "UsernameAlreadyTakenException": {
        "message": "Username is already taken",
        "status": 400
    },
    "EmailAlreadyTakenException": {
        "message": "Email is already taken",
        "status": 400
    },
    "InvalidBirthDateException": {
        "message": "You must be at least 18 years old to use this service",
        "status": 400
    },
    "SportsGameCompletedException": {
        "message": "You cannot bet on sports game that are finished",
        "status": 400
    },
    "InvalidDomainIdException": {
        "message": "The id format is not valid",
        "status": 400
    },
    "UserNotConfirmedException": {
        "message": "You must confirm your email before logging in",
        "status": 400
    }
}