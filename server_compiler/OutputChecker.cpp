#include "OutputChecker.h"

#include <sstream>
#include <fstream>

OutputChecker::OutputChecker(std::string baseDirectory) {
	m_baseDirectory = baseDirectory;
}

OutputChecker::~OutputChecker() {
	// TODO Auto-generated destructor stub
}

bool OutputChecker::isMatch(std::string userOutput, double exerciseID)
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

	//now strip spaces, new lines, tabs
	strip(userOutput, correctOutput);

	if (userOutput == correctOutput)
		return true;
	return false;
}

void OutputChecker::strip(std::string& userOutput, std::string& correctOutput)
{
	// replacing spaces
	deleteChar(userOutput, ' ');
	deleteChar(correctOutput, ' ');

	// replacing newlines
	deleteChar(userOutput, '\n');
	deleteChar(correctOutput, '\n');

	// replacing tabs
	deleteChar(userOutput, '\t');
	deleteChar(correctOutput, '\t');
}

void OutputChecker::deleteChar(std::string& s, char charToDelete)
{
	std::size_t find = s.find(charToDelete);
	while(find != std::string::npos) {
		s = s.substr(0, find) + s.substr(find+1, s.size());
		find = s.find(charToDelete);
	}
}
