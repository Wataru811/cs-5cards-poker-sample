using System;
using Poker;

namespace Poker {

	
public class PokerTest 
{
	static public void Main()
	{
		//Deck deck = new Deck(4);
		PokerDeck deck = new PokerDeck(5);
		deck.Shuffle();
		deck.HandOutCard(5);
		deck.DebHands();
		deck.CheckHands();
		deck.DebPokerResults();
	}
}




}
