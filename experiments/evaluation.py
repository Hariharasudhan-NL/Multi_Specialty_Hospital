import os
import json
import pandas as pd
from datetime import datetime
from baseline_experiment import run_baseline_experiment
from prototype_experiment import run_prototype_experiment

def run_full_evaluation(target_improvement_pct: float = 20.0) -> dict:
    baseline = run_baseline_experiment(n_samples=2000)
    prototype = run_prototype_experiment(n_samples=2000)
    
    improvement = baseline['mean_minutes'] - prototype['mean_minutes']
    improvement_pct = (improvement / baseline['mean_minutes']) * 100
    target_achieved = improvement_pct >= target_improvement_pct
    
    result = {
        'baseline': {k: v for k, v in baseline.items() if k != 'samples'},
        'prototype': {k: v for k, v in prototype.items() if k != 'samples'},
        'absolute_improvement_mean': improvement,
        'percentage_improvement': improvement_pct,
        'target_percentage': target_improvement_pct,
        'target_achieved': bool(target_achieved),
        'target_assessment': 'TARGET ACHIEVED' if target_achieved else 'TARGET NOT ACHIEVED',
        'median_improvement': baseline['median_minutes'] - prototype['median_minutes'],
        'p90_improvement': baseline['p90_minutes'] - prototype['p90_minutes'],
        'evaluated_at': datetime.now().isoformat(),
    }
    
    # Save to results/
    os.makedirs('results', exist_ok=True)
    with open('results/evaluation_report.json', 'w') as f:
        json.dump(result, f, indent=2)
    
    # Flatten nested dicts for CSV
    csv_rows = []
    for k, v in result.items():
        if isinstance(v, dict):
            for sub_k, sub_v in v.items():
                csv_rows.append({'metric': f"{k}_{sub_k}", 'value': sub_v})
        elif isinstance(v, (int, float, str, bool)):
            csv_rows.append({'metric': k, 'value': v})
            
    df = pd.DataFrame(csv_rows)
    df.to_csv('results/evaluation_report.csv', index=False)
    print("Evaluation completed. Reports saved to results/")
    
    return result

if __name__ == '__main__':
    run_full_evaluation()
