#include "OutputChecker.h"

#include <ctime>
#include <sstream>
#include <fstream>

OutputChecker::OutputChecker(std::string baseDirectory) {
	m_baseDirectory = baseDirectory;
}

OutputChecker::~OutputChecker() {
	// TODO Auto-generated destructor stub
}

bool OutputChecker::isMatch(std::string input, double exerciseID)
{
	std::stringstream ss;
	ss << exerciseID;
	std::string exerciseIDStr;
	ss >> exerciseIDStr;

	std::string exerciseDirectory = m_baseDirectory;
	std::string file = exerciseDirectory + exerciseIDStr + ".check";

	std::ifstream fileIn;
	fileIn.open(file.c_str());

	if (!fileIn)
		return false;

	std::string correctOutput = "";

	while(!fileIn.eof()){
		std::string tmp;
		getline(fileIn, tmp);
		correctOutput += tmp;
	}

	if (input == correctOutput)
		return true;
	return false;
}
