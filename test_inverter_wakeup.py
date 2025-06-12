import os, logging

os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/test_inverter_wakeup.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# …rest unchanged…
import asyncio, time
from tcp_battery_control import connect_and_login, force_charge_duration, read_param, shutdown_bridge
from huawei_solar import register_names as rn

INVERTER_IP        = "192.168.200.1"
PORT               = 6607
UNIT_ID            = 0
INSTALLER_PASSWORD = "00000a"
WAKE_TIMEOUT       = 60

async def main():
    bridge = await connect_and_login(INVERTER_IP, PORT, UNIT_ID, INSTALLER_PASSWORD, delay=5)
    if not bridge:
        logging.error("Could not connect.")
        return

    try:
        await read_param(bridge, rn.ACTIVE_POWER, "Initial Active Power (kW) — expect 0")

        logging.info("→ Triggering minimal forced-charge (1 W)…")
        await force_charge_duration(bridge, power=1, duration=0.1)

        start = time.time()
        logging.info(f"Waiting up to {WAKE_TIMEOUT}s for Active Power > 0…")
        while True:
            p = await read_param(bridge, rn.ACTIVE_POWER, "Polled Active Power (kW)")
            if p and p > 0:
                logging.info(f"Woke up after {time.time()-start:.1f}s → {p} kW")
                break
            if time.time() - start >= WAKE_TIMEOUT:
                logging.warning(f"Timed out after {WAKE_TIMEOUT}s — still {p or 0} kW")
                break
            await asyncio.sleep(1)
    finally:
        await shutdown_bridge(bridge)

if __name__ == "__main__":
    asyncio.run(main())
