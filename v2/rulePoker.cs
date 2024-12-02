using System;
using System.Linq;
using System.Collections.Generic;
using Poker;

//namespace Poker {

	
public class Hand {
	public string name;
	public int id;
	public int hc1,hc2;
	public Hand() {
		name = "";
		id = 9;
		hc1 =2;	
		hc2 =2;	
	}
}

enum IdHAND : int {
	RSF=0, SF, FKIND, HH, FL, ST, THREE, TWO, ONE, HC 
}

public class pokerSettings{
	public int maxPlayers=5;

	// clone
 	public object Clone() {
    	return rulePoker.MemberwiseClone();
    }
}

// required  class Card
public class rulePoker{
	public const pokerSettings settings;
	public const string HN_RSF = "Royal Straight Flash";
	public const string HN_SF = "Straight Flash";
	public const string HN_FKind = "Four Of A Kind";
	public const string HN_HH = "Hull House";
	public const string HN_FL = "Flush";
	public const string HN_ST = "Straight";
	public const string HN_THREE = "Tree Of A Card";
	public const string HN_TWO = "Two Pair";
	public const string HN_ONE = "One Pair";
	public const string HN_HC = "Hight Card";
	private readonly int [] royalRanks={ 0,9,10,11,12 };
	public string [] hnAry = { HN_RSF, HN_SF };		
	
	public rulePoker( pokerSettings settings )  {
		rulePoker.settings=settings;
	}

	public static checkHand( int [] cards ){

	}

	/*
	public string getHandName( int playerId ) {
		if( rulePoker.results[ playerId ].id == (int) IdHAND.HC )	
			return String.Format("{0} , hcard = {1} ", rulePoker.results[ playerId ].name, rulePoker.results[playerId].id);
		return rulePoker.results[ playerId ].name;
	}	
	*/


	// Num Pair 
	private static int NumPair( IEnumerable<int> hand, out int hc1, out int hc2 ) {
		var cnt=0;
		hc1 = 2;
		hc2 = 2;	
		List<int> hc = new List<int>();
		for( var ii=0; ii<13; ii++){
			if( rulePoker.NumRank( hand , ii ) == 2 ) {
				hc.Add( ii );
				cnt+=1;
			}
		}
		if( cnt > 0 ) {
			if( cnt > 1 ) {
				hc.Sort();
				if( hc[0] == 0 ) {
					hc1 = hc[0];	
					hc2 = hc[1];	
				}
				else {
					hc1 = hc[1];	
					hc2 = hc[0];	
				}
			}
			else {
				hc1 = hc[0];	
				hc2 = -1;	
			}	
		}
		return cnt;	
	}


	private static void getHightCard( List<int> hand, out int hc1, out int hc2 ) {
		if( hand.Contains(0) ) {
			hc1 = 0;
			hc2 = hand[4];			
			return ;
		} 
		hc1 = hand[4];			
		hc2 = hand[3];			
	}
	
		
	private void CheckHandPid( int playerId ) {
		var hand = rulePoker.playerHands[ playerId ];
		int handId = (int)IdHAND.HC;
		var name = HN_HC;
		int hc1, hc2;
		rulePoker.getHightCard( hand, out hc1, out hc2 );

		if( rulePoker.IsRSF( hand ) ){
			name = HN_RSF;	
			handId = 0;	
		} else if( rulePoker.IsStraightFlash( hand, out hc1 ) ) {
			name = HN_SF;	
			handId = 1;
		} else if( rulePoker.IsXOfAKind( hand,4, out hc1 ) ) {
			name = HN_FKind;	
			handId = 2;	
		} else if( rulePoker.IsFullHouse( hand, out hc1, out hc2 ) ) {
			name = HN_HH;	
			handId = 3;	
		} else if( rulePoker.IsFlush( hand )) {
			name = HN_FL;	
			handId = 4;	
		} else if( rulePoker.IsStraight( hand, out  hc1 )) {			
			name = HN_ST;	
			handId = 5;	
		} else if( rulePoker.IsXOfAKind( hand,3, out hc1 )) {			
			name = HN_THREE;	
			handId = 6;	
		} else if( rulePoker.IsTwoPair( hand, out hc1, out hc2 )) {			
			name = HN_TWO;	
			handId = 7;	
		} else if( rulePoker.IsOnePair( hand, out hc1,out hc2 )) {			
			name = HN_ONE;	
			handId = 8;	
		} else {
			//get rank list
			var ranks = rulePoker.getRanks( hand );
			rulePoker.getHightCard( ranks, out hc1, out hc2 );
		}
		rulePoker.results[ playerId ].name = name;
		rulePoker.results[ playerId ].id= handId;
		rulePoker.results[ playerId ].hc1 = hc1;	
		rulePoker.results[ playerId ].hc2 = hc2;	
	}	
	
	// num rank
	private static int NumRank( IEnumerable<int> hand, int rank  ) {
		var cnt=0;		
		//Console.WriteLine( "NumRank {0}", rank );
		foreach( var cc in hand ) {
		    //Console.WriteLine("card #{0} = {2}{1} ", cc, rulePoker.cards[cc].rank, rulePoker.cards[cc].suit);	
			if( rulePoker.cards[cc].rank == rank ) {
				cnt+=1;	
			}
		}	
		Console.WriteLine("numRank {0} = {1} ", rank,cnt);	
		return cnt;
	}
	// num suit
	private static int NumSuit( IEnumerable<int> hand, char suit ) {
		var cnt=0;
		foreach( var cc in hand )
			if( rulePoker.cards[cc].suit == suit )
				cnt+=1;	
		return cnt;
	}

