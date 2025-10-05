class RefereeCheckEngine:
    def run(self):
        from referee_verify import referee_verify
        print("⚖️ RefereeCheckEngine evaluating analytical rigor...")
        formulas = [
            {"formula_id": "F1", "expression": "∂u/∂t + u*∂u/∂x = -∂p/∂x + nu*∂²u/∂x²", "source": "Navier–Stokes"},
            {"formula_id": "F2", "expression": "F = -D_A*F^A + j", "source": "Yang–Mills"}
        ]
        derived, _ = FirstPrinciplesDerivationEngine().derive_all(formulas)
        constants = {"C_S": 0.678, "C_L": 1.189207, "gamma": 0.8}
        dataset = {"vorticity": [1.2, 0.8, 1.5]}
        results = referee_verify(derived, constants, dataset)
        for fid, res in results.items():
            print(f"  • {fid}: {res['status']} — {res['reason']}")
        print("✅ Referee checks complete.\n")
