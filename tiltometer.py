"""
5/24/2017
This program reads data from a motion processor, calculates the angular position from the
data and displays the vehicle information graphically.
---------------------------------------------------------
MIT LICENCE
"""

import time
import gi
import threading
from ReadIMU import get_pitch, get_roll
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib

RAD_TO_DEG = 57.29578  # Math constant for RADIAN -> DEGREE conversion

start_pitch = get_pitch()
start_roll = get_roll()


def truncate(f, n):

    """ Truncates a float f to n decimal places without rounding """

    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])


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
            mainloop_do(pitch_gauge.set_from_file, "Assets/pitch-gauge/pitch-gauge%d.png" % int(pitch_val))

        else:
            mainloop_do(pitch_gauge.set_from_file, "Assets/outside-range/pitch_outside_range_0.png")

        if int(roll_val) in range(-50, 51):
            mainloop_do(roll_gauge.set_from_file, "Assets/roll-gauge/roll-gauge%d.png" % int(roll_val))

        else:
            mainloop_do(roll_gauge.set_from_file, "Assets/outside-range/roll_outside_range_0.png")

        time.sleep(.05)


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
            time.sleep(.01)

        while self.pitch_roll_toggle.get_active() and Gtk.main_level() != 0:

            # Pitch and roll values
            pitch_val, roll_val = get_gyro_pos()

            pitch_val = "Pitch: " + str(truncate(pitch_val, 3))
            roll_val = "Roll: " + str(truncate(roll_val, 3))

            # Update screen
            mainloop_do(self.pitch_label.set_text, pitch_val)
            mainloop_do(self.roll_label.set_text, roll_val)

            time.sleep(.05)

        self.pitch_label.set_text("Pitch")
        self.roll_label.set_text("Roll")

        self.pos_data_update_thread_running = False

    def pref_window_hide(self, *args):
        self.preference_window.hide()

    @staticmethod
    def pholder_toggle(*args):
        
        """ Place holder method for TBD preference button """
        
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
builder.add_from_file("tiltometer.xml")
builder.connect_signals(Handler())

# Main window
main_window = builder.get_object("main_window")
main_window.fullscreen()
main_window.show_all()

# Main Loop and Threads
threading.Thread(target=update_position_gauges).start()
Gtk.main()
