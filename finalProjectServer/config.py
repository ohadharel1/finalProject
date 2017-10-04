#network
local_address = '0.0.0.0'
#config for db:

#connect args
db_host = "localhost"
db_user = 'root'
db_pass = '1234'
db_name = "final_project_db"

#web_app_server_args
max_num_of_web_clients = 10 + 1

#table names
motor_tbl_name = 'tblmotor'
prop_tbl_name = 'tblprops'
battery_tbl_name = 'tblbattery'
thrust_tbl_name = 'tblthrust'
flight_tbl_name = 'tblflight'
#for table insert:
motor_tbl_insert = motor_tbl_name + ' (name, kv, weight, price) VALUES (%s, %s, %s, %s)'
prop_tbl_insert = prop_tbl_name + ' (name, diameter, speed, weight, price) VALUES (%s, %s, %s, %s, %s)'
bat_tbl_insert = battery_tbl_name + ' (name, type, volt, discharge_rate, capacity, weight, price) VALUES ("%s", "%s", %s, %s, %s, %s, %s)'
flight_tbl_insert = flight_tbl_name + ' (drone_num, start_flight_time, state, log_file_path) VALUES (%s, %s, %s, %s)'

#flight_status
flight_status_active = ['takeoff', 'in_mission', 'rtl', 'land']
flight_status_before_takeoff = ['ready to takeoff']


#query numbers:
QUERY_DB_ACTIVE = 0
QUERY_GET_ACTIVE_DRONES = 1
QUERY_GET_FLIGHT_RECORDS = 2
QUERY_GET_FLIGHT_TIME_FOR_DRONE = 3
QUERY_GET_CURRENT_FLIGHT_DETAILS = 4
QUERY_GET_SETUP_SUGGESTIONS = 5
QUERY_GET_ALL_FLIGHTS = 6
QUERY_GET_DRONE_SUM_REPORT = 7
QUERY_GET_TABLE = 8
QUERY_UPDATE_TABLE = 9
QUERY_ADD_SINGLE_TO_TABLE = 10
QUERY_ADD_MULTI_TO_TABLE = 11
QUERY_DELETE_FROM_TABLE = 12
QUERY_SAVE_FLIGHT_COMMENT = 13
QUERY_GET_FLIGHTS_PER_DRONE = 14





