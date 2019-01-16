# -*- coding: utf-8 -*-
"""This file is part of the libsigrokdecode project.

Copyright (C) 2018-2019 Libor Gabaj <libor.gabaj@gmail.com>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <http://www.gnu.org/licenses/>.

"""

import sigrokdecode as srd


###############################################################################
# Enumeration classes for device parameters
###############################################################################
class GeneralCall:
    """Enumeration of parameters for general call on I2C bus."""

    (ADDRESS, WRITE, RESET) = (0x00, 0x04, 0x06)


class Address:
    """Enumeration of possible slave addresses.

    - Device address is determined by a pin, which the sensor's ADD0 pin is
      physically connected to.
    """

    (GND, VCC, SDA, SCL) = (0x48, 0x49, 0x4a, 0x4b)


class Register:
    """Enumeration of possible slave register addresses."""

    (TEMP, CONF, TLOW, THIGH) = range(0, 4)


class ConfigBits:
    """Enumeration of bits in the configuration register."""

    (
        # Byte 2 (LSB)
        EM,     # Extended mode
        AL,     # Alert
        CR0,    # Conversion rate
        CR1,
        # Byte 1 (MSB)
        SD,     # Shutdown mode
        TM,     # Thermostat mode
        POL,    # Polarity
        F0,     # Fault queue
        F1,
        R0,     # Converter resolution
        R1,
        OS,     # One-shot conversion
    ) = range(4, 16)


class CommonBits:
    """Enumeration of common bits."""

    (RESERVED,) = (0xff,)


class TempBits:
    """Enumeration of specific temperature register bits."""

    (EM, RESERVED) = (0, 1)


class Params:
    """Typical slave parameters."""

    (CUSTOM, POWERUP) = (0, 0x60a0)


###############################################################################
# Enumeration classes for annotations
###############################################################################
class AnnAddrs:
    """Enumeration of annotations for addresses."""

    (GC, GND, VCC, SDA, SCL) = range(0, 5)


class AnnRegs:
    """Enumeration of annotations for registers."""

    (
        RESET, DATA, CONF, TEMP, TLOW, THIGH,
    ) = range(AnnAddrs.SCL + 1, (AnnAddrs.SCL + 1) + 6)


class AnnBits:
    """Enumeration of annotations for configuration bits."""

    (
        RESERVED, DATA,
        EM, AL, CR0, SD, TM, POL, F0, R0, OS,
    ) = range(AnnRegs.THIGH + 1, (AnnRegs.THIGH + 1) + 11)


class AnnInfo:
    """Enumeration of annotations for formatted info."""

    (
        WARN, GRST, CHECK, WRITE, READ, CUSTOM, PWRUP,
        CONF, TEMP, TLOW, THIGH,
    ) = range(AnnBits.OS + 1, (AnnBits.OS + 1) + 11)


###############################################################################
# Parameters mapping
###############################################################################
addr_annots = {  # Convert value to annotation index
    GeneralCall.ADDRESS: AnnAddrs.GC,
    Address.GND: AnnAddrs.GND,
    Address.VCC: AnnAddrs.VCC,
    Address.SDA: AnnAddrs.SDA,
    Address.SCL: AnnAddrs.SCL,
}

reg_annots_gc = {  # Convert general call register value to annotation index
    GeneralCall.RESET: AnnRegs.RESET,
}

reg_annots = {  # Convert device register value to annotation index
    Register.CONF: AnnRegs.CONF,
    Register.TEMP: AnnRegs.TEMP,
    Register.TLOW: AnnRegs.TLOW,
    Register.THIGH: AnnRegs.THIGH,
}

prm_annots = {  # Convert device parameter value to annotation index
    Params.CUSTOM: AnnInfo.CUSTOM,
    Params.POWERUP: AnnInfo.PWRUP,
}

rates = {
    0b00: "0.25",
    0b01: "1",
    0b10: "4",
    0b11: "8",
}

radixes = {  # Convert radix option to format mask
    "Hex": "{:#02x}",
    "Dec": "{:#d}",
    "Oct": "{:#o}",
}

