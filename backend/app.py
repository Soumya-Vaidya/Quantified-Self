from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from datetime import timedelta

from resources import api, cache


app = Flask(__name__)

# Flask_cors Config
CORS(app)

# SQL ALchemny Config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy()
db.init_app(app)

# Flask_Restful Config
api.init_app(app)

# Flask_caching Config
cache.init_app(
    app,
    config={
        "CACHE_TYPE": "RedisCache",
        "CACHE_REDIS_HOST": "127.0.0.1",
        "CACHE_REDIS_PORT": 6379,
        "CACHE_REDIS_DB": 0,
        "CACHE_REDIS_URL": "redis://127.0.0.1:6379/3",
    },
)

# JWT Config
app.config["JWT_SECRET_KEY"] = "081faa5e-eef7-4486-9e40-b1e3a2ded785"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
jwt = JWTManager(app)


if __name__ == "__main__":
    app.run(debug=True, port=8000, host="0.0.0.0")

# app.app_context().push()
