#include "board.h"
#include "arc.h"
#include "csp.h"
#include <iostream>
#include <queue>
using namespace std;

bool revise(csp& csp, Arc x, Board test_board)
{
	bool revised = false;
	
	for (auto i = 0; i < csp.D[x.xi].size(); i++)
	{
		//copy variables to the tester board
		test_board.pieces = csp.X;
		//add the first piece to the board
		test_board.pieces[x.xi] = csp.D[x.xi][i];
		//test each value in the domain of j
		for (auto j = 0; j < csp.D[x.xj].size(); j++)
		{
			//add the next element in j's domain to the board
			test_board.pieces[x.xj] = csp.D[x.xj][j];

			if (!test_board.collision_count(true))
			{
				//I really don't like using goto, but it seems reasonable here
				//if there's a pair where there are no collisions, we can keep i
				goto next_i;
			}
		}
		//erase element i as no value in j satisfies that condition
		csp.D[x.xi].erase(csp.D[x.xi].begin() + i);
		i--;
		revised = true;

	next_i:;
	}

	return revised;
}

bool AC3(csp& csp)
{
	Board test_board = Board(csp.n);
	queue<Arc> q;
	// initialize queue
	for (auto i = 0; i < csp.n; i++)
	{
		for (auto j = i + 1; j < csp.n; j++)
		{
			q.push(Arc(i, j));
		}
	}
	Arc x;  //current element
	while (!q.empty())
	{
		x = q.front();
		q.pop();
		if (revise(csp, x, test_board)) 
		{
			if (!csp.D[x.xi].size())
			{
				return false;
			}

			//I'm assuming that the neighbors would be every piece because of diagonals
			for (auto k = 0; k < csp.n; k++)
			{
				if (k != x.xi)
				{
					q.push(Arc(k, x.xi));
				}
			}
		}
	}

	return true;
}

Board backtrack(Board assignment, csp c)
{
	if (assignment.check_solution()) return assignment;

	//I'm using the fail first for selection and fail last for assignments strategy in 6.3.1
	//var is the index of the variable in csp.X
	int min = c.n + 1;
	int min_var;
	int var = 0;
	while (var < c.n) 
	{ 
		//only consider unassigned variables
		if (!assignment.pieces[var])
		{
			//use \leq to avoid an array out of bounds issue
			if (c.D[var].size() <= min)
			{
				min_var = var;
				min = c.D[var].size();
			}
		}
		var++; 
	}



	if (min_var >= c.n)
	{
		printf("Uh oh. min > c.n");
		return Board(8);
	}
	var = min_var;

	for (auto i = 0; i < c.D[var].size(); i++)
	{
		// copy the csp so changes made by 
		csp next_csp = c;
		assignment.pieces[var] = next_csp.D[var][i];
		//pass true to return immediately on finding a collision rather than counting the total number of pairs
		if (!assignment.collision_count(true))
		{
			// update arc consistency
			// AC3 takes the reference so should update the csp
			// passing along the csp to backtrack without a reference makes copies for each recursive call
			next_csp.X = assignment.pieces;
			bool inference = AC3(next_csp);

			if (inference)
			{
				Board result = backtrack(assignment, next_csp);

				if (result.pieces[0] != -1) return result;
			}
		}
	}

	vector<int> failure;
	failure.push_back(-1);
	assignment.pieces = failure;
	return assignment;
}

Board backtracking_search(csp csp)
{
	//create assignment object
	Board assignment = Board(csp.n);
	assignment.pieces = csp.X;
	
	return backtrack(assignment, csp);
	
}


Board min_conflicts(csp c, int max_steps = 100)
{
	Board current = Board(c.n);
	//create a random arrangement of the queens 
	for (auto i = 0; i < c.n; i++)
	{
		current.pieces[i] = i;
	}
	std::random_shuffle(current.pieces.begin(), current.pieces.end());

	while (max_steps)
	{
		if (current.check_solution()) return current;

		vector<int> conflicts = c.check_conflicts(current);


		max_steps--;
	}

	return current;
}



int main()
{
	/*
	Board b = Board(4);
	b.add_piece(1);
	b.add_piece(2);
	b.add_piece(3);
	cout << b.collision_count() << "\n";
	cout << b.check_solution() << "\n";
	*/

	csp c = csp(30);
	
	Board result = backtracking_search(c);
	cout << "Search complete \n";
	result.print_pieces();
} 