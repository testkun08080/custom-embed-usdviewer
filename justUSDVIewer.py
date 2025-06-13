
import sys
import pxr.Usdviewq as Usdviewq

if __name__ == '__main__':
    #Let Ctrl-C kill the app.
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    try:
        file = "Sphere.usda"
        import sys

        sys.argv.append(file)
        Usdviewq.Launcher().Run()
    except Usdviewq.InvalidUsdviewOption as e:
        print("ERROR: " + str(e), file=sys.stderr)
        sys.exit(1)
