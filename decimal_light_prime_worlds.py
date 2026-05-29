import csv
import math
import time
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path

from decimal_light_router_v02 import DecimalLightRouterV2


@dataclass
class PrimeWorldMetrics:
    prime: int
    periodic_decimal: bool
    period_length: int
    unique_digits: int
    entropy_bits: float
    symmetry_midy: bool
    symmetry_score: float
    localization_score: float
    prediction_score: float


@dataclass
class PrimeBridgeMetrics:
    prime_a: int
    prime_b: int
    period_gcd: int
    period_lcm: int
    period_ratio_similarity: float
    entropy_distance: float
    symmetry_alignment: float
    bridge_score: float


class PrimeWorldAnalyzer:
    """Exploratory analyzer for the first N primes using decimal periodic structure.

    This module is exploratory and computational: it does not claim new mathematics,
    but offers a compact map of repeating-decimal signatures useful for routing,
    verification, localization and prediction experiments.
    """

    def __init__(self, top_n: int = 100):
        self.top_n = top_n
        self.router = DecimalLightRouterV2()

    @staticmethod
    def _generate_primes(n: int):
        primes = []
        candidate = 2
        while len(primes) < n:
            is_prime = True
            limit = int(candidate**0.5)
            for p in primes:
                if p > limit:
                    break
                if candidate % p == 0:
                    is_prime = False
                    break
            if is_prime:
                primes.append(candidate)
            candidate += 1 if candidate == 2 else 2
        return primes

    @staticmethod
    def _digit_entropy(block: str) -> float:
        total = len(block)
        if total == 0:
            return 0.0
        counts = {}
        for ch in block:
            counts[ch] = counts.get(ch, 0) + 1
        entropy = 0.0
        for c in counts.values():
            p = c / total
            entropy -= p * math.log2(p)
        return entropy

    @staticmethod
    def _midy_ok(block: str) -> bool:
        if len(block) % 2 != 0 or len(block) == 0:
            return False
        half = len(block) // 2
        return all(int(block[i]) + int(block[i + half]) == 9 for i in range(half))

    @staticmethod
    def _symmetry_score(block: str) -> float:
        if len(block) < 2:
            return 0.0
        # Circular mirror correlation around midpoint (0..1)
        half = len(block) // 2
        matches = 0
        checks = 0
        for i in range(half):
            checks += 1
            if (int(block[i]) + int(block[(i + half) % len(block)])) % 10 == 9:
                matches += 1
        return matches / checks if checks else 0.0

    @staticmethod
    def _window_prediction_score(block: str, window: int = 12) -> float:
        if len(block) <= window:
            return 0.0
        successes = 0
        total = 0
        for i in range(len(block) - window):
            observed = block[i : i + window]
            target = block[i + window]
            # Deterministic periodic prediction: next char from aligned position
            predicted = block[(i + window) % len(block)]
            successes += int(predicted == target and len(observed) == window)
            total += 1
        return successes / total if total else 0.0

    @staticmethod
    def _localization_score(block: str) -> float:
        # Fraction of unique length-3 trigrams; higher means easier localization of phase
        if len(block) < 3:
            return 0.0
        trigrams = [block[i : i + 3] for i in range(len(block) - 2)]
        return len(set(trigrams)) / len(trigrams)

    def analyze(self):
        metrics = []
        for p in self._generate_primes(self.top_n):
            if p in (2, 5):
                metrics.append(
                    PrimeWorldMetrics(
                        prime=p,
                        periodic_decimal=False,
                        period_length=0,
                        unique_digits=0,
                        entropy_bits=0.0,
                        symmetry_midy=False,
                        symmetry_score=0.0,
                        localization_score=0.0,
                        prediction_score=0.0,
                    )
                )
                continue

            atlas = self.router.construir_atlas(p)
            block = atlas["canales"]["Alfa"]["bloque_base"]
            metrics.append(
                PrimeWorldMetrics(
                    prime=p,
                    periodic_decimal=True,
                    period_length=len(block),
                    unique_digits=len(set(block)),
                    entropy_bits=self._digit_entropy(block),
                    symmetry_midy=self._midy_ok(block),
                    symmetry_score=self._symmetry_score(block),
                    localization_score=self._localization_score(block),
                    prediction_score=self._window_prediction_score(block),
                )
            )
        return metrics

    @staticmethod
    def _pair_bridge(a: PrimeWorldMetrics, b: PrimeWorldMetrics) -> PrimeBridgeMetrics:
        if a.period_length == 0 or b.period_length == 0:
            return PrimeBridgeMetrics(a.prime, b.prime, 0, 0, 0.0, abs(a.entropy_bits - b.entropy_bits), 0.0, 0.0)

        period_gcd = math.gcd(a.period_length, b.period_length)
        period_lcm = (a.period_length * b.period_length) // period_gcd

        longer = max(a.period_length, b.period_length)
        shorter = min(a.period_length, b.period_length)
        period_ratio_similarity = shorter / longer

        entropy_distance = abs(a.entropy_bits - b.entropy_bits)
        symmetry_alignment = 1.0 - abs(a.symmetry_score - b.symmetry_score)

        bridge_score = (
            0.40 * period_ratio_similarity
            + 0.35 * (1.0 / (1.0 + entropy_distance))
            + 0.25 * symmetry_alignment
        )

        return PrimeBridgeMetrics(
            prime_a=a.prime,
            prime_b=b.prime,
            period_gcd=period_gcd,
            period_lcm=period_lcm,
            period_ratio_similarity=period_ratio_similarity,
            entropy_distance=entropy_distance,
            symmetry_alignment=symmetry_alignment,
            bridge_score=bridge_score,
        )

    def analyze_bridges(self, metrics):
        periodic = [m for m in metrics if m.periodic_decimal]
        bridges = []
        for a, b in combinations(periodic, 2):
            bridges.append(self._pair_bridge(a, b))
        bridges.sort(key=lambda x: x.bridge_score, reverse=True)
        return bridges

    def save_bridges_csv(self, path: Path, bridges):
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "prime_a",
                "prime_b",
                "period_gcd",
                "period_lcm",
                "period_ratio_similarity",
                "entropy_distance",
                "symmetry_alignment",
                "bridge_score",
            ])
            for b in bridges:
                writer.writerow([
                    b.prime_a,
                    b.prime_b,
                    b.period_gcd,
                    b.period_lcm,
                    f"{b.period_ratio_similarity:.6f}",
                    f"{b.entropy_distance:.6f}",
                    f"{b.symmetry_alignment:.6f}",
                    f"{b.bridge_score:.6f}",
                ])

    def save_csv(self, path: Path, metrics):
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "prime",
                    "periodic_decimal",
                    "period_length",
                    "unique_digits",
                    "entropy_bits",
                    "symmetry_midy",
                    "symmetry_score",
                    "localization_score",
                    "prediction_score",
                ]
            )
            for m in metrics:
                writer.writerow(
                    [
                        m.prime,
                        int(m.periodic_decimal),
                        m.period_length,
                        m.unique_digits,
                        f"{m.entropy_bits:.6f}",
                        int(m.symmetry_midy),
                        f"{m.symmetry_score:.6f}",
                        f"{m.localization_score:.6f}",
                        f"{m.prediction_score:.6f}",
                    ]
                )


