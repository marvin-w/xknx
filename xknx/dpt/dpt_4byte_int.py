"""
Implementation of Basic KNX 4-Byte Signed and Unsigned Values.

They correspond the following KNX DPTs:
    12.yyy 4-byte/octet unsigned value, i.e. pulse counter
    13.yyy 4-byte/octet signed (2's complement), i.e. flow, energy
"""

import struct

from xknx.exceptions import ConversionError

from .dpt import DPTBase


class DPT4ByteUnsigned(DPTBase):
    """
    Abstraction for KNX 4 Byte "32-bit unsigned".

    DPT 12.***
    """

    value_min = 0
    value_max = 4294967295
    dpt_main_number = 12
    dpt_sub_number = None
    value_type = "4byte_unsigned"
    unit = ""
    resolution = 1
    payload_length = 4

    _struct_format = ">I"

    @classmethod
    def from_knx(cls, raw):
        """Parse/deserialize from KNX/IP raw data."""
        cls.test_bytesarray(raw)

        try:
            return struct.unpack(cls._struct_format, bytes(raw))[0]
        except struct.error:
            raise ConversionError("Could not parse %s" % cls.__name__, raw=raw)

    @classmethod
    def to_knx(cls, value):
        """Serialize to KNX/IP raw data."""
        try:
            knx_value = int(value)
            if not cls._test_boundaries(knx_value):
                raise ValueError
            return tuple(struct.pack(cls._struct_format, knx_value))
        except (ValueError, struct.error):
            raise ConversionError("Could not serialize %s" % cls.__name__, value=value)

    @classmethod
    def _test_boundaries(cls, value):
        """Test if value is within defined range for this object."""
        return cls.value_min <= value <= cls.value_max


class DPT4ByteSigned(DPT4ByteUnsigned):
    """
    Abstraction for KNX 4 Byte "32-bit signed".

    DPT 13.***
    """

    value_min = -2147483648
    value_max = 2147483647
    dpt_main_number = 13
    dpt_sub_number = None
    value_type = "4byte_signed"
    unit = ""
    resolution = 1

    _struct_format = ">i"


class DPTValue4Count(DPT4ByteSigned):
    """DPT 13.001 DPT_Value_4_Count (pulse)."""

    dpt_main_number = 13
    dpt_sub_number = 1
    value_type = "pulse_4byte"
    unit = "pulses"


class DPTFlowRateM3H(DPT4ByteSigned):
    """DPT 13.002 DPT_FlowRate_m3/h (m³/h)."""

    dpt_main_number = 13
    dpt_sub_number = 2
    value_type = "flow_rate_m3h"
    unit = "m³/h"
    resolution = 0.0001


class DPTActiveEnergy(DPT4ByteSigned):
    """DPT 13.010 DPT_ActiveEnergy (Wh)."""

    dpt_main_number = 13
    dpt_sub_number = 10
    value_type = "active_energy"
    unit = "Wh"


class DPTApparantEnergy(DPT4ByteSigned):
    """DPT 13.011 DPT_ActiveEnergy (VAh)."""

    dpt_main_number = 13
    dpt_sub_number = 11
    value_type = "apparant_energy"
    unit = "VAh"


class DPTReactiveEnergy(DPT4ByteSigned):
    """DPT 13.012 DPT_ActiveEnergy (VARh)."""

    dpt_main_number = 13
    dpt_sub_number = 12
    value_type = "reactive_energy"
    unit = "VARh"


class DPTActiveEnergykWh(DPT4ByteSigned):
    """DPT 13.013 DPT_ActiveEnergy_kWh (kWh)."""

    dpt_main_number = 13
    dpt_sub_number = 13
    value_type = "active_energy_kwh"
    unit = "kWh"


class DPTApparantEnergykVAh(DPT4ByteSigned):
    """DPT 13.014 DPT_ActiveEnergy_kVAh (kVAh)."""

    dpt_main_number = 13
    dpt_sub_number = 14
    value_type = "apparant_energy_kvah"
    unit = "kVAh"


class DPTReactiveEnergykVARh(DPT4ByteSigned):
    """DPT 13.015 DPT_ActiveEnergy (kVARh)."""

    dpt_main_number = 13
    dpt_sub_number = 15
    value_type = "reactive_energy_kvarh"
    unit = "kVARh"


class DPTLongDeltaTimeSec(DPT4ByteSigned):
    """DPT 13.100 DPT_LongDeltaTimeSec (s)."""

    dpt_main_number = 13
    dpt_sub_number = 100
    value_type = "long_delta_timesec"
    unit = "s"
