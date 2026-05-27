import math
import random
import time

from decimal_light_router_v02 import DecimalLightRouterV2


class PrimeFingerprintRouter:
    def __init__(self, primes):
        self.engine = DecimalLightRouterV2()
        self.primes = primes
        self.fingerprints = self._build_fingerprints(primes)

    def _build_fingerprints(self, primes):
        fingerprints = {}
        for p in primes:
            atlas = self.engine.construir_atlas(p)
            bloque = atlas["canales"]["Alfa"]["bloque_base"]
            fingerprints[p] = {
                "periodo": len(bloque),
                "bloque": bloque,
                "midy": self._midy_ok(bloque),
            }
        return fingerprints

    @staticmethod
    def _midy_ok(bloque):
        if len(bloque) % 2 != 0:
            return False
        m = len(bloque) // 2
        return all(int(bloque[i]) + int(bloque[i + m]) == 9 for i in range(m))

    def hint(self, ventana, top_k=3):
        cands = []
        for p, fp in self.fingerprints.items():
            b = fp["bloque"]
            best = -1
            best_phase = 0
            for phase in range(len(b)):
                m = 0
                for i, ch in enumerate(ventana):
                    if ch == b[(phase + i) % len(b)]:
                        m += 1
                if m > best:
                    best = m
                    best_phase = phase
            score = best / len(ventana)
            cands.append((score, p, best_phase))
        cands.sort(reverse=True)
        return cands[:top_k]


def generate_case(engine, p, length=200, phase=0, noise=0.0):
    bloque = engine.construir_atlas(p)["canales"]["Alfa"]["bloque_base"]
    s = [bloque[(phase + i) % len(bloque)] for i in range(length)]
    n = int(length * noise)
    idxs = random.sample(range(length), n)
    for idx in idxs:
        s[idx] = str((int(s[idx]) + 1) % 10)
    return "".join(s)


def eval_router():
    random.seed(7)
    primes = [7, 11, 13, 17, 19, 23, 29]
    router = PrimeFingerprintRouter(primes)
    engine = router.engine

    for noise in [0.0, 0.05, 0.1]:
        total = 0
        top1 = 0
        top3 = 0
        t0 = time.perf_counter()
        for p in primes:
            for phase in range(5):
                stream = generate_case(engine, p, length=200, phase=phase, noise=noise)
                hint = router.hint(stream[:24], top_k=3)
                pred = [h[1] for h in hint]
                total += 1
                top1 += int(pred[0] == p)
                top3 += int(p in pred)
        dt = (time.perf_counter() - t0) * 1000
        print(f"noise={noise:.2f} top1={top1/total:.3f} top3={top3/total:.3f} time_ms={dt:.2f}")


if __name__ == "__main__":
    eval_router()
