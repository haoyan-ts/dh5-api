"""
Unit tests for DH5ModbusAPI class
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from dh5_api import DH5ModbusAPI, DH5Registers, ModbusFunction


class TestDH5ModbusAPI:
    """Test suite for DH5ModbusAPI"""

    @pytest.fixture
    def mock_client(self):
        """Create a mock Modbus client"""
        with patch("dh5_api.dh5_api.ModbusSerialClient") as mock:
            client = MagicMock()
            client.connect.return_value = True
            client.connected = True
            mock.return_value = client
            yield client

    @pytest.fixture
    def api(self, mock_client):
        """Create a DH5ModbusAPI instance with mocked client"""
        api = DH5ModbusAPI(port="COM6", modbus_id=1)
        api.open_connection()
        return api

    def test_initialization(self):
        """Test API initialization"""
        api = DH5ModbusAPI(
            port="COM6",
            modbus_id=1,
            baud_rate=115200,
            stop_bits=1,
            parity="N",
            timeout=1.0,
        )
        assert api.port == "COM6"
        assert api.modbus_id == 1
        assert api.baud_rate == 115200
        assert api.stop_bits == 1
        assert api.parity == "N"
        assert api.timeout == 1.0

    def test_open_connection_success(self, mock_client):
        """Test successful connection opening"""
        api = DH5ModbusAPI(port="COM6")
        result = api.open_connection()
        assert result == DH5ModbusAPI.SUCCESS
        assert api.is_connected

    def test_open_connection_failure(self):
        """Test connection opening failure"""
        with patch("dh5_api.dh5_api.ModbusSerialClient") as mock:
            client = MagicMock()
            client.connect.return_value = False
            mock.return_value = client

            api = DH5ModbusAPI(port="COM6")
            result = api.open_connection()
            assert result == DH5ModbusAPI.ERROR_CONNECTION_FAILED

    def test_close_connection(self, api):
        """Test closing connection"""
        result = api.close_connection()
        assert result == DH5ModbusAPI.SUCCESS

    def test_context_manager(self, mock_client):
        """Test context manager usage"""
        with DH5ModbusAPI(port="COM6") as api:
            assert api.is_connected
        # Connection should be closed after exiting context

    def test_initialize_all_axes(self, api, mock_client):
        """Test initializing all axes"""
        mock_client.write_register.return_value = Mock(function_code=0x06)
        result = api.initialize(mode=2)
        assert result == DH5ModbusAPI.SUCCESS

    def test_initialize_invalid_mode(self, api):
        """Test initialization with invalid mode"""
        with pytest.raises(ValueError):
            api.initialize(mode=5)

    def test_set_all_positions(self, api, mock_client):
        """Test setting all axis positions"""
        mock_client.write_registers.return_value = Mock(function_code=0x10)
        api.max_positions = [500] * 6
        positions = [100, 150, 200, 250, 300, 350]
        result = api.set_all_positions(positions)
        assert result == DH5ModbusAPI.SUCCESS

    def test_set_all_positions_invalid_length(self, api):
        """Test setting positions with wrong number of values"""
        with pytest.raises(ValueError):
            api.set_all_positions([100, 150, 200])

    def test_get_all_positions(self, api, mock_client):
        """Test getting all axis positions"""
        mock_response = Mock()
        mock_response.registers = [100, 150, 200, 250, 300, 350]
        mock_client.read_holding_registers.return_value = mock_response

        result = api.get_all_positions()
        assert result == [100, 150, 200, 250, 300, 350]

    def test_set_axis_position(self, api, mock_client):
        """Test setting single axis position"""
        mock_client.write_register.return_value = Mock(function_code=0x06)
        result = api.set_axis_position(axis=1, position=100)
        assert result == DH5ModbusAPI.SUCCESS

    def test_set_axis_position_invalid_axis(self, api):
        """Test setting position with invalid axis number"""
        with pytest.raises(ValueError):
            api.set_axis_position(axis=7, position=100)

    def test_check_initialization(self, api, mock_client):
        """Test checking initialization status"""
        mock_response = Mock()
        # All axes initialized (0b01 for each axis)
        mock_response.registers = [0b010101010101]
        mock_client.read_holding_registers.return_value = mock_response

        result = api.check_initialization()
        assert isinstance(result, dict)
        assert len(result) == 6
        assert all(status == "initialized" for status in result.values())

    def test_reset_faults(self, api, mock_client):
        """Test resetting faults"""
        mock_client.write_register.return_value = Mock(function_code=0x06)
        result = api.reset_faults()
        assert result == DH5ModbusAPI.SUCCESS

    def test_set_all_speeds(self, api, mock_client):
        """Test setting all axis speeds"""
        mock_client.write_registers.return_value = Mock(function_code=0x10)
        speeds = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        result = api.set_all_speeds(speeds)
        assert result == DH5ModbusAPI.SUCCESS

    def test_set_all_speeds_invalid_range(self, api):
        """Test setting speeds with invalid values"""
        with pytest.raises(ValueError):
            api.set_all_speeds([0.05, 0.1, 0.2, 0.3, 0.4, 0.5])  # First value too low

    def test_set_all_forces(self, api, mock_client):
        """Test setting all axis forces"""
        mock_client.write_registers.return_value = Mock(function_code=0x10)
        forces = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        result = api.set_all_forces(forces)
        assert result == DH5ModbusAPI.SUCCESS

    def test_aging_test(self, api, mock_client):
        """Test aging test mode"""
        mock_client.write_register.return_value = Mock(function_code=0x06)
        result = api.aging_test(flag=1)
        assert result == DH5ModbusAPI.SUCCESS

    def test_aging_test_invalid_flag(self, api):
        """Test aging test with invalid flag"""
        with pytest.raises(ValueError):
            api.aging_test(flag=2)


class TestDH5Registers:
    """Test suite for DH5Registers constants"""

    def test_register_addresses(self):
        """Test that register addresses are defined"""
        assert DH5Registers.RETURN_TO_ZERO == 0x0100
        assert DH5Registers.RETURN_TO_ZERO_STATUS == 0x0200
        assert DH5Registers.SAVE_PARAM == 0x0300
        assert DH5Registers.AXIS_POSITION_BASE == 0x0101
        assert DH5Registers.AXIS_COUNT == 6


class TestModbusFunction:
    """Test suite for ModbusFunction enum"""

    def test_function_codes(self):
        """Test that function codes are defined"""
        assert ModbusFunction.READ_HOLDING_REGISTERS == 0x03
        assert ModbusFunction.WRITE_SINGLE_REGISTER == 0x06
        assert ModbusFunction.WRITE_MULTIPLE_REGISTERS == 0x10


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
