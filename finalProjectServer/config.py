
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
motor_tbl_insert = 'tblmotor (name, kv, weight, price) VALUES (%s, %s, %s, %s)'



