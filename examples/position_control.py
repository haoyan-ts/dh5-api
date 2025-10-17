"""
Position Control Example for DH5 Modbus API

This example demonstrates advanced position control including
absolute positioning, ratio-based positioning, and smooth movements.
"""

from dh5_api import DH5ModbusAPI
import time


def absolute_position_control(robot):
    """Control robot with absolute positions"""
    print("\n=== Absolute Position Control ===")

    # Define some target positions
    positions_list = [
        [100, 100, 100, 100, 100, 100],  # Home position
        [200, 150, 250, 200, 150, 250],  # Position 1
        [300, 250, 200, 300, 250, 200],  # Position 2
        [150, 200, 150, 200, 150, 200],  # Position 3
    ]

    for i, positions in enumerate(positions_list):
        print(f"\nMoving to position {i+1}: {positions}")
        result = robot.set_all_positions(positions)

        if result == robot.SUCCESS:
            print("  ✓ Command sent")
            time.sleep(2)

            # Verify position
            current = robot.get_all_positions()
            print(f"  Current positions: {current}")
        else:
            print(f"  ✗ Failed with error code: {result}")


def ratio_based_control(robot):
    """Control robot using ratio values (0.0 to 1.0)"""
    print("\n=== Ratio-Based Position Control ===")

    # First calibrate to get max positions
    print("Calibrating maximum positions...")
    result = robot.calibrate_max_positions()

    if result != robot.SUCCESS:
        print("✗ Calibration failed!")
        return

    print(f"✓ Max positions: {robot.max_positions}")

    # Define target positions as ratios
    ratio_positions = [
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Fully closed
        [0.5, 0.5, 0.5, 0.5, 0.5, 0.5],  # Half open
        [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],  # Fully open
        [0.3, 0.5, 0.7, 0.4, 0.6, 0.8],  # Mixed positions
    ]

    for i, ratios in enumerate(ratio_positions):
        print(f"\nMoving to ratio {i+1}: {ratios}")
        result = robot.set_all_positions_by_ratio(ratios)

        if result == robot.SUCCESS:
            print("  ✓ Command sent")
            time.sleep(2)

            # Show actual positions
            current = robot.get_all_positions()
            print(f"  Actual positions: {current}")
        else:
            print(f"  ✗ Failed with error code: {result}")


def smooth_movement(robot, start_positions, end_positions, steps=10, delay=0.5):
    """
    Create smooth movement by interpolating between positions

    Args:
        robot: DH5ModbusAPI instance
        start_positions: Starting positions (list of 6 values)
        end_positions: Ending positions (list of 6 values)
        steps: Number of interpolation steps
        delay: Delay between steps in seconds
    """
    print(f"\n=== Smooth Movement ({steps} steps) ===")
    print(f"From: {start_positions}")
    print(f"To:   {end_positions}")

    for step in range(steps + 1):
        # Calculate interpolated position
        t = step / steps
        positions = [
            int(start + (end - start) * t)
            for start, end in zip(start_positions, end_positions)
        ]

        print(f"Step {step}/{steps}: {positions}")
        robot.set_all_positions(positions)
        time.sleep(delay)

    print("✓ Smooth movement completed")


def speed_control_demo(robot):
    """Demonstrate speed control"""
    print("\n=== Speed Control Demo ===")

    # Set different speeds (0.1 to 1.0)
    speed_configs = [
        ([0.3, 0.3, 0.3, 0.3, 0.3, 0.3], "Slow"),
        ([0.6, 0.6, 0.6, 0.6, 0.6, 0.6], "Medium"),
        ([1.0, 1.0, 1.0, 1.0, 1.0, 1.0], "Fast"),
    ]

    test_positions = [100, 100, 100, 100, 100, 100]
    target_positions = [300, 300, 300, 300, 300, 300]

    for speeds, label in speed_configs:
        print(f"\n{label} speed: {speeds}")

        # Set speed
        result = robot.set_all_speeds(speeds)
        if result != robot.SUCCESS:
            print(f"  ✗ Failed to set speed")
            continue

        # Move to start position
        robot.set_all_positions(test_positions)
        time.sleep(2)

        # Measure time to move
        start_time = time.time()
        robot.set_all_positions(target_positions)
        time.sleep(3)  # Wait for movement
        elapsed = time.time() - start_time

        print(f"  ✓ Movement took ~{elapsed:.1f} seconds")


def force_control_demo(robot):
    """Demonstrate force control"""
    print("\n=== Force Control Demo ===")

    # Set forces (0.2 to 1.0)
    force_configs = [
        [0.3, 0.3, 0.3, 0.3, 0.3, 0.3],  # Low force
        [0.6, 0.6, 0.6, 0.6, 0.6, 0.6],  # Medium force
        [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],  # Maximum force
    ]

    for forces in force_configs:
        print(f"\nSetting forces: {forces}")
        result = robot.set_all_forces(forces)

        if result == robot.SUCCESS:
            print("  ✓ Force set successfully")
        else:
            print(f"  ✗ Failed with error code: {result}")


def individual_axis_control(robot):
    """Control individual axes"""
    print("\n=== Individual Axis Control ===")

    # Control each axis individually
    for axis in range(1, 7):
        position = 100 + (axis * 50)
        print(f"\nSetting axis {axis} to position {position}")

        result = robot.set_axis_position(axis, position)
        if result == robot.SUCCESS:
            time.sleep(1)
            current = robot.get_axis_position(axis)
            print(f"  ✓ Axis {axis} position: {current}")
        else:
            print(f"  ✗ Failed")


def main():
    """Position control examples"""

    with DH5ModbusAPI(port="COM6") as robot:
        print("Connected to DH5 robot!")

        # Initialize robot
        print("\nInitializing robot...")
        robot.initialize(mode=2)
        time.sleep(5)

        # Run examples
        absolute_position_control(robot)

        ratio_based_control(robot)

        smooth_movement(
            robot,
            start_positions=[100, 100, 100, 100, 100, 100],
            end_positions=[400, 400, 400, 400, 400, 400],
            steps=20,
            delay=0.3,
        )

        speed_control_demo(robot)

        force_control_demo(robot)

        individual_axis_control(robot)

        print("\n=== All position control examples completed ===")


if __name__ == "__main__":
    main()
