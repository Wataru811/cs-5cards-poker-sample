using System;
using System.Linq;
using System.Diagnostics;

using System.Collections.Generic;
using Poker;

// gameTableから呼ばれる
// 1回のゲームを管理

namespace Poker {

public class Hand {
	public int raking;   // 0 ~ players.length-1
	public string name;
	public int id;       //player id
	public string uid;   // player uid
	public int hc1,hc2;
	public Hand() {
		name = "";
		id = 9;
		hc1 =2;	
		hc2 =2;	
	}
}


public enum PokerRule {
	FiveCardDraw,
	JackOrBetter,
	TexasHoldem,   // 2 draw card & 5 community card
	Omaha,			// 4 draw card & 5 community card  => 2 draw card & 3 community card
}	

public enum Settings{
	BigSmall,

}

public enum IdHAND : int {
	RSF=0, SF, FKIND, HH, FL, ST, THREE, TWO, ONE, HC 
}

public enum inputType{
	bet,       // bet or leave , int 
	holdCards, // bool hc[5]

}

// ゲームサーバー　/ 暫定 FiveCardDraw 用
public class GameMaster{
		public PokerRule mPokerRule = PokerRule.FiveCardDraw;
		public int  mNumPlayer = 0;
		public string mStatus = "";
		public Hand[] mResults;
		private bool mInit = false;
		private List<Player> mPlayers ; 
		private int mode = 0;
		enum TurnMode {  // input wait の種類
			None = 0,
			BetStart,		//BET&カード配る
			Hold,
			Draw,
			Result,

		}

		public GameMaster( List<Player> pls , PokerRule gameKind ){
			mPokerRule = gameKind;
			mPlayers= pls;
			mInit=true;
			mStatus = "init";
			mResults = new Hand[ pls.Count ];
			for( var ii=0; ii< pls.Count; ii++ ){
				mResults[ii]=new Hand();	
			}
		}	

		~GameMaster(){
			Console.WriteLine("GameMaster destructor called.");
		}

		// 
		public void addPlayer( string uid, string name, int chip )	 {
			Player pl = new Player( uid, name, chip);
			mPlayers.Add(pl);
			mNumPlayer = mPlayers.Count;
		}

		// game play algo 
		//  1. deal 5 cards for each players -> initGame() 
		//  2. loop(  player.holdCards() in players  ) -> startGame, updateGame
		//  3. result
		//  
		public bool initGame()	 {
			mInit=true;
			return true;
		}

		public bool startGame()	 {
			Debug.Assert(mInit );

			return true;
		}

		public bool updateGame()	 {
			Debug.Assert(mInit );

			return true;
		}

		public bool result()	 {
			Debug.Assert(mInit );

			return true;
		}


}


}


