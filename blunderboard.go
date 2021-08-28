package main

import (
	"fmt"
	"github.com/notnil/chess"
	"github.com/notnil/chess/uci"
	"math"
	"os"
)

// stolen^H^H inspired from lichess https://github.com/ornicar/lila/blob/master/modules/analyse/src/main/Advice.scala#L79
func WinningChance(cp int) float64 {
	winning_chance := 2 / (1 + math.Exp(-0.004 * float64(cp))) - 1
	return winning_chance
}

func main() {
	reader, err := os.Open("spongeboyahoy_vs_tomlx.pgn")
	if err != nil {
		panic(err)
	}
	pgn, err := chess.PGN(reader)
	if err != nil {
		panic(err)
	}
	spongeboyahoy_vs_tomlx := chess.NewGame(pgn)
	fmt.Println(spongeboyahoy_vs_tomlx)

	engine, err := uci.New("stockfish")
	if err != nil {
		panic(err)
	}
	defer engine.Close()

	if err := engine.Run(uci.CmdUCI, uci.CmdIsReady, uci.CmdUCINewGame); err != nil {
		panic(err)
	}

	game := chess.NewGame()
	prevprev_winning_chance := 0.0
	prev_winning_chance := 0.0
	for game.Outcome() == chess.NoOutcome {
		if err := engine.Run(uci.CmdPosition{Position: game.Position()}, uci.CmdGo{Depth: 12}); err != nil {
			panic(err)
		}
		search_results := engine.SearchResults()
		cp := search_results.Info.Score.CP
		winning_chance := WinningChance(cp)
		num_of_moves := len(game.Moves())
		if (num_of_moves > 0) {
			delta := prevprev_winning_chance - winning_chance
			if (num_of_moves % 2 == 0) {
				delta *= -1;
			}
			if delta > 0.3 {
				fmt.Print("B-b-b-blunder!!")
			} else if delta > 0.2 {
				fmt.Print("That was a mistake.")
			} else if delta > 0.1 {
				fmt.Print("Meh...")
			} else {
				fmt.Print("Ok")
			}
			fmt.Printf(" (%0.2f, %0.2f, %0.2f)\n", float64(cp) / 100, winning_chance, -delta)
		}
		prevprev_winning_chance = prev_winning_chance
		prev_winning_chance = winning_chance
//		fmt.Println(game.Position().Board().Draw())
//		fmt.Println("Score (centipawns):", cp, "Winning chance:", winning_chance, "Best Move: ", search_results.BestMove)
//		fmt.Println("Move: ", search_results.BestMove)
		move := spongeboyahoy_vs_tomlx.Moves()[num_of_moves]
		fmt.Print(num_of_moves / 2 + 1, move, "\t")
		if err := game.Move(move); err != nil {
			panic(err)
		}
//		for {
//			var move string
//			fmt.Print("Move: ")
//			fmt.Scanln(&move)
//			if err := game.MoveStr(move); err == nil {
//				break
//			}
//			fmt.Println("Illegal move!")
//		}
	}
	fmt.Println(game.Outcome())
	fmt.Println(game.Position().Board().Draw())
}
