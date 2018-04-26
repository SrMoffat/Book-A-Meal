import os


class Config(object):
    """
    The parent configuration class
    """
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    


class DevelopmentConfig(Config):
    """
    Configurations for development 
    """
    DEBUG = True


class TestingConfig(Config):
    """
    Configurations for Testing, with a separte database
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/bam_db'
    DEBUG = True


class StagingConfig(Config):
    """Configurations for staging
    """
    DEBUG = True


class ProductionConfig(Config):
    """Configurations for production
    """
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig
}
