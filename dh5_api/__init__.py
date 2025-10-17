"""
DH5 API package for Modbus communication with DH5 devices.
"""

from .dh5_api import DH5ModbusAPI, DH5Registers, ModbusFunction

__version__ = "1.0.0"
__all__ = ["DH5ModbusAPI", "DH5Registers", "ModbusFunction"]
