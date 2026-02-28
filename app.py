from flask import Flask, render_template, request, jsonify
import time
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# tu będzie działanie algorytmu genetycznego
@app.route('/run_algorithm', methods=['POST'])
def run_algorithm():
    params = request.json
    start_time = time.perf_counter()

    # symulacja pracy algorytmu
    time.sleep(0.5) 

    # mock historii dla wykresu
    mock_history = []
    for i in range(1, 21):
        mock_history.append({
            "epoch": i,
            "bestFitness": 10 / (i + 1), 
            "averageFitness": 12 / (i + 0.5)
        })

    # mock najlepszego osobnika dla tabeli
    mock_best_individual = {
        "fitness": 0.000123,
        "variables": [
            {"index": 1, "binary": "10110101", "real": 2.45},
            {"index": 2, "binary": "00110011", "real": -1.20},
            {"index": 3, "binary": "11100010", "real": 0.89}
        ]
    }

    end_time = time.perf_counter()
    
    # struktura zwracana przez algorytm
    return jsonify({
        "history": mock_history,
        "best_individual": mock_best_individual
    })

if __name__ == "__main__":
    app.run(debug=True)
