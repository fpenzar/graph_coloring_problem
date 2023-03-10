
CXX:=g++
#CXX:=x86_64-w64-mingw32-g++
DEBUG_FLAG:= -g -O3
RELESE_FLAG:= -O3 -s -DNDEBUG
CURRENT_FLAGS:= $(RELESE_FLAG)
CURRENT_FLAGS += -std=c++11 -pthread -I./src -Wall -Wconversion -Wfatal-errors -Wextra
DEPENDENCIES = ./lib/openGA-1.0.5/src/openGA.hpp

all:
	$(CXX) $(CURRENT_FLAGS) $(DEPENDENCIES) test.cpp -o project.bin

clean:
	rm *.bin