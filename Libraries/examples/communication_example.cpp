#include <termios.h>
#include <string>
#include <fcntl.h>
#include <unistd.h>
#include <iostream>

#include "serial.h"

using namespace std;

// /dev/tty.usbserial-1420
// /dev/tty.usbmodem14201   direct
// /dev/tty.usbmodem141301  hub

serial_data_t serial_data;

int main() {
    int serial_fd = serialSetup("/dev/tty.usbmodem141301", 9600);
    serial_data.cmd = SHOOT;
    serial_data.data = 100;

    while (true) {
        serialRead(&serial_fd, &serial_data);

        serialSend(&serial_fd, &serial_data);
    }

    close(serial_fd);

    return 0;
}