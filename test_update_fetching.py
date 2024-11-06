from app import app
from app.update_fetcher import fetch_all_updates

if __name__ == '__main__':
    with app.app_context():
        fetch_all_updates()
