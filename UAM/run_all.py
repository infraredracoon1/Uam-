from UAM.engines.solution_engine import run_solution_engine
from UAM.engines.referee_engine import run_referee_engine
from UAM.engines.first_principles_engine import run_first_principles_engine

def run_all_engines():
    print("=== UAM Engine Sweep Starting ===")
    run_first_principles_engine()
    run_solution_engine()
    run_referee_engine()
    print("=== UAM Sweep Complete. Check UAM_provenance.db ===")

if __name__ == "__main__":
    run_all_engines()
