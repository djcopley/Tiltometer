"""
5/24/2017
This program reads data from a motion processor, calculates the angular position from the
data and displays the vehicle information graphically.
---------------------------------------------------------
MIT LICENCE
"""

import threading
import time
import gi
from lib.IMU import AccelData
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib

RAD_TO_DEG = 57.29578  # Math constant for RADIAN -> DEGREE conversion
REFRESH_RATE = .035

# Initialize AccelData class
accel_data = AccelData()
get_pitch = accel_data.get_pitch
get_roll = accel_data.get_roll

# Get starting values for pitch and roll to measure change
start_pitch = get_pitch()
start_roll = get_roll()


def level_gyro():

    """ Set base values for gyroscope so change can be calculated """

    global start_pitch, start_roll
    start_pitch = get_pitch()
    start_roll = get_roll()


def get_gyro_pos():
    
    """ Returns pitch and roll from mpu """

    return (get_pitch() - start_pitch), (get_roll() - start_roll)


def update_position_gauges():
    
    """ Updates the rotation of the Roll and Pitch Gauges """
    
    # Object imports
    pitch_gauge = builder.get_object("pitch_gauge")
    roll_gauge = builder.get_object("roll_gauge")

    # Wait for main loop
    while Gtk.main_level() == 0:
        time.sleep(.01)

    # Update loop
    while Gtk.main_level() != 0:

        pitch_val, roll_val = get_gyro_pos()
        pitch_val = int(pitch_val * RAD_TO_DEG)
        roll_val = int(roll_val * RAD_TO_DEG)

        if int(pitch_val) in range(-50, 51):
            mainloop_do(pitch_gauge.set_from_file, "assets/pitch-gauge/pitch-gauge%d.png" % int(pitch_val))

        else:
            mainloop_do(pitch_gauge.set_from_file, "assets/outside-range/pitch_outside_range_0.png")

        if int(roll_val) in range(-50, 51):
            mainloop_do(roll_gauge.set_from_file, "assets/roll-gauge/roll-gauge%d.png" % int(roll_val))

        else:
            mainloop_do(roll_gauge.set_from_file, "assets/outside-range/roll_outside_range_0.png")

        time.sleep(REFRESH_RATE)


def mainloop_do(callback, *args, **kwargs):

    """ Screen update loop - adds process to main thread """

    def cb(_none):
        callback(*args, **kwargs)
        return False

    Gdk.threads_add_idle(GLib.PRIORITY_DEFAULT, cb, None)


class Handler:

    """ Handler Class - Takes care of events and signals """

    def __init__(self):
        # Object imports
        self.preference_window = builder.get_object("pref_window")
        self.about_dialog = builder.get_object("about_dialog")

        self.pitch_roll_toggle = builder.get_object("pitch_roll_toggle")
        self.pitch_label = builder.get_object("pitch_label")
        self.roll_label = builder.get_object("roll_label")

        # Thread variables
        self.pos_data_update_thread_running = False

        # Start Positional Gyro Data
        self.pref_pos_data_toggle()

    def pref_pos_data_toggle(self, *args):
        if not self.pos_data_update_thread_running:
            threading.Thread(target=self.pos_data_update).start()

    def pos_data_update(self):

        """ Updates positional data labels on screen """

        self.pos_data_update_thread_running = True

        # Wait for gtk main loop
        while Gtk.main_level() == 0:
            time.sleep(REFRESH_RATE)

        while self.pitch_roll_toggle.get_active() and Gtk.main_level() != 0:

            # Pitch and roll values
            pitch_val, roll_val = get_gyro_pos()

            pitch_val = pitch_val * RAD_TO_DEG
            roll_val = roll_val * RAD_TO_DEG

            pitch_val = "Pitch: {0}°".format(int(pitch_val))
            roll_val = "Roll: {0}°".format(int(roll_val))

            # Update screen
            mainloop_do(self.pitch_label.set_text, pitch_val)
            mainloop_do(self.roll_label.set_text, roll_val)

            time.sleep(.2)

        self.pitch_label.set_text("Pitch")
        self.roll_label.set_text("Roll")

        self.pos_data_update_thread_running = False

    def pref_window_hide(self, *args):
        self.preference_window.hide()

    @staticmethod
    def pref_altitude_toggle(*args):
        
        """ Place holder method for Altitude """
        
        print("Test")

    @staticmethod
    def gyroscope_calibrate(*args):
        level_gyro()

    def about_dialog_show(self, *args):
        self.about_dialog.run()
        self.about_dialog.hide()

    def pref_window_show(self, *args):
        self.preference_window.show_all()

    def pref_window_close(self, *args):
        self.preference_window.hide()
        return True

    @staticmethod
    def quit_program(*args):
        Gtk.main_quit()

# Builder Imports
builder = Gtk.Builder()
builder.add_from_file("lib/tiltometer.xml")
builder.connect_signals(Handler())

# Main window
main_window = builder.get_object("main_window")
main_window.fullscreen()
invisible_cursor = Gdk.Cursor.new(Gdk.CursorType.BLANK_CURSOR)
main_window.get_window().set_cursor(invisible_cursor)
main_window.show_all()

# Main Loop and Threads
threading.Thread(target=update_position_gauges).start()
Gtk.main()
