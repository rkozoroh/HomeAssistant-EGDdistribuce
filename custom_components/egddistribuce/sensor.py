import datetime
import voluptuous as vol

from . import downloader
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.components.sensor import PLATFORM_SCHEMA

DOMAIN = 'egddistribuce'
CONF_NAME = "name"

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_NAME): cv.string,
    })
}, extra=vol.ALLOW_EXTRA)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
       vol.Required(CONF_NAME): cv.string,
    }
)

#async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
#    name = config[DOMAIN][CONF_NAME]
#    async_add_entities([TimestampSensor(name)])
#)

def setup_platform(hass, config, add_entities, discovery_info=None):
    name = config.get(CONF_NAME)
    ents = []
    ents.append(TimestampSensor(name))
    add_entities(ents)

class TimestampSensor(Entity):
    def __init__(self, name):
        self._name = name
        self._state = None

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def device_class(self):
        return SensorDeviceClass.TIMESTAMP

    async def async_update(self):
        self._state = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
