import json


class DecimalLightCompressor:
    def __init__(self, router_engine):
        self.router = router_engine

    def comprimir_cadena_decimal(self, cadena_numerica, p):
        """
        Toma una cadena de dígitos y detecta si puede reducirse a una semilla
        relacional en el territorio p.
        """
        mapa = self.router.construir_atlas(p)
        longitud_objetivo = len(cadena_numerica)

        for nombre_canal, datos_canal in mapa["canales"].items():
            bloque_base = datos_canal["bloque_base"]
            long_bloque = len(bloque_base)
            patron_extendido = bloque_base * ((longitud_objetivo // long_bloque) + 2)

            for idx_fase in range(long_bloque):
                candidata = patron_extendido[idx_fase : idx_fase + longitud_objetivo]
                if candidata == cadena_numerica:
                    semilla = {
                        "p": p,
                        "canal": nombre_canal,
                        "fase": idx_fase,
                        "escala_longitud": longitud_objetivo,
                    }
                    peso_original_bytes = len(cadena_numerica.encode("utf-8"))
                    semilla_bytes = json.dumps(semilla, separators=(",", ":")).encode("utf-8")
                    peso_semilla_bytes = len(semilla_bytes)
                    ratio = (1 - (peso_semilla_bytes / peso_original_bytes)) * 100 if peso_original_bytes else 0.0

                    return {
                        "estado": "COMPRESION_COHERENTE",
                        "semilla": semilla,
                        "peso_original_b": peso_original_bytes,
                        "peso_compreso_b": peso_semilla_bytes,
                        "ratio_compresion": f"{ratio:.2f}%",
                    }

        return {"estado": "FLUJO_INCOHERENTE_O_RUIDO"}

    def descomprimir_semilla(self, semilla):
        p = semilla["p"]
        nombre_canal = semilla["canal"]
        idx_fase = semilla["fase"]
        longitud_objetivo = semilla["escala_longitud"]

        mapa = self.router.construir_atlas(p)
        bloque_base = mapa["canales"][nombre_canal]["bloque_base"]

        salida = []
        long_b = len(bloque_base)
        for i in range(longitud_objetivo):
            salida.append(bloque_base[(idx_fase + i) % long_b])
        return "".join(salida)


if __name__ == "__main__":
    from decimal_light_router_v02 import DecimalLightRouterV2

    engine = DecimalLightRouterV2()
    compressor = DecimalLightCompressor(engine)

    print("=" * 75)
    print("DEMO DE COMPRESIÓN ESTRUCTURAL — DECIMALLIGHT COMPRESSOR v0.1")
    print("=" * 75)

    mapa_17 = engine.construir_atlas(17)
    bloque_17 = mapa_17["canales"]["Alfa"]["bloque_base"]
    bloque_rotado = bloque_17[4:] + bloque_17[:4]
    numero_masivo_500 = (bloque_rotado * (500 // len(bloque_rotado) + 1))[:500]

    print(f"\nNúmero Original (Primeros 60 dígitos): {numero_masivo_500[:60]}...")
    print(f"Longitud original: {len(numero_masivo_500)} caracteres.")

    resultado_compresion = compressor.comprimir_cadena_decimal(numero_masivo_500, p=17)

    if resultado_compresion["estado"] == "COMPRESION_COHERENTE":
        print("\n[✓] ¡Compresión Exitosa por Coherencia Relacional!")
        print(f"-> Semilla Generada: {resultado_compresion['semilla']}")
        print(f"-> Peso Original en Memoria: {resultado_compresion['peso_original_b']} bytes")
        print(f"-> Peso de la Semilla ML: {resultado_compresion['peso_compreso_b']} bytes")
        print(f"-> Ahorro en almacenamiento: {resultado_compresion['ratio_compresion']}")

        numero_reconstruido = compressor.descomprimir_semilla(resultado_compresion["semilla"])
        coincide_perfectamente = numero_masivo_500 == numero_reconstruido
        print(f"-> Verificación Lossless: {coincide_perfectamente} (El número coincide bit a bit)")
    else:
        print("\n[✗] Flujo incoherente: no se pudo comprimir el número provisto.")
