from flask import Flask, render_template, request, jsonify
import time
from genetic_algorithm.ga_core import GeneticAlgorithm

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
            "averageFitness": 12 / (i + 0.5),
            "worstFitness": 16 / (i + 0.4)
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

    try:
        ga = GeneticAlgorithm(...)
        ga.run()
        success = True

    except Exception as e:
        success = False
        error_message = str(e)

    end_time = time.perf_counter()
    execution_time = end_time - start_time

    decoded_variables = ga.best_individual.decode(ga.bounds, ga.bits_per_variable)
    binary_variables = ga.best_individual.split_genome_by_variables(ga.bits_per_variable)
    variables = []

    for i, _ in enumerate(binary_variables):
        variables.append({
            "id": f"x{i+1}",
            "binary": ''.join(map(str, binary_variables)),
            "real": decoded_variables[i]
    })

    result = {
        "success": success,
        "execution_time": execution_time,
        "history": {
            "epochs": ga.epochs,
            "best_fitness": ga.best_fitness_history,
            "worst_fitness": ga.worst_fitness_history,
            "avg_fitness": ga.median_fitness_history
        },
        "best_individual": {
            "final_fitness": ga.best_individual.fitness,
            "variables": variables
        }
    }
    
    # struktura zwracana przez algorytm
    return jsonify({
        "history": mock_history,
        "best_individual": mock_best_individual
    })

if __name__ == "__main__":
    app.run(debug=True)
