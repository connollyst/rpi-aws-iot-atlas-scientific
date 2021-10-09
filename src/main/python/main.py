from app.App import App
from app.Logger import get_logger

LOGGER = get_logger(__name__)

if __name__ == '__main__':
    App(LOGGER).start()
