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
class Address:
    """Enumeration of possible slave addresses.

    - Address item determines the pin, which the ADD0 pin of the sensor is
      hardware connected to.
    """

    (GND, VCC, SDA, SCL) = range(0x48, 0x4c)


class GeneralCall:
    """Enumeration of parameters for general call on I2C bus."""

    (ADDRESS, WRITE, RESET) = (0x00, 0x04, 0x06)


class Register:
    """Enumeration of slave registers."""

    (TEMP, CONF, TLOW, THIGH) = range(4)


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

    (RESERVED) = 0xff


class AnnRegs:
    """Enumeration of annotations for registers."""

    (TEMP, CONF, TLOW, THIGH) = range(0, 4)


class AnnBits:
    """Enumeration of annotations for configuration bits."""

    (
        RESERVED,
        EM, AL, CR0, SD, TM, POL, F0, R0, OS
    ) = range(AnnRegs.THIGH + 1, AnnRegs.THIGH + 1 + 10)


class AnnStrings:
    """Enumeration of annotations for formatted strings."""

    (
        TEMPREAD, WARN, RESET
    ) = range(AnnBits.OS + 1, AnnBits.OS + 1 + 3)


###############################################################################
# Parameter dictionaries
###############################################################################
addresses = {  # Convert value to name
    Address.GND: "ADD0_GND",
    Address.VCC: "ADD0_VCC",
    Address.SDA: "ADD0_SDA",
    Address.SCL: "ADD0_SCL",
}

rates = {  # Convert binary bits value to operational value
    0b00: 0.25,
    0b01: 1,
    0b10: 4,
    0b11: 8,
}

faults = {  # Convert binary bits value to operational value
    0b00: 1,
    0b01: 2,
    0b10: 4,
    0b11: 6,
}

resolution = {  # Convert binary bits value to operational value
    0b11: 12,
}


###############################################################################
# Parameter anotations
###############################################################################
"""
- If a parameter has a value, the last item of an annotation list is used
  repeatedly without a value.
- If a parameter has measurement unit alongside with value, the last two items
  are used repeatedly without that measurement unit.
"""

registers = {
    AnnRegs.TEMP: ["Temperature register", "Temperature", "Temp", "T"],
    AnnRegs.CONF: ["Configuration register", "Configuration", "Conf",
                   "Cfg", "C"],
    AnnRegs.TLOW: ["Low alert register", "Low alert", "Tlow", "L"],
    AnnRegs.THIGH: ["High alert register", "High alert", "Thigh", "H"],
}

bits = {
    AnnBits.RESERVED: ["Reserved bit", "Reserved", "Rsvd", "R"],
    AnnBits.EM: ["Extended mode bit", "Extended mode", "EM", "E"],
    AnnBits.AL: ["Alert bit", "Alert", "AL", "A"],
    AnnBits.CR0: ["Conversion rate bits", "Conversion rate", "Rate", "R"],
    AnnBits.SD: ["Shutdown mode", "Shutdown", "Shtd", "SD", "S"],
    AnnBits.TM: ["Thermostat mode", "Thermostat", "TMode", "TM", "T"],
    AnnBits.POL: ["Alert active", "Polarity", "Pol", "P"],
    AnnBits.F0: ["Consecutive faults", "Faults", "Flts", "F"],
    AnnBits.R0: ["Converter resolution", "Resolution", "Res", "R"],
    AnnBits.OS: ["One-shot conversion", "Oneshot", "OS", "O"],
}

