using System;
using System.Linq;
using System.Collections.Generic;
using Poker;


namespace Poker {

public enum PokerHand {
	RSF,
	SF,
	FiveKind,
	HullHouse,
	Flush,
	Straight,
	Tree,
	Two,
	One,				//JackOrBetter, (depends on rule)
	HightCard,
}

public class PokerDeck : Deck {
	public Hand[] results;
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
	
	// constructor	
	public PokerDeck( int players ) : base( players ) {
		Console.WriteLine("PokerDeck init");
		results = new Hand[ players ];
		for( var ii=0; ii< players; ii++ ){
			results[ii]=new Hand();	
		}
	}		
	public void CheckHands() {
		for( var ii=0; ii<mNumPlayers; ii++ )
			this.CheckHandPid(ii);
	}

	///
	public string getHandName( int playerId ) {
		if( this.results[ playerId ].id == (int) IdHAND.HC )	
			return String.Format("{0} , hcard = {1} ", this.results[ playerId ].name, this.results[playerId].id);
		return this.results[ playerId ].name;
	}	
	
	// Num Pair 
	private int NumPair( IEnumerable<int> hand, out int hc1, out int hc2 ) {
		var cnt=0;
		hc1 = 2;
		hc2 = 2;	
		List<int> hc = new List<int>();
		for( var ii=0; ii<13; ii++){
			if( this.NumRank( hand , ii ) == 2 ) {
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


	private void getHightCard( List<int> hand, out int hc1, out int hc2 ) {
		if( hand.Contains(0) ) {
			hc1 = 0;
			hc2 = hand[4];			
			return ;
		} 
		hc1 = hand[4];			
		hc2 = hand[3];			
	}
	
		
	private void CheckHandPid( int playerId ) {
		var hand = this.mPlayerHands[ playerId ];
		int handId = (int)IdHAND.HC;
		var name = HN_HC;
		int hc1, hc2;
		this.getHightCard( hand, out hc1, out hc2 );

		if( this.IsRSF( hand ) ){
			name = HN_RSF;	
			handId = 0;	
		} else if( this.IsStraightFlash( hand, out hc1 ) ) {
			name = HN_SF;	
			handId = 1;
		} else if( this.IsXOfAKind( hand,4, out hc1 ) ) {
			name = HN_FKind;	
			handId = 2;	
		} else if( this.IsFullHouse( hand, out hc1, out hc2 ) ) {
			name = HN_HH;	
			handId = 3;	
		} else if( this.IsFlush( hand )) {
			name = HN_FL;	
			handId = 4;	
		} else if( this.IsStraight( hand, out  hc1 )) {			
			name = HN_ST;	
			handId = 5;	
		} else if( this.IsXOfAKind( hand,3, out hc1 )) {			
			name = HN_THREE;	
			handId = 6;	
		} else if( this.IsTwoPair( hand, out hc1, out hc2 )) {			
			name = HN_TWO;	
			handId = 7;	
		} else if( this.IsOnePair( hand, out hc1,out hc2 )) {			
			name = HN_ONE;	
			handId = 8;	
		} else {
			//get rank list
			var ranks = this.getRanks( hand );
			this.getHightCard( ranks, out hc1, out hc2 );
		}
		this.results[ playerId ].name = name;
		this.results[ playerId ].id= handId;
		this.results[ playerId ].hc1 = hc1;	
		this.results[ playerId ].hc2 = hc2;	
	}	
	
	// num rank
	private int NumRank( IEnumerable<int> hand, int rank  ) {
		var cnt=0;		
		//Console.WriteLine( "NumRank {0}", rank );
		foreach( var cc in hand ) {
		    //Console.WriteLine("card #{0} = {2}{1} ", cc, mCards[cc].rank, mCards[cc].suit);	
			if( mCards[cc].rank == rank ) {
				cnt+=1;	
			}
		}	
		//Console.WriteLine("numRank {0} = {1} ", rank,cnt);	
		return cnt;
	}
	// num suit
	private int NumSuit( IEnumerable<int> hand, string suit ) {
		var cnt=0;
		foreach( var cc in hand )
			if( mCards[cc].suit == suit )
				cnt+=1;	
		return cnt;
	}

	private bool IsRank( IEnumerable<int> hand, int rank) {
		foreach( var cc in hand )
			if( mCards[cc].rank == rank )
				return true;
		return false;
	}

	private bool IsSuit( IEnumerable<int> hand, string suit ) {
		foreach( var cc in hand )
			if( mCards[cc].suit == suit )
				return true;
		return false;
	}

	// Royal Straight Flash
	private bool IsRSF( IEnumerable<int> hand ) {
		int hc1;
		if( !this.IsStraightFlash(hand,  out hc1 ) ) 
			return false;
		// royal
		if( !this.IsRank( hand , 0)  )
			return false;
		foreach( var v in this.royalRanks ){
			if( !this.IsRank(hand,v ) )
				return false;	
		}
		return true;
	}

	// straight Flash
	private bool IsStraightFlash( IEnumerable<int> hand , out int hc1 ) {
		var st = this.IsStraight(hand, out hc1 );
		if( !st )
			return false;
		var fl = this.IsFlush(hand);
		if( !fl )
			return false;
		//var ranks = this.getRanks( hand );
		return true;
	}

	// X Of a Kind 
	private bool IsXOfAKind( IEnumerable<int> hand, int X , out int hc1 ) {
		for( var ii=0; ii<13; ii++){
			if( this.NumRank( hand , ii ) == X ){
			    hc1 = ii;
				return true;
			}
		}
		hc1 = 2;
		return false;
	}

	// FullHouse 
	private bool IsFullHouse( IEnumerable<int> hand, out int hc1, out int hc2 ) {
		int hc3;	
		var tc = this.IsXOfAKind( hand ,3 , out hc1 );
		var op = this.IsOnePair(hand ,out hc2, out hc3 );
		return tc & op;
	}
	
	// Flash
	private bool IsFlush( IEnumerable<int> hand ) {
		foreach( var s in Card.suitDef ){
			if( this.NumSuit( hand , s ) == 5 )
				return true;
		}
		return false;	
	}


	// Straight 
	private List<int>getRanks( IEnumerable<int> hand ) {
		// create rank list
		List<int> ranks = new List<int>();
		foreach( var cc in hand ){
			ranks.Add( mCards[cc].rank );
		}	
		ranks.Sort();
		return ranks;
	}			

	// Straight 
	private bool IsStraight( IEnumerable<int> hand, out int hc1 ) {
		// create rank list
	//	List<int> ranks = new List<int>();
	//	foreach( var cc in hand ){
	//		ranks.Add( mCards[cc].rank );
	//	}
		var ranks = this.getRanks( hand );	
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
	private bool IsTwoPair( IEnumerable<int> hand, out int hc1, out int hc2 ) {
		if( this.NumPair( hand, out hc1, out hc2 ) == 2 ) 
			return true;	
	   	return false;
	}
	
	// One Pair 
	private bool IsOnePair( IEnumerable<int> hand, out int hc1, out int hc2 ) {
		//Console.WriteLine(" Is One Pair? " );
		if( this.NumPair( hand, out hc1, out hc2 ) == 1 ) {
			//Console.WriteLine("Bingo " );
			return true;	
		}
	   	return false;
	}

	public void DebPokerResults() {
		var cnt=0;	
		foreach( var pl in this.mPlayerHands	 ){
			Console.WriteLine( "\nPlayer hand {0} = {1}",cnt , this.results[cnt].name );
			foreach	( var cc in pl ) {
				//Console.WriteLine( "{0}: {1} , {2} ", cc, mCards[cc].suit, mCards[cc].rank );
				Console.Write( " [{0}] ", mCards[cc].getText());
			}	
			//Console.WriteLine( this.getHandName(cnt) );
			Console.Write( "\n{0}  , {1 } \n", this.results[cnt].hc1 , this.results[cnt].hc2 );
			cnt += 1;	
		}
	}

	public void DebCopyHand( int idx, int[] hands){
		List<int> hh = this.mPlayerHands[idx];
		//int[] hands = { 0,11,10,12,9 };	
		for( var ii=0; ii<5; ii++ )
			hh[ii]=hands[ii];
	}

	// build the hands for debug
	public void DebHands() {
		// player 1 
		List<int> hh = this.mPlayerHands[0];
		int[] hands = { 0,11,10,12,9 };	
		for( var ii=0; ii<5; ii++ )
			hh[ii]=hands[ii];
		
		// player 2 
		hh = this.mPlayerHands[1];
		int[] hands2 = { 0,13,26,39,9 };	
		for( var ii=0; ii<5; ii++ )
			hh[ii]=hands2[ii];
			
		// player 3 
		hh = this.mPlayerHands[2];
		int[] hands3 = { 0,13,1,14,27 };	
		for( var ii=0; ii<5; ii++ )
			hh[ii]=hands3[ii];

		// player 4 
		hh = this.mPlayerHands[3];
		int[] hands4 = { 5,18,2 ,31 ,3 };	
		for( var ii=0; ii<5; ii++ )
			hh[ii]=hands4[ii];

		// player 1 
		int[] hands5 = { 13,1,2,3,4 };	
		DebCopyHand( 4, hands5);
	
	}

}



}


