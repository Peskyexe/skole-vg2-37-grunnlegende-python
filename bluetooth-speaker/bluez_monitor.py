# Activate virtual environment with dbus_next:
# source .venv/bin/activate

import asyncio
from dbus_next.aio import MessageBus
from dbus_next.constants import BusType

BLUEZ_SERVICE = "org.bluez"
MEDIA_PLAYER_INTF = "org.bluez.MediaPlayer1"
PROPERTIES_INTF = "org.freedesktop.DBus.Properties"
OBJECT_MANAGER_INTF = "org.freedesktop.DBus.ObjectManager"

class TrackData:
    def __init__(self, media_data):
        # Initialize default values:
        self.status = "Unknown Status"
        self.title = "Unknown Title"
        self.artist = "Unknown Artist"
        self.album = "Unknown Album"
        
        self.update_data(media_data)
    
    # Gets a value like "Title" or "Album" from either track_data or media_data
    def get_data_value(self, data, value_to_get: str) -> str:
        value = data.get(value_to_get, {}).value if value_to_get in data else None
        return value
    
    # Gets track_data from media_data
    def get_track_data(self, media_data):
        track_variant = media_data.get("Track", None)
        track_data = track_variant.value if track_variant else None
        return track_data
    
    def update_data(self, media_data) -> None:
        # Update Status if it exists in this change payload
        new_status = self.get_data_value(media_data, "Status")
        if new_status:
            self.status = new_status.title()
            
        # Update Track metadata dict if it exists in this change payload
        track_data = self.get_track_data(media_data)
        if track_data:
            new_title = self.get_data_value(track_data, "Title")
            new_artist = self.get_data_value(track_data, "Artist")
            new_album = self.get_data_value(track_data, "Album")
            
            if new_title: self.title = new_title
            if new_artist: self.artist = new_artist
            if new_album: self.album = new_album
    
    def print_track_data(self) -> None:
        print("\n--- Track Data ---")
        print(f"Status : {self.status}")
        print(f"Track : {self.title}")
        print(f"Artist : {self.artist}")
        print(f"Album : {self.album}")
        print("------------------\n")  

class BlueZMonitor:
    def __init__(self, audio_manager=None):
        self.bus = None
        self.current_track = None
        self.player_path = None
        self.properties_interface = None
        self.audio_manager = audio_manager

    # Connect to BlueZ and subscribe to the active media player
    async def start(self) -> bool:
        self.bus = await MessageBus(bus_type=BusType.SYSTEM).connect()

        introspection = await self.bus.introspect(BLUEZ_SERVICE, "/")
        manager = self.bus.get_proxy_object(BLUEZ_SERVICE, "/", introspection)
        object_manager = manager.get_interface(OBJECT_MANAGER_INTF)

        print("[*] (BlueZ Monitor) BlueZ Monitor Initialized. Waiting for iPhone stream events...")

        managed_objects = await object_manager.call_get_managed_objects()
        for path, interfaces in managed_objects.items():
            if MEDIA_PLAYER_INTF in interfaces:
                self.player_path = path
                self.current_track = TrackData(interfaces[MEDIA_PLAYER_INTF])
                print(f"[+] (BlueZ Monitor) Found active media stream interface at device node: {path}")
                self.current_track.print_track_data()
                break

        if not self.player_path:
            print("[!] (BlueZ Monitor) No active media stream interface found. Is your iPhone connected and playing music?")
            return False

        player_introspection = await self.bus.introspect(BLUEZ_SERVICE, self.player_path)
        player_proxy = self.bus.get_proxy_object(BLUEZ_SERVICE, self.player_path, player_introspection)
        self.properties_interface = player_proxy.get_interface(PROPERTIES_INTF)
        self.properties_interface.on_properties_changed(self._on_properties_changed)

        print("[*] (BlueZ Monitor) Listening for media stream updates... Press Ctrl+C to exit.")
        return True

    def _on_properties_changed(self, interface_name, changed_properties, invalidated_properties):
        if interface_name != MEDIA_PLAYER_INTF or self.current_track is None:
            return

        if self.audio_manager:
            self.audio_manager.start_routing()

        self.current_track.update_data(changed_properties)
        self.current_track.print_track_data()

    async def run(self) -> None:
        if self.bus:
            await self.bus.wait_for_disconnect()

    async def stop(self) -> None:
        if self.bus:
            self.bus.disconnect()
            self.bus = None

if __name__ == "__main__":
    try:
        monitor = BlueZMonitor()
        asyncio.run(monitor.start())
    except KeyboardInterrupt:
        print("\n[-] (BlueZ Monitor) Shutting down BlueZ Monitor cleanly.")
        