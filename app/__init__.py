"""
Package: app
Package for the application models and service routes
"""
import logging
from flask import Flask
from flask_talisman import Talisman
from flask_cors import CORS

# Create Flask application
app = Flask(__name__)
app.config.from_object("config")

# Initialize Talisman for security headers
talisman = Talisman(app)

# Initialize CORS
CORS(app)

# Import the routes after the Flask app is created
# pylint: disable=wrong-import-position, cyclic-import, unused-import
from app import routes, models  # noqa: F401, E402
from app.common import error_handlers  # noqa: F401, E402

# Set up logging for production
app.logger.propagate = False
if __name__ != "__main__":
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(module)s] %(message)s", "%Y-%m-%d %H:%M:%S %z"
    )
    for handler in app.logger.handlers:
        handler.setFormatter(formatter)
    app.logger.info("Logging handler established")

app.logger.info("Service initialized")
