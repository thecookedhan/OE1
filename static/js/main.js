// inicjalizacja ikon Lucide przy załadowaniu strony
document.addEventListener('DOMContentLoaded', () => {
    if (window.lucide) {
        lucide.createIcons();
    }
    setupDynamicInputs();
});

let globalHistory = [];

// obsługa dynamicznych pól w formularzu
function setupDynamicInputs() {
    // obsługa Selekcji
    const selectionSelect = document.querySelector('select[name="selection"]');
    const updateSelection = () => {
        const val = selectionSelect?.value;
        const tournamentDiv = document.getElementById('tournament-params');
        const bestDiv = document.getElementById('best-params');
        if (tournamentDiv) tournamentDiv.classList.toggle('hidden', val !== 'tournament');
        if (bestDiv) bestDiv.classList.toggle('hidden', val !== 'best');
    };
    selectionSelect?.addEventListener('change', updateSelection);

    // obsługa Krzyżowania
    const crossoverSelect = document.querySelector('select[name="crossover"]');
    const updateCrossover = () => {
        const val = crossoverSelect?.value;
        const uniformDiv = document.getElementById('uniform-params');
        if (uniformDiv) uniformDiv.classList.toggle('hidden', val !== 'uniform');
    };
    crossoverSelect?.addEventListener('change', updateCrossover);

    // obsługa Mutacji
    const mutationSelect = document.querySelector('select[name="mutation"]');
    const updateMutation = () => {
        const val = mutationSelect?.value;
        const bitFlipDiv = document.getElementById('bit-flip-params');
        if (bitFlipDiv) bitFlipDiv.classList.toggle('hidden', val !== 'bit_flip');
    };
    mutationSelect?.addEventListener('change', updateMutation);

    // obsługa strategii elitarnej (pojawianie się pola pod przełącznikiem)
    const eliteToggle = document.getElementById('elite-toggle');
    const eliteParams = document.getElementById('elite-params');
    const updateElite = () => {
        if (eliteParams && eliteToggle) {
            eliteParams.classList.toggle('hidden', !eliteToggle.checked);
        }
    };
    eliteToggle?.addEventListener('change', updateElite);

    // obsługa operatora inwersji (pojawianie się pola pod przełącznikiem)
    const inversionToggle = document.getElementById('inversion-toggle');
    const inversionParams = document.getElementById('inversion-params');
    const updateInversion = () => {
        if (inversionParams && inversionToggle) {
            inversionParams.classList.toggle('hidden', !inversionToggle.checked);
        }
    };
    inversionToggle?.addEventListener('change', updateInversion);

    // uruchomienie początkowe
    updateSelection();
    updateCrossover();
    updateMutation();
    updateElite();
    updateInversion();
}

// funkcja renderująca wykres
function renderChart(history) {
    const placeholder = document.getElementById('chart-placeholder');
    const plotDiv = document.getElementById('fitnessPlot');
    
    if (placeholder) placeholder.style.display = 'none';
    if (plotDiv) plotDiv.classList.remove('hidden');

    const traces = [
        {
            x: history.map(d => d.epoch),
            y: history.map(d => d.bestFitness),
            name: 'Najlepsze',
            line: { color: '#3b82f6', width: 4, shape: 'spline' },
            type: 'scatter',
            mode: 'lines'
        },
        {
            x: history.map(d => d.epoch),
            y: history.map(d => d.averageFitness),
            name: 'Średnie',
            line: { color: '#ec4899', width: 2.5 },
            type: 'scatter',
            mode: 'lines'
        },
        {
            x: history.map(d => d.epoch),
            y: history.map(d => d.worstFitness),
            name: 'Najgorsze',
            line: { color: '#633e6e', width: 1.5, dash: 'dot' },
            type: 'scatter',
            mode: 'lines',
            opacity: 0.6
        }
    ];

    const layout = {
        height: 480,
        dragmode: 'pan',
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(255,255,255,0.05)', 
        font: { family: 'Poppins, sans-serif', color: '#4b5563', size: 11 },
        margin: { t: 30, r: 30, l: 60, b: 60 },
        hovermode: 'x unified',
        xaxis: { 
            gridcolor: 'rgba(0,0,0,0.05)', 
            title: { text: 'Epoka', font: { size: 12, weight: 600 } },
            zeroline: false,
            rangeslider: { visible: true, thickness: 0.05, bgcolor: 'rgba(255,255,255,0.1)' }
        },
        yaxis: { 
            gridcolor: 'rgba(0,0,0,0.05)', 
            title: { text: 'Wartość Przystosowania', font: { size: 12, weight: 600 } },
            zeroline: false,
            tickformat: '.4f'
        },
        legend: { orientation: 'h', x: 0.5, xanchor: 'center', y: -0.4 }
    };

    Plotly.newPlot('fitnessPlot', traces, layout, { responsive: true, displaylogo: false, locale: 'pl' });
}

