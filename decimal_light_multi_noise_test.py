from decimal_light_compressor import DecimalLightCompressor
from decimal_light_noise_test import localizar_ruido, reparar_cadena
from decimal_light_router_v02 import DecimalLightRouterV2


def generar_cadena(bloque, fase, longitud):
    """Genera una cadena coherente aplicando un patrón circular."""
    return "".join(bloque[(fase + i) % len(bloque)] for i in range(longitud))


def corromper_cadena(cadena, posiciones):
    """Corrompe una cadena cambiando un dígito en cada posición indicada."""
    caracteres = list(cadena)
    cambios = []

    for pos in posiciones:
        original = caracteres[pos]
        nuevo = "9" if original != "9" else "8"
        caracteres[pos] = nuevo
        cambios.append({"posicion": pos, "original": original, "corrupto": nuevo})

    return "".join(caracteres), cambios


def ejecutar_caso(p, longitud, fase, posiciones_corruptas):
    engine = DecimalLightRouterV2()
    compressor = DecimalLightCompressor(engine)

    mapa = engine.construir_atlas(p)
    bloque = mapa["canales"]["Alfa"]["bloque_base"]

    cadena_original = generar_cadena(bloque, fase, longitud)

    resultado_original = compressor.comprimir_cadena_decimal(cadena_original, p)
    compresion_original_ok = resultado_original["estado"] == "COMPRESION_COHERENTE"

    cadena_corrupta, _cambios = corromper_cadena(cadena_original, posiciones_corruptas)
    resultado_corrupta = compressor.comprimir_cadena_decimal(cadena_corrupta, p)
    corrupta_detectada = resultado_corrupta["estado"] == "FLUJO_INCOHERENTE_O_RUIDO"

    diagnostico = localizar_ruido(cadena_corrupta, bloque)
    fase_probable = diagnostico["fase_probable"]
    posiciones_detectadas = [e["posicion"] for e in diagnostico["errores"]]
    errores_detectados = diagnostico["numero_errores"]

    cadena_reparada = reparar_cadena(cadena_corrupta, bloque, fase_probable)
    reparacion_exacta = cadena_reparada == cadena_original

    resultado_reparada = compressor.comprimir_cadena_decimal(cadena_reparada, p)
    recompresion_ok = resultado_reparada["estado"] == "COMPRESION_COHERENTE"

    estado_final = all(
        [
            compresion_original_ok,
            corrupta_detectada,
            reparacion_exacta,
            recompresion_ok,
            sorted(posiciones_detectadas) == sorted(posiciones_corruptas),
        ]
    )

    return {
        "p": p,
        "longitud": longitud,
        "fase": fase,
        "posiciones_corruptas": posiciones_corruptas,
        "posiciones_detectadas": posiciones_detectadas,
        "errores_detectados": errores_detectados,
        "compresion_original_ok": compresion_original_ok,
        "corrupta_detectada": corrupta_detectada,
        "reparacion_exacta": reparacion_exacta,
        "recompresion_ok": recompresion_ok,
        "estado_final": "OK" if estado_final else "FAIL",
    }


if __name__ == "__main__":
    casos = [
        {"p": 7, "longitud": 300, "fase": 0, "posiciones": [13]},
        {"p": 13, "longitud": 500, "fase": 2, "posiciones": [99, 101]},
        {"p": 17, "longitud": 500, "fase": 4, "posiciones": [137]},
        {"p": 19, "longitud": 800, "fase": 5, "posiciones": [10, 200, 399, 777]},
        {"p": 7, "longitud": 1000, "fase": 3, "posiciones": [100, 101, 102, 103, 104]},
    ]

    print("DecimalLight Multi Noise Test\n")
    print("p | longitud | fase | errores_inyectados | errores_detectados | reparacion | estado")

    resultados = []
    for caso in casos:
        res = ejecutar_caso(caso["p"], caso["longitud"], caso["fase"], caso["posiciones"])
        resultados.append(res)
        reparacion = "OK" if res["reparacion_exacta"] else "FAIL"
        print(
            f"{res['p']} | {res['longitud']} | {res['fase']} | "
            f"{len(res['posiciones_corruptas'])} | {res['errores_detectados']} | {reparacion} | {res['estado_final']}"
        )

    fallos = [r for r in resultados if r["estado_final"] != "OK"]
    if fallos:
        raise SystemExit(f"Fallaron {len(fallos)} casos en DecimalLight multi-noise test: {fallos}")
