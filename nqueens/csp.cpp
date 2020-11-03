#include "csp.h"
#include <iostream>
using namespace std;

csp::csp(const int dim)
{
	csp::n = dim;

	//initialize X
	X.resize(n);

	//initialize D
	D.resize(n);
	for (auto i = 0; i < n; i++)
	{
		for (auto j = 0; j < n; j++)
		{
			D[i].push_back(j+1);
		}
	}
	
	
}

vector<int> csp::check_conflicts(Board board)
{
	vector<int> conflict(n);
	for (auto i = 0; i < n; i++)
	{
		if (conflict[i]) continue;

		//start from 0 so that we can skip the remainder of an iteration when we find a conflict
		for (auto j = 0; j < n; j++)
		{
			if (j == i) continue;

			if (board.pieces[i] == board.pieces[j] |
				std::abs(board.pieces[j] - board.pieces[i]) == j - i)
			{
				conflict[i] = conflict[j] = 1;
				break;
			}
		}
	}

	return conflict;


}

void csp::print_variables()
{
	for (auto i = 0; i < n; i++)
	{
		cout << X[i];
	}
	cout << "\n";
}

void csp::print_domains()
{
	for (auto i = 0; i < n; i++)
	{
		for (auto j = 0; j < D[i].size(); j++)
		{
			cout << D[i][j];
		}
		cout << "\n";
	}
}