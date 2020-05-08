#!/usr/bin/env python3

import threading
import dialog
import glob
import uinput
from evdev import InputDevice, ecodes as e
from subprocess import Popen, call, PIPE
from os import path as op


BUTTON_MAP = {
    e.BTN_DPAD_UP: uinput.KEY_UP,
    e.BTN_DPAD_DOWN: uinput.KEY_DOWN,
    e.BTN_DPAD_RIGHT: uinput.KEY_RIGHT,
    e.BTN_DPAD_LEFT: uinput.KEY_LEFT,
    e.BTN_EAST: uinput.KEY_ENTER,
    e.BTN_SOUTH: uinput.KEY_ESC,
    e.BTN_NORTH: uinput.KEY_BACKSPACE,
    e.BTN_WEST: uinput.KEY_TAB,
    e.BTN_TL: uinput.KEY_PAGEUP,
    e.BTN_TR: uinput.KEY_PAGEDOWN,
}


def _input_loop(indev, outdev, ctx):
    while 1:
        for ev in indev.read_loop():
            if ev.value == 1:
                key = BUTTON_MAP.get(ev.code)
                if ctx.enable_kb:
                    try:
                        outdev.emit_click(key)
                    except:
                        pass

def map_kbd(ctx):
    outdev = uinput.Device([v for k, v in BUTTON_MAP.items()])
    indev = InputDevice("/dev/input/by-path/platform-odroidgo2-joypad-event-joystick")

    t = threading.Thread(target=_input_loop, args=(indev, outdev, ctx))
    t.setDaemon(True)
    t.start()
    return t


class RetroLauncher(object):
    def __init__(self):
        self.enable_kb = True

        self._dialog = dialog.Dialog(dialog="dialog")
        self._dialog.set_background_title("{:^58s}".format(".-=o=-. Retro Launcher .-=o=-."))

        self._input_thread = map_kbd(self)

    def main_loop(self):
        while 1:
            cmds = self._get_cmds()

            items = [x for x in sorted(cmds.keys()) if x != "RetroLauncher"]
            items += [""]  # separator
            items += [
                "System Update",
                "Restart Retro Launcher",
                "Reboot",
                "Shutdown",
            ]

            code, tag = self._dialog.menu("Main Menu", choices=[(x, "") for x in items])

            if code == "esc" or tag == "Restart Retro Launcher":
                break
            elif tag in cmds:
                self._run_command(cmds[tag])
            elif tag == "System Update":
                self._pacman_update()
            elif tag == "Reboot":
                self._run_command("systemctl reboot", redirect=False)
            elif tag == "Shutdown":
                self._run_command("systemctl poweroff", redirect=False)

    @staticmethod
    def _get_cmds():
        cmds = dict()
        for path in glob.glob("/roms/sh/*"):
            basename = op.splitext(op.basename(path))[0]
            cmds[basename] = path
        return cmds

    def _run_command(self, cmd, redirect=True):
        self.enable_kb = False
        self._dialog.clear()
        if redirect:
            cmd += " &>> /tmp/retrolauncher.log"
        try:
            call(cmd, shell=True)
        finally:
            self.enable_kb = True


    def _choose_launcher(self):
        pass

    def _pacman_update(self):
        p = Popen("sudo pacman -Syu --noconfirm", stdout=PIPE, close_fds=True, shell=True)
        self._dialog.programbox(fd=p.stdout.fileno(), text="Pacman Update")
        p.wait()
        p.stdout.close()


if __name__ == "__main__":
    rl = RetroLauncher()
    rl.main_loop()
