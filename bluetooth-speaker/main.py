# Built for Ubuntu

# Create virtual environment:
# python3 -m venv .venv

# Activate virtual environment:
# source .venv/bin/activate

import asyncio

from audio_manager import AudioManager
from bluez_monitor import BlueZMonitor


async def run() -> None:
	audio_manager = AudioManager()
	bluez_monitor = BlueZMonitor(audio_manager)

	try:
		monitor_started = await bluez_monitor.start()
		if not monitor_started:
			return

		await bluez_monitor.run()
	finally:
		audio_manager.stop_routing()
		await bluez_monitor.stop()


def main() -> None:
	try:
		asyncio.run(run())
	except KeyboardInterrupt:
		print("\n[-] (Bluetooth Speaker) Shutting down cleanly.")


if __name__ == "__main__":
	main()