<h1 align="center"> pyMAVLinCS </h1>
<p align="center"> The high-level Python API for reliable, autonomous drone control, advanced telemetry, and MAVLink mission management. </p>

<p align="center">
  <img alt="License_new" src="https://img.shields.io/badge/License-MPL%202.0-brightgreen">
  <a href="https://noahredon.github.io/pyMAVLinCS-documentation/pyMAVLinCS.html"><img alt="Docs" src="https://img.shields.io/badge/docs-online-blue?logo=sphinx"></a>
  <a href="https://github.com/noahredon/pyMAVLinCS/actions/workflows/test.yml"><img alt="Tests" src="https://img.shields.io/github/actions/workflow/status/noahredon/pyMAVLinCS/test.yml?branch=main&label=tests&logo=github"></a>
  <img alt="GitHub" src="https://img.shields.io/badge/github-noahredon-blue?logo=github">
  <img alt="Python" src="https://img.shields.io/badge/Python-%3E%3D3.10-blue?logo=python">
</p>

***

## 📖 Table of Contents
- [✨ Overview](#-overview)
- [🚀 Key Features](#-key-features)
- [🛠️ Tech Stack & Architecture](#-tech-stack--architecture)
- [📁 Project Structure](#-project-structure)
- [⚙️ Getting Started](#-getting-started)
- [🎯 Usage](#-usage)
- [🤝 Contributing](#-contributing)
- [📝 License](#-license)

***

## ✨ Overview

> 🌐 **Full Online Documentation:** [https://noahredon.github.io/pyMAVLinCS-documentation/pyMAVLinCS.html](https://noahredon.github.io/pyMAVLinCS-documentation/pyMAVLinCS.html)

pyMAVLinCS is a powerful, professional-grade Python library designed to simplify the development of autonomous systems by providing a high-level, stable, and feature-rich interface for MAVLink-based flight controllers (like ArduPilot and PX4).

> ⚠️ **The Problem:** Developing complex drone missions or ground control stations (GCS) often requires deep, low-level integration with the MAVLink protocol. This involves handling command acknowledgments, managing asynchronous message streams (like `STATUSTEXT` or `TIMESYNC`), performing complex geographic calculations, and ensuring thread safety, leading to verbose and error-prone code.

pyMAVLinCS eliminates this complexity by wrapping the core `pymavlink` functionality into an intuitive, object-oriented API (`MAVLinCS` class). It enables developers and engineers to execute mission-critical commands, retrieve comprehensive telemetry, manage gimbal payloads, and handle inter-system communication using simple, Pythonic method calls. This allows users to focus entirely on mission logic and operational safety, drastically reducing development time and enhancing code reliability.

The library is built around core Python features, geographic computations (`geopy`), and a thread-safe MAVLink message handler (`pymavlink`). Internal handler classes ensure seamless management of complex MAVLink processes like `STATUSTEXT` chunk reconstruction, `TIMESYNC` latency calculation, automatic `.tlog` flight recording, and structured console/file logging.

***

## 🚀 Key Features

pyMAVLinCS provides comprehensive capabilities spanning control, data retrieval, mission management, and advanced system configuration through the core `MAVLinCS` class.

### 📡 Real-Time Telemetry and System Status

Gain instant access to crucial flight and system data using simple method calls that handle message retrieval and parsing automatically:
- 🛰️ **Global & Local Position:** Retrieve current GPS coordinates (`position_gps`: latitude, longitude, relative altitude, MSL altitude) and local NED coordinates (`position_local`).
- 🧭 **Attitude and Velocity:** Get precise attitude Euler angles (`angles`) and angular rates (`angular_rates`). Retrieve linear velocities in three dimensions (`speed`) and absolute speed norm (`speed_module`).
- ⚡ **Power Monitoring:** Check remaining battery percentage (`battery_percentage`) and current voltage in Volts (`battery_voltage`).
- ⚙️ **Flight Status:** Instantly check arming status (`motors_armed`, `motors_disarmed`), autopilot type (`autopilot_int`, `autopilot_str`), vehicle type (`vehicle_type_int`, `vehicle_type_str`), current flight mode (`mode`, `custom_mode`), and PX4 mode details (`base_mode`, `custom_main_mode`, `custom_sub_mode`).
- 🌐 **Fix Status:** Confirm the status of the GPS system, including 3D fix availability (`gps_3d_fix`).
- 🕒 **Timing Data:** Access system boot time in seconds (`time_boot`) and milliseconds (`time_boot_ms`), and Unix timestamp in microseconds (`time_usec`).

### 🕹️ Autonomous Control and Action Execution

Execute mission-critical commands with built-in acknowledgment handling to ensure reliable action completion:
- 🔑 **System State Management:** Safely arm (`arm`) or disarm (`disarm`) the drone, with automatic pre-arm mode checks on ArduPilot, optional forced execution, and configurable timeouts.
- 🚁 **Takeoff & Landing:** Initiate automated takeoff (`takeoff`) to a specified altitude (including in-air vertical repositioning) or perform an automated landing (`land`).
- 🔄 **Flight Mode Control:** Change the flight mode using human-readable mode names, ArduPilot mode IDs, or PX4 mode tuples (`set_mode`).
- 🗺️ **Targeted Movement:** Set precise GPS position targets (`set_gps_pos_target`) or local NED position targets (`set_local_pos_target`) with optional yaw control.
- ✈️ **Reposition** Commands the vehicle to reposition to a specific GPS location (`do_reposition`) with optional arguments. Can be used for fixed-wings in Guided/Hold mode.
- 💨 **Velocity Control:** Directly command the drone's velocity components (`set_speed`: North, East, Down in m/s) and heading.
- 🏠 **Return to Launch (RTL):** Send a Return-To-Launch request (`return_to_launch`) for safe mission abort.
- 🎯 **Dynamic Vehicle Following:** Autonomously take off and follow another moving MAVLink vehicle in real time (`do_follow`, `do_follow_with_takeoff`).
- 🛬 **Precision Landing Target:** Stream visual/IR landing target offsets in the drone's body frame (`send_landing_target`).
- 🔧 **System Configuration & Reboot:** Request the full parameter list into cache (`request_all_parameters`), read and modify flight controller parameters on the fly with `PARAM_VALUE` confirmation and automatic retries (`get_parameter`, `write_parameter`), adjust telemetry message streaming rates (`set_msg_rate`), or trigger an autopilot reboot (`reboot`).
- 🛡️ **Built-in Safety Switches:** Instantly inhibit physical flight commands (`allow_actions = False`) or abort all blocking waits across threads (`mission_ended = True`).

### 📐 Advanced Position and Geographic Utility

Utilize powerful built-in mathematical functions for complex navigation and coordinate system management:
- 📍 **Home Position Management:** Request and retrieve the designated HOME position (`request_home_position`, `home_position`) and set a new HOME location (`set_home`, `set_home_current_pos`).
- 🌍 **EKF Origin:** Get or set the EKF origin location (`ekf_origin`, `set_ekf_origin`) for accurate local navigation initialization.
- 📏 **Distance Calculation:** Calculate 2D/3D distances between the flight controller and a specified GPS point (`get_distance_with_gps_pos`) or local coordinate point (`get_distance_with_local_pos`).
- 🔄 **Coordinate Conversion Utilities:** Perform geometric transformations, including Quaternion to Euler conversion (`quaternion_to_euler`), 2D/3D distances between arbitrary points (`distance_between_two_gps_points`, `distance_between_two_local_points`), Cartesian/polar projections to GPS coordinates (`cartesian_to_geographic_point`, `polar_to_geographic_point`), and GPS-to-Cartesian displacements (`geographic_to_cartesian_point`).

### ⚙️ Mission Planning and Waypoint Management

Simplify the workflow for designing and executing automated `AUTO` missions:
- 🔢 **Reliable Mission Upload:** Upload an entire list of waypoints (`MissionItem`, `dict`, or `tuple`) in a single call (`upload_mission`) implementing the full MAVLink Mission Protocol state machine (`MISSION_COUNT` -> `MISSION_REQUEST_INT` / `MISSION_REQUEST` -> `MISSION_ITEM_INT` -> `MISSION_ACK`) with automatic retries on packet loss.
- 🛠️ **Low-Level Waypoint Primitives:** Clear stored missions (`clear_waypoints`), announce waypoint counts (`send_waypoint_count`), and upload individual mission items (`send_waypoint`).
- ▶️ **Mission Execution:** Start the loaded mission from the ground or in flight (`start_mission`).
- ✅ **Mission Status:** Check the active waypoint sequence number (`current_waypoint_seq`) and verify if the waypoint mission is completed (`is_waypoint_mission_completed`).

### 📸 Gimbal and Payload Control

Integrated support for controlling camera gimbals and servo peripherals:
- 🖼️ **Angle & Rate Control:** Orient the gimbal precisely by setting pitch/yaw angles, rotation speeds, and reference frames (`set_gimbal_angles`), or read current gimbal orientation (`gimbal_angles`).
- 📌 **ROI Position Targeting:** Command the gimbal to track a specific GPS coordinate (`set_gimbal_target`).
- 🔌 **Gimbal Modes:** Set the gimbal to retract mode (`set_gimbal_retract`) or neutral position (`set_gimbal_neutral`).
- 📏 **Servo Control:** Actuate any servo channel (`set_servo`) and read live PWM outputs (`servo_pwm`).

### 🔔 Asynchronous Communication, Callbacks & Logging

Dedicated handler classes simplify listening for and sending custom messages:
- 📼 **Automatic `.tlog` Flight Logging:** Automatically records all incoming and outgoing MAVLink packets into a standard `.tlog` binary file (`MavLogger`), ready for replay in Mission Planner or QGroundControl.
- 💬 **Status Text Handling:** Automatically reassemble multi-chunk `STATUSTEXT` messages (`StatustextReceiver`, `last_statustext_from_sysidcompid`) and send chunked status texts (`send_statustext`).
- 🕰️ **Latency Monitoring:** Broadcast `TIMESYNC` requests (`send_timesync`) and monitor one-way link latency (`get_latence_ms_with_sysidcompid`).
- 📢 **Mission Control Codes (MCC):** Define, send, check, and delete custom named integer codes (`MCC`, `send_mcc`, `check_mcc`, `delete_mcc`, `send_named_value_int`) for multi-agent or GCS-to-companion synchronization.
- ⚡ **Event Callbacks:** Register custom callbacks for incoming messages (`set_additional_recv_msg_callback`), outgoing messages (`set_additional_send_callback`), complete status texts (`set_statustext_callback`), or MCC events (`set_mcc_callback`).

### ⏳ Synchronized Wait Operations

Implement robust, blocking operations with timeout and abort support:
- 🔒 **Arming Synchronization:** Wait until motors are confirmed armed or disarmed (`wait_motors_armed`, `wait_motors_disarmed`).
- ✈️ **Mode Synchronization:** Wait for a flight mode transition to complete (`wait_mode_changed`).
- 📍 **Navigation Synchronization:** Wait for a 3D GPS fix (`wait_gps_3d_fix`), HOME position reception (`wait_for_home`), or target proximity in GPS/local coordinates (`wait_proximity_with_gps_pos`, `wait_proximity_with_local_pos`).
- 📝 **Command & Mission Acknowledgments:** Block execution until a specific `COMMAND_ACK` or `MISSION_ACK` is received and validated (`wait_command_ack`, `wait_mission_ack`).

***

## 🛠️ Tech Stack & Architecture

pyMAVLinCS is designed as a focused Python library, utilizing proven components for reliable aerospace communication and data processing.

| Technology | Purpose | Why it was Chosen |
| :--- | :--- | :--- |
| **Python (>=3.10)** | Primary development language for the API. | Provides clean type-annotated syntax ideal for robotics and embedded companion computers. |
| **pymavlink** | Core dependency for MAVLink protocol communication. | Standard library for parsing, packing, and transmitting MAVLink 2 messages. |
| **geopy** | Dependency for geographic calculations. | Provides accurate geodesics for distance, bearing, and coordinate projection. |
| **colorama** | Terminal output formatting. | Enables color-coded severity levels in the built-in console logger. |
| **pytest** | Testing framework for unit and SITL integration tests. | Powers automated continuous integration against ArduPilot SITL. |

***

## 📁 Project Structure

The project structure separates the core MAVLink interface, supporting utility classes, usage examples, and automated SITL tests.

```text
📂 pyMAVLinCS/
├── 📂 pyMAVLinCS/                              # Core Library Package
│   ├── 📄 __init__.py                          # Main entry point (MAVLinCS class definition)
│   ├── 📄 mavecstra.py                         # Threading, TimesyncHandler, StatustextReceiver, MavLogger
│   ├── 📄 mavtypes.py                          # Typed data models (GPSPosition, Angles, Speed, etc.)
│   ├── 📄 mission_control_code.py              # Class definition for MCC (Missio Control Code)
│   └── 📄 setup_logger.py                      # Logging setup utility and custom console/file formatters
├── 📂 examples/                                # Demonstrative usage scripts
│   ├── 📄 01_basic_takeoff_and_land.py         # Pre-flight telemetry, arming, takeoff, and landing
│   ├── 📄 02_guided_navigation_and_velocity.py # Local NED, GPS polar projection, velocity circle, RTL
│   ├── 📄 03_autonomous_waypoint_mission.py    # Building, uploading, and monitoring AUTO missions
│   ├── 📄 04_custom_mcc_and_callbacks.py       # Custom MCCs, asynchronous callbacks, and TIMESYNC
│   ├── 📄 05_modes_parameters_and_low_level.py # Modes, parameters, raw messages, and connection lifecycle
│   ├── 📄 06_gimbal_servo_and_precision_landing.py # Gimbal stabilization, servos, and LANDING_TARGET
│   ├── 📄 07_home_ekf_and_geometry_utils.py    # HOME/EKF origin management and geodesic utilities
│   └── 📄 08_vehicle_following.py              # Autonomous multi-vehicle following (FOLLOW mode)
├── 📂 tests/                                   # Automated test suite (Unit & ArduPilot SITL)
│   ├── 📄 conftest.py                          # Pytest configuration and automated SITL fixtures
│   ├── 📄 test_01_unit_offline.py              # Offline geometry, math, MCC, and safety guard tests
│   ├── 📄 test_02_telemetry_comms.py           # Telemetry getters, HOME, TIMESYNC, callbacks, and params
│   ├── 📄 test_03_flight_guided.py             # Full GUIDED flight test (takeoff, NED, GPS, speed, servo)
│   └── 📄 test_04_missions_auto.py             # In-air and ground-start AUTO waypoint mission tests
├── 📂 .github/                                 # GitHub configuration
│   └── 📂 workflows/                           # Continuous Integration & Delivery workflows
│       ├── 📄 test.yml                         # CI workflow (pytest against ArduPilot SITL master)
│       └── 📄 publish.yml                      # CD workflow for PyPI package publication
├── 📄 pytest.ini                               # Pytest configuration file
├── 📄 pyproject.toml                           # Project metadata, dependencies, and build requirements
├── 📄 LICENSE                                  # Project License (MPL 2.0)
├── 📄 README.md                                # Project documentation (this file)
└── 📄 .gitignore                               # Git ignore rules
```

***

## ⚙️ Getting Started

### Prerequisites

Ensure you have the following installed:
- **Python:** Version **3.10** or higher (`>=3.10` is required).
- **A MAVLink-compatible flight controller or simulator** (e.g., ArduPilot SITL, PX4, Pixhawk, Cube).
- **A communication link** (e.g., UDP, TCP, USB/Serial telemetry radio).

### Installation

1. **Install the library using pip:**

```bash
pip install pyMAVLinCS
```

2. **Verify installation:**

```python
from pyMAVLinCS import MAVLinCS
```

***

## 🎯 Usage

pyMAVLinCS is used by instantiating the `MAVLinCS` class with your connection address. The instance automatically opens the link, waits for a valid `HEARTBEAT`, configures telemetry rates, starts the background `MavThread`, and begins recording a `.tlog` file.

### 1. Establishing a Connection

```python
from pyMAVLinCS import MAVLinCS

# Example 1: Connect via UDP to an ArduPilot SITL / GCS endpoint
drone = MAVLinCS(
    address="udpin:127.0.0.1:14550",
    mavlogfile="flight.tlog",
    timeout_heartbeat=10,
    pos_rate=4
)

# Example 2: Connect via Serial (replace /dev/ttyACM0 with your serial port)
# drone = MAVLinCS(address="/dev/ttyACM0", baud=57600)
```

### 2. Performing Autonomous Actions (Control)

Execute flight commands with built-in acknowledgment and state verification:

```python
try:
    # Wait for the drone to achieve a 3D GPS fix before proceeding
    drone.logger.info("Waiting for 3D GPS Fix...")
    if not drone.wait_gps_3d_fix(timeout=30):
        raise RuntimeError("GPS 3D Fix timeout.")

    # Arm the drone (automatically switches to GUIDED mode if needed on ArduPilot)
    if not drone.arm(timeout_arming=10):
        raise RuntimeError("Drone failed to arm.")

    # Execute a takeoff to 10 meters (waits until target altitude is reached)
    if not drone.takeoff(altitude=10.0, precision=0.5, timeout_takeoff=30):
        raise RuntimeError("Drone takeoff failed.")

    # Land safely and wait for motors to disarm
    drone.land(timeout_land=60)
except KeyboardInterrupt:
    drone.mission_ended = True
finally:
    drone.close()
```

### 3. Retrieving Real-Time Telemetry

Access structured `NamedTuple` data models defining the vehicle's state:

```python
# Get current GPS position and local NED position
gps_pos = drone.position_gps()
local_pos = drone.position_local()

print("\n--- Telemetry Snapshot ---")
print(f"Lat: {gps_pos.lat:.6f}°, Lon: {gps_pos.lon:.6f}°")
print(f"Relative Alt: {gps_pos.relative_alt:.2f}m | Alt (MSL): {gps_pos.alt:.2f}m")
print(f"Local NED -> North: {local_pos.x:.2f}m, East: {local_pos.y:.2f}m, Down: {local_pos.z:.2f}m")

# Get attitude angles (roll, pitch, yaw in radians)
angles = drone.angles()
print(f"Roll: {angles.roll:.2f} rad, Pitch: {angles.pitch:.2f} rad, Yaw: {angles.yaw:.2f} rad")

# Check battery status
print(f"Battery: {drone.battery_percentage()}% ({drone.battery_voltage():.2f}V)")
```

### 4. Uploading and Running an Autonomous Waypoint Mission

Use `MissionItem` and `upload_mission()` to reliably transfer a full `AUTO` mission to the flight controller using the MAVLink Mission Protocol handshake:

```python
from pymavlink import mavutil
from pyMAVLinCS import MAVLinCS, MissionItem

gps0 = drone.position_gps()
wp1 = MAVLinCS.cartesian_to_geographic_point(gps0.lat, gps0.lon, north_displacement=30.0, east_displacement=0.0)

mission = [
    MissionItem(command=mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, x=gps0.lat, y=gps0.lon, z=0.0),      # Seq 0: HOME
    MissionItem(command=mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, x=gps0.lat, y=gps0.lon, z=15.0),      # Seq 1: Takeoff
    MissionItem(command=mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, x=wp1.latitude, y=wp1.longitude, z=15.0),
    MissionItem(command=mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH),                             # Seq 3: RTL
]

if drone.upload_mission(waypoints=mission, clear_existing=True, timeout=15.0):
    drone.start_mission(timeout=10)
```

### 5. Mission Control Codes (MCC) & Callbacks

pyMAVLinCS provides Mission Control Codes (`MCC`) to simplify event synchronization between ground stations and companion computers over MAVLink (`NAMED_VALUE_INT`):

```python
from pyMAVLinCS import MAVLinCS, MCC

# Define a custom Mission Control Code
DRONE_READY = MCC(
    value=1,
    name="DRONE_READY",
    level="SUCCESS",
    description="Drone initialized and ready for mission."
)

drone = MAVLinCS(address="udpin:127.0.0.1:14550")

# Register a callback triggered whenever an MCC is received
drone.set_mcc_callback(lambda mcc: print(f"Received MCC: {mcc}"))

# Send, check, and delete an MCC
drone.send_mcc(DRONE_READY)
if drone.check_mcc(DRONE_READY):
    drone.delete_mcc(DRONE_READY)
```

### 6. Closing the Connection (or Using a Context Manager)

Always close the connection when finished to cleanly stop the background `MavThread`, close the serial/UDP link, and flush the `.tlog` file. You can either call `drone.close()` explicitly or use `MAVLinCS` as a Python context manager (`with` statement):

```python
with MAVLinCS(address="udpin:127.0.0.1:14550", mavlogfile="flight.tlog") as drone:
    drone.wait_gps_3d_fix(timeout=30)
    print(drone.position_gps())
# Connection, background thread, and .tlog file are automatically closed here
```

***

## 🤝 Contributing

We welcome contributions to improve pyMAVLinCS! Your input helps make this project a more robust and reliable tool for autonomous vehicle development.

### How to Contribute

1. **Fork the repository:** Click the 'Fork' button at the top right of this page.
2. **Create a feature branch:**
   ```bash
   git checkout -b feature/new-telemetry-endpoint
   ```
3. **Make your changes:** Improve code, documentation, or features within the `pyMAVLinCS/` directory.
4. **Test thoroughly:** Ensure all existing and new functionality works as expected. Automated tests run on push and PR via GitHub Actions using ArduPilot SITL. You can run the test suite locally with `pytest`:
   ```bash
   # Run the automated test suite:
   pytest tests/ -v -s

   # Or execute an example script:
   python examples/01_basic_takeoff_and_land.py
   ```
5. **Commit your changes:** Write clear, descriptive commit messages.
   ```bash
   git commit -m "Fix: Corrected latency calculation in TimesyncHandler"
   ```
6. **Push to your branch:**
   ```bash
   git push origin feature/new-telemetry-endpoint
   ```
7. **Open a Pull Request:** Submit your changes for review by the maintainers.

### Development Guidelines

- ✅ Follow the existing Python code style and type-hinting conventions (` PEP 8 `).
- 📝 Add comprehensive docstrings and comments for complex logic, especially within `MAVLinCS` and `mavecstra.py`.
- 🧪 Whenever possible, ensure changes are verified against ArduPilot/PX4 SITL or real hardware.
- 📚 Update documentation, including the `README.md`, for any changed functionality or new public methods.
- 🔄 Ensure backward compatibility when modifying existing API calls.
- 🎯 Keep commits focused and atomic, addressing a single feature or bug fix per commit.

***
## 📝 License

This project is licensed under the **Mozilla Public License 2.0 (MPL-2.0)** - see the [LICENSE](LICENSE) file for complete details.

### What this means:

- ✅ **Commercial & Private Use:** You can freely use this software in commercial, private, and proprietary closed-source applications.
- ✅ **Integration:** You can import and use `pyMAVLinCS` in your proprietary project without being forced to open-source your entire project.
- ✅ **Patent Grant:** You are explicitly granted rights to use patents related to this software.
- ⚠️ **File-Level Copyleft:** If you modify the original source files of `pyMAVLinCS` itself (e.g., fixing a bug or adding a feature to the library's core), you must make the source code of those specific modified files available under the MPL 2.0. New distinct files you create for your application remain yours.
- ⚠️ **Warranty:** The software is provided "as is," without warranty of any kind.

---

<p align="center">
  <a href="#-table-of-contents">⬆️ Back to Top</a>
</p>
