import sys
import argparse
from datetime import datetime
import serial
import serial.tools.list_ports as list_ports


device_signature = '2A19:0C06'


def find_serial_device():
    candidates = list(list_ports.grep(device_signature))
    if not candidates:
        raise ValueError(f'No device with signature {device_signature} found')
    if len(candidates) > 1:
        raise ValueError(f'More than one device with signature '
                         f'{device_signature} found')
    return candidates[0].device


class Connection:
    def __init__(self, device, baud_rate=19200, verbosity=0):
        self._verbosity = verbosity
        if self._verbosity > 0:
            self._log_line(f'Using serial device {device}')
        self._conn = serial.Serial(device, baud_rate, timeout=1)

    def send(self, command: str) -> None:
        if self._verbosity > 1:
            self._log_line(f'Sending: {command}')
        line = command + '\r'
        raw = bytes(line, 'utf8')
        if self._verbosity > 2:
            self._log_line(f'Raw: {raw}')
        self._conn.write(raw)

    def receive(self) -> str:
        if self._verbosity > 2:
            print('Receiving: ', end='', flush=True)
        data = self._conn.read(25)
        if self._verbosity > 2:
            print(str(data), flush=True)
        return self._demangle(data)

    @staticmethod
    def _demangle(raw):
        return str(raw).replace('\n\r', '\r\n')

    def _log_line(self, line):
        print(datetime.now().strftime('%H:%M:%S'), end=' ')
        print(line, flush=True)


class App:
    def __init__(self, verbosity=0):
        self._verbosity = verbosity

    def connect(self):
        self._connection = Connection(find_serial_device(),
                                      verbosity=self._verbosity)
        return self

    def show_state(self):
        print(f'{self.read(0)}/{self.read(1)}')

    def set_state(self, state):
        states = state.split('/')
        self._set_state(0, states[0])
        self._set_state(1, states[1])
        self._connection.receive()

    def read(self, relay):
        return 'on' if self._get(relay) else 'off'

    def _get(self, relay):
        self._connection.send(f'relay read {relay}')
        response = self._connection.receive()
        state = 'on' in response
        return state

    def _set_state(self, relay, state):
        self._connection.send(f'relay {state} {relay}')


class Main():
    def __init__(self, args):
        self._cli_args = args

    def run(self):
        self._parse_args()
        app = App(self._args.verbose)
        app.connect()
        if self._args.read:
            return app.show_state()
        app.set_state(self._args.set_state)

    def _parse_args(self):
        parser = argparse.ArgumentParser(
            description='Interface to a Numato two-channel USB relay module',
            epilog='"on/off" means relay 0 on and relay 1 off, etc.'
        )
        parser.add_argument('-v', '--verbose', action='count', default=0,
                            help='Verbose output (repeat to increase)')
        parser.add_argument('-r', '--read', action='count', default=0,
                            help='Read state of relays')
        parser.add_argument('-s', '--set-state',
                            choices=['off/off', 'on/off', 'off/on', 'on/on'])
        self._args = parser.parse_args(args=self._cli_args)
        if not self._args.read and not self._args.set_state:
            parser.print_help()
            print()
            print('Do you want to read (-r) or set (-s)?')
            sys.exit(1)


if __name__ == '__main__':
    try:
        app = Main(sys.argv[1:])
        app.run()
        sys.exit(0)
    except Exception as error:
        print(f'Error: {error}')
        sys.exit(1)
