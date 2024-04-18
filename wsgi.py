from loguru import logger

from flask_app.app import create_app

app = create_app()

logger.add("logs/flask.log", rotation="00:00", level="ERROR", enqueue=True)

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=False)
