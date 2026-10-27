<h1 align="center"> pyMAVLinCS </h1>
<p align="center"> The high-level Python API for reliable, autonomous drone control, advanced telemetry, and MAVLink mission management. </p>

<p align="center">
  <img alt="License_new" src="https://img.shields.io/badge/License-GPL%20v3-yellow">
  <a href="https://github.com/noahredon/pyMAVLinCS/actions/workflows/test.yml"><img alt="Tests" src="https://img.shields.io/github/actions/workflow/status/noahredon/pyMAVLinCS/test.yml?branch=main&label=tests&logo=github"></a>
  <img alt="GitHub" src="https://img.shields.io/badge/github-noahredon-blue?logo=github">
  <img alt="Python" src="https://img.shields.io/badge/Python-grey?logo=python">
</p>
<!-- 
https://shields.io
-->

***

## 📖 Table of Contents
*   [✨ Overview](#-overview)
*   [🚀 Key Features](#-key-features)
*   [🛠️ Tech Stack & Architecture](#-tech-stack--architecture)
*   [📁 Project Structure](#-project-structure)
*   [📸 Demo & Screenshots](#-demo--screenshots)
*   [⚙️ Getting Started](#-getting-started)
*   [🎯 Usage](#-usage)
*   [🤝 Contributing](#-contributing)
*   [📝 License](#-license)

***

## ✨ Overview

pyMAVLinCS is a powerful, professional-grade Python library designed to simplify the development of autonomous systems by providing a high-level, stable, and feature-rich interface for MAVLink-based flight controllers (like ArduPilot and PX4).

> ⚠️ **The Problem:** Developing complex drone missions or ground control stations (GCS) often requires deep, low-level integration with the MAVLink protocol. This involves handling command acknowledgments, managing asynchronous message streams (like `STATUSTEXT` or `TIMESYNC`), performing complex geographic calculations, and ensuring thread safety, leading to verbose and error-prone code.

pyMAVLinCS eliminates this complexity by wrapping the core `pymavlink` functionality into an intuitive, object-oriented API (`MAVLinCS` class). It enables developers and engineers to execute mission-critical commands, retrieve comprehensive telemetry, manage gimbal payloads, and handle inter-system communication using simple, Pythonic method calls. This allows users to focus entirely on mission logic and operational safety, drastically reducing development time and enhancing code reliability.

The library is built around core Python features, geographic computations (`geopy`), and MAVLink messages handler (`pymavlink`). Internal handler classes ensure seamless management of complex MAVLink processes like statustext reconstruction, timesync calculation, and structured logging.

***

## 🚀 Key Features

pyMAVLinCS provides comprehensive capabilities spanning control, data retrieval, mission management, and advanced system configuration. These features are implemented through a rich set of methods in the core `MAVLinCS` class.

### 📡 Real-Time Telemetry and System Status

Gain instant access to crucial flight and system data using simple method calls that handle message retrieval and parsing automatically:
*   🛰️ **Global Position (`position_gps`):** Retrieve current GPS coordinates (latitude, longitude, altitude) and local coordinates (`position_local`).
*   🧭 **Attitude and Velocity:** Get precise attitude angles (`angles`) and angular rates (`angular_rates`). Retrieve linear velocities in three dimensions (`speed`) and absolute module speed (`speed_module`).
*   ⚡ **Power Monitoring:** Check remaining battery percentage (`battery_percentage`) and current voltage (`battery_voltage`) (requires flight controller configuration).
*   ⚙️ **Flight Status:** Instantly check arming status (`motors_armed`, `motors_disarmed`), current flight mode (`mode`, `custom_mode`), and base mode details (`base_mode`, `custom_main_mode`, `custom_sub_mode` for PX4 systems).
*   🌐 **Fix Status:** Confirm the status of the GPS system, including 3D fix availability (`gps_3d_fix`).
*   🕒 **Timing Data:** Access system boot time in seconds (`time_boot`) and milliseconds (`time_boot_ms`), and Unix timestamp in microseconds (`time_usec`).

### 🕹️ Autonomous Control and Action Execution

Execute mission-critical commands with built-in acknowledgment handling to ensure reliable action completion:
*   🔑 **System State Management:** Safely arm (`arm`) or disarm (`disarm`) the drone, with options for forced execution and command timeout.
*   🚁 **Movement Commands:** Initiate automated takeoff (`takeoff`) to a specified altitude or perform a simple landing (`land`, currently implemented for ArduPilot).
*   🔄 **Flight Mode Control:** Change the flight behavior using high-level names, integers, or tuples to specify mode (`set_mode`).
*   🗺️ **Targeted Movement:** Set precise GPS position targets (`set_gps_pos_target`) or local position targets (`set_local_pos_target`) for navigation.
*   💨 **Velocity Control:** Directly command the drone's velocity components (`set_speed`) (North, East, Down in m/s).
*   🏠 **Return to Launch (RTL):** Send a Return-To-Launch request (`return_to_launch`) for safe mission abort.

### 📐 Advanced Position and Geographic Utility

Utilize powerful built-in mathematical functions for complex navigation and coordinate system management:
*   📍 **Home Position Management:** Request and retrieve the designated HOME position (`request_home_position`, `home_position`) and set a new HOME location (`set_home`, `set_home_current_pos`).
*   🌍 **EKF Origin:** Get or set the EKF origin location (`ekf_origin`, `set_ekf_origin`) for accurate local navigation initialization.
*   📏 **Distance Calculation:** Calculate the distance between the flight controller and a specified GPS point (`get_distance_with_gps_pos`) or a local coordinate point (`get_distance_with_local_pos`).
*   🔄 **Coordinate Conversion Utilities:** Perform complex geometric transformations, including conversion from Quaternion to Euler angles (`quaternion_to_euler`), distance between two GPS points (`distance_between_two_gps_points`), and converting Cartesian or polar displacements relative to the drone's position into geographic points (`cartesian_to_geographic_point`, `polar_to_geographic_point`).

### ⚙️ Mission Planning and Waypoint Management

Simplify the workflow for designing and executing automated missions:
*   🔢 **Waypoint Management:** Send individual waypoints (`send_waypoint`), inform the flight controller of the total number of waypoints being sent (`send_waypoint_count`), or delete all stored waypoints (`clear_waypoints`).
*   ▶️ **Mission Execution:** Start the loaded mission from a specified waypoint (`start_mission`, currently implemented for ArduPilot).
*   ✅ **Mission Status:** Check the sequence number of the current waypoint (`current_waypoint_seq`) and verify if the mission is completed (`is_waypoint_mission_completed`).

### 📸 Gimbal and Payload Control

Integrated support for controlling camera gimbals and other peripherals:
*   🖼️ **Angle Setting:** Orient the gimbal precisely by setting pitch and yaw angles (`set_gimbal_angles`).
*   📌 **Position Targeting:** Send a target GPS position for the gimbal to track (`set_gimbal_target`).
*   🔌 **Mode Setting:** Set the gimbal to retract position (no stabilization, `set_gimbal_retract`) or neutral position (roll=pitch=yaw=0, `set_gimbal_neutral`).
*   📏 **Servo Control:** Directly set the PWM value for any specific servo channel (`set_servo`).

### 🔔 Asynchronous Communication & Messaging

Dedicated handler classes simplify listening for and sending custom messages:
*   💬 **Status Text Handling:** Receive and reconstruct segmented `STATUSTEXT` messages (`last_statustext_from_sysidcompid`).
*   🕰️ **Latency Monitoring:** Send `TIMESYNC` broadcasts (`send_timesync`) and retrieve the estimated one-way latency (`get_latence_ms_with_sysidcompid`) to various components.
*   📢 **Custom Messaging:** Send status messages (`send_statustext`), named integer values (`send_named_value_int`), or proprietary Mission Control Code (MCC) messages (`send_mcc`, `check_mcc`, `delete_mcc`).

### ⏳ Synchronized Wait Operations

Implement robust, blocking operations that pause execution until a required condition is met:
*   🔒 **Arming Synchronization:** Wait until motors are confirmed armed or disarmed (`wait_motors_armed`, `wait_motors_disarmed`).
*   ✈️ **Mode Synchronization:** Wait for the flight mode to successfully change (`wait_mode_changed`).
*   📍 **Position Synchronization:** Wait until a GPS 3D fix is obtained (`wait_gps_3d_fix`) or until the drone reaches proximity to a target GPS or local position (`wait_proximity_with_gps_pos`, `wait_proximity_with_local_pos`).
*   📝 **Command Acknowledgment:** Block execution until a specific `COMMAND_ACK` or `MISSION_ACK` is received and validated (`wait_command_ack`, `wait_mission_ack`).

***

## 🛠️ Tech Stack & Architecture

pyMAVLinCS is designed as a focused Python library, utilizing highly optimized core components for reliable aerospace communication and data processing.

| Technology | Purpose | Why it was Chosen |
| :--- | :--- | :--- |
| **Python** | Primary development language for the API. | Provides a clean, readable syntax ideal for complex robotics and scientific computation. |
| **pymavlink** | Core dependency for MAVLink protocol communication. | Essential library for parsing, generating, and transmitting MAVLink messages to flight controllers. |
| **geopy** | Dependency for geographic calculations. | Provides accurate tools for distance, azimuth, and coordinate transformation necessary for mission planning. |
| **pytest** | Testing framework for unit and SITL integration tests. | Provides an extensible framework for running automated tests with simulated drones (ArduPilot SITL). |
| **setuptools** | Build system component. | Standard tool used for packaging and distributing Python projects, defining the required metadata. |
| **wheel** | Build system component. | Enables the creation of standardized binary distribution packages for faster installation. |

***

## 📁 Project Structure

The project structure is organized to separate the core MAVLink interface, supporting utility classes, examples, and CI/CD configurations.

```
📂 pyMAVLinCS/
├── 📂 pyMAVLinCS/                     # Core Library Package
│   ├── 📄 __init__.py                 # Main entry point (MAVLinCS class definition, all control methods)
│   ├── 📄 mission_control_code.py     # Class definition for MCC (Mission Control Code) messages
│   ├── 📄 mavtypes.py                 # Data models (GPSPosition, Angles, Speed, HomePosition, etc.)
│   ├── 📄 setup_logger.py             # Logging setup utility and custom formatters
│   └── 📄 mavecstra.py                # Core MAVLink communication extensions (TimesyncHandler, StatustextReceiver)
├── 📂 examples/                       # Demonstrative usage scripts
│   ├── 📄 arm_drone.py                # Example script for arming procedure
│   ├── 📄 mcc_creation.py             # Example script showing MCC object usage
│   ├── 📄 __init__.py                 # Initialization file for examples package
│   └── 📄 connection_test.py          # Script to test basic flight controller connectivity
├── 📂 tests/                          # Automated test suite (unit and SITL integration tests)
│   ├── 📄 conftest.py                 # Pytest configuration and SITL fixtures
│   ├── 📄 test_basic.py               # Basic connectivity & initialization tests
│   ├── 📄 test_commands.py            # MAVLink command execution tests
│   ├── 📄 test_control.py             # Drone control & navigation tests
│   ├── 📄 test_math.py                # Mathematical and geographic utility tests
│   ├── 📄 test_mcc.py                 # Mission Control Code tests
│   ├── 📄 test_telemetry.py           # Real-time telemetry tests
│   └── 📄 __init__.py                 # Initialization file for tests package
├── 📂 .github/                        # GitHub configuration
│   └── 📂 workflows/                  # Continuous Integration & Delivery workflows
│       ├── 📄 test.yml                # CI workflow (pytest with ArduPilot SITL)
│       └── 📄 publish.yml             # CD workflow for package publication (PyPI)
├── 📄 pytest.ini                      # Pytest configuration file
├── 📄 pyproject.toml                  # Project metadata, dependencies, and build requirements
├── 📄 LICENSE                         # Project License (GPL-3.0-or-later)
├── 📄 README.md                       # Project documentation (this file)
└── 📄 .gitignore                      # Git ignore rules
```

***

## ⚙️ Getting Started

To utilize pyMAVLinCS, you need Python and the necessary dependencies. This library is distributed via standard Python package mechanisms.

### Prerequisites

Ensure you have the following installed:

*   **Python:** Version 3.8 or higher (`>=3.8` is required).
*   **A MAVLink-compatible flight controller** (e.g., ArduPilot, PX4).
*   **A stable communication link** (e.g., USB, Serial, UDP).

### Installation

Since pyMAVLinCS is packaged using `setuptools` and defined in `pyproject.toml`, standard installation methods will pull all required dependencies (`pymavlink`, `pyserial`, `geopy`).

1. **Install the library using pip:**

```bash
pip install pyMAVLinCS
```

2. **Verify installation:**
You should now be able to import the core class in your Python environment:

```python
from pyMAVLinCS import MAVLinCS

# Ready to initialize a connection
```

***

## 🎯 Usage

pyMAVLinCS is used by instantiating the core `MAVLinCS` class with the desired connection address (it opens the connection). The library handles opening and closing the MAVLink connection and managing all internal communication threads.

### 1. Establishing a Connection

The `MAVLinCS` class constructor requires an address string that specifies the connection method (e.g., TCP, UDP, serial).

```python
from pyMAVLinCS import MAVLinCS

# Example 1: Connect via UDP to a GCS port (common simulation setup)
udp_address = 'udp:127.0.0.1:14550'
drone = MAVLinCS(address=udp_address)

# Example 2: Connect via Serial (replace /dev/ttyACM0 with your serial port)
# serial_address = '/dev/ttyACM0'
# baudrate = 921600
# drone = MAVLinCS(address=serial_address, baud=baudrate)
```

### 2. Performing Autonomous Actions (Control)

Execute complex command and control actions with built-in acknowledgment waits:

```python
try:
  # Wait for the drone to achieve a 3D GPS fix before proceeding
  print("Waiting for 3D GPS Fix...") # You can also use the logger directly from the MAVLinCS object
  # drone.logger.info("Waiting for 3D GPS Fix...")
  drone.wait_gps_3d_fix()
  print("GPS Fix Acquired.")

  # Arm the drone (waits for confirmation)
  armed = drone.arm()
  if not armed:
    raise RuntimeError("Drone not armed.")
  print("Drone armed successfully.")

  # Change the flight mode to 'GUIDED' (example for ArduPilot)
  mode_changed = drone.set_mode('GUIDED')
  if not mode_changed:
    raise RuntimeError("Drone not in GUIDED mode.")
  print(f"Current Mode: {drone.mode()}")

  # Execute a takeoff to 10 meters (requires prior arming)
  takeoff_successful = drone.takeoff(altitude=10)
  if not takeoff_successful:
    raise RuntimeError("Drone takeoff failed.")
  print("Takeoff successful.")
except (Exception, KeyboardInterrupt) as e:
  drone.close()
  print("Connection closed.")
  raise e
```

### 3. Retrieving Real-Time Telemetry

Access structured data models defining the drone's state:

```python
try:
  # Get current GPS position and local position
  gps_pos = drone.position_gps()
  local_pos = drone.position_local()

  print(f"\n--- Telemetry Snapshot ---")
  print(f"Latitude: {gps_pos.lat:.6f}°, Longitude: {gps_pos.lon:.6f}°, Altitude (GPS): {gps_pos.alt:.2f}m")
  print(f"North (Local): {local_pos.x:.2f}m, East (Local): {local_pos.y:.2f}m")

  # Get attitude angles (roll, pitch, yaw)
  angles = drone.angles()
  print(f"Roll: {angles.roll:.1f}rad, Pitch: {angles.pitch:.1f}rad, Yaw: {angles.yaw:.1f}rad")

  # Check battery status
  voltage = drone.battery_voltage()
  percentage = drone.battery_percentage()
  print(f"Battery: {percentage}% ({voltage}V)")
except (Exception, KeyboardInterrupt) as e:
  drone.close()
  print("Connection closed.")
  raise e
```

### 4. Mission Management

pyMAVLinCS also allows the sending of Mission Control Codes, enabling simple communication between two ground stations.

You can create a Python file (e.g. `mcc_creation.py`) where you define some Mission Control Codes:

```python
from pyMAVLinCS.mission_control_code import MCC

DRONE_STARTED = MCC(
    value=1,
    name="DRONE_STARTED",
    level="SUCCESS",
    description="Drone started."
)
```

and in your main file, you can specify it with the `mcc_class` argument while creating a MAVLinCS instance, or you can use it like this:

```python
import mcc_creation as mcc_mod

drone.mcc_class = mcc_mod.MCC
drone.send_mcc(mcc_mod.DRONE_STARTED)
```

For the other ground station, you also need to specify the right MCC Class in your Python script. In this case, MCCs will be stored in a set and logged in a concise way: `[level][name] description`.

You can also add a callback when receiving a MCC with `set_mcc_callback`, check anytime if a MCC is stored with `check_mcc` or delete the stored MCC with `delete_mcc`.

### 5. Closing the Connection

Always ensure the connection is safely closed to stop the background communication thread and the connection closure (e.g. if using a serial link):

```python
# Close the connection when done
drone.close()
print("Connection closed.")
```

***

## 🤝 Contributing

We welcome contributions to improve pyMAVLinCS! Your input helps make this project a more robust and reliable tool for autonomous vehicle development.

### How to Contribute

1. **Fork the repository** - Click the 'Fork' button at the top right of this page.
2. **Create a feature branch**
   ```bash
   git checkout -b feature/new-telemetry-endpoint
   ```
3. **Make your changes** - Improve code, documentation, or features within the `pyMAVLinCS/` directory.
4. **Test thoroughly** - Ensure all existing and new functionality works as expected. Automated tests run on push and PR via GitHub Actions using ArduPilot SITL. You can run the test suite locally with `pytest`:
   ```bash
   # Run the automated test suite:
   pytest tests/

   # Or execute manual test scripts / examples:
   python examples/connection_test.py 
   ```
5. **Commit your changes** - Write clear, descriptive commit messages.
   ```bash
   git commit -m 'Fix: Corrected latency calculation bug in TimesyncHandler'
   ```
6. **Push to your branch**
   ```bash
   git push origin feature/new-telemetry-endpoint
   ```
7. **Open a Pull Request** - Submit your changes for review by the maintainers.

### Development Guidelines

*   ✅ Follow the existing Python code style and conventions.
*   📝 Add comprehensive docstrings and comments for complex logic, especially within `MAVLinCS` and `mavecstra.py`.
*   🧪 Whenever possible, ensure changes are verified against a MAVLink simulator or hardware.
*   📚 Update documentation, including the `README.md`, for any changed functionality or new public methods.
*   🔄 Ensure backward compatibility when modifying existing API calls.
*   🎯 Keep commits focused and atomic, addressing a single feature or bug fix per commit.

### Ideas for Contributions

We're looking for help with:

*   🐛 **Bug Fixes:** Address issues related to connection stability or command ACK timeouts.
*   ✨ **New Features:** Implement support for newly released MAVLink messages or system types.
*   📖 **Documentation:** Improve tutorials, usage examples in the `examples/` directory, and method descriptions.
*   ⚡ **Performance:** Optimize message parsing and handler loop efficiency in `mavecstra.py`.
*   🧪 **Testing:** Expand the test suite coverage in the `tests/` directory.

### Code Review Process

*   All submissions require review before merging.
*   Maintainers will provide constructive feedback on clarity, efficiency, and adherence to MAVLink best practices.
*   Changes may be requested before approval.
*   Once approved, your PR will be merged, and you'll be credited for your contribution.

### Questions?

Feel free to open an issue for any questions or concerns regarding development, usage, or MAVLink specifics. We're here to help!

***

## 📝 License

This project is licensed under the **GPL-3.0-or-later** license - see the [LICENSE](LICENSE) file for complete details.

### What this means:

*   ✅ **Commercial Use:** You can use this software for commercial purposes.
*   ✅ **Modification:** You can modify the code.
*   ✅ **Distribution:** You can distribute this software.
*   ✅ **Private Use:** You can use this project privately.
*   ✅ **Patent Use:** You are granted rights to use patents related to the software.
*   ⚠️ **Source Code Disclosure:** If you distribute modified versions of this software, you must disclose the source code under the same license terms.
*   ⚠️ **Warranty:** The software is provided "as is," without warranty of any kind.

---

<p align="center">
  <a href="#">⬆️ Back to Top</a>
</p>