from decimal_light_compressor import DecimalLightCompressor
from decimal_light_router_v02 import DecimalLightRouterV2


def localizar_ruido(cadena, bloque_base):
    """
    Evalúa todas las fases posibles del bloque_base contra la cadena.
    Retorna la fase con menor número de errores y el detalle de discrepancias.
    """
    mejor = None
    long_b = len(bloque_base)

    for fase in range(long_b):
        errores = []
        for i, observado in enumerate(cadena):
            esperado = bloque_base[(fase + i) % long_b]
            if observado != esperado:
                errores.append(
                    {
                        "posicion": i,
                        "esperado": esperado,
                        "observado": observado,
                    }
                )

        candidato = {
            "fase_probable": fase,
            "numero_errores": len(errores),
            "errores": errores,
        }

        if mejor is None or candidato["numero_errores"] < mejor["numero_errores"]:
            mejor = candidato

    return mejor


def reparar_cadena(cadena, bloque_base, fase):
    """Reconstruye la cadena esperada completa según el patrón y fase detectada."""
    long_b = len(bloque_base)
    reconstruida = []
    for i in range(len(cadena)):
        reconstruida.append(bloque_base[(fase + i) % long_b])
    return "".join(reconstruida)


if __name__ == "__main__":
    engine = DecimalLightRouterV2()
    compressor = DecimalLightCompressor(engine)

    p = 17
    longitud = 500
    fase_original = 4
    posicion_corrupta = 137

    mapa = engine.construir_atlas(p)
    bloque = mapa["canales"]["Alfa"]["bloque_base"]

    cadena_original = "".join(
        bloque[(fase_original + i) % len(bloque)] for i in range(longitud)
    )

    res_original = compressor.comprimir_cadena_decimal(cadena_original, p)
    compresion_original_ok = res_original["estado"] == "COMPRESION_COHERENTE"
    descompresion_original_ok = False
    if compresion_original_ok:
        reconstruida = compressor.descomprimir_semilla(res_original["semilla"])
        descompresion_original_ok = reconstruida == cadena_original

    lista_corrupta = list(cadena_original)
    original_en_pos = lista_corrupta[posicion_corrupta]
    lista_corrupta[posicion_corrupta] = "9" if original_en_pos != "9" else "8"
    corrupto_en_pos = lista_corrupta[posicion_corrupta]
    cadena_corrupta = "".join(lista_corrupta)

    res_corrupta = compressor.comprimir_cadena_decimal(cadena_corrupta, p)

    diagnostico = localizar_ruido(cadena_corrupta, bloque)
    fase_probable = diagnostico["fase_probable"]
    errores = diagnostico["errores"]
    posiciones = [e["posicion"] for e in errores]

    cadena_reparada = reparar_cadena(cadena_corrupta, bloque, fase_probable)
    reparacion_exacta = cadena_reparada == cadena_original

    res_reparada = compressor.comprimir_cadena_decimal(cadena_reparada, p)
    recompresion_reparada_ok = res_reparada["estado"] == "COMPRESION_COHERENTE"

    posicion_detectada_ok = posicion_corrupta in posiciones

    print("DecimalLight Noise Test")
    print(f"p={p}")
    print(f"longitud={longitud}")
    print(f"fase_original={fase_original}")
    print(f"posicion_corrupta={posicion_corrupta}")
    print(f"original={original_en_pos}")
    print(f"corrupto={corrupto_en_pos}")
    print()
    print(f"Compresion original: {'OK' if compresion_original_ok and descompresion_original_ok else 'FAIL'}")
    print(f"Compresion corrupta: {res_corrupta['estado']}")
    print(f"Errores detectados: {diagnostico['numero_errores']}")
    print(f"Posiciones: {posiciones}")
    print(f"Reparacion exacta: {reparacion_exacta}")
    print(f"Recompresion reparada: {'OK' if recompresion_reparada_ok else 'FAIL'}")

    if not (compresion_original_ok and descompresion_original_ok):
        raise SystemExit("Fallo: la cadena original no comprimió/descomprimió correctamente")
    if res_corrupta["estado"] != "FLUJO_INCOHERENTE_O_RUIDO":
        raise SystemExit("Fallo: la cadena corrupta no fue detectada como ruido")
    if not posicion_detectada_ok:
        raise SystemExit("Fallo: no se detectó la posición corrupta esperada")
    if not reparacion_exacta:
        raise SystemExit("Fallo: la reparación no reconstruyó la cadena original")
    if not recompresion_reparada_ok:
        raise SystemExit("Fallo: la cadena reparada no recomprime correctamente")
