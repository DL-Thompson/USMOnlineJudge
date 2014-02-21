#include "FileFinder.h"
#include "FileHandler.h"
#include <iostream>
#include <unistd.h>	// sleep
#include <stdlib.h> // atoi

using namespace judge_compiler;

int main(int argc, char* argv[])
{
	std::string sourceDirectory = "/home/judge/submission-q";
	std::string destDirectory = "/home/judge/submission-results";
	size_t sleepTime = 2;

	// check for arguments
	for(int i = 1; i < argc; ++i)
	{
		std::cerr << "ARGS:  " << argv[i] << std::endl;
		// specifies a directory to check for files
		if (std::string(argv[i]) == "-s" || std::string(argv[i]) == "--source" )
		{
			sourceDirectory = std::string(argv[i+1]);
			++i;
		}
		else if (std::string(argv[i]) == "-d" || std::string(argv[i]) == "--dest" )
		{
			destDirectory = std::string(argv[i+1]);
			++i;
		}
		else if (std::string(argv[i]) == "-t" || std::string(argv[i]) == "--timer" )
		{
			sleepTime = atoi(argv[i+1]);
			++i;
		}
		else if (std::string(argv[i]) == "-h" || std::string(argv[i]) == "--help" )
		{
			std::cout << "This program checks for new submissions in a specified or default\n";
			std::cout << "directory, then compiles, error checks, saves results, and removes\n";
			std::cout << "original files\nArguments:\n";
			std::cout << "-s <directory> --source <directory> specified source directory to search\n";
			std::cout << "-d <directory> --dest <directory> specified directory to save results\n";
			std::cout << "-t <time in integer> --timer <time in integer> amount to sleep between checks\n";
			std::cout << "-h --help display this help dialog\n";
			return 0;
		}
		else
		{
			std::cout << "Argument not found. Use -h for help on arguments\n";
			return 0;
		}

		std::cout << "Setup config:\n";
		std::cout << "Source directory: " << sourceDirectory << "\nDestination directory: " << destDirectory;
		std::cout << "\nSleep time between folder check: " << sleepTime << "\n";
	}

	// setup the file finder
	FileFinder finder;
	finder.setDirectories(sourceDirectory, destDirectory);

	// dummy variable, should never false unless server crashes
	bool serverOnline = true;
	while(serverOnline)
	{
		// check for new content. if so, start running the files through file handler
		if (finder.isNewContent())
		{
			std::vector<std::string> filesToCompile = finder.getFiles();
			FileHandler handler(sourceDirectory, destDirectory);
			handler.addFiles(filesToCompile);
			handler.run();
		}

		sleep(sleepTime);
	}

	return 0;
}
