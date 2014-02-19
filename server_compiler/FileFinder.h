/*
 * FileFinder.h
 *
 *  Created on: Feb 16, 2014
 *      Author: Cory Brown
 */

#ifndef FILE_FINDER_H_
#define FILE_FINDER_H_

#include <string>
#include <vector>

namespace judge_compiler {


class FileFinder
{
public:
	FileFinder(std::string sourceDir="", std::string destDir="");
	virtual ~FileFinder();
	void setDirectories(std::string sourceDir, std::string destDir);
	bool isNewContent();
	std::vector<std::string> getFiles();
private:
	std::string m_sourceDir;
	std::string m_destDir;
};


} /* namespace judge_compiler */

#endif /* FILE_FINDER_H_ */
