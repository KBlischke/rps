PROJECT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_PATH" || exit
export FLASK_APP=app.py
export FLASK_ENV=production
xdg-open http://127.0.0.1:5000/ &
flask run
