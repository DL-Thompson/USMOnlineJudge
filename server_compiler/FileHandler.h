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
	FileHandler(std::string sourceDir="", std::string destDir="");
	virtual ~FileHandler();
	void setDirectories(std::string sourceDir, std::string destDir);
	void addFiles(std::vector<std::string>& files);
	void run();
private:
	// private functions
	std::string compile(std::string file);
	std::string execute(std::string executableName);
	bool save(std::string result, std::string origFileName);
	bool clean(std::string origFileName, std::string executableName);
	// private variables
	std::vector<std::string> m_fileProcessList;
	std::string m_sourceDir;
	std::string m_destDir;
};


} /* namespace judge_compiler */

#endif /* FILE_HANDLER_H_ */
