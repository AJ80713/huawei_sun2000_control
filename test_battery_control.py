import os, logging

os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/test_battery_control.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# …rest unchanged…
import asyncio
from tcp_battery_control import (
    connect_and_login,
    force_charge_duration,
    force_discharge_duration,
    stop_charge,
    read_param,
    shutdown_bridge
)
from huawei_solar import register_names as rn

INVERTER_IP        = "192.168.200.1"
PORT               = 6607
UNIT_ID            = 0
INSTALLER_PASSWORD = "00000a"

async def main():
    bridge = await connect_and_login(INVERTER_IP, PORT, UNIT_ID, INSTALLER_PASSWORD, delay=15)
    if not bridge:
        logging.error("Could not connect.")
        return

    try:
        logging.info("=== Battery Control Test ===")
        await read_param(bridge, rn.STORAGE_STATE_OF_CAPACITY,     "Initial SoC (%)")
        await read_param(bridge, rn.STORAGE_CHARGE_DISCHARGE_POWER, "Initial Storage Power (W)")

        logging.info("→ Forcing charge: 100 W for 30 s")
        await force_charge_duration(bridge, power=100, duration=0.5)
        await read_param(bridge, rn.STORAGE_CHARGE_DISCHARGE_POWER, "Charge Power (W)")
        await read_param(bridge, rn.STORAGE_STATE_OF_CAPACITY,      "SoC (%)")
        await stop_charge(bridge)

        logging.info("→ Forcing discharge: 100 W for 30 s")
        await force_discharge_duration(bridge, power=100, duration=0.5)
        await read_param(bridge, rn.STORAGE_CHARGE_DISCHARGE_POWER, "Discharge Power (W)")
        await read_param(bridge, rn.STORAGE_STATE_OF_CAPACITY,      "SoC (%)")
        await stop_charge(bridge)
    finally:
        await shutdown_bridge(bridge)

if __name__ == "__main__":
    asyncio.run(main())
