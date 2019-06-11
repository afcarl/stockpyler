#pragma once

#include "common.hpp"
#include "Stockpyler.hpp"

class Stockpyler;

class Strategy {
	Stockpyler* sp;
public:
	Strategy(Stockpyler* sp) : sp(sp) {}
	~Strategy() = default;

	void next();
	void stop();

	int64_t get_position(SecurityID id);
	f64 get_value();
	f64 get_cash();
	bool is_trading(SecurityID id);
	Order buy(SecurityID id, int64_t num_stocks);
	Order sell(SecurityID id, int64_t num_stocks);
	Order close(SecurityID id, int64_t num_stocks);
};