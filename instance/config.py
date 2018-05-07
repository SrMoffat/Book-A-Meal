"""
--- The Configuration File for the App ---
            Author: Ngige Gitau 
            For:    Book-A-Meal API        
"""
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
    Configurations for the development environment 
    """
    DEBUG = True


class TestingConfig(Config):
    """
    Configurations for Testing, with a separte database
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:rootuser@localhost:5432/4bam_db'
    'postgresql://localhost/4bam_db'
    DEBUG = True


class StagingConfig(Config):
    """Configurations for the staging environment 
    """
    DEBUG = True


class ProductionConfig(Config):
    """Configurations for the production environment 
    """
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig
}
