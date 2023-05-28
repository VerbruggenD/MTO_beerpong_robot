#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <chrono>
#include <thread>

#include "serial.h"

using namespace std;

int main() {
    const char* serial_port = "/dev/ttyACM0";  // Replace with the actual serial port
    int baud_rate = 9600;                      // Replace with the actual baud rate

    // Open the serial port
    int serial_fd = serialSetup(serial_port, baud_rate);
    if (serial_fd < 0) {
        cout << "Failed to open serial port." << endl;
        return 1;
    }

    while (true) {
        // Open the FIFO for reading
        ifstream fifo("my_pipe");  // Replace with the actual path to your FIFO

        if (!fifo) {
            cout << "Failed to open FIFO." << endl;
            return 1;
        }

        if (fifo.peek() != ifstream::traits_type::eof()) {
            string line;
            getline(fifo, line);
            istringstream iss(line);
            string commandStr, valueStr;

            if (getline(iss, commandStr, ',') && getline(iss, valueStr, ',')) {
                // Parse command and value from the line
                char command = commandStr[0];
                // uint8_t value = static_cast<uint8_t>(stoul(valueStr));
                int value = stoi(valueStr);
                uint8_t upper = value/100;
                uint8_t lower = value % 100;

                // Create serial_data_t struct with the parsed values
                serial_data_t data;
                switch (command) {
                    case 'c':
                        data.cmd = CAM_POS;
                        break;
                    case 'l':
                        data.cmd = LEFT;
                        break;
                    case 'v':
                        data.cmd = VERTICAL_ANGL;
                        break;
                    case 's':
                        data.cmd = SHOOT;
                        break;
                    case 'r':
                        data.cmd = RIGHT;
                        break;
                    default:
                        data.cmd = ERROR;
                        break;
                }
                //data.data = value;
                data.upper = upper;
                data.lower = lower;

                // // Send data over serial
                serialSend(&serial_fd, &data);

                cout << "Sent command " << command << " value " << valueStr << " to Arduino." << endl;
            }
        }


        // Close the FIFO
        fifo.close();

        // Sleep for a short duration to avoid busy waiting
        this_thread::sleep_for(chrono::milliseconds(100));
    }

    // Close the serial port
    close(serial_fd);

    return 0;
}
