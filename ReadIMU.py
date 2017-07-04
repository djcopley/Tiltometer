"""
Functions for Initializing and Reading data from IMU
-----------------------------------------------------
MIT LICENSE
"""
import smbus
import logging
import math

bus = smbus.SMBus(1)

# Math Constants
RAD_TO_DEG = 57.29578
G_GAIN = 0.070  # [deg/s/LSB]  If you change the dps for gyro, you need to update this value accordingly

# LSM9DS0 Locations
MAG_ADDRESS = 0x1E
ACC_ADDRESS = 0x1E
GYR_ADDRESS = 0x6A

# LSM9DS0 Gyro Registers
WHO_AM_I_G = 0x0F
CTRL_REG1_G = 0x20
CTRL_REG2_G = 0x21
CTRL_REG3_G = 0x22
CTRL_REG4_G = 0x23
CTRL_REG5_G = 0x24
REFERENCE_G = 0x25
STATUS_REG_G = 0x27
OUT_X_L_G = 0x28
OUT_X_H_G = 0x29
OUT_Y_L_G = 0x2A
OUT_Y_H_G = 0x2B
OUT_Z_L_G = 0x2C
OUT_Z_H_G = 0x2D
FIFO_CTRL_REG_G = 0x2E
FIFO_SRC_REG_G = 0x2F
INT1_CFG_G = 0x30
INT1_SRC_G = 0x31
INT1_THS_XH_G = 0x32
INT1_THS_XL_G = 0x33
INT1_THS_YH_G = 0x34
INT1_THS_YL_G = 0x35
INT1_THS_ZH_G = 0x36
INT1_THS_ZL_G = 0x37
INT1_DURATION_G = 0x38

# LSM9DS0 Accelerometer and Magneto Registers
OUT_TEMP_L_XM = 0x05
OUT_TEMP_H_XM = 0x06
STATUS_REG_M = 0x07
OUT_X_L_M = 0x08
OUT_X_H_M = 0x09
OUT_Y_L_M = 0x0A
OUT_Y_H_M = 0x0B
OUT_Z_L_M = 0x0C
OUT_Z_H_M = 0x0D
WHO_AM_I_XM = 0x0F
INT_CTRL_REG_M = 0x12
INT_SRC_REG_M = 0x13
INT_THS_L_M = 0x14
INT_THS_H_M = 0x15
OFFSET_X_L_M = 0x16
OFFSET_X_H_M = 0x17
OFFSET_Y_L_M = 0x18
OFFSET_Y_H_M = 0x19
OFFSET_Z_L_M = 0x1A
OFFSET_Z_H_M = 0x1B
REFERENCE_X = 0x1C
REFERENCE_Y = 0x1D
REFERENCE_Z = 0x1E
CTRL_REG0_XM = 0x1F
CTRL_REG1_XM = 0x20
CTRL_REG2_XM = 0x21
CTRL_REG3_XM = 0x22
CTRL_REG4_XM = 0x23
CTRL_REG5_XM = 0x24
CTRL_REG6_XM = 0x25
CTRL_REG7_XM = 0x26
STATUS_REG_A = 0x27
OUT_X_L_A = 0x28
OUT_X_H_A = 0x29
OUT_Y_L_A = 0x2A
OUT_Y_H_A = 0x2B
OUT_Z_L_A = 0x2C
OUT_Z_H_A = 0x2D
FIFO_CTRL_REG = 0x2E
FIFO_SRC_REG = 0x2F
INT_GEN_1_REG = 0x30
INT_GEN_1_SRC = 0x31
INT_GEN_1_THS = 0x32
INT_GEN_1_DURATION = 0x33
INT_GEN_2_REG = 0x34
INT_GEN_2_SRC = 0x35
INT_GEN_2_THS = 0x36
INT_GEN_2_DURATION = 0x37
CLICK_CFG = 0x38
CLICK_SRC = 0x39
CLICK_THS = 0x3A
TIME_LIMIT = 0x3B
TIME_LATENCY = 0x3C
TIME_WINDOW = 0x3D


def write_acc(register, value):

    """Write to accelerometer"""

    bus.write_byte_data(ACC_ADDRESS, register, value)

    return -1


def write_mag(register, value):

    """Write to magnetometer"""

    bus.write_byte_data(MAG_ADDRESS, register, value)

    return -1


