import socket
from smbus2 import SMBus


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 5362))
    s.listen(4)

    conn, addr = s.accept()
    bus = SMBus(1)

    while True:
        data = conn.recv(5)

        if not data:
            break

        binary = bytearray(data)
        left_raw = binary[0]
        right_raw = binary[1]

        bus.write_byte(4, left_raw)
        bus.write_byte(4, right_raw)

        print('Sent:', left_raw, right_raw)


if __name__ == '__main__':
    main()
