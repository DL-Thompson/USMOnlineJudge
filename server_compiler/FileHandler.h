/*
 * FileHandler.h
 *
 *  Created on: Feb 16, 2014
 *      Author: Cory Brown
 */

#ifndef FILE_HANDLER_H_
#define FILE_HANDLER_H_

#include <string>
#include <vector>

namespace judge_compiler {

static const std::string OBJECT_PREFIX = "o3falj2j";

class FileHandler
{
public:
	FileHandler(std::string sourceDir="", std::string destDir="", std::string checkDir="", std::string inputDir="", std::string storageDir="");
	virtual ~FileHandler();
	void setDirectories(std::string sourceDir, std::string destDir, std::string checkDir, std::string inputDir, std::string storageDir);
	void addFiles(std::vector<std::string>& files);
	void run();
	std::string compile(std::string file);
	std::string execute(std::string executableName, double exID);
	bool saveResult(std::string result, std::string origFileName);
	bool saveCorrect(std::string origFileName);
	bool cleanDirectories(std::string origFileName, std::string executableName);
private:
	double getExerciseID(std::string fileName);
	double getUserID(std::string fileName);
	bool isInputFile(double exID);
	std::vector<std::string> m_fileProcessList;
	std::string m_sourceDir;
	std::string m_destDir;
	std::string m_checkDir;
	std::string m_inputDir;
	std::string m_storageDir;
	time_t m_runningTime;
	long long m_memoryUsage;
};


} /* namespace judge_compiler */

#endif /* FILE_HANDLER_H_ */
