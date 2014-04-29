FLAGS = -Wall -O3 -pthread
CXX=g++

compiler_controller:	Compiler_Runner.cpp FileFinder.o FileHandler.o OutputChecker.o PreScan.o Timer.o
	${CXX} -o compiler_controller Compiler_Runner.cpp FileFinder.o FileHandler.o OutputChecker.o PreScan.o Timer.o  ${FLAGS}

FileHandler.o:	FileHandler.h FileHandler.cpp
	${CXX} -c FileHandler.cpp ${FLAGS}

FileFinder.o:	FileFinder.h FileFinder.cpp
	${CXX} -c FileFinder.cpp ${FLAGS}

OutputChecker.o:	OutputChecker.h OutputChecker.cpp
	${CXX} -c OutputChecker.cpp ${FLAGS}

PreScan.o:	PreScan.h PreScan.cpp
	${CXX} -c PreScan.cpp ${FLAGS}

Timer.o:	Timer.h Timer.cpp
	${CXX} -c Timer.cpp ${FLAGS}

clean:
	rm compiler_controller FileHandler.o FileFinder.o PreScan.o OutputChecker.o Timer.o
