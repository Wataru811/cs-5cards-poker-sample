using System;
using System.Linq;
using System.Collections.Generic;
using Poker;

namespace Poker {


public  struct Card
{
	public char suit;
	public int  rank;
}

public class Player {
	public List<int> cards ;
	public Player()	{
	}
}

public class Deck
{
	// card define
	protected Card[] cards;
	protected readonly int[] rankDef = { 0,1,2,3,4,5,6,7,8,9,10,11,12,13 };
	protected readonly char[] suitDef = {'S', 'H', 'D', 'C'};
	
	// play work variables
	protected List<int>[] playerHands;
	List<int> shuffled;
	List<int> opened;
	List<int> dealerHand;
	List<int> discard;
	public int numPlayers;	
	public Deck(int players)
	{
		Console.Write("Deck() init ");
		numPlayers = players;	
		// all card are provided from List.shuffled to each List
		shuffled = new List<int>();
		opened = new List<int>();
		dealerHand = new List<int>();
		discard = new List<int>();
		playerHands = new List<int>[players];
		for( var ii=0; ii<players; ii++)
			playerHands[ii]=new List<int>();
		//defines ( how to replace to const ? )
		//rankDef = new int [] { 2,3,4,5,6,7,8,9,10,11,12,13,1 };
		//rankDef = new int [] { 0,1,2,3,4,5,6,7,8,9,10,11,12,13 };
		//	
		cards = new Card[52]; 
		var cnt = 0;	
		for( var j= 0; j<4; j++ ) {	
			for( var i= 0; i<13; i++ ) {
				cards[ cnt ].suit = suitDef[j];
			   	cards[ cnt ].rank = rankDef[i];
				Console.WriteLine(j +" , " + i + " - " +  cnt);
				cnt+=1;	
			}
		}
	}

	// initialize deck
	public void Shuffle() {
		Random rnd = new Random();
		// clear 
		this.shuffled.Clear();
		this.opened.Clear();
		this.dealerHand.Clear();
		this.discard.Clear();
		foreach( var pl in this.playerHands ) {
			pl.Clear();
		}			
		
		this.shuffled = new List<int>();
		this.playerHands = new List<int>[this.numPlayers];
		for( var ii=0; ii<this.numPlayers; ii++ )
			this.playerHands[ii] = new List<int>();	
		// create shuffled deck
		int[] arr = Enumerable.Range(0, 52).OrderBy(c => rnd.Next()).ToArray();
		// debug
		Console.WriteLine( "\nShuffled order" );
		foreach( var ii in arr ) {
			this.shuffled.Add( ii );	
			Console.WriteLine( ii );
		}
		//this.shuffled.ForEach(i => Console.Write("{0}\t", i));
	}

	// hand out num card to each players
	public bool HandOutSingleCard() {
		if( this.shuffled.Count < this.numPlayers ){
			Console.WriteLine("HandOutSingle error, {0} / {1}",this.shuffled.Count, this.numPlayers );
			return false;
		}
		for( var ii=0; ii<this.numPlayers; ii++) {
			var c = this.shuffled[0];
			Console.WriteLine( "Add  card {0}", c );
			this.playerHands[ii].Add(c);
			this.shuffled.RemoveAt(0);
		}
		return true;
	}
	
	// hand out num card to each players
	public bool HandOutCard( int num_card ) {
		// card rest check
		var num = num_card * this.numPlayers;
		if( this.shuffled.Count < num ){
			Console.WriteLine("HandOutCard error, {0} / {1}",this.shuffled.Count, num  );
			return false;
		}
		//	hand out n time
		for( var ii = 0 ; ii<num_card ; ii++ ) {
			this.HandOutSingleCard();	
		}
		return true;		
	} 

	public void DebShowHands() {
		var cnt=0;	
		foreach( var pl in this.playerHands	 ){
			Console.WriteLine( "Player hand "+cnt );
			foreach	( var cc in pl ) {
				Console.WriteLine( "{0}: {1} , {2} ", cc, this.cards[cc].suit, this.cards[cc].rank );
			}	
			cnt += 1;	
		}
	}
}






} //namespace


