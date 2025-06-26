package server

import os

DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
L_OPTION = os.environ.get('L_OPTION', 'False').lower() == 'true'
D_OPTION = os.environ.get('D_OPTION', 'False').lower() == 'true'

DEFAULT_FCONFIGURE_OPTIONS = {
    'channel1': {
        'option1': 'value1',
        'option2': 'value2'
    },
    'channel2': {
        'option3': 'value3',
        'option4': 'value4'
    }
}

def validate_config_options():
    if not isinstance(DEBUG, bool):
        raise TypeError("DEBUG must be a boolean")
    if not isinstance(L_OPTION, bool):
        raise TypeError("L_OPTION must be a boolean")
    if not isinstance(D_OPTION, bool):
        raise TypeError("D_OPTION must be a boolean")
    if not isinstance(DEFAULT_FCONFIGURE_OPTIONS, dict):
        raise TypeError("DEFAULT_FCONFIGURE_OPTIONS must be a dictionary")

def get_config_option(option):
    try:
        return os.environ.get(option)
    except Exception as e:
        print(f"Error getting environment variable {option}: {str(e)}")
        return None

def set_config_option(option, value):
    try:
        os.environ[option] = value
    except Exception as e:
        print(f"Error setting environment variable {option}: {str(e)}")

def get_default_fconfigure_options():
    return DEFAULT_FCONFIGURE_OPTIONS

def set_default_fconfigure_options(options):
    if not isinstance(options, dict):
        raise TypeError("DEFAULT_FCONFIGURE_OPTIONS must be a dictionary")
    global DEFAULT_FCONFIGURE_OPTIONS
    DEFAULT_FCONFIGURE_OPTIONS = options

validate_config_options()