# DH5 API

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](https://github.com/yourusername/dh5-api)

Python API for Modbus RTU communication with DH5 robot controllers. This library provides a high-level interface for controlling DH5 robotic systems via serial communication.

## Features

- 🤖 **Complete DH5 Robot Control** - Full support for all 6 axes
- 📡 **Modbus RTU Communication** - Reliable serial communication protocol
- 🎯 **Position Control** - Precise position control with safety limits
- ⚡ **Speed & Force Control** - Configurable speed and force parameters
- 🔄 **Initialization & Calibration** - Automatic homing and calibration routines
- 📊 **Status Monitoring** - Real-time position, speed, and current readings
- 🛡️ **Error Handling** - Comprehensive fault detection and recovery
- 🔧 **Easy Configuration** - Simple UART and parameter configuration

## Installation

### From PyPI (when published)

```bash
pip install dh5-api
```

### From Source

```bash
git clone https://github.com/yourusername/dh5-api.git
cd dh5-api
pip install -e .
```

### Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- `loguru>=0.7.0` - Advanced logging
- `pymodbus>=3.0.0` - Modbus communication

## Quick Start

### Basic Usage

```python
from dh5_api import DH5ModbusAPI

# Initialize the API
robot = DH5ModbusAPI(
    port="COM6",           # Serial port
    modbus_id=1,          # Modbus device ID
    baud_rate=115200,     # Baud rate
    timeout=1.0           # Communication timeout
)

# Open connection
if robot.open_connection() == robot.SUCCESS:
    print("Connected to DH5 robot!")
    
    # Initialize robot (open position)
    robot.initialize(mode=2)
    
    # Wait for initialization to complete
    import time
    time.sleep(3)
    
    # Get current positions
    positions = robot.get_all_positions()
    print(f"Current positions: {positions}")
    
    # Set new positions
    robot.set_all_positions([100, 150, 200, 250, 300, 350])
    
    # Close connection
    robot.close_connection()
```

### Using Context Manager

```python
from dh5_api import DH5ModbusAPI

# Automatic connection management
with DH5ModbusAPI(port="COM6") as robot:
    # Initialize
    robot.initialize(mode=2)
    
    # Control robot
    robot.set_all_positions([100, 100, 100, 100, 100, 100])
    
    # Get status
    status = robot.check_initialization()
    print(f"Status: {status}")
```

## API Reference

### DH5ModbusAPI Class

#### Initialization

```python
DH5ModbusAPI(
    port: str = "COM6",
    modbus_id: int = 1,
    baud_rate: int = 115200,
    stop_bits: int = 1,
    parity: str = "N",
    timeout: float = 1.0
)
```

#### Connection Methods

- `open_connection()` - Open serial connection
- `close_connection()` - Close serial connection
- `is_connected` - Check connection status (property)

#### Robot Control

- `initialize(mode: int)` - Initialize all axes
  - Mode 1: Close position
  - Mode 2: Open position
  - Mode 3: Find total stroke
- `initialize_axis(axis: int, mode: int)` - Initialize specific axis
- `set_all_positions(positions: List[int])` - Set all axis positions
- `set_all_positions_by_ratio(ratios: List[float])` - Set positions by ratio (0.0-1.0)
- `set_all_speeds(speeds: List[float])` - Set all axis speeds (0.1-1.0)
- `set_all_forces(forces: List[float])` - Set all axis forces (0.2-1.0)
- `set_axis_position(axis: int, position: int)` - Set single axis position
- `set_axis_speed(axis: int, speed: int)` - Set single axis speed
- `set_axis_force(axis: int, force: int)` - Set single axis force

#### Status & Monitoring

- `get_all_positions()` - Get current positions of all axes
- `get_axis_position(axis: int)` - Get position of specific axis
- `get_axis_speed(axis: int)` - Get speed of specific axis
- `get_axis_current(axis: int)` - Get current of specific axis
- `check_initialization()` - Check initialization status of all axes
- `get_history_faults()` - Get fault history

#### System Commands

- `reset_faults()` - Reset current faults
- `restart_system()` - Restart robot system
- `aging_test(flag: int)` - Enable/disable aging test mode
- `calibrate_max_positions()` - Calibrate maximum positions
- `set_save_param(flag: int)` - Save parameters to non-volatile memory

### DH5Registers Class

Constants for register addresses:

```python
# Initialization
RETURN_TO_ZERO = 0x0100
RETURN_TO_ZERO_STATUS = 0x0200

# Configuration
SAVE_PARAM = 0x0300
UART_CONFIG = 0x0302

# Position registers
AXIS_POSITION_BASE = 0x0101
AXIS_CURRENT_POSITION_BASE = 0x0207

# And more...
```

### ModbusFunction Enum

```python
READ_HOLDING_REGISTERS = 0x03
WRITE_SINGLE_REGISTER = 0x06
WRITE_MULTIPLE_REGISTERS = 0x10
```

## Examples

See the `examples/` directory for more detailed examples:

- `basic_usage.py` - Basic connection and control
- `initialization.py` - Initialization procedures
- `position_control.py` - Advanced position control

## Error Codes

- `SUCCESS = 0` - Operation successful
- `ERROR_CONNECTION_FAILED = 1` - Connection failed
- `ERROR_INVALID_RESPONSE = 2` - Invalid response from device
- `ERROR_CRC_CHECK_FAILED = 3` - CRC check failed
- `ERROR_INVALID_COMMAND = 4` - Invalid command

## Development

### Setup Development Environment

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black dh5_api/
isort dh5_api/
```

### Linting

```bash
flake8 dh5_api/
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

### Version 1.0.0 (2025-10-17)

- Initial stable release
- Complete Modbus RTU implementation
- Support for all 6 axes
- Position, speed, and force control
- Initialization and calibration
- Comprehensive error handling
- Context manager support

## Support

For issues, questions, or contributions, please visit:
- [GitHub Issues](https://github.com/yourusername/dh5-api/issues)
- [Documentation](https://github.com/yourusername/dh5-api#readme)

## Acknowledgments

- Built with [pymodbus](https://github.com/pymodbus-dev/pymodbus)
- Logging powered by [loguru](https://github.com/Delgan/loguru)
