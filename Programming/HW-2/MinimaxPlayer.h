/*
 * MinimaxPlayer.h
 *
 *  Created on: Apr 17, 2015
 *      Author: wong
 */

#ifndef MINIMAXPLAYER_H
#define MINIMAXPLAYER_H

#include "OthelloBoard.h"
#include "Player.h"
#include <vector>



struct ActionStateTup{
	float util;
	int row;
	int col;
	OthelloBoard *board;
	ActionStateTup(float u, int r, int c, OthelloBoard *b) : util(u), row(r), col(c), board(b){}
};

/**
 * This class represents an AI player that uses the Minimax algorithm to play the game
 * intelligently.
 */
class MinimaxPlayer : public Player {
public:

	/**
	 * @param symb This is the symbol for the minimax player's pieces
	 */
	MinimaxPlayer(char symb);

	/**
	 * Destructor
	 */
	virtual ~MinimaxPlayer();

	/**
	 * @param b The board object for the current state of the board
	 * @param col Holds the return value for the column of the move
	 * @param row Holds the return value for the row of the move
	 */
    void get_move(OthelloBoard* b, int& col, int& row);

    /**
     * @return A copy of the MinimaxPlayer object
     * This is a virtual copy constructor
     */
    MinimaxPlayer* clone();
	
	ActionStateTup maxValue(ActionStateTup value, char maxPlayer, char minPlayer);
	ActionStateTup minValue(ActionStateTup value, char maxPlayer, char minPlayer);
	std::vector<ActionStateTup> successor(OthelloBoard *board, char player);
	
	float utility(OthelloBoard *b);
	bool terminal_test(OthelloBoard *b);

private:

};


#endif