faults = {
    0b00: "1",
    0b01: "2",
    0b10: "4",
    0b11: "6",
}

resolutions = {
    0b11: "12",
}

temp_units = {  # Convert temperature scale option to measurement unit
    "Celsius": "°C",
    "Fahrenheit": "°F",
    "Kelvin": "K",
}


###############################################################################
# Parameters anotations definitions
###############################################################################
"""
- If a parameter has a value, the last item of an annotation list is used
  repeatedly without a value.
- If a parameter has measurement unit alongside with value, the last two items
  are used repeatedly without that measurement unit.
"""
addresses = {
    AnnAddrs.GC: ["General call", "GEN_CALL", "GC", "G"],
    AnnAddrs.GND: ["ADD0 grounded", "ADD0_GND", "AG"],
    AnnAddrs.VCC: ["ADD0 powered", "ADD0_VCC", "AV"],
    AnnAddrs.SDA: ["ADD0 to SDA", "ADD0_SDA", "AD"],
    AnnAddrs.SCL: ["ADD0 to SCL", "ADD0_SSCL", "AC"],
}

registers = {
    AnnRegs.RESET: ["Reset register", "Reset", "Rst", "R"],
    AnnRegs.DATA: ["Register content", "Content", "Data", "D"],
    AnnRegs.CONF: ["Configuration register", "Configuration", "Conf",
                   "Cfg", "C"],
    AnnRegs.TEMP: ["Temperature register", "Temperature", "Temp", "T"],
    AnnRegs.TLOW: ["Low alert register", "Low alert", "Tlow", "L"],
    AnnRegs.THIGH: ["High alert register", "High alert", "Thigh", "H"],
}

bits = {
    AnnBits.RESERVED: ["Reserved bit", "Reserved", "Rsvd", "R"],
    AnnBits.DATA: ["Data bit", "Data", "D"],
    AnnBits.EM: ["Extended mode", "EM", "E"],
    AnnBits.AL: ["Alert", "AL", "A"],
    AnnBits.CR0: ["Conversion rate bits", "Conversion rate", "Rate", "R"],
    AnnBits.SD: ["Shutdown mode", "Shutdown", "Shtd", "SD", "S"],
    AnnBits.TM: ["Thermostat mode", "Thermostat", "TMode", "TM", "T"],
    AnnBits.POL: ["Alert active", "Polarity", "Pol", "P"],
    AnnBits.F0: ["Consecutive faults", "Faults", "Flts", "F"],
    AnnBits.R0: ["Converter resolution", "Resolution", "Res", "R"],
    AnnBits.OS: ["One-shot conversion", "Oneshot", "OS", "O"],
}

info = {
    AnnInfo.WARN: ["Warnings", "Warn", "W"],
    AnnInfo.GRST: ["General reset", "GenReset", "GRST", "Rst", "R"],
    AnnInfo.CHECK: ["Slave presence check", "Slave check", "Check",
                    "Chk", "C"],
    AnnInfo.WRITE: ["Write", "Wr", "W"],
    AnnInfo.READ: ["Read", "Rd", "R"],
    AnnInfo.CUSTOM: ["Custom", "Cst", "C"],
    AnnInfo.PWRUP: ["Power-up reset", "PwrReset", "Pwr", "P"],
    AnnInfo.CONF: ["Configuration", "Conf", "Cfg", "C"],
    AnnInfo.TEMP: ["Measured temperature", "Temperature", "Temp", "T"],
    AnnInfo.TLOW: ["Low temperature limit", "Low limit", "Low", "L"],
    AnnInfo.THIGH: ["High temperature limit", "High limit", "High", "H"],
}


