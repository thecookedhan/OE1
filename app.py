from flask import Flask, render_template, request, jsonify
import time
import math
import traceback
from genetic_algorithm.ga_core import GeneticAlgorithm

app = Flask(__name__)

# funkcja celu (na razie tylko nasza)
def michalewicz_function(x, m=10):
    total_sum = 0
    n = len(x)
    for i in range(n):
        xi = x[i]
        term1 = math.sin(xi)
        term2 = math.sin(((i + 1) * (xi**2)) / math.pi)
        total_sum += term1 * (term2 ** (2 * m))
    
    return -total_sum

# trasy
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_algorithm', methods=['POST'])
def run_algorithm():
    # pobieramy dane z formularza
    params = request.json
    start_time = time.perf_counter()

    try:
        main_args = params.get('main_arguments', {})
        sel_args = params.get('selection_arguments', {})
        mut_args = params.get('mutation_arguments', {})
        
        num_vars = int(main_args.get('number_of_variables', 2))
        bounds = main_args.get('bounds', [0, 3.1415])
        pop_size = int(main_args.get('population_size', 100))
        epochs = int(main_args.get('number_of_generations', 50))
        precision = int(main_args.get('bits_per_variable', 16))
        elitism_size = int(main_args.get('elitism_size', 0))
        max_seg = float(main_args.get('max_segment_ratio', 0.2)) 

        selection = sel_args.get('selection_method', 'tournament')
        crossover = params.get('crossover_method', 'one_point')
        mutation = mut_args.get('mutation_method', 'bit_flip')
        
        cross_prob = float(params.get('crossover_probability', 0.8))
        mut_prob = float(mut_args.get('mutation_probability', 0.1))

        bit_mut_rate = float(mut_args.get('bit_mutation_rate', 0.01))
        uni_cross_rate = float(params.get('uniform_crossover_rate', 0.5))


        ga = GeneticAlgorithm(
            population_size=pop_size,
            number_of_genertions=epochs,
            fitness_function=michalewicz_function,
            bounds=bounds,
            bits_per_variable=precision,
            number_of_variables=num_vars,
            selection_method=selection,
            crossover_method=crossover,
            mutation_method=mutation,
            elitism_size=elitism_size,
            # parametry specyficzne przekazywane jako dodatkowe argumenty
            tournament_size=int(sel_args.get('tournament_size', 3)),
            best_percentage=float(sel_args.get('best_percentage', 0.1)),
            mutation_probability=mut_prob,
            crossover_probability=cross_prob,
            bit_mutation_rate=bit_mut_rate,
            uniform_crossover_rate=uni_cross_rate,
            max_segment_ratio=max_seg
        )

        # uruchomienie ewolucji
        ga.run()

        # dekodowanie najlepszego osobnika do czytelnej formy
        decoded_vars = ga.best_individual.decode(ga.bounds, ga.bits_per_variable)
        binary_segments = ga.best_individual.split_genome_by_variables(ga.bits_per_variable)
        
        variables_to_front = []
        for i in range(len(decoded_vars)):
            variables_to_front.append({
                "index": i + 1,
                "binary": "".join(map(str, binary_segments[i])),
                "real": decoded_vars[i]
            })

        # przygotowanie historii do wykresu
        history_to_front = []
        for i in range(len(ga.best_fitness_history)):
            history_to_front.append({
                "epoch": i,
                "bestFitness": ga.best_fitness_history[i],
                "averageFitness": ga.average_fitness_history[i] if hasattr(ga, 'average_fitness_history') else ga.median_fitness_history[i],
                "worstFitness": ga.worst_fitness_history[i]
            })

        execution_time = time.perf_counter() - start_time

        # odpowiedź JSON
        return jsonify({
            "success": True,
            "execution_time": round(execution_time, 4),
            "history": history_to_front,
            "best_individual": {
                "final_fitness": ga.best_individual.fitness,
                "variables": variables_to_front
            }
        })

    except Exception as e:
        # błąd w konsoli dla łatwiejszego debugowania
        print("--- BŁĄD PODCZAS URUCHAMIANIA GA ---")
        print(traceback.format_exc())
        return jsonify({
            "success": False, 
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True)