# -*- coding: utf-8 -*-

# https://www.decentlab.com/products/indoor-ambiance-monitor-including-co2-tvoc-and-motion-sensor-for-lorawan

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import struct
from base64 import binascii

PROTOCOL_VERSION = 2

# Name
# DL-IAM    70B3D57BA0000DE0, 70B3D57BA0000DE1, 70B3D57BA0000DE2
# DL-SHT21  0004A30B002426AF
# DL-ATM41  0004A30B00239E55
# DL-TRS12  70B3D57BA0001215


def get_SENSOR(EUI):

    # DL-IAM Sensor   70B3D57BA0000DE0, 70B3D57BA0000DE1, 70B3D57BA0000DE2
    if EUI == "70B3D57BA0000DE0" or EUI == "70B3D57BA0000DE1" or EUI == "70B3D57BA0000DE2":

        SENSORS = [
            {"length": 1,
             "values": [{"name": "Battery voltage",
                         "convert": lambda x: x[0] / 1000,
                         "unit": "V"}]},
            {"length": 2,
             "values": [{"name": "Air temperature",
                         "convert": lambda x: 175 * x[0] / 65535 - 45,
                         "unit": "°C"},
                        {"name": "Air humidity",
                         "convert": lambda x: 100 * x[1] / 65535,
                         "unit": "%"}]},
            {"length": 1,
             "values": [{"name": "Barometric pressure",
                         "convert": lambda x: x[0] * 2,
                         "unit": "Pa"}]},
            {"length": 2,
             "values": [{"name": "Ambient light (visible + infrared)",
                         "convert": lambda x: x[0]},
                        {"name": "Ambient light (infrared)",
                         "convert": lambda x: x[1]},
                        {"name": "Illuminance",
                         "convert": lambda x: max(max(1.0 * x[0] - 1.64 * x[1], 0.59 * x[0] - 0.86 * x[1]), 0) * 1.5504,
                         "unit": "lx"}]},
            {"length": 3,
             "values": [{"name": "CO2 concentration",
                         "convert": lambda x: x[0] - 32768,
                         "unit": "ppm"},
                        {"name": "CO2 sensor status",
                         "convert": lambda x: x[1]},
                        {"name": "Raw IR reading",
                         "convert": lambda x: x[2]}]},
            {"length": 1,
             "values": [{"name": "Activity counter",
                         "convert": lambda x: x[0]}]},
            {"length": 1,
             "values": [{"name": "Total VOC",
                         "convert": lambda x: x[0],
                         "unit": "ppb"}]}
        ]

    # DL-LP8P Sensor 0004A30B001F97AA
    elif EUI == "0004A30B001F97AA":

        SENSORS = [
            {"length": 2,
             "values": [{"name": "Air temperature",
                         "convert": lambda x: 175.72 * x[0] / 65536 - 46.85,
                         "unit": "°C"},
                        {"name": "Air humidity",
                         "convert": lambda x: 125 * x[1] / 65536 - 6,
                         "unit": "%"}]},
            {"length": 2,
             "values": [{"name": "Barometer temperature",
                         "convert": lambda x: (x[0] - 5000) / 100,
                         "unit": "°C"},
                        {"name": "Barometric pressure",
                         "convert": lambda x: x[1] * 2,
                         "unit": "Pa"}]},
            {"length": 8,
             "values": [{"name": "CO2 concentration",
                         "convert": lambda x: x[0] - 32768,
                         "unit": "ppm"},
                        {"name": "CO2 concentration LPF",
                         "convert": lambda x: x[1] - 32768,
                         "unit": "ppm"},
                        {"name": "CO2 sensor temperature",
                         "convert": lambda x: (x[2] - 32768) / 100,
                         "unit": "°C"},
                        {"name": "Capacitor voltage 1",
                         "convert": lambda x: x[3] / 1000,
                         "unit": "V"},
                        {"name": "Capacitor voltage 2",
                         "convert": lambda x: x[4] / 1000,
                         "unit": "V"},
                        {"name": "CO2 sensor status",
                         "convert": lambda x: x[5]},
                        {"name": "Raw IR reading",
                         "convert": lambda x: x[6]},
                        {"name": "Raw IR reading LPF",
                         "convert": lambda x: x[7]}]},
            {"length": 1,
             "values": [{"name": "Battery voltage",
                         "convert": lambda x: x[0] / 1000,
                         "unit": "V"}]}
        ]

    # DL-SHT21 Sensor 0004A30B002426AF, 0004A30B00241452
    elif EUI == "0004A30B002426AF" or EUI == "0004A30B00241452":

        SENSORS = [
            {"length": 2,
             "values": [{"name": "Air temperature",
                         "convert": lambda x: 175.72 * x[0] / 65536 - 46.85,
                         "unit": "°C"},
                        {"name": "Air humidity",
                         "convert": lambda x: 125 * x[1] / 65536 - 6,
                         "unit": "%"}]},
            {"length": 1,
             "values": [{"name": "Battery voltage",
                         "convert": lambda x: x[0] / 1000,
                         "unit": "V"}]}
        ]

    # DL-ATM41 Sensor 0004A30B00239E55
    elif EUI == "0004A30B00239E55":

        SENSORS = [
            {"length": 17,
             "values": [{"name": "Solar radiation",
                         "convert": lambda x: x[0] - 32768,
                         "unit": "W⋅m⁻²"},
                        {"name": "Precipitation",
                         "convert": lambda x: (x[1] - 32768) / 1000,
                         "unit": "mm"},
                        {"name": "Lightning strike count",
                         "convert": lambda x: x[2] - 32768},
                        {"name": "Lightning average distance",
                         "convert": lambda x: x[3] - 32768,
                         "unit": "km"},
                        {"name": "Wind speed",
                         "convert": lambda x: (x[4] - 32768) / 100,
                         "unit": "m⋅s⁻¹"},
                        {"name": "Wind direction",
                         "convert": lambda x: (x[5] - 32768) / 10,
                         "unit": "°"},
                        {"name": "Maximum wind speed",
                         "convert": lambda x: (x[6] - 32768) / 100,
                         "unit": "m⋅s⁻¹"},
                        {"name": "Air temperature",
                         "convert": lambda x: (x[7] - 32768) / 10,
                         "unit": "°C"},
                        {"name": "Vapor pressure",
                         "convert": lambda x: (x[8] - 32768) / 100,
                         "unit": "kPa"},
                        {"name": "Atmospheric pressure",
                         "convert": lambda x: (x[9] - 32768) / 100,
                         "unit": "kPa"},
                        {"name": "Relative humidity",
                         "convert": lambda x: (x[10] - 32768) / 10,
                         "unit": "%"},
                        {"name": "Sensor temperature (internal)",
                         "convert": lambda x: (x[11] - 32768) / 10,
                         "unit": "°C"},
                        {"name": "X orientation angle",
                         "convert": lambda x: (x[12] - 32768) / 10,
                         "unit": "°"},
                        {"name": "Y orientation angle",
                         "convert": lambda x: (x[13] - 32768) / 10,
                         "unit": "°"},
                        {"name": "Compass heading",
                         "convert": lambda x: x[14] - 32768,
                         "unit": "°"},
                        {"name": "North wind speed",
                         "convert": lambda x: (x[15] - 32768) / 100,
                         "unit": "m⋅s⁻¹"},
                        {"name": "East wind speed",
                         "convert": lambda x: (x[16] - 32768) / 100,
                         "unit": "m⋅s⁻¹"}]},
            {"length": 1,
             "values": [{"name": "Battery voltage",
                         "convert": lambda x: x[0] / 1000,
                         "unit": "V"}]}
        ]

    # DL-TRS12 Sensor 70B3D57BA0001215
    elif EUI == "70B3D57BA0001215":

        SENSORS = [
            {"length": 3,
             "values": [{"name": "Dielectric permittivity",
                         "convert": lambda x: pow(0.000000002887 * pow(x[0]/10, 3) - 0.0000208 * pow(x[0]/10, 2) + 0.05276 * (x[0]/10) - 43.39, 2)},
                        {"name": "Volumetric water content",
                         "convert": lambda x: x[0]/10 * 0.0003879 - 0.6956,
                         "unit": "m³⋅m⁻³"},
                        {"name": "Soil temperature",
                         "convert": lambda x: (x[1] - 32768) / 10,
                         "unit": "°C"},
                        {"name": "Electrical conductivity",
                         "convert": lambda x: x[2],
                         "unit": "µS⋅cm⁻¹"}]},
            {"length": 1,
             "values": [{"name": "Battery voltage",
                         "convert": lambda x: x[0] / 1000,
                         "unit": "V"}]}
        ]

    return (SENSORS)


