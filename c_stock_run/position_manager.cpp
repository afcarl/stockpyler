#include "common.hpp"
#include "Stockpyler.hpp"
#include "position_manager.hpp"

std::vector<SecurityID> PositionManager::get_positions() {
	std::vector<SecurityID> retval;
	for (auto const& element : this->positions) {
		retval.push_back(element.first);
	}
	return retval;
}

int64_t PositionManager::position_size(SecurityID id) {
	auto it = this->positions.find(id);
	if (it == this->positions.end()) {
		return 0;
	}
	return this->positions[id];
}


Order PositionManager::buy(SecurityID id, int64_t num_stocks) {
	Order ret = Order(id, OrderAction::buy, num_stocks);
	this->orders.push_back(ret);
	return ret;
}

Order PositionManager::sell(SecurityID id, int64_t num_stocks) {
	Order ret = Order(id, OrderAction::sell, num_stocks);
	this->orders.push_back(ret);
	return ret;
}

Order PositionManager::close(SecurityID id, int64_t num_stocks) {
	if (this->position_size(id) > 0) {
		return this->sell(id, num_stocks);
	}
	else if(this->position_size(id) < 0) {
		return this->buy(id, num_stocks);
	}
	else {
		return Order();
	}
}

bool PositionManager::in_position(SecurityID id) {
	return this->position_size(id) != 0;
}

double PositionManager::current_cash() {
	return this->cash;
}

double PositionManager::current_value() {
	double ret = this->current_cash();
}


void PositionManager::next() {

}