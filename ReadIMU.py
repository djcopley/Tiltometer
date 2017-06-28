"""

"""
import smbus
import time
import math
from LSM9DS0 import *
import datetime

# Define bus
bus = smbus.SMBus(1)

# Math Constants
RAD_TO_DEG = 57.29578
G_GAIN = 0.070  # [deg/s/LSB]  If you change the dps for gyro, you need to update this value accordingly
AA = 0.40  # Complementary filter constant


def writeACC(register, value):
    bus.write_byte_data(ACC_ADDRESS, register, value)
    return -1


def writeMAG(register, value):
    bus.write_byte_data(MAG_ADDRESS, register, value)
    return -1


def writeGRY(register, value):
    bus.write_byte_data(GYR_ADDRESS, register, value)
    return -1


def readACCx():
    acc_l = bus.read_byte_data(ACC_ADDRESS, OUT_X_L_A)
    acc_h = bus.read_byte_data(ACC_ADDRESS, OUT_X_H_A)
    acc_combined = (acc_l | acc_h << 8)

    return acc_combined if acc_combined < 32768 else acc_combined - 65536


def readACCy():
    acc_l = bus.read_byte_data(ACC_ADDRESS, OUT_Y_L_A)
    acc_h = bus.read_byte_data(ACC_ADDRESS, OUT_Y_H_A)
    acc_combined = (acc_l | acc_h << 8)

    return acc_combined if acc_combined < 32768 else acc_combined - 65536


def readACCz():
    acc_l = bus.read_byte_data(ACC_ADDRESS, OUT_Z_L_A)
    acc_h = bus.read_byte_data(ACC_ADDRESS, OUT_Z_H_A)
    acc_combined = (acc_l | acc_h << 8)

    return acc_combined if acc_combined < 32768 else acc_combined - 65536


def readMAGx():
    mag_l = bus.read_byte_data(MAG_ADDRESS, OUT_X_L_M)
    mag_h = bus.read_byte_data(MAG_ADDRESS, OUT_X_H_M)
    mag_combined = (mag_l | mag_h << 8)

    return mag_combined if mag_combined < 32768 else mag_combined - 65536


def readMAGy():
    mag_l = bus.read_byte_data(MAG_ADDRESS, OUT_Y_L_M)
    mag_h = bus.read_byte_data(MAG_ADDRESS, OUT_Y_H_M)
    mag_combined = (mag_l | mag_h << 8)

    return mag_combined if mag_combined < 32768 else mag_combined - 65536


def readMAGz():
    mag_l = bus.read_byte_data(MAG_ADDRESS, OUT_Z_L_M)
    mag_h = bus.read_byte_data(MAG_ADDRESS, OUT_Z_H_M)
    mag_combined = (mag_l | mag_h << 8)

    return mag_combined if mag_combined < 32768 else mag_combined - 65536


def readGYRx():
    gyr_l = bus.read_byte_data(GYR_ADDRESS, OUT_X_L_G)
    gyr_h = bus.read_byte_data(GYR_ADDRESS, OUT_X_H_G)
    gyr_combined = (gyr_l | gyr_h << 8)

    return gyr_combined if gyr_combined < 32768 else gyr_combined - 65536


def readGYRy():
    gyr_l = bus.read_byte_data(GYR_ADDRESS, OUT_Y_L_G)
    gyr_h = bus.read_byte_data(GYR_ADDRESS, OUT_Y_H_G)
    gyr_combined = (gyr_l | gyr_h << 8)

    return gyr_combined if gyr_combined < 32768 else gyr_combined - 65536


def readGYRz():
    gyr_l = bus.read_byte_data(GYR_ADDRESS, OUT_Z_L_G)
    gyr_h = bus.read_byte_data(GYR_ADDRESS, OUT_Z_H_G)
    gyr_combined = (gyr_l | gyr_h << 8)

    return gyr_combined if gyr_combined < 32768 else gyr_combined - 65536


# initialise the accelerometer
writeACC(CTRL_REG1_XM, 0b01100111)  # z,y,x axis enabled, continuous update,  100Hz data rate
writeACC(CTRL_REG2_XM, 0b00100000)  # +/- 16G full scale

# initialise the magnetometer
writeMAG(CTRL_REG5_XM, 0b11110000)  # Temp enable, M data rate = 50Hz
writeMAG(CTRL_REG6_XM, 0b01100000)  # +/-12gauss
writeMAG(CTRL_REG7_XM, 0b00000000)  # Continuous-conversion mode