	private static bool IsRank( IEnumerable<int> hand, int rank) {
		foreach( var cc in hand )
			if( rulePoker.cards[cc].rank == rank )
				return true;
		return false;
	}

	private static bool IsSuit( IEnumerable<int> hand, char suit ) {
		foreach( var cc in hand )
			if( rulePoker.cards[cc].suit == suit )
				return true;
		return false;
	}

	// Royal Straight Flash
	private static bool IsRSF( IEnumerable<int> hand ) {
		int hc1;
		if( !rulePoker.IsStraightFlash(hand,  out hc1 ) ) 
			return false;
		// royal
		if( !rulePoker.IsRank( hand , 0)  )
			return false;
		foreach( var v in rulePoker.royalRanks ){
			if( !rulePoker.IsRank(hand,v ) )
				return false;	
		}
		return true;
	}

	// straight Flash
	private static bool IsStraightFlash( IEnumerable<int> hand , out int hc1 ) {
		var st = rulePoker.IsStraight(hand, out hc1 );
		if( !st )
			return false;
		var fl = rulePoker.IsFlush(hand);
		if( !fl )
			return false;
		//var ranks = rulePoker.getRanks( hand );
		return true;
	}

	// X Of a Kind 
	private static bool IsXOfAKind( IEnumerable<int> hand, int X , out int hc1 ) {
		for( var ii=0; ii<13; ii++){
			if( rulePoker.NumRank( hand , ii ) == X ){
			    hc1 = ii;
				return true;
			}
		}
		hc1 = 2;
		return false;
	}

	// FullHouse 
	private static bool IsFullHouse( IEnumerable<int> hand, out int hc1, out int hc2 ) {
		int hc3;	
		var tc = rulePoker.IsXOfAKind( hand ,3 , out hc1 );
		var op = rulePoker.IsOnePair(hand ,out hc2, out hc3 );
		return tc & op;
	}
	
	// Flash
	private static bool IsFlush( IEnumerable<int> hand ) {
		foreach( var s in rulePoker.suitDef ){
			if( rulePoker.NumSuit( hand , s ) == 5 )
				return true;
		}
		return false;	
	}


	// Straight 
	private static List<int> getRanks( IEnumerable<int> hand ) {
		// create rank list
		List<int> ranks = new List<int>();
		foreach( var cc in hand ){
			ranks.Add( rulePoker.cards[cc].rank );
		}	
		ranks.Sort();
		return ranks;
	}			

	// Straight 
	private static bool IsStraight( IEnumerable<int> hand, out int hc1 ) {
		// create rank list
	//	List<int> ranks = new List<int>();
	//	foreach( var cc in hand ){
	//		ranks.Add( rulePoker.cards[cc].rank );
	//	}
		var ranks = rulePoker.getRanks( hand );	
		hc1 = ranks[0];	
		// check contiuas 5 numbers 
		if( ranks.Contains( 0 ) & ranks.Contains( 12 )  ) {
			ranks.Remove(0);
			ranks.Add(13);
			ranks.Sort();
		}
		// check the continuous 5 digit	
		for( var ii=0; ii<4 ; ii++ ){
			if( ranks[ii]+ 1 != ranks[ii+1])
				return false;
		}
		return true;	
	}

	// Two Pair 
	private static bool IsTwoPair( IEnumerable<int> hand, out int hc1, out int hc2 ) {
		if( rulePoker.NumPair( hand, out hc1, out hc2 ) == 2 ) 
			return true;	
	   	return false;
	}
	
	// One Pair 
	private static bool IsOnePair( IEnumerable<int> hand, out int hc1, out int hc2 ) {
		Console.WriteLine(" Is One Pair? " );
		if( rulePoker.NumPair( hand, out hc1, out hc2 ) == 1 ) {
			Console.WriteLine("Bingo " );
			return true;	
		}
	   	return false;
	}

	/*
	public void DebPokerResults() {
		var cnt=0;	
		foreach( var pl in rulePoker.playerHands	 ){
			Console.WriteLine( "\nPlayer hand "+cnt );

			foreach	( var cc in pl ) {
				Console.WriteLine( "{0}: {1} , {2} ", cc, rulePoker.cards[cc].suit, rulePoker.cards[cc].rank );
			}	
			//Console.WriteLine( rulePoker.getHandName(cnt) );
			Console.WriteLine( rulePoker.results[cnt].name );
			Console.WriteLine( rulePoker.results[cnt].hc1 );
			Console.WriteLine( rulePoker.results[cnt].hc2 );
			cnt += 1;	
		}
	}
	*/


	/*
	// build the hands for debug
	public void DebHands() {
		// player 1 
		List<int> hh = rulePoker.playerHands[0];
		int[] hands = { 0,11,10,12,9 };	
		for( var ii=0; ii<5; ii++ )
			hh[ii]=hands[ii];
		
		// player 2 
		hh = rulePoker.playerHands[1];
		int[] hands2 = { 0,13,26,39,9 };	
		for( var ii=0; ii<5; ii++ )
			hh[ii]=hands2[ii];
			
		// player 3 
		hh = rulePoker.playerHands[2];
		int[] hands3 = { 0,13,1,14,27 };	
		for( var ii=0; ii<5; ii++ )
			hh[ii]=hands3[ii];

		// player 4 
		hh = rulePoker.playerHands[3];
		int[] hands4 = { 5,18,2 ,31 ,3 };	
		for( var ii=0; ii<5; ii++ )
			hh[ii]=hands4[ii];
	}
	*/

}

//}