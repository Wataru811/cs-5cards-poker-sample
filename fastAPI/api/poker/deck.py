"""
1. Card
	definition of trump card.
	1.1 suit,rank
	1.2 one set of ard as array as 'static cards[52]'


2. Deck  
	2.1 shuffle(): random index array for cards[52]
	2.2 deal():  for providing card, using counter ()

	
3. Rule
	- score
	- suit check
	- jack or better


"""


from card import Card
import random

class Deck:
	def __init__(self,players):
		self.mCards =[]
		self.mPlayerHands =[]
		self.mShuffled = []
		self.mCntDeal =0
		mCntDeal =0
		self.mNumPlayers = players	
		self.mPlayerHands = []
		self.mCards= list(range(52))
		print(self.mCards)
		random.shuffle( self.mCards)
		print(self.mCards)
		"""
		mCards = Card[52] 
		var cnt = 0	
		for( var j= 0 j<4 j++ ) :	
			for( var i= 0 i<13 i++ ) :
				mCards[cnt ] = new Card( Card.suitDef[j], Card.rankDef[i])
				cnt+=1	
			}
		}
		"""

	## initialize deck
	def Shuffle(self) :
		self.mShuffled= list(range(52))
		print(self.mShuffled)
		random.shuffle( self.mShuffled)
		print(self.mShuffled)
		"""
		#Random rnd = new Random()
		# clear 
		mShuffled.Clear()
		mCntDeal =0
		mShuffled = new List<int>()
		## create shuffled deck
		int[] arr = Enumerable.Range(0, 52).OrderBy(c => rnd.Next()).ToArray()
		# debug
		Console.WriteLine( "\nShuffled order" )
		foreach( var ii in arr ) :
			mShuffled.Add( ii )	
		}
		#mShuffled.ForEach(i => Console.WriteLine(" :0}", this.cards[shuffled[i]].getText()  ))
		"""	

	## カードを一枚ひく
	def deal(self):
		if self.mCntDeal >= self.mShuffled.Count:
			return None 
		ret = self.mShuffled[ self.mCntDeal]	 
		self.mCntDeal+=1
		return ret

	def idx2card(idx):


	"""
	## hand out num card to each players
	def HandOutSingleCard(self):
		if self.mShuffled.Count < self.mNumPlayers :
			#print("HandOutSingle error, :0} / :1}",mShuffled.Count, mNumPlayers )
			return False
		for ii in range(self.mNumPlayers)  :
			c = self.mShuffled[0]
			self.mPlayerHands[ii].append(c)
			self.mShuffled.RemoveAt(0)
		return True
	
	## hand out num card to each players
	def HandOutCard( int num_card ) :
		# card rest check
		var num = num_card * mNumPlayers
		if mShuffled.Count < num :
			Console.WriteLine("HandOutCard error, :0} / :1}",mShuffled.Count, num  )
			return False
		##	hand out n time
		for var ii = 0  ii<num_card  ii++  :
			this.HandOutSingleCard()	
		return True		

	def DebShowHands() :
		var cnt=0	
		foreach( var pl in mPlayerHands	 ):
			Console.WriteLine( "Player hand "+cnt )
			foreach	( var cc in pl ) :
				Console.WriteLine( ":0}: :1} , :2} ", cc, mCards[cc].suit, mCards[cc].rank )
			cnt += 1	

	"""