if __name__ == "__main__":
    t0 = time.perf_counter()
    analyzer = PrimeWorldAnalyzer(top_n=100)
    metrics = analyzer.analyze()
    out = Path("results/prime_worlds_v0_1.csv")
    bridges_out = Path("results/prime_bridges_v0_1.csv")
    analyzer.save_csv(out, metrics)
    bridges = analyzer.analyze_bridges(metrics)
    analyzer.save_bridges_csv(bridges_out, bridges)

    best_sym = max(metrics, key=lambda m: m.symmetry_score)
    best_loc = max(metrics, key=lambda m: m.localization_score)
    best_pred = max(metrics, key=lambda m: m.prediction_score)

    print("Prime world analysis completed")
    print(f"- total primes: {len(metrics)}")
    print(f"- best symmetry: p={best_sym.prime} score={best_sym.symmetry_score:.3f}")
    print(f"- best localization: p={best_loc.prime} score={best_loc.localization_score:.3f}")
    print(f"- best prediction: p={best_pred.prime} score={best_pred.prediction_score:.3f}")
    print(f"- csv worlds: {out}")
    if bridges:
        top_bridge = bridges[0]
        print(f"- top bridge: ({top_bridge.prime_a}, {top_bridge.prime_b}) score={top_bridge.bridge_score:.3f}")
    print(f"- csv bridges: {bridges_out}")
    print(f"- elapsed_ms: {(time.perf_counter() - t0) * 1000:.2f}")
