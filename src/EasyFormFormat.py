from gui import window

import logging

LOG_FILE = "log.txt"
TITLE = "Easy Form Format"


def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        # TODO: Write log in file for production only.
        filename=LOG_FILE,
        format="[%(levelname)s][%(filename)s:%(lineno)s %(funcName)s] %(message)s",
    )


def main():
    configure_logging()
    logging.info("app started")
    window.Window.start()


if __name__ == "__main__":
    main()
