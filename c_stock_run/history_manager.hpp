#pragma once

#include <unordered_map>

#include "common.hpp"
#include "rff_tools.hpp"

class Stockpyler;

class HistoryManager {
	bool done;
	time_t today, earliest_date, latest_date;
	RFF rff;
	std::unordered_map<std::string, std::tuple<time_t, time_t>> start_end_dates;
	std::unordered_map<SecurityID, std::vector<double>> prev_positions;
	Stockpyler* sp;
public:
	HistoryManager(Stockpyler* sp) : sp(sp) {};
	~HistoryManager() = default;

	double ohlcv(SecurityID id);
};