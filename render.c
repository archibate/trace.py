#include <stdio.h>
#if defined(__linux__) || defined(__MACOSX)
#include <sys/time.h>
#elif defined (WIN32) || defined(_WIN32)
#include <windows.h>
#else
        Unsupported Platform !!!
#endif
#include "display.h"

Camera camera;

unsigned int *pixels;
int width = 640;
int height = 480;

double WallClockTime() {
#if defined(__linux__) || defined(__MACOSX)
	struct timeval t;
	gettimeofday(&t, NULL);

	return t.tv_sec + t.tv_usec / 1000000.0;
#elif defined (WIN32) || defined(_WIN32)
	return GetTickCount() / 1000.0;
#else
	Unsupported Platform !!!
#endif
}

void UpdateRendering(void) {
}

