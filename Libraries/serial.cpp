#include <termios.h>
#include <string>
#include <fcntl.h>
#include <unistd.h>
#include <iostream>

#include "serial.h"

using namespace std;

State state = Idle;
extern serial_data_t serial_data;


int serialSetup(const char* serial_port, int baud_rate) {

    int serial_fd = open(serial_port, O_RDWR | O_NOCTTY | O_NONBLOCK);
    if (serial_fd < 0) {
        cout << "Error: could not open serial port " << serial_port << endl;
        return 1;
    }
    else {
        cout << "Succesfully connected: " << serial_port << endl;

    }

    struct termios options;
    tcgetattr(serial_fd, &options);
    cfsetispeed(&options, baud_rate);
    cfsetospeed(&options, baud_rate);
    options.c_cflag |= (CLOCAL | CREAD);
    options.c_cflag &= ~CSIZE;
    options.c_cflag |= CS8;
    options.c_cflag &= ~PARENB;
    options.c_cflag &= ~CSTOPB;
    options.c_cflag &= ~CRTSCTS;
    options.c_lflag &= ~(ICANON | ECHO | ECHOE | ISIG);
    options.c_oflag &= ~OPOST;
    options.c_cc[VMIN] = 0;
    options.c_cc[VTIME] = 1;
    tcsetattr(serial_fd, TCSANOW, &options);

    return serial_fd;
}

void serialRead(int *serial_fd, serial_data_t *data) {
    char buffer[1024];
    ssize_t count = read(*serial_fd, buffer, sizeof(buffer));
    if (count > 0) {
        for (int i = 0; i < count; i++) {
            char c = buffer[i];
            switch (state) {
                case Idle:
                    switch (c) {
                        case 's':
                            data->cmd = HOR_SCAN;
                            state = ReadingValue;
                            break;
                        case 'p':
                            data->cmd = STEPS;
                            state = ReadingValue;
                            break;
                        case 'd':
                            data->cmd = DISTANCE;
                            state = ReadingValue;
                            break;
                        case 'f':
                            data->cmd = SHOOT;
                            state = ReadingValue;
                            break;
                        case 'r':
                            data->cmd = RETRACT;
                            state = ReadingValue;
                            break;
                        default:
                            if (c == 'e') {
                                data->cmd = ERROR;
                                state = ReadingValue;
                            }
                            break;
                    }
                    break;

                case ReadingValue:
                    data->data = c;
                    cout << "Command " << data->cmd << " value " << data->data << endl;
                    state = Idle;
                    break;
            }
        }
    }
}

void serialSend(int *serial_fd, serial_data_t *data) {
    uint8_t cmdChar = 0;
    switch (data->cmd) {
        case HOR_SCAN:
        cmdChar = 's';  // scan
        break;
        case STEPS:
        cmdChar = 'p';  // position
        break;
        case DISTANCE:
        cmdChar = 'd';  // distance
        break;
        case SHOOT:
        cmdChar = 'f';  // fire
        break;
        case RETRACT:
        cmdChar = 'r';  // retract
        break;
        default:
        cmdChar = 'e';  // error message
        break;
    }
    uint8_t dataChar = data->data;
    uint8_t buffer[2] = {cmdChar, dataChar};
    write(*serial_fd, buffer, sizeof(buffer));
}
