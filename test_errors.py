import os, logging

os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/test_errors.log",
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
        logging.error("Connection failed.")
        return

    try:
        logging.info("=== Inverter Error Status ===")
        await read_param(bridge, rn.FAULT_CODE, "Current Fault Code")
        await read_param(bridge, rn.ALARM_1,    "Alarm Register 1")
        await read_param(bridge, rn.ALARM_2,    "Alarm Register 2")
        await read_param(bridge, rn.ALARM_3,    "Alarm Register 3")
        await read_param(bridge, rn.METER_STATUS,   "Meter Status Code (0=OK)")
        await read_param(bridge, rn.GRID_VOLTAGE,   "Grid Voltage (V)")
        await read_param(bridge, rn.GRID_FREQUENCY, "Grid Frequency (Hz)")
    finally:
        await shutdown_bridge(bridge)

if __name__ == "__main__":
    asyncio.run(main())
# This script tests the error handling and status reporting of the Huawei inverter.
# It connects to the inverter, retrieves various error and status registers,    
# and logs the results. If any errors occur during the connection or reading,
# they are logged appropriately. The script is designed to run asynchronously
# and uses the asyncio library for non-blocking operations.
# Ensure the logs directory exists and log into logs/test_errors.log