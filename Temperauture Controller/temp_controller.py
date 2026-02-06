from pymodbus.client import ModbusSerialClient
from pymodbus.server import ModbusSerialServer # add a simulator server for debug

def send_modbus_frame(message, port='COM3', baudrate=9600):
    # Initialize the Modbus RTU client over RS485
    client = ModbusSerialClient(
        port=port,
        baudrate=baudrate,
        timeout=1,
        stopbits=1,
        bytesize=8,
        parity='N'
    )
    
    client.connect()

    if client.connected:
    	print("connected")
    else:
    	print("not connected")

    # Calculate CRC
    highbyte, lowbyte = calculate_crc(message)
    
    # Append the CRC to the message
    message.append(lowbyte)
    message.append(highbyte)

    # Prepare the frame to be sent, adding the address at the beginning
    print("Frame to be sent:", bytes(message))

    # Send the frame to the slave device
    client.socket.write(bytes(message))

    # Optionally, read the response
    response = client.socket.read(100)  # Adjust size as necessary
    client.close()
    
    return response

def calculate_crc(message):
    crc = 0xFFFF
    
    for byte in message:
        crc ^= byte
        for _ in range(8):
            lastbit = crc & 1
            crc >>= 1
            if lastbit:
                crc ^= 0xA001
    
    highbyte = (crc >> 8) & 0xFF
    lowbyte = crc & 0xFF
    
    return highbyte, lowbyte

if __name__ == '__main__':
	message = [0x02, 0x03, 0x00, 0x7F, 0x00, 0x01]
	print(send_modbus_frame(message))
