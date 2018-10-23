class MockRequest:
    def __init__(self, status_code=200, json_data={}, url=''):
        self.status_code = status_code
        self.json_data = json_data
        self.url = url

    def json(self):
        return self.json_data
