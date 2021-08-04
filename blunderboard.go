package main

import (
	"fmt"
	"github.com/notnil/chess"
	"github.com/notnil/chess/uci"
	"math"
)

// stolen^H^H inspired from lichess https://github.com/ornicar/lila/blob/master/modules/analyse/src/main/Advice.scala#L79
func WinningChance(cp int) float64 {
	winning_chance := 2 / (1 + math.Exp(-0.004 * float64(cp))) - 1
	return winning_chance
}

func main() {
	engine, err := uci.New("stockfish")
	if err != nil {
		panic(err)
	}
	defer engine.Close()

	if err := engine.Run(uci.CmdUCI, uci.CmdIsReady, uci.CmdUCINewGame); err != nil {
		panic(err)
	}

	game := chess.NewGame()
	for game.Outcome() == chess.NoOutcome {
		if err := engine.Run(uci.CmdPosition{Position: game.Position()}, uci.CmdGo{Depth: 12}); err != nil {
			panic(err)
		}
		search_results := engine.SearchResults()
		fmt.Println("Best Move: ", search_results.BestMove)
		cp := search_results.Info.Score.CP
		fmt.Println("Score (centipawns): ", cp)
		winning_chance := WinningChance(cp)
		fmt.Println("Winning chance: ", winning_chance)
		fmt.Println(game.Position().Board().Draw())
		for {
			var move string
			fmt.Print("Move: ")
			fmt.Scanln(&move)
			if err := game.MoveStr(move); err == nil {
				break
			}
			fmt.Println("Illegal move!")
		}
	}
	fmt.Println(game.Outcome())
	fmt.Println(game.Position().Board().Draw())
}
