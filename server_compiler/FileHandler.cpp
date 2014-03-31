/*
 * FileHandler.cpp
 *
 *  Created on: Feb 16, 2014
 *      Author: Cory Brown
 */

#include "FileHandler.h"
#include "PreScan.h"
#include "OutputChecker.h"

#include <stdio.h>
#include <fstream>
#include <iostream>
#include <pthread.h>
#include <sys/types.h>
#include <sys/sysinfo.h>
#include <sstream>
#include <unistd.h>	//sleep
#include <ctime>	//clock
#include <sys/time.h> //gettimeofday

namespace judge_compiler {

/*
// ***CLASS UTILITIES*** //
typedef struct td {
	std::string fileName;
	std::string sourceDir;
	std::string destDir;
	std::string checkDir;
	double exID;
	double userID;
} ThreadData;
*/
void* runFile(void* arguments)
{
	/*
	judge_compiler::ThreadData* data;
	data = (judge_compiler::ThreadData*)arguments;

	std::string f = data->fileName;
	std::string source = data->sourceDir;
	std::string dest = data->destDir;
	std::string checkDir = data->checkDir;
	double exID = data->exID;
	double userID = data->userID;

	PreScan scanner;
	FileHandler fh(source, dest);
	// pre-scan
	if (!scanner.isClean(f))
	{
		// save error report
		if (!fh.save("error-pre-scan", f))
			std::cerr << "Error saving file\n";
	}
	else
	{
		// compile
		std::string executable = fh.compile(f);

		std::string result;

		if (executable.find("error:", 0) == std::string::npos)
		{
			// run and get result
			result = fh.execute(executable);

			// check result to answer
			OutputChecker checker(checkDir);
			checker.isMatch(result, exID);

		}
		else
		{
			result = executable;
			executable = "";
		}



		// save result
		if (!fh.save(result, f))
			std::cerr << "Error saving file\n";

		// remove file from queue and executable
		if (!fh.clean(f, executable))
			std::cerr << "Error cleaning files\n";

	}
	*/
	return NULL;

}

// ***CLASS FUNCTIONS*** //

FileHandler::FileHandler(std::string sourceDir, std::string destDir, std::string checkDir, std::string storageDir)
{
	m_sourceDir = sourceDir;
	m_destDir = destDir;
	m_checkDir = checkDir;
	m_storageDir = storageDir;
	m_runningTime = 0;
	m_memoryUsage = 0;
}

FileHandler::~FileHandler()
{
}

void FileHandler::setDirectories(std::string sourceDir, std::string destDir, std::string checkDir, std::string storageDir)
{
	m_sourceDir = sourceDir;
	m_destDir = destDir;
	m_checkDir = checkDir;
	m_storageDir = storageDir;
}

void FileHandler::addFiles(std::vector<std::string>& files)
{
	if (m_fileProcessList.empty())
	{
		m_fileProcessList = files;
	}
	else
	{
		for(size_t i = 0; i < files.size(); ++i)
			m_fileProcessList.push_back(files[i]);
	}
}

void FileHandler::run()
{
	if (m_fileProcessList.empty())
		return;


	/*						TEMPORARILY REMOVING THREADING
	// thread variables
	ThreadData t_data[num_files];
	pthread_t threads[num_files];
	int error[num_files];

	// setting up the arguments for each thread
	for(size_t t = 0; t < num_files; t++)
	{
		t_data[t].fileName = m_fileProcessList[t];
		t_data[t].sourceDir = m_sourceDir;
		t_data[t].destDir = m_destDir;
		t_data[t].checkDir = m_checkDir;
		t_data[t].exID = getExerciseID(m_fileProcessList[t]);
		t_data[t].userID = getUserID(m_fileProcessList[t]);
	}

	// running the threads
	for(size_t file = 0; file < num_files; ++file)
	{
		error[file] = pthread_create(&threads[file], NULL, judge_compiler::runFile, (void*)&t_data[file]);
	}

	// joining and checking errors
	for(size_t i = 0; i < num_files; i++)
	{
		pthread_join(threads[i], NULL);
		if (error[i] != 0)
			std::cerr << "Error joining threads\n";
	}
	*/

	PreScan scanner;
	FileHandler fh(m_sourceDir, m_destDir);

	for(size_t f = 0; f < m_fileProcessList.size(); f++)
	{
		std::string file = m_fileProcessList[f];

		double exID = getExerciseID(file);
		//double userID = getUserID(file);

		// pre-scan
		if (!scanner.isClean(file))
		{
			// save error report
			if (!fh.saveResult("error-pre-scan", file))
				std::cerr << "Error saving file\n";
		}
		else
		{
			// compile
			std::string executable = fh.compile(file);

			std::string result;

			if (executable.find("error:", 0) == std::string::npos)
			{
				// run and get result
				result = fh.execute(executable);

				// check result to answer
				/*
				 * if output is OK, save submitted file to permanent storage with time and mem tags to filename
				 */
				OutputChecker checker(m_checkDir);
				if (checker.isMatch(result, exID))
				{
					std::cout << "CORRECT\n";
					saveCorrect(file);
				}
				else
				{
					std::cout << "Incorrect Match\n";
					result = "incorrect";
				}

			}
			else
			{
				result = executable;
				executable = "";
			}

			// save result
			if (!fh.saveResult(result, file))
				std::cerr << "Error saving file\n";

			// remove file from queue and executable
			if (!fh.clean(file, executable))
				std::cerr << "Error cleaning files\n";

		}
	}
	m_fileProcessList.clear();
}

std::string FileHandler::compile(std::string file)
{
	std::string dir = m_sourceDir;

	std::string obj = OBJECT_PREFIX + "-" + file;

	std::string path = dir + file;
	std::string command = "g++ -o " + dir + obj + " " + path + " 2>&1";

	FILE *in;
	char buff[256];

	if (! (in = popen(command.c_str(), "r") )) {
		return "-1";
	}

	std::string result = "";
	while(fgets(buff, sizeof(buff), in) != NULL) {
		result += buff;
	}

	pclose(in);

	if (result.find("error:", 0) != std::string::npos)
		return result;

	return obj;
}

std::string FileHandler::execute(std::string executableName)
{
	std::string dir = m_sourceDir;
	std::string command = dir + executableName;

	timeval a;
	timeval b;


	FILE *in;
	char buff[256];

	// start checking the time
	gettimeofday(&a, 0);
	double t_start = a.tv_sec + (a.tv_usec / 1000000);

	// start checking the memory
	/* not implemented */

	//run it
	if (! (in = popen(command.c_str(), "r") )) {
		return "-1";
	}

	// check end time
	gettimeofday(&b, 0);
	double t_end = b.tv_sec + (b.tv_usec / 1000000);
	m_runningTime = t_end - t_start;

	// check end memory
	/* not implemented */

	std::string result = "";
	while(fgets(buff, sizeof(buff), in) != NULL) {
		result += buff;
	}
	pclose(in);

	return result;
}

bool FileHandler::saveResult(std::string result, std::string origFileName)
{
	std::string content = result;
	std::string filePath = "";

	// adding fail/success suffix to file
	if (result.find("error:", 0) != std::string::npos)
	{
		filePath += m_destDir + origFileName + "-error";
	}
	else if (result.find("incorrect", 0) != std::string::npos)
	{
		filePath += m_destDir + origFileName + "-incorrect";
	}
	else
	{
		filePath += m_destDir + origFileName + "-success";
	}

	std::ofstream outFile;
	outFile.open(filePath.c_str());

	if (!outFile)
		return false;

	outFile << "Time: " << m_runningTime << "\n";
	outFile.close();

	return true;
}

bool FileHandler::saveCorrect(std::string origFileName)
{
	// copies the good submitted code to a permanent location

	std::string fileCopyContent;
	std::string origFilePath = m_sourceDir + origFileName;
	std::string storageFilePath = m_storageDir + origFileName;
	std::ifstream in;
	in.open(origFilePath.c_str());
	if (!in) {
		std::cerr << "Error opening " << origFilePath << std::endl;
		return false;
	}

	while(!in.eof())
	{
		std::string tmp;
		getline(in, tmp);
		fileCopyContent += tmp;
	}

	in.close();

	std::ofstream out;
	out.open(storageFilePath.c_str());
	if (!out) {
		std::cerr << "Error opening output file " << storageFilePath << std::endl;
		return false;
	}
	out << fileCopyContent;
	out.close();

	return true;
}

bool FileHandler::clean(std::string origFileName, std::string executableName)
{
	std::string filePath = m_sourceDir + origFileName;
	std::string execPath = m_sourceDir + executableName;

	if (remove(filePath.c_str()) != 0)
		return false;
	if (executableName != "")
	{
		if (remove(execPath.c_str()) != 0)
			return false;
	}

	return true;
}

double FileHandler::getExerciseID(std::string fileName)
{
	double id;

	// get first of split, split on -
	std::string splitLeft;
	size_t endPos = fileName.find('-');
	splitLeft = fileName.substr(0, endPos);
	std::cout << "exercise id = " << splitLeft << "\n";
	std::stringstream ss;
	ss << splitLeft;
	ss >> id;
	return id;
}

double FileHandler::getUserID(std::string fileName)
{
	double id;

	// get second of split, split on -
	std::string splitMiddle;
	size_t startPos = fileName.find('-') + 1;
	size_t endPos = fileName.size();
	splitMiddle = fileName.substr(startPos, endPos);
	std::cout << "user id = " << splitMiddle << "\n";
	std::stringstream ss;
	ss << splitMiddle;
	ss >> id;

	return id;

}

} /* namespace judge_compiler */
