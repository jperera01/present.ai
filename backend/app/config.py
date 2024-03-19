from decouple import config


class DevConfig:
    SECRET_KEY = config('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = config('SQLALCHEMY_TRACK_MODIFICATIONS',
                                            cast=bool)
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost/presentai_test1"
    SQLALCHEMY_ECHO = True
    DEBUG = True