strings = {
    AnnStrings.TEMPREAD: ["Read temperature", "Temperature", "Temp", "T"],
    AnnStrings.WARN: ["Warnings", "Warn", "W"],
    AnnStrings.RESET: ["General reset", "Gen reset", "Reset", "Rst", "R"],
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
        # Registers
        ("reg-temp", registers[AnnRegs.TEMP][0]),          # 0
        ("reg-conf", registers[AnnRegs.CONF][0]),          # 1
        ("reg-tlow", registers[AnnRegs.TLOW][0]),          # 2
        ("reg-thigh", registers[AnnRegs.THIGH][0]),        # 3
        # Common bits
        ("bit-reserved", bits[AnnBits.RESERVED][0]),        # 4
        # Configuration bits
        ("bit-em", bits[AnnBits.EM][0]),                    # 5
        ("bit-al", bits[AnnBits.AL][0]),                    # 6
        ("bit-rate", bits[AnnBits.CR0][0]),                 # 7
        ("bit-sd", bits[AnnBits.SD][0]),                    # 8
        ("bit-tm", bits[AnnBits.TM][0]),                    # 9
        ("bit-pol", bits[AnnBits.POL][0]),                  # 10
        ("bit-fault", bits[AnnBits.F0][0]),                 # 11
        ("bit-res", bits[AnnBits.R0][0]),                   # 12
        ("bit-os", bits[AnnBits.OS][0]),                    # 13
        # Strings
        ("read-temp", strings[AnnStrings.TEMPREAD][0]),     # 14
        ("warnings", strings[AnnStrings.WARN][0]),          # 15
        ("gen-reset", strings[AnnStrings.RESET][0]),        # 16
    )

    annotation_rows = (
        ("regs", "Registers", tuple(range(AnnRegs.TEMP, AnnRegs.THIGH + 1))),
        ("bits", "Bits", tuple(range(AnnBits.RESERVED, AnnBits.OS + 1))),
        ("temp", "Temperature", (AnnStrings.TEMPREAD,)),
        ("warnings", "Warnings", (AnnStrings.WARN, AnnStrings.RESET))
    )

    def __init__(self):
        """Initialize decoder."""
        self.reset()

    def reset(self):
        """Reset decoder and initialize instance variables."""
        # Common parameters for I2C sampling
        self.ss = 0         # Start sample
        self.es = 0         # End sample
        self.ssb = 0        # Start sample of a formatted string block
        self.esb = 0        # End sample of a formatted string block
        self.bits = []      # List of recent byte bits
        self.state = "IDLE"
        # Specific parameters for a device
        self.reg = 0x00     # Processed slave register (default pointer one)
        self.regbits = []   # List of multibyte register bits
        self.regbytes = []  # List of multibyte register bytes
        self.temp = None

    def start(self):
        """Actions before the beginning of the decoding."""
        self.out_ann = self.register(srd.OUTPUT_ANN)

    def check_slave(self, addr_slave, check_gencall=False):
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
            annotations.

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
                    ann_item += " {}".format(unit)
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
        self.put(self.regbits[bit_start][1], self.regbits[bit_stop][2],
                 self.out_ann, data)

    def put_reserved(self, bit_reserved):
        """Span output under reserved bit.

        - Output is an annotation block from the start  to the end sample
          of a reserved bit.
        """
        annots = self.compose_annot(bits[AnnBits.RESERVED])
        self.put(self.regbits[bit_reserved][1], self.regbits[bit_reserved][2],
                 self.out_ann, [AnnBits.RESERVED, annots])

    def handle_reset(self):
        """Process general reset."""
        annots = self.compose_annot(strings[AnnStrings.RESET])
        self.put(self.ssb, self.es, self.out_ann, [AnnStrings.RESET, annots])

    def handle_slave_reg(self, databyte):
        """Collect byte of a register."""
        if len(self.regbytes) == 0:
            self.ssb = self.ss
            self.regbytes.append(databyte)
            self.regbits = self.bits
        else:
            self.esb = self.es
            self.regbytes.insert(0, databyte)
            self.regbits = self.bits + self.regbits

    def handle_reg(self):
        """Create name and call current slave registers handler.

        - Honor caching pointer register value from the recent write operation
          for subsequent reading operation.
        """
        fn = getattr(self, "handle_reg_{:#04x}".format(self.reg))
        fn()

    def handle_reg_0x01(self):
        """Process configuration register."""
        regword = (self.regbytes[1] << 8) + self.regbytes[0]
        # Registers row
        annots = self.compose_annot(registers[AnnRegs.CONF],
                                    "{:#06x}".format(regword))
        self.put(self.ssb, self.esb, self.out_ann, [AnnRegs.CONF, annots])
        # Bits row - OS bit - one-shot measurement
        os = 1 if (regword & (1 << ConfigBits.OS)) else 0
        os_l = ("en" if (os) else "dis") + "abled"
        os_s = os_l[0].upper()
        annots = self.compose_annot(bits[AnnBits.OS], [os, os_l, os_s])
        self.put_data(ConfigBits.OS, ConfigBits.OS, [AnnBits.OS, annots])
        # Bits row - R0/R1 bits - converter resolution
        res = resolution[(regword >> ConfigBits.R0) & 0b11]
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
        # Bits row - OS bit - one-shot measurement
        sd = 1 if (regword & (1 << ConfigBits.SD)) else 0
        sd_l = ("en" if (sd) else "dis") + "abled"
        sd_s = sd_l[0].upper()
        annots = self.compose_annot(bits[AnnBits.SD], [sd, sd_l, sd_s])
        self.put_data(ConfigBits.SD, ConfigBits.SD, [AnnBits.SD, annots])
        # Bits row - reserved bits
        for i in range(ConfigBits.EM - 1, -1, -1):
            self.put_reserved(i)

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
            self.bits = databyte
            return

        # State machine
        if self.state == "IDLE":
            """Wait for an I2C START condition.
            - By start condition a new transmission begins.
            """
            if cmd != "START":
                return
            self.state = "ADDRESS SLAVE"
            self.ssb = self.ss

        elif self.state == "ADDRESS SLAVE":
            """Wait for a slave address write operation.
            - Every transmission starts with writing a register pointer
              to the slave of for general call, so that the slave address
              should be always followed by the write bit.
            """
            if cmd != "ADDRESS WRITE":
                return
            if not self.check_slave(databyte, True):
                self.state = "IDLE"  # Start waiting for expected transmission
                return
            if databyte == GeneralCall.ADDRESS:
                self.state = "ADDRESS GENERAL"
            else:
                self.state = "ADDRESS REGISTER"

        elif self.state == "ADDRESS GENERAL":
            """Wait for a general reset.

            - Master issued a general call to the I2C bus.
            - If parameter of general call is the reset command, display it.
            - After general call start waiting for another transmission.
            """
            if cmd != "DATA WRITE":
                return
            if databyte == GeneralCall.RESET:
                self.state = "GENERAL RESET"
            else:
                self.state = "IDLE"

        elif self.state == "GENERAL RESET":
            """Wait for stop condition and display general reset."""
            if cmd != "STOP":
                return
            self.handle_reset()
            self.state = "IDLE"

        elif self.state == "ADDRESS REGISTER":
            """Wait for a data write.
            - Master selects the slave register by writing to the pointer one.
            """
            if cmd != "DATA WRITE":
                return
            self.reg = databyte
            self.state = "REGISTER WRITE"

        elif self.state == "REGISTER WRITE":
            """Analyze situation after selecting slave register.
            - Repeated Start condition signals, that reading sequence follows.
            - Subsequent writes signals writing to the slave.
            - Otherwise Stop condition is expected.
            """
            if cmd == "START REPEAT":
                self.state = "REGISTER READ"
                return
            elif cmd == "DATA WRITE":
                """Writing to selected register."""
                # self.handle_reg(databyte)
            elif cmd == "STOP":
                """Output formatted string with written data.
                - This is end of an I2C transmission. Start waiting for another
                  one.
                """
                # self.output_datetime(AnnStrings.DTWRITE, "Written")
                self.state = "IDLE"  # Start waiting for another transmission

        elif self.state == "REGISTER READ":
            """Wait for a slave address read operation.
            - This is start of reading sequence with preceeding slave address.
            """
            if cmd != "ADDRESS READ":
                return
            if not self.check_slave(databyte):
                self.state = "IDLE"  # Start waiting for expected transmission
                return
            self.state = "SUBSEQUENT READ"
        elif self.state == "SUBSEQUENT READ":
            if cmd == "DATA READ":
                self.handle_slave_reg(databyte)
            elif cmd == "STOP":
                self.handle_reg()
                self.state = "IDLE"  # Start waiting for another transmission
