#Libraries
import RPi.GPIO as GPIO
# from homeassistant.components import rpi_gpio
import time

#GPIO Mode (BOARD / BCM)

#set GPIO Pins
# GPIO_TRIGGER = 18
# GPIO_ECHO = 24

#set GPIO direction (IN / OUT)
# GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
# GPIO.setup(GPIO_ECHO, GPIO.IN)


COLORGREEN = 'GREEN'
COLORAMBER = 'AMBER'
COLORRED = 'RED'

#preferences
# compensation=0
depth=75
levelamber = 30
levelred = 65


class ultrasonic(object):

    def __init__(self, gpio_trigger, gpio_echo, depth, compensation=0):
        self.distance = None
        self.startTime = None
        self.distance = None
        self.gpio_trigger = gpio_trigger
        self.gpio_echo = gpio_echo
        self.depth = depth
        self.compensation = compensation

        GPIO.setmode(GPIO.BCM)

        #set GPIO direction (IN / OUT)
        # rpi_gpio.setup_output(self.gpio_trigger)
        # rpi_gpio.setup_input(self.gpio_echo)
        GPIO.setup(self.gpio_trigger, GPIO.OUT)
        GPIO.setup(self.gpio_echo, GPIO.IN)

    def retrieveDistance(self):
        # set Trigger to HIGH
        # rpi_gpio.write_output(self.gpio_trigger, True)
        GPIO.output(self.gpio_trigger, True)
     
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        # rpi_gpio.write_output(self.gpio_trigger, False)
        GPIO.output(self.gpio_trigger, False)

        # self.startTime = time.time()
        self.startTime = time.time()
        startElapsed = time.perf_counter()
        # StopTime = time.time()
        stopElapsed = time.perf_counter()
     
        # save StartTime
        # while rpi_gpio.read_input(self.gpio_echo) == 0:
        while GPIO.input(self.gpio_echo) == 0 and (time.perf_counter() - startElapsed) < 30:
            # self.startTime = time.time()
            startElapsed = time.perf_counter()
        if (time.perf_counter() - startElapsed) >= 30:
            pass
            #TODO: Raise an Error
     
        # save time of arrival
        # while rpi_gpio.read_input(self.gpio_echo) == 1:
        while GPIO.input(self.gpio_echo) == 1 and (time.perf_counter() - stopElapsed) < 30:
            # StopTime = time.time()
            stopElapsed = time.perf_counter()
        if (time.perf_counter() - stopElapsed) >= 30:
            pass
            #TODO: Raise an Error
     
        # time difference between start and arrival
        TimeElapsed = stopElapsed - startElapsed
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        disdistance = (TimeElapsed * 34300) / 2 + self.compensation
        self.distance = round(disdistance, 0)

    def getDistance(self):
        if self.distance is None:
            self.retrieveDistance()

        return self.distance

    def waterLevel(self):
        if self.distance is None:
            self.retrieveDistance()

        return self.depth - self.distance

    def waterLevelPercent(self):
        """Return the water level in percentage."""
        if self.distance is None:
            self.retrieveDistance()

        return round((self.depth - self.distance) / self.depth * 100 ,0)
