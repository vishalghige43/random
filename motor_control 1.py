import time
from pymodbus.client import ModbusSerialClient
import logging
import struct

logging.basicConfig(level=logging.DEBUG)

def calculate_crc(data):
    crc = 0xFFFF
    for pos in data:
        crc ^= pos
        for _ in range(8):
            if (crc & 1) != 0:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return crc

def build_command(slave_id, function_code, address, data):
    command = [slave_id, function_code, address >> 8, address & 0xFF, data >> 8, data & 0xFF]
    crc = calculate_crc(command)
    command.append(crc & 0xFF)
    command.append((crc >> 8) & 0xFF)
    return bytes(command)

def int_to_bytes(value, length):
    """ Convert an integer to bytes """
    return value.to_bytes(length, byteorder='big', signed=True)

class MotorController:
    def __init__(self, port, slave_id, baudrate=38400, timeout=1):
        self.client = ModbusSerialClient(method='rtu', port=port, baudrate=baudrate, timeout=timeout)
        self.slave_id = slave_id
        if not self.client.connect():
            raise Exception(f"Failed to connect to the Modbus server on port {port} for slave ID {slave_id}")

    def send_command(self, command):
        logging.debug(f"Sending command to slave ID {self.slave_id}: {command}")
        response = self.client.send(command)
        logging.debug(f"Received response from slave ID {self.slave_id}: {response}")
        return response

    def set_mode_velocity_control(self):
        command = build_command(self.slave_id, 6, 0x6200, 0x0002)
        self.send_command(command)
        time.sleep(0.1)

    def set_velocity(self, rpm):
        rpm_bytes = int_to_bytes(rpm, 2)
        data = struct.unpack(">H", rpm_bytes)[0]
        command = build_command(self.slave_id, 6, 0x6203, data)
        self.send_command(command)
        time.sleep(0.1)

    def set_acceleration(self, acceleration):
        command = build_command(self.slave_id, 6, 0x6204, acceleration)
        self.send_command(command)
        time.sleep(0.1)

    def set_deceleration(self, deceleration):
        command = build_command(self.slave_id, 6, 0x6205, deceleration)
        self.send_command(command)
        time.sleep(0.1)

    def set_direction_and_velocity(self, direction, rpm):
        if direction == "reverse":
            rpm = -rpm  # Set negative RPM for reverse
        self.set_velocity(rpm)

    def start_motion(self):
        command = build_command(self.slave_id, 6, 0x6002, 0x0010)
        self.send_command(command)
        time.sleep(0.1)

    def stop_motion(self):
        command = build_command(self.slave_id, 6, 0x6002, 0x0040)
        self.send_command(command)
        time.sleep(0.1)

    def close(self):
        self.client.close()

if __name__ == "__main__":
    # Motor 1 on /dev/ttyUSB0 and Motor 2 on /dev/ttyUSB1
    motor1 = MotorController(port='/dev/ttyUSB0', slave_id=2)
    motor2 = MotorController(port='/dev/ttyUSB1', slave_id=1)

    try:
        # Set both motors to velocity control mode
        logging.info("Setting motor 1 to velocity control mode")
        motor1.set_mode_velocity_control()
        logging.info("Setting motor 2 to velocity control mode")
        motor2.set_mode_velocity_control()

        # Set both motors speed to 4000 RPM forward
        logging.info("Setting motor 1 speed to 4000 RPM forward")
        motor1.set_direction_and_velocity("forward", 2000)
        logging.info("Setting motor 2 speed to 4000 PM forward")
        motor2.set_direction_and_velocity("forward", 2000)

        # Set acceleration and deceleration for both motors (example values)
        logging.info("Setting acceleration and deceleration for motor 1")
        motor1.set_acceleration(200)
        motor1.set_deceleration(200)
        logging.info("Setting acceleration and deceleration for motor 2")
        motor2.set_acceleration(200)
        motor2.set_deceleration(200)

        # Start both motors in forward direction
        logging.info("Starting motor 1")
        motor1.start_motion()
        logging.info("Starting motor 2")
        motor2.start_motion()
        print("Both motors started at 4000 RPM in forward direction")
        time.sleep(10)  # Run both motors for 10 seconds

        # Stop both motors
        logging.info("Stopping motor 1")
        motor1.stop_motion()
        logging.info("Stopping motor 2")
        motor2.stop_motion()
        print("Both motors stopped")

        # Change direction to reverse and start again
        logging.info("Setting motor 1 speed to 4000 RPM reverse")
        motor1.set_direction_and_velocity("reverse", 4000)
        logging.info("Setting motor 2 speed to 4000 RPM reverse")
        motor2.set_direction_and_velocity("reverse", 4000)
        logging.info("Starting motor 1 in reverse")
        motor1.start_motion()
        logging.info("Starting motor 2 in reverse")
        motor2.start_motion()
        print("Both motors started at 4000 RPM in reverse direction")
        time.sleep(10)  # Run both motors for 10 seconds in reverse

        # Stop both motors
        logging.info("Stopping motor 1")
        motor1.stop_motion()
        logging.info("Stopping motor 2")
        motor2.stop_motion()
        print("Both motors stopped")

    finally:
        motor1.close()
        motor2.close()
