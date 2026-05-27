import statistics
import time
import zlib

from decimal_light_compressor import DecimalLightCompressor
from decimal_light_router_v02 import DecimalLightRouterV2


def medir_ms(fn, repeticiones=5):
    tiempos = []
    out = None
    for _ in range(repeticiones):
        t0 = time.perf_counter()
        out = fn()
        t1 = time.perf_counter()
        tiempos.append((t1 - t0) * 1000)
    return statistics.mean(tiempos), out


def generar_periodica(p, fase, longitud, engine):
    bloque = engine.construir_atlas(p)["canales"]["Alfa"]["bloque_base"]
    return "".join(bloque[(fase + i) % len(bloque)] for i in range(longitud))


def generar_cuasi_periodica(base, paso=997):
    chars = list(base)
    for i in range(0, len(chars), paso):
        chars[i] = "9" if chars[i] != "9" else "8"
    return "".join(chars)


def generar_aleatoria(longitud):
    # determinista para reproducibilidad
    x = 123456789
    out = []
    for _ in range(longitud):
        x = (1103515245 * x + 12345) % (2**31)
        out.append(str(x % 10))
    return "".join(out)


def ratio(packed, original):
    return 100.0 * (1.0 - (packed / original))


def run_case(nombre, s, comp, p):
    b = s.encode("utf-8")
    n = len(b)

    t_dl, dl_res = medir_ms(lambda: comp.comprimir_cadena_decimal(s, p))
    ok_dl = dl_res.get("estado") == "COMPRESION_COHERENTE"
    dl_size = dl_res.get("peso_compreso_b", n)

    t_z, z = medir_ms(lambda: zlib.compress(b, level=6))
    z_size = len(z)

    return {
        "caso": nombre,
        "bytes": n,
        "dl_ok": ok_dl,
        "dl_ms": t_dl,
        "dl_ratio": ratio(dl_size, n),
        "z_ms": t_z,
        "z_ratio": ratio(z_size, n),
    }


if __name__ == "__main__":
    engine = DecimalLightRouterV2()
    comp = DecimalLightCompressor(engine)

    base = generar_periodica(19, fase=5, longitud=200_000, engine=engine)
    casos = [
        ("periodica_limpia", base, 19),
        ("cuasi_periodica_ruido", generar_cuasi_periodica(base), 19),
        ("aleatoria", generar_aleatoria(200_000), 19),
    ]

    print("Benchmark DecimalLight vs Tradicional (zlib)")
    print("caso | bytes | DL_coherente | DL_ms | DL_ratio% | zlib_ms | zlib_ratio%")
    for nombre, data, p in casos:
        r = run_case(nombre, data, comp, p)
        print(
            f"{r['caso']} | {r['bytes']} | {r['dl_ok']} | {r['dl_ms']:.3f} | {r['dl_ratio']:.3f} | {r['z_ms']:.3f} | {r['z_ratio']:.3f}"
        )
