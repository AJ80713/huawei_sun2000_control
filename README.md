# ☀️ Huawei SUN2000 Inverter Control Examples ⚡

This repository provides **clean, educational, and fully working examples** for controlling **Huawei SUN2000** inverters and LUNA2000 batteries using **Modbus TCP and RTU protocols**. It aims to be beginner-friendly and well-documented so you can:

- Read telemetry from the inverter and battery
- Control forced charge/discharge behavior
- Validate inverter responses (errors, alarms, wake-up/sleep)
- Extract performance metrics (e.g., efficiency, voltage curves)

Every script runs standalone and uses [**`huawei_solar`**](https://github.com/wlcrs/huawei-solar) under the hood. You can adapt them for integration with home automation, data loggers, testing tools, etc.

---

## 🚀 Getting Started (Step-by-Step)

### 1. Clone this Repository
```bash
git clone https://github.com/YOUR_USERNAME/sun2000-control-examples.git
cd sun2000-control-examples
```

### 2. Install Python Dependencies
> With Internet:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

> Without Internet (from `packages/` folder):
```bash
python -m pip install --no-index --find-links packages -r requirements.txt
```

### 3. Check Your Inverter Connection
- **Modbus TCP**:
  - IP: e.g., `192.168.200.1`
  - Port: `6607`
  - Password: default is `00000a`
- **Modbus RTU**:
  - USB RS485 adapter (COMx or `/dev/ttyUSBx`)
  - Baudrate: 9600
  - Slave ID: usually `1`

### 4. Run Any Script
Each script is self-contained and can be launched from the terminal:
```bash
python battery_info.py
```

---

## 🔋 Scripts Explained

| Script | Description |
|--------|-------------|
| `battery_info.py` | Shows current forced charge/discharge configuration from the inverter. |
| `minimal_rtu_read.py` | Smallest possible RTU example: reads one register. Great for testing cable and port. |
| `read_rtu.py` | Tries common RTU configs (baudrate/slave ID). Useful for discovering valid RTU setup. |
| `rtu_battery_control.py` | Core RTU functions: force charging/discharging by power, period, or SoC target. |
| `rtu_command_tests.py` | Example flow: perform full charge/discharge cycles over RTU. Logs behavior. |
| `tcp_battery_control.py` | Core TCP helpers: login, set charge/discharge, idle, etc. |
| `tcp_command_tests.py` | Test commands like charge-to-80%, discharge-to-20% over TCP. |
| `test_battery_control.py` | Control battery and log responses. Useful for validation. |
| `test_errors.py` | Dump alarm registers like overvoltage, grid fault, battery disconnect. |
| `test_inverter_behavior.py` | Observe inverter state: sleeping, idling, running. Great for power-on tests. |
| `test_inverter_wakeup.py` | Force wake-up or idle and log time, voltage, conditions. |
| `test_register_map.py` | Dumps a subset of known Modbus registers and values to CSV. |
| `test_telemetry_data.py` | Reads inverter power, SoC, PV power, battery flow every X seconds. |

---

## 🗂️ Folder Structure

```
.
├── battery_info.py
├── minimal_rtu_read.py
├── tcp_command_tests.py
├── rtu_battery_control.py
├── ... (other test scripts)
├── packages/              # Offline wheels for dependency installation
├── logs/                  # All logs from tests (telemetry, errors, performance...)
└── requirements.txt       # Dependency list for pip
```

---

## 🎡 Use Case Examples

### A. Get Real-Time Power Readings
```bash
python test_telemetry_data.py
```
Logs include:
```
[TELEMETRY] Inverter Active Power (W): 2700
[TELEMETRY] Battery SoC (%): 55.0
[TELEMETRY] PV String Power (W): 3000
```

### B. Trigger a Forced Discharge Cycle (TCP)
```bash
python tcp_command_tests.py
```
Expected:
- Charge @ 500 W for 2 min
- Discharge to 20% SoC
- Results logged to `logs/battery_control.log`

### C. Test Invalid Configurations
```bash
python test_errors.py
```
It sends incorrect values (like 150% SoC) and logs inverter’s clamping behavior and error flags.

---

## 💡 Tips & Notes

- RTU is great for offline/field environments
- TCP is easier for local network or remote login
- Default installer password is often `00000a`
- Many registers are validated and clamped (e.g., SoC max 100%)
- `logs/` folder contains detailed logs for each script run

---

## 📚 Documentation & Protocol
- The tests follow the [IW Inverter Testing Protocol](docs/IW-Inverter%20Testing%20Protocol-160425-160348%20(1).pdf)
- Inverter specs and register map based on:
  - [SUN2000 User Manual](docs/SUN2000-(3KTL-10KTL)-M1%User%Manual.pdf)
  - `Hybrid_Inverter_Registers.xltx` (Modbus reference)

---

## 📜 License
MIT License © 2025 Andraž Jančar  
Faculty of Electrical Engineering, University of Ljubljana
