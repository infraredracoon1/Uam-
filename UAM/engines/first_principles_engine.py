import sympy as sp
from ..provenance.registry import add_equation, log_failure
from ..provenance.explainer import explain_derivation

def run_first_principles_engine():
    try:
        u, nu, grad_u = sp.symbols('u nu grad_u')
        energy_eq = sp.Eq(sp.Derivative(u, 't'), -u*grad_u - sp.Symbol('grad(p)') + nu*sp.Symbol('Δu'))
        add_equation(
            name="Navier-Stokes Momentum Eq.",
            expression=energy_eq,
            variables=["u", "nu", "grad_u"],
            derivation="First principles from conservation of momentum and incompressibility.",
            explanation=explain_derivation(energy_eq)
        )
        print("First Principles Engine: core PDE registered.")
    except Exception as e:
        log_failure("First Principles Engine", str(e), "Symbolic derivation error.")
