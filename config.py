import os


class Base(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')


class Development(Base):
    """Development configurations."""
    DEBUG = True


class Testing(Base):
    """Configurations for Testing."""
    TESTING = True
    DEBUG = True


class Staging(Base):
    """Configurations for Staging."""
    DEBUG = True


class Production(Base):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False


app_config = {
    'development': Development,
    'testing': Testing,
    'staging': Staging,
    'production': Production,
}
