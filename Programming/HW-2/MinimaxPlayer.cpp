/*
 * MinimaxPlayer.cpp
 *
 *  Created on: Apr 17, 2015
 *      Author: wong
 */
#include <iostream>
#include <assert.h>
#include <cmath>
#include <algorithm>
#include "MinimaxPlayer.h"

using std::vector;
using std::pair;
using std::max;
using std::min;

MinimaxPlayer::MinimaxPlayer(char symb) :
		Player(symb) {

}

MinimaxPlayer::~MinimaxPlayer() {

}
MinimaxPlayer* MinimaxPlayer::clone() {
	MinimaxPlayer* result = new MinimaxPlayer(symbol);
	return result;
}

/*********************************************************************************
	* returns a vector of next possible boards after valid moves by 'player'
**********************************************************************************/
vector<ActionStateTup> MinimaxPlayer::successor(OthelloBoard *board, char player){
	vector<ActionStateTup> succs;

	for(int row = 0; row < board->get_num_rows(); row++){
		for(int col = 0; col < board->get_num_cols(); col++){
			if(board->is_legal_move(col, row, player)){
				OthelloBoard *newB = new OthelloBoard(*board);
				newB->play_move(col, row, player);
				succs.push_back(ActionStateTup(INFINITY, row, col, newB));
			}
		}
	}

	return succs;
}

/*********************************************************************************
	* returns the maximum value that maxPlayer can achieve (i.e most optimal move)
**********************************************************************************/
ActionStateTup MinimaxPlayer::maxValue(ActionStateTup value, char maxPlayer, char minPlayer){
	if(terminal_test(value.board)){
		value.util = utility(value.board);
		return value;
	}
	
	/* get successor states of maxPlayer */	
	vector<ActionStateTup> succs = successor(value.board, maxPlayer);
	vector<ActionStateTup>::iterator itr;

	/* go through all successor states */	
	for(itr = succs.begin(); itr != succs.end(); itr++){
		struct ActionStateTup tmp = minValue(*itr, maxPlayer, minPlayer);
		if(value.util == INFINITY || tmp.util > value.util){
			value.util = tmp.util;
			value.row = itr->row;
			value.col = itr->col;
		}
	}

	return value;
}
/*********************************************************************************
	* returns the minimum value that minPlayer can achieve (i.e most optimal move)
**********************************************************************************/
ActionStateTup MinimaxPlayer::minValue(ActionStateTup value, char maxPlayer, char minPlayer){
	if(terminal_test(value.board)){
		value.util = utility(value.board);
		return value;
	}

	/* get successor states of maxPlayer */	
	vector<ActionStateTup> succs = successor(value.board, minPlayer);
	vector<ActionStateTup>::iterator itr;

	/* go through all successor states */	
	for(itr = succs.begin(); itr != succs.end(); itr++){
		struct ActionStateTup tmp = maxValue(*itr, maxPlayer, minPlayer);
		if(value.util == INFINITY || tmp.util < value.util){
			value.util = tmp.util;
			value.row = itr->row;
			value.col = itr->col;
		}
	}

	return value;
}

/*********************************************************************************
	* sets the computer's next move in arguments 'col' and 'row'
**********************************************************************************/
void MinimaxPlayer::get_move(OthelloBoard *board, int &col, int &row) {
	struct ActionStateTup value(INFINITY, -1, -1, board);
	
	/* see if computer is p1 = MAX or p2 = MIN */
	if(this->get_symbol() == board->get_p1_symbol()){
		value = maxValue(value, this->get_symbol(), board->get_p2_symbol());
	}
	else{
		value = minValue(value, board->get_p1_symbol(), this->get_symbol());
	}

	row = value.row;
	col = value.col;
}
/*********************************************************************************
	* Returns 1 if computer won, 0 if computer lost, and .5 if players tied
**********************************************************************************/
float MinimaxPlayer::utility(OthelloBoard* board){
	int p1Score = board->count_score(board->get_p1_symbol());
	int p2Score = board->count_score(board->get_p2_symbol());

	return p1Score - p2Score;
}
/*********************************************************************************
	* Returns true if computer has no more valid moves 
**********************************************************************************/
bool MinimaxPlayer::terminal_test(OthelloBoard *board){
	return !board->has_legal_moves_remaining(this->get_symbol());
}

