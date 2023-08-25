import serial, time

ser = serial.Serial('/dev/ttyACM0', baudrate=9600, timeout=5)

def send_command(command):
    ser.write(command.encode() + b'\n')
    response = ser.readline().strip().decode()
    return response

response = send_command('1')
print("Response:",response)

time.sleep(1)

response = send_command('2')
print("Response:",response)

time.sleep(1)

response = send_command('1')
print("Response:",response)

time.sleep(1)

response = send_command('2')
print("Response:",response)

time.sleep(1)

response = send_command('1')
print("Response:",response)

ser.close()
