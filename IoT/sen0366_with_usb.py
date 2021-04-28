
import re
import time

import serial

'''
SKU:SEN0366

Operating Voltage: DC3.3V~5V
Measuring Range: indoor 0.05-50m, outdoor 0.05-80m
Accuracy(Standard Deviation): ±1.0mm
Laser Type: 620~690nm
Laser Class: Ⅱ, <1mW
Spot Diameter at Distance M: 6mm@10m，30mm@50m
Single Measurement Time: 0.05~1s
Protection Level: IP40
Operating Temperature: -10~+60℃
Storage Temperature: -20~+80℃
Weight: about 60g
Dimension: 48×42×18mm/1.89×1.65×0.71”

https://wiki.dfrobot.com/Infrared_Laser_Distance_Sensor_50m_80m_SKU_SEN0366
'''


class SEN0366WithUSB:
    def __init__(self, com_port):
        self.ser = serial.Serial()
        self.ser.port = com_port

        #  115200,N,8,1
        self.ser.baudrate = 9600
        self.ser.bytesize = serial.EIGHTBITS  # number of bits per bytes
        self.ser.parity = serial.PARITY_NONE  # set parity check
        self.ser.stopbits = serial.STOPBITS_ONE  # number of stop bits

        self.ser.timeout = 0.5  # non-block read 0.5s
        self.ser.writeTimeout = 0.5  # timeout for write 0.5s
        self.ser.xonxoff = False  # disable software flow control
        self.ser.rtscts = False  # disable hardware (RTS/CTS) flow control
        self.ser.dsrdtr = False  # disable hardware (DSR/DTR) flow control

    def write(self, write_data):
        self._check_serial_is_open()

        if self.ser.isOpen():

            try:
                self.ser.flushInput()  # flush input buffer
                self.ser.flushOutput()  # flush output buffer

                # write 8 byte data
                self.ser.write(write_data)
                print(f"write 8 byte data: {write_data}")

                time.sleep(1)  # wait 0.5s
            except Exception as e1:
                print("communicating error " + str(e1))

            finally:
                self.ser.close()

        else:
            print("open serial port error")

    def read(self):
        self._check_serial_is_open()
        if self.ser.isOpen():

            try:
                response = self.ser.read(16)
                # print("read 16 byte data:", response.hex())
                res_list = re.findall(r'.{2}', response.hex())
                res_asc_list = [chr(int(i, 16)) for i in res_list]
                if "".join(res_list[0:3]) == "800683":
                    print("".join(res_asc_list[4:10]))
            except Exception as e1:
                print("communicating error " + str(e1))

            finally:
                self.ser.close()
        else:
            print("open serial port error")

    def close(self):
        self.ser.close()

    def _check_serial_is_open(self):
        try:
            self.ser.open()
        except Exception as ex:
            print("open serial port error " + str(ex))


if __name__ == "__main__":
    sen = SEN0366WithUSB("COM8")

    # write_data = [0x80, 0x04, 0x02, 0x7A]  # close_data
    # write_data = [0x80, 0x06, 0x02, 0x78]  #  单次测量
    write_data = [0x80, 0x06, 0x03, 0x77]  # 連續测量
    # write_data = [0x80, 0x06, 0x05, 0x00, 0x75]  # 關燈
    # write_data = [0x80, 0x06, 0x05, 0x01, 0x74] # 開燈
    sen.write(write_data)
    while 1:
        sen.read()
    sen.close()
