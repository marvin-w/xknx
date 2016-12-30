from .device import Device
from .telegram import Telegram
from .address import Address
import time

class CouldNotParseDimmerTelegram(Exception):
    pass

class Dimmer(Device):
    def __init__(self, xknx, name, config):
        Device.__init__(self, xknx, name)
        self.group_address_switch = Address(config.get("group_address_switch"))
        self.group_address_dimm = Address(config.get("group_address_dimm"))
        self.group_address_dimm_feedback = Address(config.get("group_address_dimm_feedback"))

        self.state = False
        self.brightness = 0

    def has_group_address(self, group_address):
            return ( self.group_address_switch == group_address ) or (self.group_address_dimm == group_address ) or (self.group_address_dimm_feedback == group_address )

    def __str__(self):
        return "<Dimmer group_address_switch={0}, group_address_dimm={0}, group_address_dimm_feedback={2},name={3}>".format(self.group_address_switch,self.group_address_dimm,self.group_address_dimm_feedback,self.name)

    def set_internal_state(self, state):
        if state != self.state:
            self.state = state
            self.after_update_callback(self)

    def set_internal_brightness(self, brightness):
        if brightness != self.brightness:
            self.brightness = brightness
            self.after_update_callback(self)


    def send(self, group_address, payload = None):
        telegram = Telegram()
        telegram.group_address=group_address

        if isinstance(payload, list):
            for p in payload:
                telegram.payload.append(p)
        elif isinstance(payload, int):
                telegram.payload.append(payload)
        elif payload == None:
                telegram.payload = None
        else:
            print("Cannot understand payload")

        self.xknx.telegrams.put(telegram)

    def set_on(self):
        self.send(self.group_address_switch, [1])
        self.set_internal_state(True)

    def set_off(self):
        self.send(self.group_address_switch, [0])
        self.set_internal_state(False)

    def set_brightness(self, brightness):
        self.send(self.group_address_dimm_feedback, [0x80,brightness] )
        self.set_internal_brightness(brightness)

    def request_state(self):
        self.send(self.group_address_switch)
        if not self.group_address_dimm_feedback.is_set():
            print("group_address_dimm_feedback not defined for device {0}".format(self.get_name()))
            return

        # We have to request both ..
        self.send(self.group_address_dimm_feedback)
        self.send(self.group_address_switch)

    def process(self,telegram):
        if telegram.group_address == self.group_address_switch:
            self._process_state(telegram)
        elif telegram.group_address == self.group_address_dimm_feedback:
            self._process_dimm(telegram) 

    def _process_dimm(self,telegram):
        if len(telegram.payload) != 2:
            raise(CouldNotParseDimmerTelegram)

        # telegram.payload[0] is 0x40 if state was requested, 0x80 if state of shutter was changed
        self.set_internal_brightness(telegram.payload[1])

    def _process_state(self,telegram):

        if len(telegram.payload) != 1:
            raise(CouldNotParseDimmerTelegram)

        if telegram.payload[0] == 0 :
            self.set_internal_state(False)
        elif telegram.payload[0] == 1 :
            self.set_internal_state(True)
        else:
            print("Could not parse payload for binary output %s".format( telegram.payload ))
