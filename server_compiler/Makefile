FLAGS = -Wall -O3 -pthread
CXX=g++

compiler_controller:	Compiler_Runner.cpp FileFinder.o FileHandler.o PreScan.o
	${CXX} -o compiler_controller Compiler_Runner.cpp FileFinder.o FileHandler.o PreScan.o  ${FLAGS}

FileHandler.o:	FileHandler.h FileHandler.cpp
	${CXX} -c FileHandler.cpp ${FLAGS}

FileFinder.o:	FileFinder.h FileFinder.cpp
	${CXX} -c FileFinder.cpp ${FLAGS}

PreScan.o:	PreScan.h PreScan.cpp
	${CXX} -c PreScan.cpp ${FLAGS}

clean:
	rm compiler_controller FileHandler.o FileFinder.o PreScan.o
