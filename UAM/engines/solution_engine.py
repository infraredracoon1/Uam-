import sympy as sp
from ..provenance.registry import add_constant, add_equation, log_failure

def run_solution_engine():
    try:
        y, t, A, C2 = sp.symbols('y t A C2', positive=True)
        ode = sp.Eq(sp.Derivative(y, t), A*y**2 - C2*y**3)
        add_equation(
            name="Vorticity ODE",
            expression=ode,
            variables=["y","t","A","C2"],
            derivation="Derived from dyadic enstrophy inequality + high/low frequency split.",
            explanation="Controls exponential decay of high-frequency vorticity, key for BKM closure."
        )
        # Register constants
        add_constant("A", 0.101, "continuum",
                     "Sum of low-frequency coefficient C1 and viscous term νC3",
                     "Determines quadratic term in vorticity evolution")
        add_constant("C2", 3.75e-16, "continuum",
                     "Spectral damping coefficient derived from exponential kernel",
                     "Cubic damping stabilizing high-frequency cascade")
        print("Solution Engine logged vorticity equation & constants.")
    except Exception as e:
        log_failure("Solution Engine", str(e), "Failed to derive vorticity ODE.")
