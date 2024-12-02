using System;
using System.Linq;
using System.Collections.Generic;
using Poker;


namespace Poker {


public enum PlayerStatus {
	init,
	waiting,
	playing,
	leaving
}

public class Player {
		public string mUid = "";
		public string mName = "";
		public int mChip = 0;
		public bool mLeaving = false;    //今回のプレーの後離脱したい
		public bool mIsChat = false;
		public bool mIsVoice= false;

		public PlayerStatus mStatus = PlayerStatus.init;
	
	public Player( string uid, string name , int chip) {
		mUid =uid;
		mName=name;
		mChip=chip;
		mStatus = PlayerStatus.waiting; 
	}
}


}


