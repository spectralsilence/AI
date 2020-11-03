#include "board.h"
#include <iostream>
#include <cmath>

Board::Board(int dim)
{
	Board::dim = dim;
}

void Board::add_piece(int x)
{
	if (x < 0 | x >= dim)
	{
		std::cout << "Invalid piece location";
		return;
	}
	pieces.push_back(x);
}

void Board::remove_piece(int i)
{
	Board::pieces.erase(Board::pieces.begin() + i);
}

int Board::collision_count(bool solve)
{
	// the solve parameter denotes that we're checking to see if we've found a solution
	// with solve = False, this method acts as a heuristic, returning the number of pairs in collision
	int count = 0;
	for (auto i = 0; i < Board::pieces.size(); i++)
	{
		// ignore unitiialized pieces (i.e. with value=0)
		if (!Board::pieces[i]) continue;
		for (auto j = i + 1; j < Board::pieces.size(); j++)
		{
			// ignore unitiialized pieces (i.e. with value=0)
			if (!Board::pieces[j]) continue;
			//terminate as soon as count is nonzero to save time
			if (solve and count)
			{
				return -1;
			}
			//check for collision 
			if (Board::pieces[i] == Board::pieces[j] |
				std::abs(Board::pieces[i] - Board::pieces[j]) == j - i)
			{
				count++;
			}
		}
	}
	return count;
}

bool Board::check_solution()
{
	for (auto i =0 ; i < Board::pieces.size(); i++)
	{
		if (!Board::pieces[i]) return false;
	}
	if (Board::pieces.size() == Board::dim &&
		!Board::collision_count(true))
	{
		return true;
	}
	return false;
}

void Board::print_pieces()
{
	for (auto i = 0; i < pieces.size(); i++)
	{
		cout << pieces[i] << " ";
	}
	cout << "\n";
}