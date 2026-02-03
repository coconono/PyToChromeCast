import pychromecast

def list_cast_devices():
    print("Searching for Chromecast devices on the local network...")
    chromecasts, browser = pychromecast.get_chromecasts()
    if not chromecasts:
        print("No Chromecast devices found.")
    else:
        print(f"Found {len(chromecasts)} device(s):")
        for cc in chromecasts:
            print(f"- {cc.name} ({cc.cast_info.host})")
    # Shut down discovery
    pychromecast.discovery.stop_discovery(browser)

if __name__ == "__main__":
    list_cast_devices()
