
import controller
import threading
import config
import os
import json
import logging.config


def setup_logging(
                    default_path='logging.json',
                    default_level=logging.INFO,
                    env_key='LOG_CFG'):

    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

def start_web_app_server():
    web_server = controller.get_instance().get_webapp_server()
    # web_server = web_app_server
    web_server.start_server()

def start_drones_server():
    drones_server = controller.get_instance().get_drone_server()
    drones_server.start_server()


if __name__ == '__main__':
    try:
        setup_logging()
        # web_app_thread = threading.Thread(target=start_web_app_server)
        drones_thread = threading.Thread(target=start_drones_server)
        # web_app_thread.start()
        drones_thread.start()
        start_web_app_server()
    except Exception, e:
        pass