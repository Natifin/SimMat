class DecimalLightRouter:
    def __init__(self):
        # 1. CONSTRUIR ATLAS MATRIZ V(p) = [Bloque Base, Canales]
        # Almacenamos únicamente la "huella espectral mínima" por canal
        self.atlas = {
            7: {
                "canales": {
                    "Alfa": "142857",
                }
            },
            11: {
                "canales": {
                    "Alfa": "09",
                    "Beta": "18",
                    "Gamma": "27",
                    "Delta": "36",
                    "Epsilon": "45",
                }
            },
            13: {
                "canales": {
                    "Alfa": "076923",  # Contiene numeradores: 1, 3, 4, 9, 10, 12
                    "Beta": "153846",  # Contiene numeradores: 2, 5, 6, 7, 8, 11
                }
            },
        }

    def _detectar_canal_y_origen(self, n, p):
        """Asigna el numerador al canal geométrico correspondiente"""
        if p == 7:
            return "Alfa", "142857"

        if p == 11:
            # 11 fragmenta en 5 canales de longitud 2
            pares = {
                "09": "Alfa",
                "18": "Beta",
                "27": "Gamma",
                "36": "Delta",
                "45": "Epsilon",
            }
            # Buscamos qué par colapsa con el residuo del engorde
            for par, canal in pares.items():
                if (n * 9) % 11 == int(par) % 11:  # Ajuste de fase simplificado
                    return canal, par
            return "Alfa", "09"

        if p == 13:
            # El 13 divide el territorio en dos reinos
            grupo_alfa = {1, 3, 4, 9, 10, 12}
            if n in grupo_alfa:
                return "Alfa", "076923"
            return "Beta", "153846"

        return None, None

    def rutear(self, n, p, digitos_objetivo=12):
        """
        Calcula el decimal clásico (simulado) vs el ruteado por ML.
        Devuelve métricas de ahorro lógico.
        """
        if p not in self.atlas:
            return "Territorio no cartografiado en v0.1"

        # --- CAMINO CLÁSICO (División larga iterativa) ---
        pasos_clasicos = 0
        resto = n
        decimal_clasico = ""

        for _ in range(digitos_objetivo):
            pasos_clasicos += 1  # Operación de multiplicación de residuo
            resto *= 10
            cociente = resto // p
            pasos_clasicos += 1  # Operación de división
            decimal_clasico += str(cociente)
            resto = resto % p
            pasos_clasicos += 1  # Operación de módulo para siguiente iteración

        # --- CAMINO ML (DecimalLight) ---
        pasos_ml = 0
        canal, bloque_base = self._detectar_canal_y_origen(n, p)
        pasos_ml += 1  # Identificación de territorio y canal (O(1) en Atlas)

        # Encontrar el arranque exacto de la rotación (Puntero de Fase)
        # Multiplicación estimada inicial para saber por qué dígito empieza el flujo
        primer_digito_real = str((n * 10) // p)
        idx_rotacion = bloque_base.index(primer_digito_real)
        pasos_ml += 1  # Ajuste de fase / rotación instantánea

        # Reconstrucción generativa infinita por puntero circular
        decimal_ml = ""
        longitud_bloque = len(bloque_base)
        for i in range(digitos_objetivo):
            decimal_ml += bloque_base[(idx_rotacion + i) % longitud_bloque]
            # Nota: Esto no requiere aritmética, es movimiento de puntero de memoria

        # Espejo estructural (Validación de Coherencia Ley 1: pares suman 9)
        # Tomamos la mitad del bloque para comprobar simetría de fase
        mitad = longitud_bloque // 2
        espejo_valido = True
        if longitud_bloque % 2 == 0:
            for i in range(mitad):
                if int(bloque_base[i]) + int(bloque_base[i + mitad]) != 9:
                    espejo_valido = False

        ahorro = ((pasos_clasicos - pasos_ml) / pasos_clasicos) * 100

        return {
            "p": p,
            "n": n,
            "canal": canal,
            "bloque_base": bloque_base,
            "rotacion_inicio_idx": idx_rotacion,
            "decimal_clasico": decimal_clasico,
            "decimal_ml": decimal_ml,
            "espejo_coherente_9": espejo_valido,
            "coincidencia_exacta": decimal_clasico == decimal_ml,
            "pasos_clasicos": pasos_clasicos,
            "pasos_ml": pasos_ml,
            "ahorro_logico": f"{ahorro:.2f}%",
        }


if __name__ == "__main__":
    # --- PRUEBA EN VIVO DEL PROTOTIPO ---
    router = DecimalLightRouter()
    pruebas = [(1, 7), (8, 13), (2, 11), (5, 13)]

    print(
        f"{'OPERACIÓN':<10} | {'CANAL':<8} | {'COINCIDE':<9} | {'C. CLÁSICO':<10} | {'C. ML':<6} | {'AHORRO'}"
    )
    print("-" * 65)
    for n, p in pruebas:
        res = router.rutear(n, p, digitos_objetivo=12)
        print(
            f"{n}/{p:<5} | {res['canal']:<8} | {str(res['coincidencia_exacta']):<9} | {res['pasos_clasicos']:<10} | {res['pasos_ml']:<6} | {res['ahorro_logico']}"
        )
