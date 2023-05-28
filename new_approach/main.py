import os
import struct

fifo_path = 'my_fifo'  # Replace with the actual path to your FIFO

# Create the FIFO if it doesn't exist
if not os.path.exists(fifo_path):
    os.mkfifo(fifo_path)

# Open the FIFO in write mode
fifo_fd = os.open(fifo_path, os.O_WRONLY)

# Define the command and value
command = b'c'  # Example command
value = 42  # Example value

# Pack the command and value into a binary string
data = struct.pack('cB', command, value)

# Write the data to the FIFO
os.write(fifo_fd, data)

# Close the FIFO
os.close(fifo_fd)