# initialise the gyroscope
writeGRY(CTRL_REG1_G, 0b00001111)  # Normal power mode, all axes enabled
writeGRY(CTRL_REG4_G, 0b00110000)  # Continuous update, 2000 dps full scale

gyroXangle = 0.0
gyroYangle = 0.0
gyroZangle = 0.0
CFangleX = 0.0
CFangleY = 0.0

a = datetime.datetime.now()

while True:

    # Read the accelerometer,gyroscope and magnetometer values
    ACCx = readACCx()
    ACCy = readACCy()
    ACCz = readACCz()
    GYRx = readGYRx()
    GYRy = readGYRy()
    GYRz = readGYRz()
    MAGx = readMAGx()
    MAGy = readMAGy()
    MAGz = readMAGz()

    # Calculate loop Period(LP). How long between Gyro Reads
    b = datetime.datetime.now() - a
    a = datetime.datetime.now()
    LP = b.microseconds / (1000000 * 1.0)
    print("Loop Time | %5.2f|" % (LP)),

    # Convert Gyro raw to degrees per second
    rate_gyr_x = GYRx * G_GAIN
    rate_gyr_y = GYRy * G_GAIN
    rate_gyr_z = GYRz * G_GAIN

    # Calculate the angles from the gyro.
    gyroXangle += rate_gyr_x * LP
    gyroYangle += rate_gyr_y * LP
    gyroZangle += rate_gyr_z * LP

    # Convert Accelerometer values to degrees
    AccXangle = (math.atan2(ACCy, ACCz) + math.pi) * RAD_TO_DEG
    AccYangle = (math.atan2(ACCz, ACCx) + math.pi) * RAD_TO_DEG

    # convert the values to -180 and +180
    AccXangle -= 180.0
    if AccYangle > 90:
        AccYangle -= 270.0
    else:
        AccYangle += 90.0

    # Complementary filter used to combine the accelerometer and gyro values.
    CFangleX = AA * (CFangleX + rate_gyr_x * LP) + (1 - AA) * AccXangle
    CFangleY = AA * (CFangleY + rate_gyr_y * LP) + (1 - AA) * AccYangle

    # Calculate heading
    heading = 180 * math.atan2(MAGy, MAGx) / math.pi

    # Only have our heading between 0 and 360
    if heading < 0:
        heading += 360

    # Normalize accelerometer raw values.
    accXnorm = ACCx / math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)
    accYnorm = ACCy / math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)

    # Calculate pitch and roll
    pitch = math.asin(accXnorm)
    roll = -math.asin(accYnorm / math.cos(pitch))

    # Calculate the new tilt compensated values
    magXcomp = MAGx * math.cos(pitch) + MAGz * math.sin(pitch)
    magYcomp = MAGx * math.sin(roll) * math.sin(pitch) + MAGy * math.cos(roll) - MAGz * math.sin(roll) * math.cos(pitch)

    # Calculate tilt compensated heading
    tiltCompensatedHeading = 180 * math.atan2(magYcomp, magXcomp) / math.pi

    # if tiltCompensatedHeading < 0:
    #     tiltCompensatedHeading += 360
    #
    # if 1:  # Change to '0' to stop showing the angles from the accelerometer
    #     print("\033[1;34;40mACCX Angle %5.2f ACCY Angle %5.2f  \033[0m  " % (AccXangle, AccYangle)),
    #
    # if 1:  # Change to '0' to stop  showing the angles from the gyro
    #     print("\033[1;31;40m\tGRYX Angle %5.2f  GYRY Angle %5.2f  GYRZ Angle %5.2f" % (
    #     gyroXangle, gyroYangle, gyroZangle)),
    #
    # if 1:  # Change to '0' to stop  showing the angles from the complementary filter
    #     print("\033[1;35;40m   \tCFangleX Angle %5.2f \033[1;36;40m  CFangleY Angle %5.2f \33[1;32;40m" %
    #           (CFangleX, CFangleY)),
    #
    # if 1:  # Change to '0' to stop  showing the heading
    #     print("HEADING  %5.2f \33[1;37;40m tiltCompensatedHeading %5.2f" % (heading, tiltCompensatedHeading))
    print('\x1b[6;30;42m' + 'Pitch:' + '\x1b[0m', str(pitch), '\x1b[6;30;42m' + 'Roll:' + '\x1b[0m', roll)

    # slow program down a bit, makes the output more readable
    time.sleep(0.03)
