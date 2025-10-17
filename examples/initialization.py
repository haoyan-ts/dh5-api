"""
Initialization Example for DH5 Modbus API

This example demonstrates different initialization modes
and monitoring initialization progress.
"""

from dh5_api import DH5ModbusAPI
import time


def wait_for_initialization(robot, timeout=30):
    """
    Wait for all axes to complete initialization

    Args:
        robot: DH5ModbusAPI instance
        timeout: Maximum wait time in seconds

    Returns:
        True if successful, False if timeout
    """
    start_time = time.time()

    while time.time() - start_time < timeout:
        status = robot.check_initialization()

        if isinstance(status, dict):
            print(f"Status: {status}")

            if all(s == "initialized" for s in status.values()):
                return True

            # Show which axes are still initializing
            initializing = [k for k, v in status.items() if v == "initializing"]
            if initializing:
                print(f"  Still initializing: {initializing}")

        time.sleep(1)

    return False


def initialize_to_close(robot):
    """Initialize all axes to close position"""
    print("\n=== Initializing to CLOSE position (mode 1) ===")
    robot.initialize(mode=1)

    if wait_for_initialization(robot):
        print("✓ Successfully initialized to close position")
        positions = robot.get_all_positions()
        print(f"  Final positions: {positions}")
    else:
        print("✗ Initialization timeout!")


def initialize_to_open(robot):
    """Initialize all axes to open position"""
    print("\n=== Initializing to OPEN position (mode 2) ===")
    robot.initialize(mode=2)

    if wait_for_initialization(robot):
        print("✓ Successfully initialized to open position")
        positions = robot.get_all_positions()
        print(f"  Final positions: {positions}")
    else:
        print("✗ Initialization timeout!")


def calibrate_stroke(robot):
    """Find total stroke for all axes"""
    print("\n=== Finding total stroke (mode 3) ===")
    robot.initialize(mode=3)

    if wait_for_initialization(robot, timeout=60):
        print("✓ Successfully calibrated stroke")
        positions = robot.get_all_positions()
        print(f"  Final positions: {positions}")
    else:
        print("✗ Calibration timeout!")


def initialize_single_axis(robot, axis, mode):
    """Initialize a single axis"""
    mode_names = {1: "close", 2: "open", 3: "find stroke"}
    print(f"\n=== Initializing axis {axis} to {mode_names[mode]} ===")

    robot.initialize_axis(axis, mode)

    start_time = time.time()
    while time.time() - start_time < 30:
        status = robot.check_initialization()
        if isinstance(status, dict):
            axis_key = f"axis_F{axis}"
            print(f"  Axis {axis} status: {status.get(axis_key)}")

            if status.get(axis_key) == "initialized":
                print(f"✓ Axis {axis} initialized!")
                return True

        time.sleep(1)

    print(f"✗ Axis {axis} initialization timeout!")
    return False


def main():
    """Initialization example"""

    # Using context manager for automatic connection management
    with DH5ModbusAPI(port="COM6") as robot:
        print("Connected to DH5 robot!")

        # Example 1: Initialize all axes to open position
        initialize_to_open(robot)
        time.sleep(2)

        # Example 2: Initialize all axes to close position
        initialize_to_close(robot)
        time.sleep(2)

        # Example 3: Initialize single axis
        initialize_single_axis(robot, axis=1, mode=2)
        time.sleep(2)

        # Example 4: Calibrate maximum positions
        print("\n=== Calibrating maximum positions ===")
        result = robot.calibrate_max_positions()
        if result == robot.SUCCESS:
            print(f"✓ Max positions: {robot.max_positions}")
        else:
            print("✗ Calibration failed!")

        print("\n=== All initialization examples completed ===")


if __name__ == "__main__":
    main()
