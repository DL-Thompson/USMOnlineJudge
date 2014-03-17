#ifndef OUTPUTCHECKER_H_
#define OUTPUTCHECKER_H_

#include <string>

class OutputChecker {
public:
	OutputChecker(std::string baseDirectory="");
	virtual ~OutputChecker();
	bool isMatch(std::string input, double exerciseID);
private:
	std::string m_baseDirectory;
};

#endif /* OUTPUTCHECKER_H_ */
