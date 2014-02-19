#include "FileFinder.h"
#include "FileHandler.h"
#include <iostream>
#include <unistd.h>	// sleep
#include <stdlib.h> // atoi

using namespace judge_compiler;

int main(int argc, char* argv[])
{
	std::string sourceDirectory = "/home/cory/Desktop/OJ/sq/";
	std::string destDirectory = "/home/cory/Desktop/OJ/sr/";
	size_t sleepTime = 2;

	// check for arguments
	for(int i = 1; i < argc; ++i)
	{
		// specifies a directory to check for files
		if (argv[i] == const_cast<char*>("-s") || argv[i] == const_cast<char*>("--source") )
		{
			sourceDirectory = argv[i+1];
			++i;
		}
		else if (argv[i] == const_cast<char*>("-d") || argv[i] == const_cast<char*>("--dest") )
		{
			destDirectory = argv[i+1];
			++i;
		}
		else if (argv[i] == const_cast<char*>("-t") || argv[i] == const_cast<char*>("--timer") )
		{
			sleepTime = atoi(argv[i+1]);
			++i;
		}
		else if (argv[i] == const_cast<char*>("-h") || argv[i] == const_cast<char*>("--help") )
		{
			std::cout << "This program checks for new submissions in a specified or default\n";
			std::cout << "directory, then compiles, error checks, saves results, and removes\n";
			std::cout << "original files\nArguments:\n";
			std::cout << "-s <directory> --source <directory> specified source directory to search\n";
			std::cout << "-d <directory> --dest <directory> specified directory to save results\n";
			std::cout << "-t <time in integer> --timer <time in integer> amount to sleep between checks\n";
			std::cout << "-h --help display this help dialog\n";
		}
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
