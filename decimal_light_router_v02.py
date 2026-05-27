class DecimalLightRouterV2:
    """Router con AutoAtlas para territorios primos periódicos."""

    def __init__(self):
        self._atlas_cache = {}

    def _decimal_periodico(self, p):
        vistos = {}
        resto = 1 % p
        digitos = []

        while resto and resto not in vistos:
            vistos[resto] = len(digitos)
            resto *= 10
            digitos.append(str(resto // p))
            resto %= p

        if resto == 0:
            return ""

        inicio = vistos[resto]
        return "".join(digitos[inicio:])

    def construir_atlas(self, p):
        if p in self._atlas_cache:
            return self._atlas_cache[p]

        bloque_base = self._decimal_periodico(p)
        if not bloque_base:
            raise ValueError(f"El primo {p} no genera decimal periódico no trivial.")

        atlas = {
            "p": p,
            "canales": {
                "Alfa": {
                    "bloque_base": bloque_base,
                }
            },
        }
        self._atlas_cache[p] = atlas
        return atlas
