import random
import numpy as np

def run_prototype_experiment(n_samples: int = 2000, early_start_probability: float = 0.6, seed: int = 42) -> dict:
    random.seed(seed)
    np.random.seed(seed)
    
    samples = []
    for _ in range(n_samples):
        exit_duration = random.uniform(10, 45)
        cleaning_duration = random.uniform(30, 90)
        
        # Prototype has 0 notification delay
        total = exit_duration + cleaning_duration
        
        # Early start bonus
        if random.random() < early_start_probability:
            bonus = random.uniform(10, 25)
            total -= bonus
            
        samples.append(total)
        
    return {
        'system': 'PROTOTYPE',
        'n_samples': n_samples,
        'mean_minutes': float(np.mean(samples)),
        'median_minutes': float(np.median(samples)),
        'p90_minutes': float(np.percentile(samples, 90)),
        'std_minutes': float(np.std(samples)),
        'min_minutes': float(np.min(samples)),
        'max_minutes': float(np.max(samples)),
        'samples': samples
    }
