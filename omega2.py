# -*- coding: utf-8 -*-

import subprocess


class Omega2(object):
    def __init__(self):
        self.version = self.get_omega_version()
        self.led_path = "/sys/class/leds/%s:amber:system/" % self.version
        self.RGB_pins = {'R': '17', 'G': '16', 'B': '15'}

        # https://docs.onion.io/omega2-docs/using-gpios.html#fast-gpio
        self._gpio_tool = ['gpioctl', 'fast-gpio'][1]

    def _shell(self, cmd_args, check_output=False):
        if check_output:
            return str(subprocess.check_output(cmd_args, shell=True))
        else:
            return subprocess.call(" ".join(cmd_args), shell=True)

    def get_omega_version(self):
        """Returns 'omega2' for Omega2 and 'omega2p' for Omega2+"""
        return self._shell(["uci", "get", "system.@led[0].sysfs"], True).split(":")[0]

    def led_control(self, state, delay_on=None, delay_off=None,
                    message=None, morse_speed=None):
        """
        Pass a boolean argument to turn the Omega2 LED on and off.
        Pass a string to trigger the LED mode.
        Available modes: 'none', 'mmc0', 'timer', 'default-on', 'netdev',
                         'transient', 'gpio', 'heartbeat', 'morse', 'oneshot'.
            - When switching to the 'timer' mode, pass the *delay_on* and
                *delay_off* arguments.
            - When switching to the 'morse' mode, pass the *message* argument.
        Details: https://docs.onion.io/omega2-docs/the-omega-led.html
        """
        if type(state) in {bool, int}:  # pylint: disable=C0123
            path = self.led_path + 'brightness'
            open(path, 'w').write('1' if state else '0')
            return bool(int(open(path, 'r').read()))
        elif type(state) is str:  # pylint: disable=C0123
            path = self.led_path + 'trigger'
            open(path, 'w').write(state)
            if state == 'timer':
                if delay_on is None or delay_off is None:
                    return "Pass the 'delay_on' and 'delay_off' arguments"
                open(self.led_path + 'delay_on', 'w').write(delay_on)
                open(self.led_path + 'delay_off', 'w').write(delay_off)
            elif state == 'morse':
                if message is None:
                    return "Pass the 'message' argument"
                open(self.led_path + 'message', 'w').write(message)
                if morse_speed is not None:
                    open(self.led_path + 'delay', 'w').write(morse_speed)
            return open(path, 'r').read()

    def RGB_init(self):
        """Configeure RGB LED pins as output"""
        for _, pin in self.RGB_pins.items():
            self.gpio_dir_out_1(pin)

    def RGB_color(self, red, green, blue):
        """Set color of RGB LED on Expansion Baord"""
        def s(color, val):
            if val >= 100: self.gpio_set(self.RGB_pins[color], 0)
            if val <= 0: self.gpio_set(self.RGB_pins[color], 1)
            if 0 < val < 100: self.gpio_pwm(self.RGB_pins[color], 100-val)
        s('R', red)
        s('G', green)
        s('B', blue)

    def gpio_dir_in(self, pin):
        """Set pin direction to INPUT and don't care about logical level"""
        command = 'dirin' if self._gpio_tool == 'gpioctl' else 'set-input'
        return not self._shell([self._gpio_tool, command, str(pin)])

    def gpio_dir_in_0(self, pin):
        """Set pin direction to INPUT and keep LOW logical level"""
        return not self._shell(["gpioctl", "dirin-low", str(pin)])

    def gpio_dir_in_1(self, pin):
        """Set pin direction to INPUT and keep HIGH logical level"""
        return not self._shell("gpioctl", "dirin-high" + str(pin))

    def gpio_dir_out(self, pin):
        """Set pin direction to OUTPUT and don't care about logical level"""
        command = 'dirout' if self._gpio_tool == 'gpioctl' \
            else 'set-output'
        return not self._shell([self._gpio_tool, command, str(pin)])

    def gpio_dir_out_0(self, pin):
        """Set pin direction to OUTPUT and keep LOW logical level"""
        return not self._shell(["gpioctl", "dirout-low", str(pin)])

    def gpio_dir_out_1(self, pin):
        """Set pin direction to OUTPUT and keep HIGH logical level"""
        return not self._shell(["gpioctl", "dirout-high", str(pin)])

    def gpio_get(self, pin):
        """Get the logical level on the pin"""
        command = 'get' if self._gpio_tool == 'gpioctl' else 'read'
        output = self._shell([self._gpio_tool, command, str(pin)], True)

        if self._gpio_tool == 'gpioctl':
            return True if 'HIGH' in output else \
                False if 'LOW' in output else None
        else:
            try:
                return bool(output.split(": ")[1])
            except IndexError:
                return None

    def gpio_set(self, pin, value):
        """Set the pin's logical level to value"""
        if self._gpio_tool == 'gpioctl':
            arg1, arg2 = 'set' if value else 'clear', str(pin)
        else:
            arg1, arg2 = str(pin), str(int(value))
        return not self._shell([self._gpio_tool, arg1, arg2])

    def gpio_pwm(self, pin, duty_cycle_percent):
        """Sends PWM on a pin"""
        return not self._shell(['fast-gpio', 'pwm', str(pin), '1000', 
                                str(duty_cycle_percent)])
