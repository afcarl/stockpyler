#pragma once

#include <cstdint>
#include <cstdio>
#include <sys/mman.h>

#include <string>

#include "common.hpp"

constexpr int64_t RFF_LINE_SIZE = 128;

struct RFFLine
{
	long long int timestamp;
	char symbol[24];
	double open, high, low, close, volume, turnover, unadj_close, close_ma200, averagefloat, _pad0, _pad1, _pad2;
};

class RFF {
	FILE* file_handle;
	void* mmap_handle;
	RFFLine* lines;
	int64_t len;
	int64_t pos;
	bool done;
public:
	RFF() = default;
	RFF(std::string path);
	~RFF();
	RFFLine* next();
	RFFLine* at(int64_t index);
};

