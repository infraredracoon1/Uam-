def htfe_compress(data, mse_target=1e-8, max_rank=32):
    """
    Real tensor compression:
      - ≥3D: Tucker/HOSVD with auto-ranks
      - 2D : SVD (energy-based rank selection)
      - 1D : rejected (needs ≥2D)
    Returns (reconstruction, info)
    """
    arr = np.asarray(data, dtype=float)
    if arr.ndim < 2:
        raise ValueError("HTFE requires ≥2D array for compression.")
    info = {}

    def mse(a, b): return float(np.mean((a - b) ** 2))

    if arr.ndim == 2:
        # Energy-based SVD rank selection
        U, S, Vt = np.linalg.svd(arr, full_matrices=False)
        energy = np.cumsum(S**2) / np.sum(S**2)
        r = int(np.searchsorted(energy, 1.0 - mse_target**0.5)) + 1
        r = max(1, min(r, min(arr.shape), max_rank))
        recon = (U[:, :r] @ np.diag(S[:r]) @ Vt[:r, :])
        info = {
            "method": "SVD",
            "rank": r,
            "compression_ratio": float(arr.size / recon.size),
            "fidelity": mse(arr, recon),
        }
        return recon, info

    # ≥3D: Tucker with automatic rank clipping
    import tensorly as tl
    from tensorly.decomposition import tucker
    tl.set_backend("numpy")
    # heuristic ranks: min(max_rank, dim) per mode
    ranks = [min(max_rank, s) for s in arr.shape]
    core, factors = tucker(arr, ranks=ranks, init="svd")
    recon = tl.tucker_to_tensor((core, factors))
    err = mse(arr, recon)

    # If fidelity not met, try smaller rank sweep (coarse)
    if err > mse_target:
        best = (err, recon, ranks)
        for shrink in [24, 16, 12, 8]:
            ranks = [min(shrink, s) for s in arr.shape]
            core, factors = tucker(arr, ranks=ranks, init="svd")
            recon2 = tl.tucker_to_tensor((core, factors))
            e2 = mse(arr, recon2)
            if e2 < best[0]:
                best = (e2, recon2, ranks)
            if e2 <= mse_target:
                recon, err, ranks = recon2, e2, ranks
                break
        else:
            # take best found
            err, recon, ranks = best

    info = {
        "method": "Tucker(HOSVD)",
        "ranks": ranks,
        "compression_ratio": float(arr.size / recon.size),
        "fidelity": err,
    }
    return recon, info
def compress_any(self):
    path = filedialog.askopenfilename(title="Select file to compress")
    if not path: return
    data = Path(path).read_bytes()
    # Try to reshape raw bytes into a 2D tensor (robust default)
    arr = np.frombuffer(data, dtype=np.uint8)
    side = int(np.sqrt(arr.size))
    if side*side < arr.size:
        arr = arr[:side*side]
    arr2d = arr.reshape(side, side)

    recon, info = htfe_compress(arr2d, mse_target=1e-8, max_rank=32)
    self.conn.execute(
        "INSERT INTO compressed_data(path,author,created_at,ratio,fidelity,metadata,algo,ranks_json) "
        "VALUES (?,?,?,?,?,?,?,?)",
        (path, self.user, datetime.datetime.utcnow().isoformat()+"Z",
         info["compression_ratio"], info["fidelity"], json.dumps(_safe_json(info)),
         info.get("method","unknown"), json.dumps(info.get("ranks", [])))
    )
    self.conn.commit()
    self.write_log(f"Compressed '{os.path.basename(path)}' "
                   f"algo={info.get('method')} ratio={info['compression_ratio']:.2f} "
                   f"MSE={info['fidelity']:.2e} ranks={info.get('ranks')}")
    manifest_log("compress_file", info)
def crawl_compression_methods(topic="tensor compression", depth=10):
    """
    Sweep arXiv for modern compression methods:
    TT, CP, Tucker, Quantized TT, Hierarchical Tucker, Low-r
