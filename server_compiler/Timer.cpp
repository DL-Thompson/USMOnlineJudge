/*
 * Timer.cpp:
 *  Simple timing utility
 *  Here be dragons.
 */

#include "Timer.h"
#include <sys/time.h>
#include <cstddef>

Timer::Timer() {
	start();
}

void Timer::start() {
	timeval timev;
	gettimeofday(&timev, NULL);
	microseconds_since_epoch = timev.tv_sec * 1000 * 1000 + timev.tv_usec;
}

unsigned long Timer::get_microseconds() const {
	Timer now;
	return now.microseconds_since_epoch - microseconds_since_epoch;
}
