#network
local_address = '10.0.0.13'
#config for db:

#connect args
db_host = "localhost"
db_user = 'root'
db_pass = '1234'
db_name = "final_project_db"
#table names
motor_tbl_name = 'tblmotor'
prop_tbl_name = 'tblprop'
battery_tbl_name = 'tblbattery'
thrust_tbl_name = 'tblthrust'
flight_tbl_name = 'tblflight'
#for table insert:
motor_tbl_insert = motor_tbl_name + ' (name, kv, weight, price) VALUES (%s, %s, %s, %s)'
flight_tbl_insert = flight_tbl_name + ' (drone_num, start_flight_time, state, log_file_path) VALUES (%s, %s, %s, %s)'

#flight_status
flight_status_active = ['takeoff', 'in_mission', 'rtl', 'land']
flight_status_before_takeoff = ['ready_to_takeoff']


