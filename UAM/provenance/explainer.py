import sympy as sp

def explain_derivation(expr):
    """Generate a readable natural-language explanation of a symbolic derivation."""
    free_vars = [str(v) for v in expr.free_symbols]
    return f"Equation derived with respect to variables {free_vars}. Expression: {sp.latex(expr)}"
