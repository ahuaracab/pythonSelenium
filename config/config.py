import os


class TestConfig:
    def __init__(self):
        self.base_url = os.environ.get('BASE_URL')
        self.username = os.environ.get('USERNAME')
        self.password = os.environ.get('PASSWORD')
