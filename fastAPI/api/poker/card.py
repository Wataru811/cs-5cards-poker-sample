"""
	#rank
	RANK_A= 'A'
	RANK_2= '2'
	RANK_3= '3'
	RANK_4= '4'
	RANK_5= '5'
	RANK_6= '6'
	RANK_7= '7'
	RANK_8= '8'
	RANK_9= '9'
	RANK_10= 'O'
	RANK_J= 'J'
	RANK_Q= 'Q'
	RANK_K= 'K'
"""
	
class Card:
	# --- class variables ---
	SUIT_SPADE = "S"
	SUIT_DIA= "D"
	SUIT_HEART= "H"
	SUIT_CLUB= "C"
	suitDef = ["S", "H", "D", "C"]
	rankDef= [0,1,2,3,4,5,6,7,8,9,10,11,12 ]
	rankDefStr= ["A", "2","3","4","5","6","7","8","9","10","J","Q","K" ]
	dictMark= {
		SUIT_SPADE:"♠",
		SUIT_DIA:"♦️",
		SUIT_HEART:"️❤️",
		SUIT_CLUB:"♣"
	}
	cardAry = []
	for ss in suitDef:
		for rr in rankDef:
			cardAry.append( {"rank": rr, "suit":ss   })

	# ----------------------------------------------------------
	def __init__( self, s, r) :
		self.suit = s
		self.rank = r

	@staticmethod
	def getText(idx):
		obj = Card.cardAry[idx]
		return 	Card.dictMark[obj["suit"]] +" "+ Card.rankDefStr[obj["rank"]]


	@staticmethod
	def getCard( idx ):
		return Card.cardAry[idx]

	@staticmethod
	def getSuitChar( suit ) :
		return Card.dictMark[suit]
	