def write_gyro(register, value):

    """Write to gyroscope"""

    bus.write_byte_data(GYR_ADDRESS, register, value)

    return -1


def read_acc_x():

    """Read accelerometer x value"""

    acc_l = bus.read_byte_data(ACC_ADDRESS, OUT_X_L_A)
    acc_h = bus.read_byte_data(ACC_ADDRESS, OUT_X_H_A)
    acc_combined = (acc_l | acc_h << 8)

    return acc_combined if acc_combined < 32768 else acc_combined - 65536


def read_acc_y():

    """Read accelerometer y value"""

    acc_l = bus.read_byte_data(ACC_ADDRESS, OUT_Y_L_A)
    acc_h = bus.read_byte_data(ACC_ADDRESS, OUT_Y_H_A)
    acc_combined = (acc_l | acc_h << 8)

    return acc_combined if acc_combined < 32768 else acc_combined - 65536


def read_acc_z():

    """Read accelerometer z value"""

    acc_l = bus.read_byte_data(ACC_ADDRESS, OUT_Z_L_A)
    acc_h = bus.read_byte_data(ACC_ADDRESS, OUT_Z_H_A)
    acc_combined = (acc_l | acc_h << 8)

    return acc_combined if acc_combined < 32768 else acc_combined - 65536


def read_mag_x():

    """Read magnetometer x value"""

    mag_l = bus.read_byte_data(MAG_ADDRESS, OUT_X_L_M)
    mag_h = bus.read_byte_data(MAG_ADDRESS, OUT_X_H_M)
    mag_combined = (mag_l | mag_h << 8)

    return mag_combined if mag_combined < 32768 else mag_combined - 65536


def read_mag_y():

    """Read magnetometer y value"""

    mag_l = bus.read_byte_data(MAG_ADDRESS, OUT_Y_L_M)
    mag_h = bus.read_byte_data(MAG_ADDRESS, OUT_Y_H_M)
    mag_combined = (mag_l | mag_h << 8)

    return mag_combined if mag_combined < 32768 else mag_combined - 65536


def read_mag_z():

    """Read magnetometer z value"""

    mag_l = bus.read_byte_data(MAG_ADDRESS, OUT_Z_L_M)
    mag_h = bus.read_byte_data(MAG_ADDRESS, OUT_Z_H_M)
    mag_combined = (mag_l | mag_h << 8)

    return mag_combined if mag_combined < 32768 else mag_combined - 65536


def read_gyro_x():

    """Read gyroscope x value"""

    gyr_l = bus.read_byte_data(GYR_ADDRESS, OUT_X_L_G)
    gyr_h = bus.read_byte_data(GYR_ADDRESS, OUT_X_H_G)
    gyr_combined = (gyr_l | gyr_h << 8)

    return gyr_combined if gyr_combined < 32768 else gyr_combined - 65536


def read_gyro_y():

    """Read gyroscope y value"""

    gyr_l = bus.read_byte_data(GYR_ADDRESS, OUT_Y_L_G)
    gyr_h = bus.read_byte_data(GYR_ADDRESS, OUT_Y_H_G)
    gyr_combined = (gyr_l | gyr_h << 8)

    return gyr_combined if gyr_combined < 32768 else gyr_combined - 65536


def read_gyro_z():

    """Read gyroscope z value"""

    gyr_l = bus.read_byte_data(GYR_ADDRESS, OUT_Z_L_G)
    gyr_h = bus.read_byte_data(GYR_ADDRESS, OUT_Z_H_G)
    gyr_combined = (gyr_l | gyr_h << 8)

    return gyr_combined if gyr_combined < 32768 else gyr_combined - 65536


# Initialise the accelerometer
write_acc(CTRL_REG1_XM, 0b01100111)  # z,y,x axis enabled, continuous update,  100Hz data rate
write_acc(CTRL_REG2_XM, 0b00100000)  # +/- 16G full scale

# Initialise the magnetometer
write_mag(CTRL_REG5_XM, 0b11110000)  # Temp enable, M data rate = 50Hz
write_mag(CTRL_REG6_XM, 0b01100000)  # +/-12gauss
write_mag(CTRL_REG7_XM, 0b00000000)  # Continuous-conversion mode

# Initialise the gyroscope
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
