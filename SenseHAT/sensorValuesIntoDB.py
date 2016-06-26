# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from datetime import datetime
from sense_hat import SenseHat
from time import sleep

def get_timestamp():
    """Get the current time as an SQL timestamp"""
    sql_format = "'%Y-%m-%d %H:%M:%S'"
    now = datetime.now()
    return now.strftime(sql_format)


def read_environ_sensors(sense):
    """Read current temperature, humidity and pressure sensor values"""
    data = []
    data.append(sense.get_temperature())
    data.append(sense.get_humidity())
    data.append(sense.get_pressure())
    data.append(sense.get_temperature_from_humidity())
    data.append(sense.get_temperature_from_pressure())
    return data

def read_imu_sensors(sense):
    """Read current inertial measurement unit sensore values"""
    data = []
    o = sense.get_orientation()
    data.append(o["yaw"])
    data.append(o["pitch"])
    data.append(o["roll"])
    mag = sense.get_compass_raw()
    data.append(mag["x"])
    data.append(mag["y"])
    data.append(mag["z"])
    acc = sense.get_accelerometer_raw()
    data.append(acc["x"])
    data.append(acc["y"])
    data.append(acc["z"])
    gyro = sense.get_gyroscope_raw()
    data.append(gyro["x"])
    data.append(gyro["y"])
    data.append(gyro["z"])
    return data

def store_in_db(con, ts, env, imu):
    """Store both kind of sensor values into db"""
    con.execute("INSERT INTO environ_data VALUES (datetime(" + ts + "), ?,?,?,?,?)", *env)
    con.execute("INSERT INTO imu_data VALUES (datetime(" + ts + "), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", *imu)

def create_db_tables(con):
    """Create the database tables environ_data and imu_data"""
    sql = """CREATE TABLE environ_data (
        timestamp TEXT UNIQUE,
        temp REAL,
        humidity REAL,
        pressure REAL,
        temp_h REAL,
        temp_p REAL
    )"""
    con.execute(sql)
    sql = """CREATE TABLE imu_data (
        timestamp TEXT UNIQUE,
        yaw REAL,
        pitch REAL,
        roll REAL,
        magX REAL,
        magY REAL,
        magZ REAL,
        accX REAL,
        accY REAL,
        accZ REAL,
        gyroX REAL,
        gyroY REAL,
        gyroZ REAL
    )"""
    con.execute(sql)

def init_db(url):
    """Connect to database and create tables if they dont already exist"""
    engine = create_engine(url)
    con = engine.connect()
    if not engine.dialect.has_table(con, 'environ_data'):
        create_db_tables(con)
    return con

def main_loop(sense, conn):
    while True:
       ts = get_timestamp()
       env = read_environ_sensors(sense)
       imu = read_imu_sensors(sense)
       store_in_db(conn, ts, env, imu)
       sleep(30)


db_dir = "/home/pi"
db_file = "sensors.db"
db_url = "sqlite:///{0}/{1}".format(db_dir, db_file)

connection = init_db(db_url)
sense = SenseHat()
try:
    main_loop(sense, connection)
except KeyboardInterrupt:
    connection.close()
