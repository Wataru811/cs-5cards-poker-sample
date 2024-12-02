using System;
using System.Linq;
using System.Collections.Generic;
using Poker;


namespace Poker {

	// ゲームサーバー　
	// 1.ゲーム開始までのセットアップ
	//   ゲームの種類と設定
	//   プレーヤーと並び順 
	//  
	// 2.継続的プレイのための処理
	//    pot 管理 
	//    次のゲーム開始までの受付時間
	// 
	// 

	public class GameTable {
		public static readonly string GTKIND_POKER = "Standard Poker";
		public static readonly string GTKIND_JACKorBETTER= "Jack or Better";
		public static readonly string GTKIND_TEXAS_HOLDEM= "Texas Hold'em";
		public PokerRule mPokerRule = PokerRule.FiveCardDraw;
			
		public int  numPlayer = 0;
		public string status = "";
		private List<Player> mPlayers = new List<Player>();
		// 
		public string chatRoomUID = "";
		public string voiceRoomUID = "";


		// 
		private GameMaster mGM ;

		public GameTable( PokerRule kind){
			mPokerRule = kind;
			Console.WriteLine(kind);
		}

		public void init( string kind){
			mPlayers = new List<Player>();
			mGM = new GameMaster( mPlayers, mPokerRule)	;
		}

		public void addPlayer( string uid, string name, int chip )	 {
			Player pl = new Player( uid, name, chip);
			mPlayers.Add(pl);
			this.numPlayer = mPlayers.Count;
		}

		public bool initGame()	 {
			return true;
		}

		public bool startGame()	 {
			return true;
		}

		public bool updateGame()	 {
			return true;
		}

		public bool devResult()	 {
			mGM.result();
			return true;
		}



	}


}


