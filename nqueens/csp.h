#pragma once
#include "board.h"
#include <vector>

class csp {
public:
	csp(int dim);
	int n;
	std::vector<int> X;
	std::vector<std::vector<int>> D;

	void print_variables();
	void print_domains();
	vector<int> check_conflicts(Board board);
};

