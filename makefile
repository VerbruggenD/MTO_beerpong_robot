TARGET = app
SRCS = main.cpp

CXX = g++
CXXFLAGS = -std=c++11 -Wall

$(TARGET): $(SRCS)
	$(CXX) $(CXXFLAGS) $(SRCS) -o $(TARGET)

.PHONY: clean

clean:
	rm -f $(TARGET) *.o
