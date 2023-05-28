#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <signal.h>

using namespace std;

const char* CMD_PIPE = "cmd_pipe";
const char* STATUS_PIPE = "status_pipe";

int main() {
  
  // setup function

  // Create the FIFO pipe if it doesn't exist
  if (mkfifo(CMD_PIPE, 0666) == -1 && errno != EEXIST) {
      cout << "Error: Failed to create the FIFO pipe\n";
      return 1;
  }

  // Open the FIFO for read only
  int fd = open(CMD_PIPE, O_RDONLY | O_NONBLOCK);
  if (fd == -1) {
      std::cerr << "Error: Failed to open the FIFO pipe\n";
      return 1;
  } else {
      std::cout << "Opened FIFO pipe for read only\n";
  }

  while(true) {

    // loop function

    unsigned char response[2];
    int num_bytes = read(fd, response, sizeof(response));
    if (num_bytes == -1) {
      std::cerr << "Error: Failed to read from the FIFO pipe\n";
      break;
    } else if (num_bytes > 0) {
      cout << "Received response: " << (int)response[0] << " " << (int)response[1] << endl;
    }

      // sleep to reduce CPU usage
      usleep(1000);
  }

  close(fd); // Close the fifo when done

  unlink(CMD_PIPE);

  return 0;
}