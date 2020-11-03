#pragma once
#include <vector>
#include <string>

using namespace std;

class Board {
public:
	int dim;
	Board(int dim);
	vector<int> pieces;
	void add_piece(int x);
	void remove_piece(int i);
	int collision_count(bool solve = false);
	bool check_solution();
	void print_pieces();
};

