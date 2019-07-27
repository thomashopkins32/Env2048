
#include <iostream>
#include <iomanip>
#include <string>
#include <cstdlib>

void printBoard(int** board) {
	for(int i = 0; i < 4; ++i) {
		for(int j = 0; j < 4; ++j) {
			std::cout << std::right << std::setw(10) << board[i][j];
		}
		std::cout << std::endl;
	}
}

void add_two(int** board) {
	int i = rand() % 4;
	int j = rand() % 4;
	while(board[i][j] != 0) {
		i = rand() % 4;
		j = rand() % 4;
	}
	board[i][j] = 2;
}

void right(int** board) {
	for(int i = 0; i < 4; ++i) {
		for(int j = 3; j > 0; --j) {
			for(int k = j-1; k > -1; --k) {
				if(board[i][k] != 0) {
					if(board[i][j] == board[i][k]) {
						board[i][j] += board[i][k];
						board[i][k] = 0;
						break;
					}
					else if(board[i][j] == 0) {
						board[i][j] = board[i][k];
						board[i][k] = 0;
					}
					else
						break;
				}
			}
		}
	}
}

void left(int** board) {
	for(int i = 0; i < 4; ++i) {
		for(int j = 0; j < 3; ++j) {
			for(int k = j+1; k < 4; ++k) {
				if(board[i][k] != 0) {
					if(board[i][j] == board[i][k]) {
						board[i][j] += board[i][k];
						board[i][k] = 0;
						break;
					}
					else if(board[i][j] == 0) {
						board[i][j] = board[i][k];
						board[i][k] = 0;
					}
					else
						break;
				}
			}
		}
	}
}

void up(int** board) {
	for(int j = 0; j < 4; ++j) {
		for(int i = 0; i < 3; ++i) {
			for(int k = i+1; k < 4; ++k) {
				if(board[k][j] != 0) {
					if(board[i][j] == board[k][j]) {
						board[i][j] += board[k][j];
						board[k][j] = 0;
						break;
					}
					else if(board[i][j] == 0) {
						board[i][j] = board[k][j];
						board[k][j] = 0;
					}
					else
						break;
				}
			}
		}
	}
}

void down(int** board) {
	for(int j = 0; j < 4; ++j) {
		for(int i = 3; i > 0; --i) {
			for(int k = i-1; k > -1; --k) {
				if(board[k][j] != 0) {
					if(board[i][j] == board[k][j]) {
						board[i][j] += board[k][j];
						board[k][j] = 0;
						break;
					}
					else if(board[i][j] == 0) {
						board[i][j] = board[k][j];
						board[k][j] = 0;
					}
					else
						break;
				}
			}
		}
	}
}

int main(int argc, char * argv[]) {
	srand(12);
	int ** board = new int*[4];
	for(int i = 0; i < 4; ++i) {
		board[i] = new int[4];
		for(int j = 0; j < 4; ++j) {
			board[i][j] = 0;
		}
	}
	add_two(board);
	add_two(board);
	printBoard(board);
	while(true) {
		std::string move;
		std::cin >> move;
		if(move == "r")
			right(board);
		else if(move == "l")
			left(board);
		else if(move == "u")
			up(board);
		else if(move == "d")
			down(board);
		else
			return EXIT_SUCCESS;
		add_two(board);
		printBoard(board);
	}


	return EXIT_SUCCESS;
}