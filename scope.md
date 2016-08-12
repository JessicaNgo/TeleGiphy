# Project Name: TeleGiphy (Gipherino?)

##Team Members:
- Jessica Ngo
  - Le [github](https://github.com/JessicaNgo )
  - Le [linkedin](https://ca.linkedin.com/in/ngojessica)
  - Le [facebook](https://www.facebook.com/jessica.ngo.1069)
  - Le biographie: I am an avid doge lover and code writer
- Brian Wu
  - Le [facebook](www.facebook.com/poenbwu)
  - Le [linkedin](www.linkedin.com/poenbrianwu)
  - Le [github](www.github.com/Zizibaluba)
  - Le biographie: 3 serious 5 satire, so I make my own (that no one understands). Wants to be grow up to be an Internet Detective. See also:  Japan-o-phile, foodie, gamer, librarian, and coder.
- Christopher Pourier
  - La [website] (http://corez.nl/) (its outdated and simple af doe)
  - La [linkedin] (https://an.linkedin.com/in/christopher-pourier-81042828)
  - La [github] (https://github.com/corez92)
  - La biografia: Yo soy yo. 
- Adrian Hintermaier
  - Le [github](https://github.com/Mester)
  - Le [linkedin](https://se.linkedin.com/in/adrianhintermaier)
  - Le [facebook](https://www.facebook.com/adrian.hintermaier)
  - Le biographie: 

## Overview
TeleGiphy is based off the icebreaker game, “Telephone”, where an original message is passed along a chain of players through whispers, and is entertaining through the often very distorted message at the end. TeleGiphy is a spin-off of the game that relies on Giphy’s magnificent random-ness when selecting gifs instead of whispers to distort messages. 

## Purpose/Goals
- To create an enjoyable social experience through a simple party game.
- To allow for an asynchronous experience in social contexts.
- Usage of the giphy platform 

## Business Requirements (App features?)
- A user must be able to create an active game where other players may join by a URL link.
- The game will be able to be played asynchronously, with different clients, with the states of the game tracked by the app.
- A UI will be created to abide by the [game flow](https://github.com/JessicaNgo/TeleGiphy/wiki/Game-Flow) and [gameplay](https://github.com/JessicaNgo/TeleGiphy/wiki/Gameplay) as outlined in the wiki.

## Secondary Goals
- Client needs to be able to see other clients within the game, and be directed to the next round/aspect of the game.
- Chat; potentially acts to provide the functionality as above.


## Technology Requirements
- django framework
- [Giphy API](https://github.com/Giphy/GiphyAPI)
- Bootstrap (?)

## TeleGiphy UI
- HOME PAGE
# Create game
# Join game by token

- GAME LOBBY
# Shows game token/link
# Button for GAME START

GAME START: 
randomize order of players, no new players can join now
each turn is 20 seconds? DING sound?
FIRST PLAYER: sees word and makes giphy based off of that
NEXT PLAYER: guesses word off that giphy, makes another giphy
NEXT PLAYER: repeats above steps
. 
.
.
LAST PLAYER: guesses word from giphy, check if word is right, if it is give a giphy trophy.
otherwise, give some funny gif or meme, and then goes to game summary

GAME SUMMARY:
then displays each persons' guess for each turn and a giphy

