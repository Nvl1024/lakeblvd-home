# activate venv
source "/Users/devuser/local/dev/fornax/lakeblvd.net/.venv-lakeblvd/bin/activate"
# set up environment variables
export APP_ENV="dev"
export FLASK_KEY="b72ee9b7-3c6e-470b-a912-007df5bca4e8"
export DATABASE_URL="sqlite:///lakeblvd-home.db"
# run flask with gunicorn
gunicorn -b 127.0.0.1:5000 "app:create_app()" 