#pragma once

#include <vector>
#include <memory>

#include "common.hpp"
#include "history_manager.hpp"
#include "position_manager.hpp"
#include "Strategy.hpp"
#include "Observer.hpp"


class Stockpyler {
	bool live;
	std::vector<std::shared_ptr<Strategy>> strategies;
	std::vector<std::shared_ptr<Observer>> observers;
	HistoryManager hm;
	PositionManager pm;
public:
	Stockpyler() : live(false), pm(this), hm(this) {};
	~Stockpyler() = default;
	void add_strategy(std::shared_ptr<Strategy> strategy) { this->strategies.push_back(strategy); }
	void add_observer(std::shared_ptr<Observer> observer) { this->observers.push_back(observer); }

	void start();
	void run();
	void stop();

	int64_t get_position(SecurityID id);
	f64 get_value();
	f64 get_cash();
	bool is_trading(SecurityID id);
	Order buy(SecurityID id, int64_t num_stocks);
	Order sell(SecurityID id, int64_t num_stocks);
	Order close(SecurityID id, int64_t num_stocks);
};