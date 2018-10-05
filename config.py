"""ENV configs module"""
import os


class Base:
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    USER = os.getenv('USER')
    PASSWORD = os.getenv('PASSWORD')
    HOST = os.getenv('localhost')


class Development(Base):
    """Development configurations."""
    DEBUG = True
    DATABASE = os.getenv('DEV_DATABASE')


class Testing(Base):
    """Configurations for Testing."""
    TESTING = True
    DEBUG = True
    DATABASE = os.getenv('TEST_DATABASE')


class Staging(Base):
    """Configurations for Staging."""
    DEBUG = True


class Production(Base):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False


APP_CONFIG = {
    'development': Development,
    'testing': Testing,
    'staging': Staging,
    'production': Production,
}
