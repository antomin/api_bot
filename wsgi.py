from common.settings import settings
from flask_app.app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host="web", port=5000, debug=settings.DEBUG)
