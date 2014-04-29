#ifndef OUTPUTCHECKER_H_
#define OUTPUTCHECKER_H_

#include <string>

class OutputChecker {
public:
	OutputChecker(std::string checkDirectory="");
	virtual ~OutputChecker();
	bool isMatch(std::string userOutput, double exerciseID);
private:
	void strip(std::string& userOutput, std::string& correctOutput);
	void deleteChar(std::string& str, char charToDelete);
	std::string m_baseDirectory;
};

#endif /* OUTPUTCHECKER_H_ */
