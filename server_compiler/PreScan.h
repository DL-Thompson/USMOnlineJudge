/*
 * PreScan.h
 *
 *  Created on: Feb 16, 2014
 *      Author: Cory Brown
 */

#ifndef PRESCAN_H_
#define PRESCAN_H_

#include <string>

namespace judge_compiler
{


class PreScan
{
public:
	PreScan();
	virtual ~PreScan();
	bool isClean(std::string file);
};


} /* namespace judge_compiler */

#endif /* PRESCAN_H_ */
