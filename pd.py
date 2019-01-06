# -*- coding: utf-8 -*-
"""This file is part of the libsigrokdecode project.

Copyright (C) 2018 Libor Gabaj <libor.gabaj@gmail.com>

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
# Enumeration classes
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

    (EM,) = (0,)


class Params:
    """Typical slave parameters."""

    (CUSTOM, POWERUP) = (0, 0x60a0)


class AnnAddrs:
    """Enumeration of annotations for addresses."""

    (GC, GND, VCC, SDA, SCL) = range(0, 5)


class AnnRegs:
    """Enumeration of annotations for registers."""

    (
        RESET, DATA, CONF, TEMP, TLOW, THIGH
    ) = range(AnnAddrs.SCL + 1, (AnnAddrs.SCL + 1) + 6)


class AnnBits:
    """Enumeration of annotations for configuration bits."""

    (
        RESERVED,
        EM, AL, CR0, SD, TM, POL, F0, R0, OS
    ) = range(AnnRegs.THIGH + 1, (AnnRegs.THIGH + 1) + 10)


class AnnStrings:
    """Enumeration of annotations for formatted strings."""

    (
        WARN, GRST, CHECK, CUSTOM, PWRUP,
        CONF, TEMP, TLOW, THIGH,
    ) = range(AnnBits.OS + 1, (AnnBits.OS + 1) + 9)


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
    Params.CUSTOM: AnnStrings.CUSTOM,
    Params.POWERUP: AnnStrings.PWRUP,
}

rates = {
    0b00: "0.25",
    0b01: "1",
    0b10: "4",
    0b11: "8",
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

strings = {
    AnnStrings.WARN: ["Warnings", "Warn", "W"],
    AnnStrings.GRST: ["General reset", "GenReset", "GRST", "Rst", "R"],
    AnnStrings.CHECK: ["Slave presence check", "Slave check", "Check",
                       "Chk", "C"],
    AnnStrings.CUSTOM: ["Custom", "Cst", "C"],
    AnnStrings.PWRUP: ["Power-up reset", "PwrReset", "Pwr", "P"],
    AnnStrings.CONF: ["Configuration", "Conf", "Cfg", "C"],
    AnnStrings.TEMP: ["Measured temperature", "Temperature", "Temp", "T"],
    AnnStrings.TLOW: ["Low temperature limit", "Low limit", "Low", "L"],
    AnnStrings.THIGH: ["High temperature limit", "High limit", "High", "H"],
}


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
        {"id": "units", "desc": "Temperature units", "default": "Celsius",
         "values": ("Celsius", "Fahrenheit", "Kelvin")},
    )

    annotations = (
        # Addresses
        ("addr-gc", addresses[AnnAddrs.GC][0]),
        ("addr-gnd", addresses[AnnAddrs.GND][0]),
        ("addr-vcc", addresses[AnnAddrs.VCC][0]),
        ("addr-sda", addresses[AnnAddrs.SDA][0]),
        ("addr-scl", addresses[AnnAddrs.SCL][0]),
        # Registers
        ("reg-grst", registers[AnnRegs.RESET][0]),
        ("reg-data", registers[AnnRegs.DATA][0]),
        ("reg-conf", registers[AnnRegs.CONF][0]),
        ("reg-temp", registers[AnnRegs.TEMP][0]),
        ("reg-tlow", registers[AnnRegs.TLOW][0]),
        ("reg-thigh", registers[AnnRegs.THIGH][0]),
        # Common bits
        ("bit-reserved", bits[AnnBits.RESERVED][0]),
        # Configuration bits
        ("bit-em", bits[AnnBits.EM][0]),
        ("bit-al", bits[AnnBits.AL][0]),
        ("bit-rate", bits[AnnBits.CR0][0]),
        ("bit-sd", bits[AnnBits.SD][0]),
        ("bit-tm", bits[AnnBits.TM][0]),
        ("bit-pol", bits[AnnBits.POL][0]),
        ("bit-fault", bits[AnnBits.F0][0]),
        ("bit-res", bits[AnnBits.R0][0]),
        ("bit-os", bits[AnnBits.OS][0]),
        # Strings
        ("warnings", strings[AnnStrings.WARN][0]),
        ("gen-reset", strings[AnnStrings.GRST][0]),
        ("custom", strings[AnnStrings.CUSTOM][0]),
        ("power-up", strings[AnnStrings.PWRUP][0]),
        ("conf", strings[AnnStrings.CONF][0]),
        ("temp", strings[AnnStrings.TEMP][0]),
        ("tlow", strings[AnnStrings.TLOW][0]),
        ("thigh", strings[AnnStrings.THIGH][0]),
    )

    annotation_rows = (
        ("bits", "Bits", tuple(range(AnnBits.RESERVED, AnnBits.OS + 1))),
        ("regs", "Registers", tuple(range(AnnAddrs.GC, AnnRegs.THIGH + 1))),
        ("info", "Info", tuple(range(AnnStrings.GRST, AnnStrings.THIGH + 1))),
        ("warnings", "Warnings", (AnnStrings.WARN,)),
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
        self.state = "IDLE"
        # Specific parameters for a device
        self.addr = Address.GND     # Slave address (default ADD0 grounded)
        self.reg = Register.TEMP    # Processed slave register (default temp)
        self.em = False              # Extended mode (default Normal)

    def start(self):
        """Actions before the beginning of the decoding."""
        self.out_ann = self.register(srd.OUTPUT_ANN)

    def compose_annot(self, ann_list, ann_value=None, ann_unit=None):
        """Compose list of annotations enriched with value and unit.

        Arguments
        ---------
        ann_list : list
            List of annotations for enriching with values and units.
            *The argument is mandatory and has no default value.*
        ann_value : list
            List of values to be added item by item to all annotations.
        ann_unit : list
            List of measurement units to be added item by by item to all
            annotations. The method does not add separation space between
            the value and the unit.

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
        if not isinstance(ann_list, list):
            tmp = ann_list
            ann_list = []
            ann_list.append(tmp)

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

        # Add value and unit to all annotation, if declared
        annots = []
        for ann in ann_list:
            ann_item = None
            for val in ann_value:
                ann_item = "{}: {}".format(ann, val)
                annots.append(ann_item)  # Without units
                for unit in ann_unit:
                    ann_item += "{}".format(unit)
                    annots.append(ann_item)
            if ann_item is None:
                annots.append(ann)

        # Add last 2 annotation items without values
        if len(ann_value) > 0:
            for ann in ann_list[-2:]:
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

    def put_reserved(self, bit_reserved):
        """Span output under reserved bit.

        - Output is an annotation block from the start  to the end sample
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
                 [AnnStrings.WARN,
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
        # Extended mode (13-bit resolution)
        if self.em or (rawdata & (1 << TempBits.EM)):
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
        """Create name and call corresponding slave register handler."""
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
        annots = self.compose_annot(strings[AnnStrings.CHECK])
        self.put(self.ssb, self.es, self.out_ann, [AnnStrings.CHECK, annots])

    def handle_data(self):
        """Create name and call corresponding data register handler."""
        fn = getattr(self, "handle_datareg_{:#04x}".format(self.reg))
        fn()
        self.clear_data()

    def handle_datareg_0x06(self):
        """Process general reset register."""
        # Info row
        annots = self.compose_annot(strings[AnnStrings.GRST])
        self.put(self.ssb, self.es, self.out_ann, [AnnStrings.GRST, annots])

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
            self.put_reserved(i)
        # Registers row
        annots = self.compose_annot(registers[AnnRegs.DATA],
                                    "{:#06x}".format(regword))
        self.put(self.ssd, self.esd, self.out_ann, [AnnRegs.DATA, annots])
        # Info row
        if regword == Params.POWERUP:
            ann_idx = prm_annots[regword]
        else:
            ann_idx = prm_annots[Params.CUSTOM]
        annots = self.compose_annot(strings[AnnStrings.CONF], strings[ann_idx])
        self.put(self.ssb, self.es, self.out_ann, [AnnStrings.CONF, annots])

    def handle_datareg_0x00(self):
        """Process temperature register."""
        regword = (self.bytes[1] << 8) + self.bytes[0]
        temp, unit = self.calculate_temperature(regword)
        # Bits row - EM bit - extended mode
        em = 1 if (regword & (1 << TempBits.EM)) else 0
        self.em = bool(em)
        em_l = ("en" if (em) else "dis") + "abled"
        em_s = em_l[0].upper()
        annots = self.compose_annot(bits[AnnBits.EM], [em, em_l, em_s])
        self.put_data(TempBits.EM, TempBits.EM, [AnnBits.EM, annots])
        # Registers row
        annots = self.compose_annot(registers[AnnRegs.DATA],
                                    "{:#06x}".format(regword))
        self.put(self.ssd, self.esd, self.out_ann, [AnnRegs.TEMP, annots])
        # Info row
        annots = self.compose_annot(strings[AnnStrings.TEMP], temp, unit)
        self.put(self.ssb, self.es, self.out_ann, [AnnStrings.TEMP, annots])

    def handle_datareg_0x02(self):
        """Process TLOW register."""
        regword = (self.bytes[1] << 8) + self.bytes[0]
        temp, unit = self.calculate_temperature(regword)
        # Registers row
        annots = self.compose_annot(registers[AnnRegs.DATA],
                                    "{:#06x}".format(regword))
        self.put(self.ssd, self.esd, self.out_ann, [AnnRegs.TLOW, annots])
        # Info row
        annots = self.compose_annot(strings[AnnStrings.TLOW], temp, unit)
        self.put(self.ssb, self.es, self.out_ann, [AnnStrings.TLOW, annots])

    def handle_datareg_0x03(self):
        """Process THIGH register."""
        regword = (self.bytes[1] << 8) + self.bytes[0]
        temp, unit = self.calculate_temperature(regword)
        # Registers row
        annots = self.compose_annot(registers[AnnRegs.DATA],
                                    "{:#06x}".format(regword))
        self.put(self.ssd, self.esd, self.out_ann, [AnnRegs.THIGH, annots])
        # Info row
        annots = self.compose_annot(strings[AnnStrings.THIGH], temp, unit)
        self.put(self.ssb, self.es, self.out_ann, [AnnStrings.THIGH, annots])

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
                if self.check_addr(databyte, True):
                    self.collect_data(databyte)
                    self.handle_addr()
                    if cmd == "ADDRESS READ":
                        self.state = "REGISTER DATA"
                    elif cmd == "ADDRESS WRITE":
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
            if cmd == "START REPEAT":
                self.state = "ADDRESS SLAVE"
                return
            elif cmd in ["DATA WRITE", "DATA READ"]:
                self.collect_data(databyte)
            elif cmd == "STOP":
                """Output formatted string with register data.
                - This is end of an I2C transmission. Start waiting for another
                  one.
                """
                self.handle_data()
                self.state = "IDLE"
