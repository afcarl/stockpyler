#pragma once

#include <string>
#include <unordered_map>
#include <vector>

#include "common.hpp"

enum class OrderStatus {
	placed,
	executed,
	cancelled,
	margin,
	rejected,
};

enum class CommissionType {
	none,
	fixed,
	per_contract
};

enum class SecurityType {
	stock,
	future,
	option
};

enum class OrderAction {
	buy,
	sell
};

struct Security {
	std::string symbol;
	SecurityType security_type;
	CommissionType commission_type;
};

class Order {
private:
	int64_t id;
	OrderStatus status;
	SecurityID security;
	OrderAction action;
	int64_t num_stocks;
	static int64_t current_order_id;

public:
	Order(OrderStatus status, SecurityID security, OrderAction action, int64_t num_stocks) :
		id(current_order_id++),
		status(status),
		security(security),
		action(action),
		num_stocks(num_stocks) {}
	Order(SecurityID security, OrderAction action, int64_t num_stocks) :
		id(current_order_id++),
		security(security),
		action(action),
		num_stocks(num_stocks) {
		this->status = num_stocks < 0 ? OrderStatus::placed : OrderStatus::rejected;
	}
	Order() : id(current_order_id++), status(OrderStatus::rejected) {};
	~Order() = default;
};

class Stockpyler;

class PositionManager
{

	double cash;
	std::unordered_map<SecurityID, int64_t> positions;
	std::vector<Order> orders;
	Stockpyler* sp;
public:
	PositionManager(Stockpyler* sp) : sp(sp) {}
	~PositionManager() = default;

	Order buy(SecurityID id, int64_t num_stocks);
	Order sell(SecurityID id, int64_t num_stocks);
	Order close(SecurityID id, int64_t num_stocks);

	void next();
	void add_position(SecurityID id, int64_t num_stocks);
	bool in_position(SecurityID id);
	int64_t position_size(SecurityID id);
	std::vector<SecurityID> get_positions();
	double current_cash();
	double current_value();
};