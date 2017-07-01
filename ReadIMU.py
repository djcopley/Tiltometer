"""
Collections of functions for writing and retrieving data from IMU
"""
import smbus
import logging
import math
from LSM9DS0 import *

# Define bus
bus = smbus.SMBus(1)

# Math Constants
RAD_TO_DEG = 57.29578
G_GAIN = 0.070  # [deg/s/LSB]  If you change the dps for gyro, you need to update this value accordingly
AA = 0.40  # Complementary filter constant


def write_acc(register, value):
    bus.write_byte_data(ACC_ADDRESS, register, value)
    return -1


def write_mag(register, value):
    bus.write_byte_data(MAG_ADDRESS, register, value)
    return -1


def write_gyro(register, value):
    bus.write_byte_data(GYR_ADDRESS, register, value)
    return -1


def read_acc_x():
    acc_l = bus.read_byte_data(ACC_ADDRESS, OUT_X_L_A)
    acc_h = bus.read_byte_data(ACC_ADDRESS, OUT_X_H_A)
    acc_combined = (acc_l | acc_h << 8)

    return acc_combined if acc_combined < 32768 else acc_combined - 65536


def read_acc_y():
    acc_l = bus.read_byte_data(ACC_ADDRESS, OUT_Y_L_A)
    acc_h = bus.read_byte_data(ACC_ADDRESS, OUT_Y_H_A)
    acc_combined = (acc_l | acc_h << 8)

    return acc_combined if acc_combined < 32768 else acc_combined - 65536


def read_acc_z():
    acc_l = bus.read_byte_data(ACC_ADDRESS, OUT_Z_L_A)
    acc_h = bus.read_byte_data(ACC_ADDRESS, OUT_Z_H_A)
    acc_combined = (acc_l | acc_h << 8)

    return acc_combined if acc_combined < 32768 else acc_combined - 65536


def read_mag_x():
    mag_l = bus.read_byte_data(MAG_ADDRESS, OUT_X_L_M)
    mag_h = bus.read_byte_data(MAG_ADDRESS, OUT_X_H_M)
    mag_combined = (mag_l | mag_h << 8)

    return mag_combined if mag_combined < 32768 else mag_combined - 65536


def read_mag_y():
    mag_l = bus.read_byte_data(MAG_ADDRESS, OUT_Y_L_M)
    mag_h = bus.read_byte_data(MAG_ADDRESS, OUT_Y_H_M)
    mag_combined = (mag_l | mag_h << 8)

    return mag_combined if mag_combined < 32768 else mag_combined - 65536


def read_mag_z():
    mag_l = bus.read_byte_data(MAG_ADDRESS, OUT_Z_L_M)
    mag_h = bus.read_byte_data(MAG_ADDRESS, OUT_Z_H_M)
    mag_combined = (mag_l | mag_h << 8)

    return mag_combined if mag_combined < 32768 else mag_combined - 65536


def read_gyro_x():
    gyr_l = bus.read_byte_data(GYR_ADDRESS, OUT_X_L_G)
    gyr_h = bus.read_byte_data(GYR_ADDRESS, OUT_X_H_G)
    gyr_combined = (gyr_l | gyr_h << 8)

    return gyr_combined if gyr_combined < 32768 else gyr_combined - 65536


def read_gyro_y():
    gyr_l = bus.read_byte_data(GYR_ADDRESS, OUT_Y_L_G)
    gyr_h = bus.read_byte_data(GYR_ADDRESS, OUT_Y_H_G)
    gyr_combined = (gyr_l | gyr_h << 8)

    return gyr_combined if gyr_combined < 32768 else gyr_combined - 65536


def read_gyro_z():
    gyr_l = bus.read_byte_data(GYR_ADDRESS, OUT_Z_L_G)
    gyr_h = bus.read_byte_data(GYR_ADDRESS, OUT_Z_H_G)
    gyr_combined = (gyr_l | gyr_h << 8)

    return gyr_combined if gyr_combined < 32768 else gyr_combined - 65536


# initialise the accelerometer
write_acc(CTRL_REG1_XM, 0b01100111)  # z,y,x axis enabled, continuous update,  100Hz data rate
write_acc(CTRL_REG2_XM, 0b00100000)  # +/- 16G full scale

# initialise the magnetometer
write_mag(CTRL_REG5_XM, 0b11110000)  # Temp enable, M data rate = 50Hz
write_mag(CTRL_REG6_XM, 0b01100000)  # +/-12gauss
write_mag(CTRL_REG7_XM, 0b00000000)  # Continuous-conversion mode

# initialise the gyroscope
write_gyro(CTRL_REG1_G, 0b00001111)  # Normal power mode, all axes enabled
write_gyro(CTRL_REG4_G, 0b00110000)  # Continuous update, 2000 dps full scale


def get_pitch():

    """ Return Pitch Value"""

    acc_x = read_acc_x()
    acc_y = read_acc_y()
    acc_z = read_acc_z()

    acc_x_norm = acc_x / math.sqrt(acc_x * acc_x + acc_y * acc_y + acc_z * acc_z)

    try:
        pitch = math.asin(acc_x_norm)
        return pitch

    except Exception as e:
        logging.debug(e)
        return 0


def get_roll():

    """ Returns Roll Value """

    acc_x = read_acc_x()
    acc_y = read_acc_y()
    acc_z = read_acc_z()

    acc_y_norm = acc_y / math.sqrt(acc_x * acc_x + acc_y * acc_y + acc_z * acc_z)

    try:
        roll = -math.asin(acc_y_norm / math.cos(get_pitch()))
        return roll

    except Exception as e:
        logging.debug(e)
        return 0
