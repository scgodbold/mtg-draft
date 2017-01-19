import secret

DEBUG = secret.DEBUG
SECRET_KEY = secret.SECRET_KEY

# SQL settings
SQLALCHEMY_DATABASE_URI = secret.SQLALCHEMY_DATABASE_URI

# Use for random name generation
ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
            'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
            'w', 'x', 'y', 'z'
            ]
