/*
 * FileFinder.cpp
 *
 *  Created on: Feb 16, 2014
 *      Author: Cory Brown
 */

#include "FileFinder.h"

#include <string>
#include <sys/types.h>
#include <dirent.h>
#include <stdio.h>

namespace judge_compiler {


FileFinder::FileFinder(std::string sourceDir, std::string destDir)
{
	m_sourceDir = sourceDir;
	m_destDir = destDir;
}

FileFinder::~FileFinder()
{
	// TODO Auto-generated destructor stub
}

void FileFinder::setDirectories(std::string sourceDir, std::string destDir)
{
	m_sourceDir = sourceDir;
	m_destDir = destDir;
}

bool FileFinder::isNewContent()
{
	DIR *directory;

	// -2 accounting for directories having . and .. folders
	int i = -2;
	struct dirent *ep;
	directory = opendir(m_sourceDir.c_str());

	if (directory != NULL) {
		ep = readdir(directory);
		while(ep)
		{
			++i;
			ep = readdir(directory);
		}
		(void) closedir (directory);
	}

	return i > 0;
}

std::vector<std::string> FileFinder::getFiles()
{
	std::vector<std::string> files;
	DIR *directory;

	struct dirent *ep;
	directory = opendir(m_sourceDir.c_str());

	if (directory != NULL) {
		ep = readdir(directory);
		while(ep)
		{
			std::string name = ep->d_name;
			if (name != "." && name != "..")
				files.push_back(name);

			ep = readdir(directory);
		}
		(void) closedir (directory);
	}

	return files;
}

} /* namespace judge_compiler */