def decode(msg, EUI, hex=False):
    """msg: payload as one of hex string, list, or bytearray"""

    bytes_ = bytearray(binascii.a2b_hex(msg) if hex else msg)
    version = bytes_[0]

    if version != PROTOCOL_VERSION:
        raise ValueError(
            "protocol version {} doesn't match v2".format(version))

    devid = struct.unpack(">H", bytes_[1:3])[0]
    bin_flags = bin(struct.unpack(">H", bytes_[3:5])[0])
    flags = bin_flags[2:].zfill(struct.calcsize(">H") * 8)[::-1]

    words = [struct.unpack(">H", bytes_[i:i + 2])[0]
             for i
             in range(5, len(bytes_), 2)]

    cur = 0
    result = {"Device ID": devid, "Protocol version": version}

    SENSORS = get_SENSOR(EUI)

    for flag, sensor in zip(flags, SENSORS):
        if flag != "1":
            continue

        x = words[cur:cur + sensor["length"]]
        cur += sensor["length"]
        for value in sensor["values"]:
            if "convert" not in value:
                continue

            result[value["name"]] = {"value": value["convert"](x),
                                     "unit": value.get("unit", None)}

    return(result)


"""
import pprint

data = b"0208a400038000800080008000810d86dc828a80aa808aa70582c680a68009800780007ef480150b48"
EUI = "70B3D57BA0001215"

pprint.pprint(decode(data, EUI, hex=True))
print("")
#"""
