import os
from flask import Flask

def create_app():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    app = Flask(
        __name__,
        static_folder=os.path.join(BASE_DIR, "static"),
        template_folder=os.path.join(BASE_DIR, "templates"),
        static_url_path="/static"   # 🔥 THIS IS THE KEY
    )

    # Enable session support
    app.secret_key = "super-secret-key"   # 👈 Add this line

    from app.routes import main
    app.register_blueprint(main)

    return app