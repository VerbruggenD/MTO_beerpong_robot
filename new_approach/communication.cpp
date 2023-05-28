#include <fcntl.h>
#include <unistd.h>
#include <iostream>

#include "serial.h"

using namespace std;

// ... Other code ...

void handleCommand(char cmd, uint8_t value) {
    // Create a serial_data_t object with the received command and value
    serial_data_t data;
    switch (cmd) {
        case 'c':
            data.cmd = CAM_POS;
            data.data = value;
            break;
        // Handle other commands and values as needed
    }

    // Open the serial port
    const char* serial_port = "/dev/ttyUSB0";  // Replace with your serial port
    int baud_rate = 9600;  // Replace with your baud rate
    int serial_fd = serialSetup(serial_port, baud_rate);

    // Send data over serial
    serialSend(&serial_fd, &data);

    cout << "serial sent\n";

    // Close the serial port
    close(serial_fd);
}

int main() {
    const char* fifo_path = "my_pipe";  // Replace with the actual path to your FIFO

    // Open the FIFO in read-only mode
    int fifo_fd = open(fifo_path, O_RDONLY);

    cout << "fifo open\n";

    while(true) {

        // Read from the FIFO
        char cmd;
        uint8_t value;
        ssize_t count = read(fifo_fd, &cmd, sizeof(cmd));

        cout << "fifo read\n";

        if (count > 0) {
            // Read the value from the FIFO
            count = read(fifo_fd, &value, sizeof(value));
            if (count > 0) {
                handleCommand(cmd, value);
            }
        }

    }

    // Close the FIFO
    close(fifo_fd);

    return 0;
}