def create_annots():
    """Create a tuple with all annotation definitions."""
    annots = []
    # Addresses
    for attr, value in vars(AnnAddrs).items():
        if not attr.startswith('__'):
            annots.append(tuple(["addr-" + attr.lower(), addresses[value][0]]))
    # Registers
    for attr, value in vars(AnnRegs).items():
        if not attr.startswith('__'):
            annots.append(tuple(["reg-" + attr.lower(), registers[value][0]]))
    # Bits
    for attr, value in vars(AnnBits).items():
        if not attr.startswith('__'):
            annots.append(tuple(["bit-" + attr.lower(), bits[value][0]]))
    # Info
    for attr, value in vars(AnnInfo).items():
        if not attr.startswith('__'):
            annots.append(tuple(["info-" + attr.lower(), info[value][0]]))
    return tuple(annots)


###############################################################################
# Decoder
###############################################################################
class Decoder(srd.Decoder):
    """Protocol decoder for digital temperature sensor ``TMP102``."""

    api_version = 3
    id = "tmp102"
    name = "TMP102"
    longname = "Digial temperature sensor TMP102"
    desc = "Low power digital temperature sensor protocol decoder, v 1.0.0."
    license = "gplv2+"
    inputs = ["i2c"]
    outputs = ["tmp102"]

    options = (
        {"id": "radix", "desc": "Number format", "default": "Hex",
         "values": ("Hex", "Dec", "Oct")},
        {"id": "units", "desc": "Temperature unit", "default": "Celsius",
         "values": ("Celsius", "Fahrenheit", "Kelvin")},
    )

    annotations = create_annots()
    annotation_rows = (
        ("bits", "Bits", tuple(range(AnnBits.RESERVED, AnnBits.OS + 1))),
        ("regs", "Registers", tuple(range(AnnAddrs.GC, AnnRegs.THIGH + 1))),
        ("info", "Info", tuple(range(AnnInfo.GRST, AnnInfo.THIGH + 1))),
        ("warnings", "Warnings", (AnnInfo.WARN,)),
    )

    def __init__(self):
        """Initialize decoder."""
        self.reset()

    def reset(self):
        """Reset decoder and initialize instance variables."""
        # Common parameters for I2C sampling
        self.ss = 0         # Start sample
        self.es = 0         # End sample
        self.ssb = 0        # Start sample of an annotation transmission block
        self.ssd = 0        # Start sample of an annotation data block
        self.esd = 0        # End sample of an annotation data block
        self.bits = []      # List of recent processed byte bits
        self.bytes = []     # List of recent processed bytes
        self.write = True   # Flag about recent write action (default write)
        self.state = "IDLE"
        # Specific parameters for a device
        self.addr = Address.GND     # Slave address (default ADD0 grounded)
        self.reg = Register.TEMP    # Processed slave register (default temp)
        self.em = False             # Flag about extended mode (default Normal)

    def start(self):
        """Actions before the beginning of the decoding."""
        self.out_ann = self.register(srd.OUTPUT_ANN)

    def compose_annot(self, ann_label, ann_value=None, ann_unit=None,
                      ann_action=None):
        """Compose list of annotations enriched with value and unit.

        Arguments
        ---------
        ann_label : list
            List of annotation label for enriching with values and units and
            prefixed with actions.
            *The argument is mandatory and has no default value.*
        ann_value : list
            List of values to be added item by item to all annotations.
        ann_unit : list
            List of measurement units to be added item by item to all
            annotations. The method does not add separation space between
            the value and the unit.
        ann_action : list
            List of action prefixes prepend item by item to all annotations.
            The method separates action and annotation with a space.

        Returns
        -------
        list of str
            List of a annotations potentially enriched with values and units
            with items sorted by length descending.

        Notes
        -----
        - Usually just one value and one unit is used. However for flexibility
          more of them can be used.
        - If the annotation values list is not defined, the annotation units
          list is not used, even if it is defined.

        """
        if not isinstance(ann_label, list):
            tmp = ann_label
            ann_label = []
            ann_label.append(tmp)

        if ann_value is None:
            ann_value = []
        elif not isinstance(ann_value, list):
            tmp = ann_value
            ann_value = []
            ann_value.append(tmp)

        if ann_unit is None:
            ann_unit = []
        elif not isinstance(ann_unit, list):
            tmp = ann_unit
            ann_unit = []
            ann_unit.append(tmp)

        if ann_action is None:
            ann_action = []
        elif not isinstance(ann_action, list):
            tmp = ann_action
            ann_action = []
            ann_action.append(tmp)
        if len(ann_action) == 0:
            ann_action = [""]

        # Compose annotation
        annots = []
        for act in ann_action:
            for lbl in ann_label:
                ann = "{} {}".format(act, lbl).strip()
                ann_item = None
                for val in ann_value:
                    ann_item = "{}: {}".format(ann, val)
                    annots.append(ann_item)  # Without units
                    for unit in ann_unit:
                        ann_item += "{}".format(unit)
                        annots.append(ann_item)  # With units
                if ann_item is None:
                    annots.append(ann)

        # Add last 2 annotation items without values
        if len(ann_value) > 0:
            for ann in ann_label[-2:]:
                annots.append(ann)
        annots.sort(key=len, reverse=True)
        return annots

    def put_data(self, bit_start, bit_stop, data):
        """Span data output across bit range.

        - Output is an annotation block from the start sample of the first bit
          to the end sample of the last bit.
        """
        self.put(self.bits[bit_start][1], self.bits[bit_stop][2],
                 self.out_ann, data)

    def put_bit_data(self, bit_reserved):
        """Span output under general data bit.

        - Output is an annotation block from the start to the end sample
          of a data bit.
        """
        annots = self.compose_annot(bits[AnnBits.DATA])
        self.put(self.bits[bit_reserved][1], self.bits[bit_reserved][2],
                 self.out_ann, [AnnBits.DATA, annots])

    def put_bit_reserve(self, bit_reserved):
        """Span output under reserved bit.

        - Output is an annotation block from the start to the end sample
          of a reserved bit.
        """
        annots = self.compose_annot(bits[AnnBits.RESERVED])
        self.put(self.bits[bit_reserved][1], self.bits[bit_reserved][2],
                 self.out_ann, [AnnBits.RESERVED, annots])

    def check_addr(self, addr_slave, check_gencall=False):
        """Check correct slave address or general call."""
        if addr_slave in (
            Address.GND,
            Address.VCC,
            Address.SDA,
            Address.SCL,
        ) or not check_gencall or addr_slave == GeneralCall.ADDRESS:
            return True
        self.put(self.ssb, self.es, self.out_ann,
                 [AnnInfo.WARN,
                  ["Unknown slave address ({:#04x})"
                   .format(addr_slave)]])
        return False

    def calculate_temperature(self, rawdata):
        """Calculate and convert temperature.

        Arguments
        ---------
        rawdata : int
            Content of the temperature, TLOW, or THIGH register.

        Returns
        -------
        tuple: float, string
            Temperature and unit in a scale determined by corresponding decoder
            option.

        """
        if rawdata & (1 << TempBits.EM):
            self.em = True
        # Extended mode (13-bit resolution)
        if self.em:
            rawdata >>= 3
            if rawdata > 0x0fff:
                rawdata |= 0xe000  # 2s complement
        # Normal mode (12-bit resolution)
        else:
            rawdata >>= 4
            if rawdata > 0x07ff:
                rawdata |= 0xf000  # 2s complement
        temperature = rawdata / 16  # Celsius
        if self.options["units"] == "Fahrenheit":
            temperature *= 9 / 5
            temperature += 32
        elif self.options["units"] == "Kelvin":
            temperature += 273.15
        # Measurement unit
        unit = " {}".format(temp_units[self.options["units"]])
        return temperature, unit

    def collect_data(self, databyte):
        """Collect data byte to a data cache."""
        self.esd = self.es
        if len(self.bytes) == 0:
            self.ssd = self.ss
            self.bytes.append(databyte)
        else:
            self.bytes.insert(0, databyte)

    def clear_data(self):
        """Clear data cache."""
        self.ssd = self.esd = 0
        self.bytes = []
        self.bits = []

    def format_data(self, data):
        """Format data value according to the radix option."""
        return radixes[self.options["radix"]].format(data)

    def handle_addr(self):
        """Process slave address."""
        if len(self.bytes) == 0:
            return
        # Registers row
        self.addr = self.bytes[0]
        ann_idx = addr_annots[self.addr]
        annots = self.compose_annot(addresses[ann_idx])
        self.put(self.ssd, self.esd, self.out_ann, [ann_idx, annots])
        self.clear_data()

    def handle_reg(self):
        """Process slave register."""
        if len(self.bytes) == 0:
            return
        self.reg = self.bytes[0]
        if self.addr == GeneralCall.ADDRESS:
            ann_idx = reg_annots_gc[self.reg]
        else:
            ann_idx = reg_annots[self.reg]
        # Registers row
        annots = self.compose_annot(registers[ann_idx])
        self.put(self.ssd, self.esd, self.out_ann, [ann_idx, annots])
        self.clear_data()

    def handle_nodata(self):
        """Process transmission without any data."""
        # Info row
        annots = self.compose_annot(info[AnnInfo.CHECK])
        self.put(self.ssb, self.es, self.out_ann, [AnnInfo.CHECK, annots])

    def handle_data(self):
        """Create name and call corresponding data register handler."""
        fn = getattr(self, "handle_datareg_{:#04x}".format(self.reg))
        fn()
        self.clear_data()

    def handle_datareg_0x06(self):
        """Process general reset register."""
        # Info row
        annots = self.compose_annot(info[AnnInfo.GRST])
        self.put(self.ssb, self.es, self.out_ann, [AnnInfo.GRST, annots])

    def handle_datareg_0x01(self):
        """Process configuration register."""
        regword = (self.bytes[1] << 8) + self.bytes[0]
        # Bits row - OS bit - one-shot measurement
        os = 1 if (regword & (1 << ConfigBits.OS)) else 0
        os_l = ("en" if (os) else "dis") + "abled"
        os_s = os_l[0].upper()
        annots = self.compose_annot(bits[AnnBits.OS], [os, os_l, os_s])
        self.put_data(ConfigBits.OS, ConfigBits.OS, [AnnBits.OS, annots])
        # Bits row - R0/R1 bits - converter resolution
        res = resolutions[(regword >> ConfigBits.R0) & 0b11]
        annots = self.compose_annot(bits[AnnBits.R0],
                                    "{}".format(res), "bit")
        self.put_data(ConfigBits.R1, ConfigBits.R0, [AnnBits.R0, annots])
        # Bits row - F0/F1 bits - fault queue
        flt = faults[(regword >> ConfigBits.F0) & 0b11]
        annots = self.compose_annot(bits[AnnBits.F0], "{}".format(flt))
        self.put_data(ConfigBits.F1, ConfigBits.F0, [AnnBits.F0, annots])
        # Bits row - POL bit - polarity, alert active
        pol = 1 if (regword & (1 << ConfigBits.POL)) else 0
        pol_l = ("high" if (pol) else "low")
        pol_s = pol_l[0].upper()
        annots = self.compose_annot(bits[AnnBits.POL], [pol, pol_l, pol_s])
        self.put_data(ConfigBits.POL, ConfigBits.POL, [AnnBits.POL, annots])
        # Bits row - TM bit - thermostat mode
        tm = 1 if (regword & (1 << ConfigBits.TM)) else 0
        tm_l = ("interrupt" if (tm) else "comparator")
        tm_s = tm_l[0].upper()
        annots = self.compose_annot(bits[AnnBits.TM], [tm, tm_l, tm_s])
        self.put_data(ConfigBits.TM, ConfigBits.TM, [AnnBits.TM, annots])
        # Bits row - SD bit - shutdown mode
        sd = 1 if (regword & (1 << ConfigBits.SD)) else 0
        sd_l = ("en" if (sd) else "dis") + "abled"
        sd_s = sd_l[0].upper()
        annots = self.compose_annot(bits[AnnBits.SD], [sd, sd_l, sd_s])
        self.put_data(ConfigBits.SD, ConfigBits.SD, [AnnBits.SD, annots])
        # Bits row - CR0/CR1 bits - conversion rate
        rate = rates[(regword >> ConfigBits.CR0) & 0b11]
        annots = self.compose_annot(bits[AnnBits.CR0], rate, "Hz")
        self.put_data(ConfigBits.CR1, ConfigBits.CR0, [AnnBits.CR0, annots])
        # Bits row - AL bit - alert
        al = 1 if (regword & (1 << ConfigBits.AL)) else 0
        al_l = ("in" if (al ^ pol) else "") + "active"
        al_s = al_l[0].upper()
        annots = self.compose_annot(bits[AnnBits.AL], [al, al_l, al_s])
        self.put_data(ConfigBits.AL, ConfigBits.AL, [AnnBits.AL, annots])
        # Bits row - EM bit - extended mode
        em = 1 if (regword & (1 << ConfigBits.EM)) else 0
        self.em = bool(em)
        em_l = ("en" if (em) else "dis") + "abled"
        em_s = em_l[0].upper()
        annots = self.compose_annot(bits[AnnBits.EM], [em, em_l, em_s])
        self.put_data(ConfigBits.EM, ConfigBits.EM, [AnnBits.EM, annots])
        # Bits row - reserved bits
        for i in range(ConfigBits.EM - 1, -1, -1):
            self.put_bit_reserve(i)
        # Registers row
        annots = self.compose_annot(registers[AnnRegs.DATA],
                                    self.format_data(regword))
        self.put(self.ssd, self.esd, self.out_ann, [AnnRegs.DATA, annots])
        # Info row
        if regword == Params.POWERUP:
            val_idx = prm_annots[regword]
        else:
            val_idx = prm_annots[Params.CUSTOM]
        act_idx = AnnInfo.WRITE if (self.write) else AnnInfo.READ
        annots = self.compose_annot(info[AnnInfo.CONF],
                                    ann_value=info[val_idx],
                                    ann_action=info[act_idx])
        self.put(self.ssb, self.es, self.out_ann, [AnnInfo.CONF, annots])

    def handle_datareg_0x00(self):
        """Process temperature register."""
        regword = (self.bytes[1] << 8) + self.bytes[0]
        temp, unit = self.calculate_temperature(regword)
        # Bits row - EM bit - extended mode
        em = 1 if (self.em) else 0
        em_l = ("en" if (self.em) else "dis") + "abled"
        em_s = em_l[0].upper()
        annots = self.compose_annot(bits[AnnBits.EM], [em, em_l, em_s])
        self.put_data(TempBits.EM, TempBits.EM, [AnnBits.EM, annots])
        # Bits row - reserved bits
        res_bits = 2 if (self.em) else 3
        for i in range(0, res_bits):
            self.put_bit_reserve(i + TempBits.RESERVED)
        # Bits row - data bits
        data_bits = 8 * len(self.bytes) - 1 - res_bits
        for i in range(0, data_bits):
            self.put_bit_data(i + TempBits.RESERVED + res_bits)
        # Registers row
        annots = self.compose_annot(registers[AnnRegs.DATA],
                                    self.format_data(regword))
        self.put(self.ssd, self.esd, self.out_ann, [AnnRegs.TEMP, annots])
        # Info row
        # act_idx = AnnInfo.WRITE if (self.write) else AnnInfo.READ
        annots = self.compose_annot(info[AnnInfo.TEMP],
                                    ann_value=temp,
                                    ann_unit=unit,
                                    # ann_action=info[act_idx],
                                    )
        self.put(self.ssb, self.es, self.out_ann, [AnnInfo.TEMP, annots])

    def handle_datareg_0x02(self):
        """Process TLOW register."""
        regword = (self.bytes[1] << 8) + self.bytes[0]
        temp, unit = self.calculate_temperature(regword)
        # Registers row
        annots = self.compose_annot(registers[AnnRegs.DATA],
                                    self.format_data(regword))
        self.put(self.ssd, self.esd, self.out_ann, [AnnRegs.TLOW, annots])
        # Info row
        act_idx = AnnInfo.WRITE if (self.write) else AnnInfo.READ
        annots = self.compose_annot(info[AnnInfo.TLOW],
                                    ann_value=temp,
                                    ann_unit=unit,
                                    ann_action=info[act_idx])
        self.put(self.ssb, self.es, self.out_ann, [AnnInfo.TLOW, annots])

    def handle_datareg_0x03(self):
        """Process THIGH register."""
        regword = (self.bytes[1] << 8) + self.bytes[0]
        temp, unit = self.calculate_temperature(regword)
        # Registers row
        annots = self.compose_annot(registers[AnnRegs.DATA],
                                    self.format_data(regword))
        self.put(self.ssd, self.esd, self.out_ann, [AnnRegs.THIGH, annots])
        # Info row
        act_idx = AnnInfo.WRITE if (self.write) else AnnInfo.READ
        annots = self.compose_annot(info[AnnInfo.THIGH],
                                    ann_value=temp,
                                    ann_unit=unit,
                                    ann_action=info[act_idx])
        self.put(self.ssb, self.es, self.out_ann, [AnnInfo.THIGH, annots])

    def decode(self, startsample, endsample, data):
        """Decode samples provided by parent decoder."""
        cmd, databyte = data
        self.ss, self.es = startsample, endsample

        if cmd == "BITS":
            """Collect packet of bits that belongs to the following command.
            - Packet is in the form of list of bit lists:
                ["BITS", bitlist]
            - Bit list is a list of 3 items list
                [[bitvalue, startsample, endsample], ...]
            - Samples are counted for aquisition sampling frequency.
            - Parent decoder ``i2c``stores individual bits in the list from
              the least significant bit (LSB) to the most significant bit
              (MSB) as it is at representing numbers in computers, although I2C
              bus transmits data in oposite order with MSB first.
            """
            self.bits = databyte + self.bits
            return

        # State machine
        if self.state == "IDLE":
            """Waiting for an I2C transmissionself.
            - Wait for start condition.
            - By start condition a new transmission begins.
            """
            if cmd != "START":
                return
            self.ssb = self.ss
            self.state = "ADDRESS SLAVE"

        elif self.state == "ADDRESS SLAVE":
            """Wait for a slave address write operation.
            - Every transmission starts with writing a register pointer
              to the slave of for general call, so that the slave address
              should be always followed by the write bit.
            """
            if cmd in ["ADDRESS WRITE", "ADDRESS READ"]:
                if self.check_addr(databyte, check_gencall=True):
                    self.collect_data(databyte)
                    self.handle_addr()
                    if cmd == "ADDRESS READ":
                        self.write = False
                        self.state = "REGISTER DATA"
                    elif cmd == "ADDRESS WRITE":
                        self.write = True
                        self.state = "REGISTER ADDRESS"
                else:
                    self.state = "IDLE"

        elif self.state == "REGISTER ADDRESS":
            """Process slave register"""
            if cmd in ["DATA WRITE", "DATA READ"]:
                self.collect_data(databyte)
                self.handle_reg()
                self.state = "REGISTER DATA"
            elif cmd == "STOP":
                """Output end of transmission without any register and data."""
                self.handle_nodata()
                self.state = "IDLE"

        elif self.state == "REGISTER DATA":
            """Process writing or reading data for a slave register.
            - Repeated Start condition signals, that reading sequence follows
              starting with slave address.
            - Subsequent writes signals writing to the slave.
            - Otherwise Stop condition is expected.
            """
            if cmd in ["DATA WRITE", "DATA READ"]:
                self.collect_data(databyte)
            elif cmd == "START REPEAT":
                self.state = "ADDRESS SLAVE"
            elif cmd == "STOP":
                """Output formatted string with register data.
                - This is end of an I2C transmission. Start waiting for another
                  one.
                """
                self.handle_data()
                self.state = "IDLE"
