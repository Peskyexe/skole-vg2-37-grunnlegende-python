import subprocess
import re
import shlex
import os
import asyncio

class AudioManager:
    def __init__(self):
        self.loopback_process = None

    def is_routing_active(self) -> bool:
        return self.loopback_process is not None and self.loopback_process.poll() is None
    
    # Discovers the bluetooth node for iPhone audio
    def discover_bluetooth_node(self) -> str:
        try:
            # Capture the stdout of 'pw-link -o' as a string
            result = subprocess.run(
                ["pw-link", "-o"],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Use RegEx to extract anything starting with 'bluez_input' up until the trailing colon.
            matches = re.findall(r'(bluez_input\.[^\:]+)', result.stdout)
            
            if matches:
                return matches[0]
                
            return None
        
        except subprocess.CalledProcessError as e:
            print(f"[!] (Audio Manager) Failed to query PipeWire: {e}")
            return None
        except FileNotFoundError:
            print("[!] (Audio Manager) 'pw-link' utility not found. Is PipeWire/WirePlumber installed?")
            return None

    # Starts a targeted loopback daemon based on the discovered bluetooth node
    def start_routing(self):
        print("[*] (Audio Manager) Activating audio routing...")
        
        if self.is_routing_active():
            print("[!] (Audio Manager) Audio Routing is already active.")
            return

        self.loopback_process = None
        
        node_name = self.discover_bluetooth_node()
        
        if not node_name:
            print("[!] (Audio Manager) Could not detect any actve Bluetooth audio nodes. Ensure your iPhone is connected and actively playing music.")
            return
        
        cmd = f"pw-loopback -C {node_name}"
        
        # Start the process in a seperate process group so it runs in the background
        self.loopback_process = subprocess.Popen(
            shlex.split(cmd),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            preexec_fn=os.setsid
        )
        
        print("[+] (Audio Manager) Audio routing activated.")
    
    # Safely tears down the targeted loopback daemon.
    def stop_routing(self):
        if self.loopback_process:
            print("[*] (Audio Manager) Terminating audio routing.")
            try:
                # Kills the process group to ensure no rogue audio artifacts stay open
                os.killpg(os.getpgid(self.loopback_process.pid), 15) # 15 is SIGTERM
                self.loopback_process.wait(timeout=2)
            except Exception:
                # Fallback forced kill if it hangs
                if self.loopback_process:
                    self.loopback_process.kill()
            
            self.loopback_process = None
            print("[-] (Audio Manager) Audio routing terminated.")
        else:
            print("[!] (Audio Manager) No active audio routing to terminate.")
