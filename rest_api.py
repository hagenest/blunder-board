from flask import Flask, request, jsonify
from stockfish import Stockfish

app = Flask(__name__)

# Replace YOUR_API_TOKEN with the API token you want to use for authentication
API_TOKEN = "blunderboard-security-token"

default_engine_settings = {
    "Debug Log File": "stocklog.txt",
    "Contempt": 0,
    "Min Split Depth": 0,
    "Threads": 2,
    # More threads will make the engine stronger, but should be kept at less than
    # the number of logical processors on your computer.
    "Ponder": "false",
    "Hash": 516,
    # Default size is 16 MB. It's recommended that you increase this value, but keep
    # it as some power of 2. E.g., if you're fine using 2 GB of RAM, set Hash to
    # 2048 (11th power of 2).
    "MultiPV": 1,
    "Skill Level": 20,
    "Move Overhead": 10,
    "Minimum Thinking Time": 5,
    "Slow Mover": 100,
    "UCI_Chess960": "false",
    "UCI_LimitStrength": "false",
    "UCI_Elo": 1350,
    # "NNUE": "true", # TODO Find out if NNUE can be used with the python wrapper
}

# Create a Stockfish chess engine instance
engine = Stockfish(path="/usr/bin/stockfish")

# Set the engine settings
engine.update_engine_parameters(default_engine_settings)


@app.route("/api/get_evaluation", methods=["POST"])
def get_evaluation():
    # Get the API token from the request header
    token = request.headers.get("Authorization")

    # If the API token is not provided or is invalid, return an error
    if token != API_TOKEN:
        return jsonify({"error": "Invalid API token"}), 401

    # Get the current chess position and the desired depth from the request body
    data = request.get_json()
    position = data.get("position")
    depth = data.get("depth")

    # Set the position and search depth in the chess engine
    engine.set_fen_position(position)
    engine.set_depth(depth)

    # Get the evaluation in centipawns
    evaluation = engine.get_evaluation()

    # Return the evaluation to the client
    return evaluation


if __name__ == "__main__":
    app.run(host="")
