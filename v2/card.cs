using System;
using System.Linq;
using System.Collections.Generic;
using Poker;

namespace Poker {


public  class Card
{
	// suit 
	public static string SUIT_SPADE = "S";
	public static string SUIT_DIA= "D";
	public static string SUIT_HEART= "H";
	public static string SUIT_CLUB= "C";
	public static string [] suitDef = {"S", "H", "D", "C"};
	public static int [] rankDef= {0,1,2,3,4,5,6,7,8,9,10,11,12 };
	public static string [] rankDefStr= {"A", "2","3","4","5","6","7","8","9","10","J","Q","K" };

	public string suit;
	public int  rank;


	public Card( string s, int r) {
		suit = s;
		rank = r;
	}

	public readonly Dictionary<string, string> mDic1 = new Dictionary<string, string>(){
		{SUIT_SPADE,"♠"},
		{SUIT_DIA,"♦️"},
		{SUIT_HEART,"️❤️"},
		{SUIT_CLUB,"♣"}
	};

// rank
	public const char RANK_A= 'A';
	public const char RANK_2= '2';
	public const char RANK_3= '3';
	public const char RANK_4= '4';
	public const char RANK_5= '5';
	public const char RANK_6= '6';
	public const char RANK_7= '7';
	public const char RANK_8= '8';
	public const char RANK_9= '9';
	public const char RANK_10= 'O';
	public const char RANK_J= 'J';
	public const char RANK_Q= 'Q';
	public const char RANK_K= 'K';
	
	public string getText() {
		return 	this.mDic1[this.suit] +" "+ rankDefStr[this.rank];
	}

}






} //namespace


