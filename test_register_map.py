import os, logging

# ensure logs folder exists and log into logs/test_register_map.log
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/test_register_map.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# …the rest of your script follows unchanged…
import asyncio
from tcp_battery_control import connect_and_login, read_param, shutdown_bridge
from huawei_solar import register_names as rn

INVERTER_IP        = "192.168.200.1"
PORT               = 6607
UNIT_ID            = 0
INSTALLER_PASSWORD = "00000a"

async def main():
    # now all logging.info()/error() calls (including those inside read_param) go to the file
    bridge = await connect_and_login(INVERTER_IP, PORT, UNIT_ID, INSTALLER_PASSWORD, delay=5)
    if not bridge:
        logging.error("Could not connect to inverter.")
        return

    try:
        logging.info("=== Inverter Register Map + Live Values ===")
        tests = [
            (rn.ACTIVE_POWER,         "Instantaneous AC Output Power (kW)"),
            (rn.DAILY_YIELD_ENERGY,   "Energy Produced Today (kWh)"),
            (rn.INVERTER_RATED_POWER, "Inverter Rated Power (kW)"),
            (rn.GRID_VOLTAGE,         "Grid Voltage (V)"),
            (rn.SERIAL_NUMBER,        "Inverter Serial Number"),
        ]
        for reg, desc in tests:
            logging.info(f"→ {desc}: {reg}")
            await read_param(bridge, reg, "Value")
    finally:
        await shutdown_bridge(bridge)

if __name__ == "__main__":
    asyncio.run(main())