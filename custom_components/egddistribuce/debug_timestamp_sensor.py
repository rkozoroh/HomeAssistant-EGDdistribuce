from datetime import timedelta, datetime, date
import sys
from pathlib import Path
from homeassistant.helpers.entity import Entity
from homeassistant.components.binary_sensor import BinarySensorEntity
import requests

# Add the current directory to the Python path
current_dir = Path(__file__).resolve().parent
sys.path.append(str(current_dir))

import downloader

#from egddistribuce.downloader import



class EgdDistribuce(BinarySensorEntity):
    def __init__(self, name, psc, codeA, codeB, codeDP):
        """Initialize the sensor."""
        self._name = name
        self.psc = psc
        self.codeA = codeA
        self.codeB = codeB
        self.codeDP = codeDP
        self.responseRegionJson = "[]"
        self.responseHDOJson ="[]"
        self.region ="[]"
        self.status= False
        self.HDO_Cas_Od = []
        self.HDO_Cas_Do = []
        self.update()
        self._attributes = {}
        self.HDO_next_from = None
        self.HDO_next_to = None

    @property
    def name(self):
        return self._name

    @property
    def icon(self):
        if self.status == True:
            return "mdi:transmission-tower"
        else:
            return "mdi:power-off"
    
    @property
    def is_on(self):
        datum = datetime.now()
        #datum = datetime(2023, 5, 19, 17, 30, 0)
        self.status, self.HDO_Cas_Od,self.HDO_Cas_Do, self.HDO_next_from, self.HDO_next_to  = downloader.parseHDO(self.responseHDOJson,self.region,self.codeA,self.codeB,self.codeDP,datum) 
        return self.status

    @property
    def extra_state_attributes(self):
        """Return extra state attributes."""
        attributes = dict(
            HDOTimes = self.get_times(),
            HDOTimesHTML = self.get_times().replace('\n | ', '<br/>'),
            HDO_next_from = self.HDO_next_from,
            HDO_next_to = self.HDO_next_to,
        )
        return attributes
 
    @property
    def should_poll(self):
        return True

    @property
    def available(self):
        return self.last_update_success

    @property
    def device_class(self):
        return ''

    def get_times(self):
        i=0
        timeReport=""
        for n in self.HDO_Cas_Od:
            timeReport = timeReport + '{}'.format(n) + ' - ' +self.HDO_Cas_Do[i] + '\n | '
            i += 1
        return timeReport[:-3]

    #@Throttle(MIN_TIME_BETWEEN_SCANS)
    def update(self):
        responseRegion = requests.get(downloader.getRegion(), verify=False)
        if responseRegion.status_code == 200:
            self.responseRegionJson = responseRegion.json() 
            self.region=downloader.parseRegion(self.responseRegionJson,self.psc)
            responseHDO = requests.get(downloader.getHDO(), verify=False)
            if responseHDO.status_code == 200:
                self.responseHDOJson = responseHDO.json()
                self.last_update_success = True
        else:
            self.last_update_success = False
        


if __name__ == '__main__':
    sensor = EgdDistribuce('Test Sensor','66462','1','4','05')
    sensor.update()
 
    print(f"Sensor name: {sensor.name}")
    print(f"Sensor state: {sensor.is_on}")
    print(f"Sensor attributes: {sensor.extra_state_attributes}")

