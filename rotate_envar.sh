#!/bin/zsh
# indicator for heroku production environment
heroku config:set HEROKU_PROD_ENV=true
# flask secret key
uid=$(python -c "import uuid; print(uuid.uuid4())")
heroku config:set FLASK_KEY=$uid
# the postgre is already set, confirm it's persistent
