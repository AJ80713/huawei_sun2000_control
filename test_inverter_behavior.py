import os, logging

# Ensure logs directory exists and configure file logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/test_inverter_behavior.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Existing imports and script logic follow unchanged:
import asyncio, time
from tcp_battery_control import connect_and_login, read_param, shutdown_bridge
from huawei_solar import register_names as rn

# === Inverter Connection Parameters ===
INVERTER_IP        = "192.168.200.1"
PORT               = 6607
UNIT_ID            = 0
INSTALLER_PASSWORD = "00000a"

async def main():
    # 1) Connect & login
    bridge = await connect_and_login(
        host=INVERTER_IP,
        port=PORT,
        slave_id=UNIT_ID,
        password=INSTALLER_PASSWORD,
        delay=5
    )
    if not bridge:
        print("⚠️  Could not connect to inverter.")
        return

    try:
        # 2) Idle check
        await read_param(bridge, rn.ACTIVE_POWER, "Initial Active Power (kW) — expect 0")

        # 3) Wait for PV wake-up (Active Power > 0)
        print("Waiting for inverter wake-up (Active Power > 0)…")
        start = time.time()
        while True:
            power = await read_param(bridge, rn.ACTIVE_POWER, "Polled Active Power (kW)")
            if power and power > 0:
                elapsed = time.time() - start
                print(f"Woke up after {elapsed:.1f}s, Active Power = {power} kW")
                break
            await asyncio.sleep(1)

        # 4) Optionally trigger a quick charge to test behavior…
        print("\nTriggering minimal forced-charge (1 W)…")
        await bridge.client.set(rn.STORAGE_FORCIBLE_CHARGE_POWER, 1, slave=UNIT_ID)
        await bridge.client.set(rn.STORAGE_FORCIBLE_CHARGE_DISCHARGE_WRITE, 1, slave=UNIT_ID)
        print("Charge trigger sent. Watching Active Power…")
        start2 = time.time()
        while True:
            power = await read_param(bridge, rn.ACTIVE_POWER, "Polled Active Power (kW)")
            if power and power > 0:
                elapsed2 = time.time() - start2
                print(f"Woke up after {elapsed2:.1f}s following trigger, Active Power = {power} kW")
                break
            await asyncio.sleep(0.5)

    finally:
        await shutdown_bridge(bridge)

if __name__ == "__main__":
    asyncio.run(main())
# This script tests the inverter's behavior when idle, during wake-up, and after a forced charge trigger.
# It logs all actions and results to a file for later analysis.