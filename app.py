from flask import Flask, render_template, request
from main import solve

app = Flask(__name__)


@app.route('/')
def index():
    puzzle = (request.args.get("a", "") +
              request.args.get("b", "") +
              request.args.get("c", "") +
              request.args.get("d", ""))

    if len(puzzle) != 12 or not puzzle.isalpha() or len(set(puzzle)) != 12:
        return render_template("index.html", solution="Incorrect input", request_args=request.args)

    puzzle = list(puzzle)
    box = [
        puzzle[:3],
        puzzle[3:6], puzzle[6:9],
        puzzle[9:12]
    ]
    solution = solve(box)
    if not solution:
        solution = "No solution."
    else:
        solution = ", ".join(solve(box))
    return render_template("index.html", solution=solution, request_args=request.args)
