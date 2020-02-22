import socket
import serial


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 5362))
    s.listen(4)

    conn, addr = s.accept()
    ser = serial.Serial('/dev/cu.usbserial-1460', 9600)
    print(ser)
    print(ser.name)

    while True:
        data = conn.recv(5)

        if not data:
            break

        binary = bytearray(data)
        left_raw = binary[0]
        right_raw = binary[1]

        ser.write(bytes([left_raw, right_raw]))
        ser.flush()
        print('Sent:', left_raw, right_raw)
        # print('Read:', ser.readline().decode('utf-8'))


if __name__ == '__main__':
    main()
