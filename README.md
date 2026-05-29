# SimMat

Prototipos iniciales de **DecimalLight Router**, **DecimalLight Compressor** y un motor unificado en Rust.

## Ejecutar demos Python

```bash
python3 decimal_light_router.py
python3 decimal_light_compressor.py
python3 decimal_light_noise_test.py
python3 decimal_light_multi_noise_test.py
python3 benchmark_decimal_vs_traditional.py
python3 decimal_light_prime_fingerprint.py
```

## Ejecutar motor total en Rust

```bash
cargo run --release
```

## Artificial Photosynthesis Research Direction

El módulo biomimético de transporte energético **no crea fotosíntesis artificial directamente**.
Es una base computacional local para explorar cómo la geometría modular, el ruido asistido
y la disipación selectiva podrían inspirar futuros diseños de captación energética limpia.

Su propósito actual es experimental: evaluar estabilidad de canal y eficiencia bajo perturbación.

## Urban Leaf Coating — Hoja Urbana Biomimética

### Visión

No buscamos copiar un árbol completo. Buscamos extraer únicamente el canal funcional mínimo:

- captar luz,
- capturar CO₂,
- usar humedad/agua,
- liberar O₂.

La idea es un recubrimiento urbano distribuido sobre edificios e infraestructuras.

### Principio ML/FIS

La naturaleza es compleja porque debe sobrevivir; la ingeniería puede aislar la trayectoria útil mínima.

Atajo funcional objetivo:

**fotón → energía útil → transferencia eficiente → fijación de CO₂ → liberación de O₂**

### Arquitectura conceptual

1. **Captación fotónica:** superficie para absorber luz solar con alta eficiencia.
2. **Canal resonante:** geometría modular con pérdidas mínimas.
3. **Captura de CO₂:** interacción activa con aire urbano.
4. **Conversión biofotónica:** transformación inspirada en fotosíntesis para producir O₂.
5. **Disipación inteligente:** estabilización térmica y energética distribuida.

### Objetivo real

Urban Leaf Coating se plantea como infraestructura ambiental activa:

- fachada fotosintética,
- superficie urbana activa,
- sistema distribuido de mejora atmosférica.

### Relación con SimMat

El simulador biomimético de SimMat se usa para:

- estudiar rutas energéticas eficientes,
- explorar geometrías modulares,
- analizar ruido asistido,
- optimizar transporte energético,
- buscar trayectorias mínimas funcionales inspiradas en sistemas fotosintéticos.

### Filosofía central

La complejidad natural nace de la supervivencia.
La ingeniería puede buscar el núcleo mínimo útil.

## Documento conceptual

- `MANIFESTO_CLAUSURA_LOGICA.md`: declaración de principios de arquitectura sobre clausura estructural, colapso geométrico y atajo mínimo.

## Biomimetic State Sweep

Se añadió un barrido sistemático del espacio de estados biomimético para explorar estabilidad
computacional bajo perturbación térmica:

- acoplamiento_fmo: 0.1 a 2.0
- amplitud_ruido: 0.1 a 5.0
- 1000 muestras por simulación

Salida: `results/biomimetic_sweep_v0_1.csv` con eficiencia, energía, disipación y éxito de captura
por configuración.

**Nota prudente:** este barrido no valida fotosíntesis artificial real; es un análisis exploratorio
del modelo biomimético y su estabilidad computacional.


## Prime Worlds (first 100 primes)

Run the exploratory prime-world analyzer to map periodic-decimal signatures of the first 100 primes:

```bash
python3 decimal_light_prime_worlds.py
```

This produces:
- `results/prime_worlds_v0_1.csv` with per-prime metrics for period, entropy, symmetry, localization and short-window prediction,
- `results/prime_bridges_v0_1.csv` with pairwise bridge metrics based on period compatibility, entropy distance and symmetry alignment.

> Note: this is a computational exploration module. It does **not** claim a proof of new prime physics; it provides measurable signatures for routing/verification experiments.


### Verifiable vs Conjectural (Prime Worlds)

**Verifiable in this repo:**
- each prime has a measurable decimal-period signature,
- period dynamics are tied to modular arithmetic,
- symmetry (including Midy-like patterns) can be measured,
- bridge scores between prime worlds can be quantified from period/entropy/symmetry metrics.

**Conjectural framing:**
- interpreting these signatures as fundamental physical laws,
- claiming universal emergence of all mathematics from these prime-world dynamics.

The current implementation is explicitly computational and exploratory.
