#network
local_address = '132.74.214.3'
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
prop_tbl_name = 'tblprop'
battery_tbl_name = 'tblbattery'
thrust_tbl_name = 'tblthrust'
flight_tbl_name = 'tblflight'
#for table insert:
motor_tbl_insert = motor_tbl_name + ' (name, kv, weight, price) VALUES (%s, %s, %s, %s)'
bat_tbl_insert = battery_tbl_name + ' (name, type, volt, discharge_rate, capacity, weight, price) VALUES (%s, %s, %s, %s, %s, %s, %s)'
flight_tbl_insert = flight_tbl_name + ' (drone_num, start_flight_time, state, log_file_path) VALUES (%s, %s, %s, %s)'

#flight_status
flight_status_active = ['takeoff', 'in_mission', 'rtl', 'land']
flight_status_before_takeoff = ['ready_to_takeoff']


#query numbers:
QUERY_GET_ACTIVE_DRONES = 1
QUERY_GET_FLIGHT_RECORDS = 2
QUERY_GET_FLIGHT_TIME_FOR_DRONE = 3





