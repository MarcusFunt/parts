import optuna
import numpy as np
from threading import Event, Thread
from simulation import Simulation
from geometry import SplineProfile


def default_control_points():
    return [(0.0, 0.0), (0.2, 0.1), (0.4, 0.1), (0.6, 0.0)]


class Optimizer(Thread):
    """Runs Optuna optimization in a background thread."""

    def __init__(self, hardware, targets, bounds, iterations, callback, surface_roughness=False):
        super().__init__()
        self.hardware = hardware
        self.targets = targets
        self.bounds = bounds
        self.iterations = iterations
        self.callback = callback
        self.surface_roughness = surface_roughness
        self.stop_event = Event()
        self.study = optuna.create_study(direction="maximize")

    def objective(self, trial):
        points = []
        for i, (low, high) in enumerate(self.bounds):
            x = trial.suggest_float(f"p{i}x", low[0], high[0])
            y = trial.suggest_float(f"p{i}y", low[1], high[1])
            points.append((x, y))
        sim = Simulation(self.hardware, surface_roughness=self.surface_roughness)
        metrics = sim.run(points)
        score = 0
        for key, weight in self.targets.items():
            score += metrics.get(key, 0) * weight
        if self.callback:
            self.callback(points, metrics, score)
        return score

    def run(self):
        self.study.optimize(self.objective, n_trials=self.iterations, timeout=None, gc_after_trial=True)

    def stop(self):
        self.stop_event.set()
