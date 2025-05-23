# Dieses Skript benötigt PyUSB. Du kannst es mit pip install pyusb installieren.
# Außerdem benötigst du libusb.

# Ich entschuldige mich aufrichtig dafür, dass dieser Prozess übermäßig kompliziert ist. Anscheinend sind Python und Windows
# nicht sehr freundlich zueinander :(
# Windows Anleitung:
# 1. Lade Zadig von https://zadig.akeo.ie/ herunter.
# 2. Schließe deine Switch an und gehe im Tinfoil USB-Installationsmenü
#    auf "List All Devices" im Optionsmenü von Zadig und wähle libnx USB comms aus.
# 3. Wähle libusbK aus der Treiberliste und klicke auf "Replace Driver".
# 4. Führe dieses Skript aus.

# macOS Anleitung:
# 1. Installiere Homebrew https://brew.sh
# 2. Installiere Python 3
#      `sudo mkdir /usr/local/Frameworks`
#      `sudo chown $(whoami) /usr/local/Frameworks`
#      `brew install python`
# 3. Installiere PyUSB
#      `pip3 install pyusb`
# 4. Installiere libusb
#      `brew install libusb`
# 5. Schließe deine Switch an und gehe zu Tinfoil > Title Management > USB Install NSP
# 6. Führe dieses Skript aus
#      `python3 usb_install_pc.py <pfad/zum/nsp_ordner>`

import usb.core
import usb.util
import struct
import sys
from pathlib import Path
import time

CMD_ID_EXIT = 0
CMD_ID_FILE_RANGE = 1

CMD_TYPE_RESPONSE = 1

# Liste der unterstützten Dateiendungen.
EXTS = (".nsp", ".xci", ".nsz", ".xcz")

def send_response_header(out_ep, cmd_id, data_size):
    """Sendet den Response-Header an die Switch.

    Args:
        out_ep: Das Output-Endpoint-Objekt.
        cmd_id (int): Die ID des Befehls.
        data_size (int): Die Größe der Daten.
    """
    out_ep.write(b'TUC0')  # Tinfoil USB Command 0
    out_ep.write(struct.pack('<B', CMD_TYPE_RESPONSE))
    out_ep.write(b'\x00' * 3)
    out_ep.write(struct.pack('<I', cmd_id))
    out_ep.write(struct.pack('<Q', data_size))
    out_ep.write(b'\x00' * 0xC)


def file_range_cmd(nsp_dir, in_ep, out_ep, data_size):
    """Verarbeitet den File-Range-Befehl.

    Args:
        nsp_dir (Path): Das Verzeichnis mit den NSP-Dateien.
        in_ep: Das Input-Endpoint-Objekt.
        out_ep: Das Output-Endpoint-Objekt.
        data_size (int): Die Größe der Daten.
    """
    file_range_header = in_ep.read(0x20)

    range_size = struct.unpack('<Q', file_range_header[:8])[0]
    range_offset = struct.unpack('<Q', file_range_header[8:16])[0]
    nsp_name_len = struct.unpack('<Q', file_range_header[16:24])[0]
    # in_ep.read(0x8) # Reserviert
    nsp_name = bytes(in_ep.read(nsp_name_len)).decode('utf-8')

    print('Range Size: {}, Range Offset: {}, Name len: {}, Name: {}'.format(range_size, range_offset, nsp_name_len, nsp_name))
    send_response_header(out_ep, CMD_ID_FILE_RANGE, range_size)

    with open(nsp_name, 'rb') as f:
        f.seek(range_offset)

        curr_off = 0x0
        end_off = range_size
        read_size = 0x800000

        while curr_off < end_off:
            if curr_off + read_size >= end_off:
                read_size = end_off - curr_off

            buf = f.read(read_size)
            out_ep.write(data=buf, timeout=0)
            curr_off += read_size


