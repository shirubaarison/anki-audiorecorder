import subprocess

'''
sorry i think this only works if you use pipewire-pulse
'''

def create_virtual_sink(sink_name):
    try:
        # create null sink
        subprocess.run(["pactl", "load-module", "module-null-sink", f"sink_name={sink_name}"], check=True)
        
        # load loopback module
        subprocess.run(["pactl", "load-module", "module-loopback", f"sink={sink_name}"], check=True)
        
        # Set default source to monitor of built-in analog audio
        subprocess.run(["pactl", "set-default-source", "alsa_input.pci-0000_00_1f.3.analog-stereo.monitor"], check=True)
        print(f"Virtual sink '{sink_name}' created successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error creating virtual sink: {e}")


def verify_virtual_sink(sink_name):
    try:
        output = subprocess.run(["pactl", "list", "sinks"], capture_output=True, text=True, check=True)
        if sink_name in output.stdout:
            print(f"Virtual sink '{sink_name}' already exists.")
            return True
        else:
            print(f"Virtual sink '{sink_name}' not found.")
            return False
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return False