// funkcja renderująca tabelę wyników
function renderTable(individual) {
    const section = document.getElementById('results-section');
    const body = document.getElementById('results-table-body');
    const fitnessVal = document.getElementById('final-fitness');

    if (!section || !body) return;

    section.classList.remove('hidden');
    body.innerHTML = '';
    
    fitnessVal.innerText = individual.final_fitness !== undefined ? individual.final_fitness.toFixed(8) : "0.000000";

    individual.variables.forEach((v, idx) => {
        const row = document.createElement('tr');
        row.className = "border-b border-white/10 hover:bg-white/5 transition-colors";
        const label = v.index ? `x${v.index}` : `x${idx + 1}`;
        
        row.innerHTML = `
            <td class="p-4 font-semibold text-gray-700 w-20">${label}</td>
            <td class="p-4">
                <div class="bg-slate-900/5 border border-slate-200/50 p-3 rounded-xl shadow-inner group hover:bg-white/50 transition-all">
                    <code class="text-blue-600 font-mono text-sm leading-relaxed break-all tracking-[0.15em] font-medium">
                        ${v.binary}
                    </code>
                </div>
            </td>
            <td class="p-4 text-right font-mono text-gray-800 font-bold w-32">
                ${v.real.toFixed(6)}
            </td>
        `;
        body.appendChild(row);
    });
}

// główna obsługa formularza
const configForm = document.getElementById('configForm');
if (configForm) {
    configForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const startTime = performance.now();
        const btn = e.target.querySelector('button[type="submit"]');
        const btnText = document.getElementById('btnText');
        const downloadCsvBtn = document.getElementById('download-csv-btn');
        
        btn.disabled = true;
        const originalText = btnText.innerText;
        btnText.innerText = "Obliczanie...";

        const formData = new FormData(e.target);
        const raw = Object.fromEntries(formData.entries());
        
        // konstrukcja paczki JSON dla app.py
        const payload = {
            "main_arguments": {
                "population_size": parseInt(raw.populationSize),
                "number_of_generations": parseInt(raw.numEpochs),
                "bounds": [parseFloat(raw.rangeFrom), parseFloat(raw.rangeTo)],
                "bits_per_variable": parseInt(raw.precision),
                "number_of_variables": parseInt(raw.numVariables),
                "elitism_size": formData.has('eliteStrategy') ? parseInt(raw.eliteSize || 2) : 0,
                "inversion_probability": formData.has('inversion') ? 0.1 : 0.0,
                "max_segment_ratio": parseFloat(raw.maxSegmentRatio || 0.2)
            },
            "selection_arguments": {
                "selection_method": raw.selection,
                "tournament_size": parseInt(raw.tournamentSize || 3),
                "best_percentage": parseFloat(raw.bestPercentage || 0.1)
            },
            "mutation_arguments": {
                "mutation_method": raw.mutation,
                "mutation_probability": parseFloat(raw.mutationProb || 0.05),
                "bit_mutation_rate": parseFloat(raw.bitMutationProb || 0.01)
            },
            "crossover_method": raw.crossover,
            "crossover_probability": parseFloat(raw.crossoverProb || 0.8),
            "uniform_crossover_rate": parseFloat(raw.geneExchangeProb || 0.5)
        };

        try {
            const res = await fetch('/run_algorithm', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const data = await res.json();

            if (!res.ok || !data.success) {
                throw new Error(data.error || "Błąd serwera");
            }

            globalHistory = data.history;
            renderChart(data.history);
            renderTable(data.best_individual);
            
            const duration = data.execution_time || ((performance.now() - startTime) / 1000).toFixed(2);
            document.getElementById('calc-time').innerText = `${duration}s`;
            
            if (downloadCsvBtn) downloadCsvBtn.disabled = false;

        } catch (err) {
            console.error("Błąd połączenia:", err);
            alert(`Błąd: ${err.message}`);
        } finally {
            btn.disabled = false;
            btnText.innerText = originalText;
        }
    });
}

// eksport do CSV
const downloadBtn = document.getElementById('download-csv-btn');
if (downloadBtn) {
    downloadBtn.addEventListener('click', () => {
        if (globalHistory.length === 0) return;
        const headers = 'Epoch,Best Fitness,Average Fitness,Worst Fitness\n';
        const rows = globalHistory.map(h => `${h.epoch},${h.bestFitness},${h.averageFitness},${h.worstFitness}`).join('\n');
        const blob = new Blob([headers + rows], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `wyniki_ga_${new Date().getTime()}.csv`;
        a.click();
        window.URL.revokeObjectURL(url);
    });
}