def poll_commands(nsp_dir, in_ep, out_ep):
    """Wartet auf Befehle von der Switch und verarbeitet sie.

    Args:
        nsp_dir (Path): Das Verzeichnis mit den NSP-Dateien.
        in_ep: Das Input-Endpoint-Objekt.
        out_ep: Das Output-Endpoint-Objekt.
    """
    while True:
        cmd_header = bytes(in_ep.read(0x20, timeout=0))
        magic = cmd_header[:4]
        print('Magic: {}'.format(magic), flush=True)

        if magic != b'TUC0':  # Tinfoil USB Command 0
            continue

        cmd_type = struct.unpack('<B', cmd_header[4:5])[0]
        cmd_id = struct.unpack('<I', cmd_header[8:12])[0]
        data_size = struct.unpack('<Q', cmd_header[12:20])[0]

        print('Cmd Type: {}, Command id: {}, Data size: {}'.format(cmd_type, cmd_id, data_size), flush=True)

        if cmd_id == CMD_ID_EXIT:
            print('Exiting...')
            break
        elif cmd_id == CMD_ID_FILE_RANGE:
            file_range_cmd(nsp_dir, in_ep, out_ep, data_size)


def send_nsp_list(nsp_dir, out_ep):
    """Sendet die Liste der verfügbaren NSP-Dateien an die Switch.

    Args:
        nsp_dir (Path): Das Verzeichnis mit den NSP-Dateien.
        out_ep: Das Output-Endpoint-Objekt.
    """
    nsp_path_list = list()
    nsp_path_list_len = 0

    # Fügt alle Dateien mit den unterstützten Dateiendungen im angegebenen Verzeichnis hinzu
    for nsp_path in [f for f in nsp_dir.iterdir() if f.is_file() and (f.suffix in EXTS)]:
        nsp_path = bytes(nsp_path.__str__(), 'utf8') + b'\n'
        nsp_path_list.append(nsp_path)
        nsp_path_list_len += len(nsp_path)

    print('Sending header...')

    out_ep.write(b'TUL0')  # Tinfoil USB List 0
    out_ep.write(struct.pack('<I', nsp_path_list_len))
    out_ep.write(b'\x00' * 0x8)  # Padding

    print('Sending NSP list: {}'.format(nsp_path_list))

    for nsp_path in nsp_path_list:
        out_ep.write(nsp_path)


def print_usage():
    """Gibt die Nutzungsinformationen aus."""
    print("""\
usb_install_pc.py

Used for the installation of NSPs over USB.

Usage: usb_install_pc.py <nsp folder>""")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print_usage()
        sys.exit(1)

    nsp_dir = Path(sys.argv[1])

    if not nsp_dir.is_dir():
        raise ValueError('1st argument must be a directory')

    print("waiting for switch...\n")
    dev = None

    while (dev is None):
        dev = usb.core.find(idVendor=0x057E, idProduct=0x3000)
        time.sleep(0.5)

    print("found the switch!\n")

    cfg = None

    try:
        cfg = dev.get_active_configuration()
        print("found active config")
    except usb.core.USBError:
        print("no currently active config")
        cfg = None

    if cfg is None:
        dev.reset()
        dev.set_configuration()
        cfg = dev.get_active_configuration()

    is_out_ep = lambda ep: usb.util.endpoint_direction(ep.bEndpointAddress) == usb.util.ENDPOINT_OUT
    is_in_ep = lambda ep: usb.util.endpoint_direction(ep.bEndpointAddress) == usb.util.ENDPOINT_IN
    out_ep = usb.util.find_descriptor(cfg[(0,0)], custom_match=is_out_ep)
    in_ep = usb.util.find_descriptor(cfg[(0,0)], custom_match=is_in_ep)

    assert out_ep is not None
    assert in_ep is not None

    print("iManufacturer: {} iProduct: {} iSerialNumber: {}".format(dev.manufacturer, dev.product, dev.serial_number))
    print("bcdUSB: {} bMaxPacketSize0: {}".format(hex(dev.bcdUSB), dev.bMaxPacketSize0))

    send_nsp_list(nsp_dir, out_ep)
    poll_commands(nsp_dir, in_ep, out_ep)
