from enum import Enum
from .card import Card


class Hand() :
	def __init__(self, cards):
		self.cards = cards
		self.dump=[]
		for cc in cards:
			self.dump.append( Card.getText(cc))

		#for result
		self.name=""
		self.id=""
		self.hc1 = None
		self.hc2 = None

class IdHAND(Enum): 
	RSF=0
	SF=1
	FKIND=2
	HH=3
	FL=4
	ST=5
	THREE=6
	TWO=7
	ONE=8
	HC = 9


class pokerSettings:
	def __init__(self):
		self.maxPlayers=1


# required  class Card
class rulePoker():
	SETTINGS = pokerSettings()
	HN_RSF = "Royal Straight Flash"
	HN_SF = "Straight Flash"
	HN_FKind = "Four Of A Kind"
	HN_HH = "Hull House"
	HN_FL = "Flush"
	HN_ST = "Straight"
	HN_THREE = "Tree Of A Card"
	HN_TWO = "Two Pair"
	HN_ONE = "One Pair"
	HN_HC = "Hight Card"
	ROYAL_RANKS=[ 0,9,10,11,12 ]
	# HN_ARY = [ HN_RSF, HN_SF ]
	cards=[]

	def __init__(self):
		self.hc1 =None
		self.hc2 =None

# 	
	#@staticmethod
	def checkHandPid(self, hand) :
		name = None #rulePoker.HN_HC
		handId = None #IdHAND.HC
		self.hc1 =None
		self.hc2 =None
		result= Hand(hand)
		
		self._getHightCard( hand)  

		if self.IsRSF( hand ) :
			name = rulePoker.HN_RSF	
			handId = IdHAND.RSF	
		elif self.IsStraightFlash( hand )  :
			name = rulePoker.HN_SF	
			handId = IdHAND.SF 
		elif self.IsXOfAKind( hand,4)  :
			name = rulePoker.HN_FKind	
			handId = IdHAND.FKIND
		elif self.IsFullHouse( hand )  :
			name = rulePoker.HN_HH	
			handId = IdHAND.HH
		elif self.IsFlush( hand ) :
			name = rulePoker.HN_FL	
			handId = IdHAND.FL
		elif self.IsStraight( hand ) :			
			name = rulePoker.HN_ST	
			handId = IdHAND.ST
		elif self.IsXOfAKind( hand,3 ) :			
			name = rulePoker.HN_THREE	
			handId = IdHAND.THREE
		elif self.IsTwoPair( hand ) :			
			name = rulePoker.HN_TWO	
			handId = IdHAND.TWO
		elif self.IsOnePair( hand ) :			
			name = rulePoker.HN_ONE	
			handId = IdHAND.ONE
		else :
			#get rank list
			ranks = rulePoker.getRanks( hand )
			self._getHightCard( ranks )
			handId = IdHAND.HC
			name = rulePoker.HN_HC
		
		result.name = name
		result.id= handId
		result.hc1 = self.hc1
		result.hc2 = self.hc2
		"""
		result = {}
		result["name"] = name
		result["id"] = handId
		result["hc1"] = self.hc1	
		result["hc2"] = self.hc2	
		"""
		return result 
	
	@staticmethod
	def setRrulePoker( settings ) :
		rulePoker.SETTINGS =settings

	# Num Pair 
	#@staticmethod
	def _numPair(self, hand) :  # return (h1,h2) 
		cnt=0
		self.hc1 = 2
		self.hc2 = 2	
		hc = []
		for  ii in range(13) :
			if rulePoker._numRank( hand , ii ) == 2  :
				hc.append( ii )
				cnt+=1
		
		if cnt > 0 :
			if cnt > 1 :
				hc.sort()
				if hc[0] == 0 :
					self.hc1 = hc[0]	
					self.hc2 = hc[1]	
				else: 
					self.hc1 = hc[1]	
					self.hc2 = hc[0]	
			else: 
				self.hc1 = hc[0]	
				self.hc2 = -1	
		return cnt	


	#@staticmethod
	def _getHightCard(self, hand ):
		#if hand.Contains(0) :
		if 0 in hand :
			self.hc1 = 0
			self.hc2 = hand[4]			
			return 
		self.hc1 = hand[4]			
		self.hc2 = hand[3]			
	
	
	# num rank
	#@staticmethod
	def _numRank(  hand, rank  ) :
		cnt=0		
		#Console.WriteLine( "_numRank :0", rank )
		for cc in hand  :
			if Card.cardAry[cc]["rank"] == rank  :
				cnt+=1	
		return cnt
	
	# num suit
	@staticmethod
	def NumSuit(  hand, suit ) :
		cnt=0
		for cc in hand :
			if Card.cardAry[cc]["suit"] == suit :
				cnt+=1	
		return cnt
	

	@staticmethod
	def IsRank(  hand, rank) :
		for  cc in hand :
			if Card.cardAry[cc]["rank"] == rank :
				return True
		return False
	

	@staticmethod
	def IsSuit(  hand, suit ) :
		for  cc in hand:
			if Card.cardAry[cc]["suit"] == suit :
				return True
		return False

	# common 
	@staticmethod
	def getRanks( hand ) :
		# create rank list
		ranks = []
		for cc in hand :
			ranks.append( Card.cardAry[cc]["rank"] )
		ranks.sort()
		return ranks

	# Royal Straight Flash
	def IsRSF(  self,hand ) :
		#int hc1
		if not self.IsStraightFlash(hand ): 
			return False
		# royal
		if not rulePoker.IsRank( hand , 0)  :
			return False
		for v in rulePoker.ROYAL_RANKS :
			if not rulePoker.IsRank(hand,v ) :
				return False	
		return True
	

	# straight Flash
	def IsStraightFlash(self,  hand ) :
		st = self.IsStraight(hand )
		if not st :
			return False
		fl = self.IsFlush(hand)
		if not fl :
			return False
		return True
	

	# X Of a Kind 
	def IsXOfAKind(self,  hand, X ) :
		for  ii in range(13):
			if rulePoker._numRank( hand , ii ) == X :
				self.hc1 = ii
				return True
		self.hc1 = 2
		return False
	
	# FullHouse 
	def IsFullHouse(self, hand ) :
		tc = self.IsXOfAKind( hand ,3  )
		op = self.IsOnePair( hand  )
		return tc & op
	
	# Flash
	def IsFlush( self,hand ) :
		for s in Card.suitDef :
			if rulePoker.NumSuit( hand , s ) == 5 :
				return True
		return False	
	
	def IsStraight(self,  hand ) :
		ranks = rulePoker.getRanks( hand )	
		self.hc1 = ranks[0]	
		# check contiuas 5 numbers 
		#if ranks.Contains( 0 ) and ranks.Contains( 12 ) : 
		#if 0 in ranks and 12 in ranks : 
		if 0 in ranks and sum(ranks)==(12+11+10+9) :  # A J Q K 10 のパターン
			ranks.remove(0)
			ranks.append(13)
			ranks.sort()
		# check the continuous 5 digit	
		for ii in range(4):
			if ranks[ii]+ 1 != ranks[ii+1] :
				return False
		return True	

	# Two Pair 
	def IsTwoPair( self,hand ) :
		if self._numPair( hand ) == 2 : 
			return True	
		return False
	
	# One Pair 
	def IsOnePair(self, hand) :
		if self._numPair( hand ) == 1 : 
			return True	
		return False



