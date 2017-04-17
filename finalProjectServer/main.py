
import controller
import threading
import web_app_server
import tornado
#import db_handler
import config

# if __name__ == '__main__':
#     server = server.DronesServer()
#     server.start_server()


# if __name__ == '__main__':
#     db = db_handler.get_instance()
#     args = ('vs', 5, 20, 10)
#     db.insert_to_table(config.motor_tbl_insert, args)
#     args = ('fvsdvirst', 6, 20, 10)
#     db.insert_to_table(config.motor_tbl_insert, args)
#     args = ('firhbgdfhst', 7, 20, 10)
#     db.insert_to_table(config.motor_tbl_insert, args)
#     args = ('nfdgn', 8, 20, 10)
#     db.insert_to_table(config.motor_tbl_insert, args)
#     args = ('fnfn', 9, 20, 10)
#     db.insert_to_table(config.motor_tbl_insert, args)
#
#     db.get_table(config.motor_tbl_name)



def start_web_app_server():
    web_server = controller.get_instance().get_webapp_server()
    # web_server = web_app_server
    web_server.start_server()

def start_drones_server():
    drones_server = controller.get_instance().get_drone_server()
    drones_server.start_server()


if __name__ == '__main__':
    # web_app_thread = threading.Thread(target=start_web_app_server)
    drones_thread = threading.Thread(target=start_drones_server)
    # web_app_thread.start()
    drones_thread.start()
    start_web_app_server()