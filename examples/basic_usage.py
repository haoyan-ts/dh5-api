"""
Basic Usage Example for DH5 Modbus API

This example demonstrates basic connection, initialization,
and position control.
"""

from dh5_api import DH5ModbusAPI
import time


def main():
    """Basic usage example"""

    # Create API instance
    robot = DH5ModbusAPI(
        port="COM6",  # Change to your serial port
        modbus_id=1,
        baud_rate=115200,
        timeout=1.0,
    )

    # Open connection
    print("Connecting to DH5 robot...")
    if robot.open_connection() != robot.SUCCESS:
        print("Failed to connect!")
        return

    print("Connected successfully!")

    try:
        # Initialize robot (open position - mode 2)
        print("\nInitializing robot to open position...")
        robot.initialize(mode=2)

        # Wait for initialization to complete
        time.sleep(3)

        # Check initialization status
        status = robot.check_initialization()
        print(f"Initialization status: {status}")

        # Wait until all axes are initialized
        while True:
            status = robot.check_initialization()
            if isinstance(status, dict) and all(
                s == "initialized" for s in status.values()
            ):
                print("All axes initialized!")
                break
            print("Waiting for initialization...")
            time.sleep(1)

        # Get current positions
        positions = robot.get_all_positions()
        print(f"\nCurrent positions: {positions}")

        # Set new positions
        print("\nMoving to new positions...")
        new_positions = [100, 150, 200, 250, 300, 350]
        result = robot.set_all_positions(new_positions)
        if result == robot.SUCCESS:
            print(f"Set positions to: {new_positions}")

        time.sleep(2)

        # Read positions again
        positions = robot.get_all_positions()
        print(f"Updated positions: {positions}")

        # Get status of specific axis
        print("\nReading axis 1 details:")
        pos = robot.get_axis_position(1)
        print(f"  Position: {pos}")
        speed = robot.get_axis_speed(1)
        print(f"  Speed: {speed}")
        current = robot.get_axis_current(1)
        print(f"  Current: {current}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close connection
        print("\nClosing connection...")
        robot.close_connection()
        print("Done!")


if __name__ == "__main__":
    main()
