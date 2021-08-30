# Command-line interface for Numato relay module

This is a python implementation of a command-line interface to [Numato two-channel USB relay module](https://numato.com/product/2-channel-usb-powered-relay-module/).

## First-time setup on a new machine

### MacOS / Linux

    $ python3 -m venv venv
    $ source venv/bin/activate
    $ pip install --upgrade pip
    $ pip install -r requirements.txt
    
### Windows

    PS> python3 -m venv venv
    PS> venv\Scripts\activate.bat & ^
        pip install -r requirements.txt

## Run directly

    $ source venv/bin/activate
    $ python relay-control.py

```
usage: relay-control.py [-h] [-v] [-r] [-s {off/off,on/off,off/on,on/on}]

Interface to a Numato two-channel USB relay module

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Verbose output (repeat to increase)
  -r, --read            Read state of relays
  -s {off/off,on/off,off/on,on/on}, --set-state {off/off,on/off,off/on,on/on}

"on/off" means relay 0 on and relay 1 off, etc.
```

## Compile stand-alone executable

### MacOS / Linux

    $ pip install -r requirements-dev.txt
    $ build-app.sh

### Windows

    PS> pip install -r requirements-dev.txt
    PS> build-app.bat
