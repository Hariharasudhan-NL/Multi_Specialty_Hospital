import random
import numpy as np

def run_baseline_experiment(n_samples: int = 2000, notification_delay_min: int = 30, notification_delay_max: int = 120, seed: int = 42) -> dict:
    random.seed(seed)
    np.random.seed(seed)
    
    samples = []
    for _ in range(n_samples):
        delay = random.uniform(notification_delay_min, notification_delay_max)
        exit_duration = random.uniform(10, 45)
        cleaning_duration = random.uniform(30, 90)
        total = delay + exit_duration + cleaning_duration
        samples.append(total)
        
    return {
        'system': 'BASELINE',
        'n_samples': n_samples,
        'mean_minutes': float(np.mean(samples)),
        'median_minutes': float(np.median(samples)),
        'p90_minutes': float(np.percentile(samples, 90)),
        'std_minutes': float(np.std(samples)),
        'min_minutes': float(np.min(samples)),
        'max_minutes': float(np.max(samples)),
        'samples': samples
    }
