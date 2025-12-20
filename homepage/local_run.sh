# activate venv
source "/Users/devuser/local/dev/fornax/lakeblvd.net/.venv-lakeblvd/bin/activate"
# set up environment variables
if $test
    then echo "running on TEST environment"
    export APP_ENV="test"
else
    echo "running on DEV environment"
    export APP_ENV="dev"
fi
export FLASK_KEY="b72ee9b7-3c6e-470b-a912-007df5bca4e8"
# export DATABASE_URL="sqlite:///lakeblvd-home.db"
export DATABASE_URL="postgresql+psycopg://localhost/lakeblvd_dev"
export REQUIRE_INVITATION="true"
# run flask with gunicorn
# gunicorn -b 127.0.0.1:5000 "app:create_app()" 
flask --app app run --debug