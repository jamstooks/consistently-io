class MockRequest:
    def __init__(self, status_code=200, json_data={}):
        self.status_code = status_code
        self.json_data = json_data

    def json(self):
        return self.json_data
