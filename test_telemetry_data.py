import os, logging

os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/test_telemetry_data.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# …rest unchanged…
import asyncio
from tcp_battery_control import connect_and_login, read_param, shutdown_bridge
from huawei_solar import register_names as rn

INVERTER_IP        = "192.168.200.1"
PORT               = 6607
UNIT_ID            = 0
INSTALLER_PASSWORD = "00000a"

async def main():
    bridge = await connect_and_login(INVERTER_IP, PORT, UNIT_ID, INSTALLER_PASSWORD, delay=5)
    if not bridge:
        logging.error("Cannot connect.")
        return

    try:
        logging.info("=== Live Telemetry Data ===")
        tests = [
            (rn.ACTIVE_POWER,                  "Total AC Output Power (kW)"),
            (rn.TOTAL_DC_INPUT_POWER,          "Total DC Input Power (kW)"),
            (rn.GRID_A_VOLTAGE,                "Grid Phase A Voltage (V)"),
            (rn.GRID_B_VOLTAGE,                "Grid Phase B Voltage (V)"),
            (rn.GRID_C_VOLTAGE,                "Grid Phase C Voltage (V)"),
            (rn.ACTIVE_GRID_A_POWER,           "Phase A AC Power (kW)"),
            (rn.ACTIVE_GRID_B_POWER,           "Phase B AC Power (kW)"),
            (rn.ACTIVE_GRID_C_POWER,           "Phase C AC Power (kW)"),
            (rn.GRID_FREQUENCY,                "Grid Frequency (Hz)"),
            (rn.POWER_FACTOR_EXTERNAL_ENERGY_SENSOR, "Power Factor (ext. meter)"),
            (rn.INTERNAL_TEMPERATURE,          "Internal Temperature (°C)"),
        ]
        for reg, desc in tests:
            logging.info(f"→ {desc}: {reg}")
            await read_param(bridge, reg, "Value")
    finally:
        await shutdown_bridge(bridge)

if __name__ == "__main__":
    asyncio.run(main())
