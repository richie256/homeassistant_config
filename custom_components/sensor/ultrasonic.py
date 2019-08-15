import logging

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import LENGTH_CENTIMETERS
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv

# from .ultrasonic_distance import ultrasonic
# import pyultrasonic

"""Icon helper methods."""
from typing import Optional

REQUIREMENTS = ['pyultrasonic==0.1.2']

_LOGGER = logging.getLogger(__name__)

CONF_DEPTH = 'depth'  # type: str
CONF_GPIO_TRIGGER_PIN = 'trigger_pin'  # type: str
CONF_GPIO_ECHO_PIN = 'echo_pin'  # type: str
CONF_COMPENSATION = 'compensation'  # type: str
DEFAULT_COMPENSATION = 0

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_DEPTH): cv.positive_int,
    vol.Required(CONF_GPIO_TRIGGER_PIN): cv.positive_int,
    vol.Required(CONF_GPIO_ECHO_PIN): cv.positive_int,
    vol.Optional(CONF_COMPENSATION, default=DEFAULT_COMPENSATION): cv.small_float,
})

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Setup the sensor platform."""

    from pyultrasonic import UltrasonicSensorModule

    # Test if passed in info (user/pass/host etc.) works.

    # Distance or depth
    depth = config.get(CONF_DEPTH)
    compensation = config.get(CONF_COMPENSATION)

    # Define GPIO to use on Pi
    trigger_pin = config.get(CONF_GPIO_TRIGGER_PIN)
    echo_pin = config.get(CONF_GPIO_ECHO_PIN)

    pump = UltrasonicSensorModule(trigger_pin, echo_pin, depth, compensation)
    # add_devices([UltrasonicSensor(trigger_pin, echo_pin, depth, compensation)])
    add_entities([UltrasonicSensor(pump)])

class UltrasonicSensor(Entity):
    """Ultrasonic Measurement."""

    def __init__(self, pump):
        """Initialize the sensor."""
        self.pump = pump
        self._name = 'Ultrasonic Sensor'
        self._state = None
        #self.depth = depth
        #self.compensation = compensation

        #self.pump = ultrasonic(trigger_pin, echo_pin, self.depth, self.compensation)
        # self.distance = pump.getDistance()
        self.pump.retrieveDistance()
        self._state = self.pump.getDistance()

    @property
    def unique_id(self):
        """Return a unique ID."""
        return 'ultrasonic.sensor'

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Sump pump level'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self):
        """
        'mdi:circle-outline'
        'mdi:circle-slice-1'
        'mdi:circle-slice-2'
        'mdi:circle-slice-3'
        'mdi:circle-slice-4'
        'mdi:circle-slice-5'
        'mdi:circle-slice-6'
        'mdi:circle-slice-7'
        'mdi:circle-slice-8'
        'mdi:alert-circle'
        """
        return 'mdi:circle-slice-8'

        # return self.icon_for_water_level(self.pump.waterLevelPercent())

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return LENGTH_CENTIMETERS

    def update(self):
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        self.pump.retrieveDistance()
        self._state = self.pump.getDistance()

    def icon_for_water_level(water_level: Optional[int] = None) -> str:
        """
        return the icon representation of the water level progress
        """

        if water_level is None:
            return 'mdi:circle-outline'
        else:
            wperc = int(round((water_level / 10) - .01)) * 10

        if wperc >= 90:
            icon = 'mdi:alert-circle'
        elif wperc < 10:
            icon = 'mdi:circle-outline'
        else:
            # icon = x
            # icon = (wperc/10)
            icon = 'mdi:circle-slice'
            icon += '-{}'.format(wperc / 10)

        return icon
