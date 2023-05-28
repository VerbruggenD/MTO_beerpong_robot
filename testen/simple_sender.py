import os

PIPE_NAME = "cmd_pipe"

# Open the named pipe for reading and writing
fifo = open(PIPE_NAME, 'wb')

# Send a response back through the named pipe

cmd = iets
value=0

response = bytes([cmd]+[value])
fifo.write(response)

# Close the named pipe
fifo.close()