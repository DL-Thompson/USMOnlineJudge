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


namespace judge_compiler {


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

	PreScan scanner;

	for(size_t file = 0; file < m_fileProcessList.size(); ++file)
	{
		std::string f = m_fileProcessList[file];

		// pre-scan
		if (!scanner.isClean(f))
		{
			// save error report
			if (!save("error-pre-scan", f))
				std::cerr << "Error saving file\n";
		}
		else
		{
			// compile
			std::string executable = compile(f);

			// run and get result
			std::string result = execute(executable);

			// check result to answer

			// save result
			if (!save(result, f))
				std::cerr << "Error saving file\n";

			// remove file from queue and executable
			if (!clean(f, executable))
				std::cerr << "Error cleaning files\n";
		}

	}

	m_fileProcessList.clear();
}

std::string FileHandler::compile(std::string file)
{
	std::string dir = m_sourceDir;

	// below should add a special suffix for the problem type
	std::string obj = OBJECT_PREFIX;

	std::string path = dir + file;
	std::string command = "g++ -o " + dir + obj + " " + path;

	FILE *in;
	char buff[256];

	if (! (in = popen(command.c_str(), "r") )) {
		return "-1";
	}
	while(fgets(buff, sizeof(buff), in) != NULL) {
		std::cout << buff << std::endl;
	}
	pclose(in);

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

	while(fgets(buff, sizeof(buff), in) != NULL) {
		std::cout << buff << std::endl;
	}
	pclose(in);

	return buff;
}

bool FileHandler::save(std::string result, std::string origFileName)
{
	std::string content = result;
	std::string filePath = "";

	// adding fail/success suffix to file
	if (result == "error-pre-scan")
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
	if (remove(execPath.c_str()) != 0)
		return false;
	return true;
}


} /* namespace judge_compiler */
