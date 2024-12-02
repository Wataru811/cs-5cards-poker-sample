using System;
using System.Linq;
using System.Collections.Generic;
using Poker;

namespace Poker {

/*
public class Player {
	public List<int> cards ;
	public Player()	{
	}
} */

public class Deck
{
	protected Card[] mCards;
	protected List<int>[] mPlayerHands;
	List<int> mShuffled;
	public int mNumPlayers;	
	public int mCntDeal;	

	// initilize
	public Deck(int players)
	{
		mCntDeal =0;
		mNumPlayers = players;	
		Console.Write("Deck() init ");
		// all card are provided from List.shuffled to each List
		mShuffled = new List<int>();
		mPlayerHands = new List<int>[players];
		for( var ii=0; ii<players; ii++)
			mPlayerHands[ii]=new List<int>();
		mCards = new Card[52]; 
		var cnt = 0;	
		for( var j= 0; j<4; j++ ) {	
			for( var i= 0; i<13; i++ ) {
				mCards[cnt ] = new Card( Card.suitDef[j], Card.rankDef[i]);
				cnt+=1;	
			}
		}
	}

	// initialize deck
	public void Shuffle() {
		Random rnd = new Random();
		// clear 
		mShuffled.Clear();
		mCntDeal =0;
		mShuffled = new List<int>();
		// create shuffled deck
		int[] arr = Enumerable.Range(0, 52).OrderBy(c => rnd.Next()).ToArray();
		// debug
		Console.WriteLine( "\nShuffled order" );
		foreach( var ii in arr ) {
			mShuffled.Add( ii );	
		}
		//mShuffled.ForEach(i => Console.WriteLine(" {0}", this.cards[shuffled[i]].getText()  ));
	}

	// カードを一枚ひく
	public Card deal(){
		if( mCntDeal >= mShuffled.Count)
			return null;
		Card obj = mCards[ mShuffled[ mCntDeal]	 ] ;
		mCntDeal++;
		return obj;
	}

	// hand out num card to each players
	public bool HandOutSingleCard() {
		if( mShuffled.Count < mNumPlayers ){
			Console.WriteLine("HandOutSingle error, {0} / {1}",mShuffled.Count, mNumPlayers );
			return false;
		}
		for( var ii=0; ii<mNumPlayers; ii++) {
			var c = mShuffled[0];
			mPlayerHands[ii].Add(c);
			mShuffled.RemoveAt(0);
		}
		return true;
	}
	
	// hand out num card to each players
	public bool HandOutCard( int num_card ) {
		// card rest check
		var num = num_card * mNumPlayers;
		if( mShuffled.Count < num ){
			Console.WriteLine("HandOutCard error, {0} / {1}",mShuffled.Count, num  );
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
		foreach( var pl in mPlayerHands	 ){
			Console.WriteLine( "Player hand "+cnt );
			foreach	( var cc in pl ) {
				Console.WriteLine( "{0}: {1} , {2} ", cc, mCards[cc].suit, mCards[cc].rank );
			}	
			cnt += 1;	
		}
	}
}






} //namespace


