import json

from server import app


def custom_openapi():
    scheme = json.dumps(app.app.openapi())
    print(scheme)


if __name__ == '__main__':
    custom_openapi()
