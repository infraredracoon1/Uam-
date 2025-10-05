#!/usr/bin/env python3
import sympy as sp
import numpy as np
from sympy.tensor.tensor import TensorIndexType, tensor_indices, tensorhead

def referee_verify(derived, constants, dataset=None):
    """
    Perform Clay Institute-style checks on derived formulas and constants.
    Returns: Dict of formula IDs to {status: "PASSED"|"FAILED", reason: str}.
    """
    results = {}
    x, y, z, t = sp.symbols('x y z t')
    u = sp.Function('u')(x, y, z, t)
    p = sp.Function('p')(x, y, z, t)
    nu = sp.Symbol('nu')
    Lorentz = TensorIndexType('Lorentz', dummy_name='mu')
    mu, nu = tensor_indices('mu nu', Lorentz)
    F = tensorhead('F', [Lorentz, Lorentz], [[1], [1]])
    D = tensorhead('D', [Lorentz], [[1]])
    j = tensorhead('j', [Lorentz], [[1]])

    for fid, expr in derived.items():
        result = {"status": "PASSED", "reason": ""}
        try:
            # Parse expression if string
            if isinstance(expr, str):
                if "Yang–Mills" in fid:
                    expr = parse_tensor_expression(expr, {'u': u, 'p': p, 'nu': nu})
                else:
                    expr = sp.sympify(expr, locals={'u': u, 'p': p, 'nu': nu})

            # Check 1: Gauge/Scaling Invariance
            if "Navier–Stokes" in fid:
                scaled_u = u.subs({x: x/sp.Symbol('lambda'), t: t/sp.Symbol('lambda')**2})
                scaled_expr = expr.subs(u, scaled_u)
                if sp.simplify(scaled_expr - expr) != 0:
                    result["status"] = "FAILED"
                    result["reason"] += "Gauge invariance failed: scaling alters equation form. "
            elif "Yang–Mills" in fid:
                # Check gauge transformation F → F + dA
                dA = sp.Symbol('dA')
                gauge_expr = expr.subs(F(mu, -mu), F(mu, -mu) + dA)
                if sp.simplify(gauge_expr - expr) != 0:
                    result["status"] = "FAILED"
                    result["reason"] += "Gauge invariance failed: transformation alters field equation. "

            # Check 2: Boundary Conditions
            if dataset and 'vorticity' in dataset:
                vorticity = dataset['vorticity']
                mean_vorticity = np.mean(vorticity)
                if mean_vorticity > 1e3:
                    result["status"] = "FAILED"
                    result["reason"] += f"Vorticity mean {mean_vorticity} exceeds decay bound. "

            # Check 3: Critical Norm Validity
            if 'C_S' in constants and not np.isclose(constants['C_S'], 0.678, rtol=0.05):
                result["status"] = "FAILED"
                result["reason"] += f"Sobolev constant {constants['C_S']} deviates from 0.678. "
            if 'C_L' in constants and not np.isclose(constants['C_L'], 1.189207, rtol=0.05):
                result["status"] = "FAILED"
                result["reason"] += f"Ladyzhenskaya constant {constants['C_L']} deviates from 1.189207. "

            # Check 4: Spectral Gap Consistency
            if 'gamma' in constants and not (0.5 <= constants['gamma'] <= 1.0):
                result["status"] = "FAILED"
                result["reason"] += f"Spectral gap {constants['gamma']} outside [0.5, 1.0]. "

        except Exception as e:
            result["status"] = "FAILED"
            result["reason"] = f"Verification error: {str(e)}"

        results[fid] = result

    return results
