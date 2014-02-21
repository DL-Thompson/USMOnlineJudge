/*
 * FileHandler.cpp
 *
 *  Created on: Feb 16, 2014
 *      Author: Cory Brown
 */

#include "FileHandler.h"
#include "PreScan.h"

#include <stdio.h>
#include <fstream>
#include <iostream>
#include <pthread.h>

namespace judge_compiler {

// ***CLASS UTILITIES*** //
typedef struct td {
	std::string fileName;
	std::string sourceDir;
	std::string destDir;
} ThreadData;

void* runFile(void* arguments)
{
	judge_compiler::ThreadData* data;
	data = (judge_compiler::ThreadData*)arguments;

	std::string f = data->fileName;
	std::string source = data->sourceDir;
	std::string dest = data->destDir;

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

	return NULL;
}

// ***CLASS FUNCTIONS*** //

FileHandler::FileHandler(std::string sourceDir, std::string destDir)
{
	m_sourceDir = sourceDir;
	m_destDir = destDir;
}

FileHandler::~FileHandler()
{
}

void FileHandler::setDirectories(std::string sourceDir, std::string destDir)
{
	m_sourceDir = sourceDir;
	m_destDir = destDir;
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

	size_t num_files = m_fileProcessList.size();

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

	return result;
}

bool FileHandler::save(std::string result, std::string origFileName)
{
	std::string content = result;
	std::string filePath = "";

	// adding fail/success suffix to file
	if (result.find("error:", 0) != std::string::npos)
	{
		filePath += m_destDir + origFileName + "-error";
	}
	else
	{
		filePath += m_destDir + origFileName + "-success";
	}

	std::ofstream outFile;
	outFile.open(filePath.c_str());

	if (!outFile)
		return false;

	outFile << content;
	outFile.close();

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


} /* namespace judge_compiler */
