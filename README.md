# cs-5cards-poker-sample
learning cs / 5 card porker deck sample 

## setup 

```dotnetcli

brew install mono

```
https://formulae.brew.sh/formula/mono


### how to run 
```dotnetcli

mcs pokerTest.cs pokerDeck.cs Deck.cs
mono pokerTest.exe
```




## V2

- deck  ５２（＋１）のカード管理
  - shuffle
  - provide a card one by one
  - reset

- rulePoker
  - required deck class
  - rule settings
  - rule
	- getHand( cards[]) , result { hand:<str>, score:<int> ,  cards_order[] }  
	- 

	poker rule
		- Jacks or Better


- gamePoker
	- required: deck, rulePoker class
	- init by 
    	- max players 
    	- rule settings
        	- 
	- add player with chip value
	- status
	- nextTurn



- gameTable
	- players[]
	- pot 
	- jackPot
	- rule.settings
    	- progressive jackpot  : { settings }
        	- pot rate (default 5% total win)
        	- 
    	- 
	- game (gamePoker)
	- connection (api) : user
	- data persistence  (db)
	- chat




```mermaild



```

### Deck




## V1. make and exec

Please see v1/mk.sh





