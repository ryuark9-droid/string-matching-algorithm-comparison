"""String matching algorithms with simple operation counters for teaching."""
from time import perf_counter


def naive_search(text, pattern):
    hits, comparisons = [], 0
    n, m = len(text), len(pattern)
    for start in range(n - m + 1):
        j = 0
        while j < m:
            comparisons += 1
            if text[start + j] != pattern[j]:
                break
            j += 1
        if j == m:
            hits.append(start)
    return hits, comparisons


def build_lps(pattern):
    lps = [0] * len(pattern)
    length, i = 0, 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length:
            length = lps[length - 1]
        else:
            i += 1
    return lps


def kmp_search(text, pattern):
    hits, comparisons = [], 0
    lps, i, j = build_lps(pattern), 0, 0
    while i < len(text):
        comparisons += 1
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == len(pattern):
                hits.append(i - j)
                j = lps[j - 1]
        elif j:
            j = lps[j - 1]
        else:
            i += 1
    return hits, comparisons


def rabin_karp_search(text, pattern):
    """Rabin–Karp with a rolling hash; verify equal hashes character-by-character."""
    hits, comparisons = [], 0
    n, m = len(text), len(pattern)
    if m > n:
        return hits, comparisons
    base, mod = 256, 1_000_000_007
    high = pow(base, m - 1, mod)
    pattern_hash = window_hash = 0
    for i in range(m):
        pattern_hash = (base * pattern_hash + ord(pattern[i])) % mod
        window_hash = (base * window_hash + ord(text[i])) % mod
    for start in range(n - m + 1):
        if pattern_hash == window_hash:
            j = 0
            while j < m:
                comparisons += 1
                if text[start + j] != pattern[j]:
                    break
                j += 1
            if j == m:
                hits.append(start)
        if start < n - m:
            window_hash = (base * (window_hash - ord(text[start]) * high) + ord(text[start + m])) % mod
    return hits, comparisons


ALGORITHMS = {
    "naive": {"name": "Naive search", "complexity": "O(n · m)", "space": "O(1)", "run": naive_search},
    "kmp": {"name": "Knuth–Morris–Pratt", "complexity": "O(n + m)", "space": "O(m)", "run": kmp_search},
    "rabin_karp": {"name": "Rabin–Karp", "complexity": "Average O(n + m)", "space": "O(1)", "run": rabin_karp_search},
}


def compare_algorithms(text, pattern, selected=None):
    selected = selected or list(ALGORITHMS)
    unknown = set(selected) - set(ALGORITHMS)
    if unknown:
        raise ValueError(f"Unknown algorithm: {', '.join(sorted(unknown))}")
    results = []
    for key in selected:
        algorithm = ALGORITHMS[key]
        started = perf_counter()
        positions, comparisons = algorithm["run"](text, pattern)
        elapsed_ms = (perf_counter() - started) * 1000
        results.append({
            "id": key, "name": algorithm["name"], "complexity": algorithm["complexity"],
            "space": algorithm["space"], "positions": positions,
            "count": len(positions), "comparisons": comparisons,
            "time_ms": round(elapsed_ms, 4),
        })
    return {"text_length": len(text), "pattern_length": len(pattern), "results": results}
