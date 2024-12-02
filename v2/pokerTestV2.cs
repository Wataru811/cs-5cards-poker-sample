using System;
using Poker;

namespace Poker {

	
public class PokerTest 
{
	static public void Main()
	{
		if(false) {	
			PokerDeck deck = new PokerDeck(5);
			deck.Shuffle();
			deck.HandOutCard(5);
			deck.DebHands();
			deck.CheckHands();
			deck.DebPokerResults();
		}	
		
		GameTable mGT = new GameTable( PokerRule.FiveCardDraw );
		mGT.addPlayer( "1", "Player-1",1000);

		//mGT.addPlayer( "2", "Player-2",2000);
		//mGT.addPlayer( "3", "Player-3",3000);
		//mGT.addPlayer( "4", "Player-4",1500);

		mGT.initGame();
		mGT.startGame();
		mGT.updateGame();
	}
}



}
