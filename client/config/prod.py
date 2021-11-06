import sys


config = {
    'SOLVE_ENDPOINT': 'https://acoder.herokuapp.com/solve',
    'LOGGING_LEVEL': None,
    'BASE_PATH': sys._MEIPASS if getattr(sys, 'frozen', False) else ''
}
