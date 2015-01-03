from app import app
import app.config as config

if __name__ == "__main__":
    app.secret_key = config.APP_SECRET_KEY
    app.run(debug=True)
