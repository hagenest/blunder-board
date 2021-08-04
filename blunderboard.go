package main

import (
	"fmt"
	"github.com/notnil/chess"
	"github.com/notnil/chess/uci"
	"math/rand"
	"time"
)

func main() {
	engine, err := uci.New("stockfish")
	if err != nil {
		panic(err)
	}
	defer engine.Close()

	if err := engine.Run(uci.CmdUCI, uci.CmdIsReady, uci.CmdUCINewGame); err != nil {
		panic(err)
	}

	rand.Seed(time.Now().UnixNano())

	// random vs stockfish
	game := chess.NewGame()
	for game.Outcome() == chess.NoOutcome {
		moves := game.ValidMoves()
		game.Move(moves[rand.Intn(len(moves))])

		if err := engine.Run(uci.CmdPosition{Position: game.Position()}, uci.CmdGo{MoveTime: time.Second / 100}); err != nil {
			panic(err)
		}
		game.Move(engine.SearchResults().BestMove)
	}
	fmt.Println(game.String())
	fmt.Println(game.Position().Board().Draw())
}
