"""This script is a simple USD viewer using the pxr.Usdviewq module."""

import sys
import pxr.Usdviewq as Usdviewq

if __name__ == "__main__":
    # Let Ctrl-C kill the app.
    import signal

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    try:
        usd_path = "assets/Sphere.usda"
        sys.argv.append(usd_path)
        Usdviewq.Launcher().Run()
    except Usdviewq.InvalidUsdviewOption as e:
        print("ERROR: " + str(e), file=sys.stderr)
        sys.exit(1)
