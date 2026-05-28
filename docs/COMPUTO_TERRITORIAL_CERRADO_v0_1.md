# Cómputo Territorial Cerrado (CTC)

**Especificación de invariabilidad matemática en el ecosistema Nexus**  
**Autor:** Antonio Javier Domínguez Dueñas  
**Proyecto:** SimMat / Nexus / ML Matemática Líquida  
**Versión:** v0.1  
**Fecha:** Mayo 2026

---

## 0. Estado del documento

Este documento define una arquitectura conceptual y técnica para un modelo de ejecución cerrado por dominio. Distingue explícitamente entre:

- **Garantías matemáticas internas:** propiedades verificables dentro del espacio formal del motor.
- **Garantías de implementación:** propiedades que dependen del código real, tests, compilador y entorno.
- **Riesgos externos:** sistema operativo, binario, hardware, entradas manipuladas y canales laterales.

El CTC no afirma ser imposible de hackear en sentido absoluto. Su objetivo es reducir la ambigüedad interna obligando a cada estado computado a demostrar pertenencia, cierre y reconstrucción.

---

## 1. Principio fundamental

El **Cómputo Territorial Cerrado (CTC)** es un paradigma de ejecución donde las funciones informáticas no operan sobre variables abiertas o continuas, sino como operadores de desplazamiento dentro de estructuras algebraicas finitas, rígidas y cíclicas.

Ejemplos de dominios:

```text
R7   -> rueda de 7 estados
R49  -> toro/rueda territorial 7x7
R360 -> rueda modular extendida
R_M  -> rueda finita de M estados
```

La premisa núcleo es:

> El motor no confía en la integridad absoluta del entorno de ejecución. Obliga a cada resultado a demostrar su pertenencia, cierre y reconstrucción geométrica antes de consolidar un estado.

En forma mínima:

```text
El primo llama la función.
La rueda limita el mundo.
La posición fija el punto.
La trayectoria demuestra el resultado.
```

---

## 2. Modelo de instrucción

Una instrucción CTC se expresa como una llamada compacta:

```text
CALL Pp Rm Xx Tt
```

Donde:

```text
Pp = identificador primo de función u operador
Rm = rueda/dominio modular de tamaño m
Xx = posición inicial dentro de la rueda
Tt = número de pasos de trayectoria
```

Ejemplo:

```text
CALL P13 R49 X21 T7
```

Interpretación:

```text
Usar el operador asociado al primo 13.
Trabajar sobre la rueda cerrada de 49 posiciones.
Anclar la ejecución en la posición inicial 21.
Emitir/auditar una trayectoria de 7 estados.
```

---

## 3. Los tres candados de certeza interna

Para que una instrucción sea admitida y procesada por el motor Nexus/SimMat, debe superar una triple auditoría geométrica en tiempo de ejecución:

```text
[Instrucción entrante]
         |
         v
1. CANDADO PRIMO
   ¿El identificador funcional Pp existe en el glosario primo?
         |
         v
2. CANDADO CIRCULAR
   ¿Todos los estados xi pertenecen estrictamente al rango [1..m]?
         |
         v
3. CANDADO DE TRAYECTORIA
   ¿La secuencia completa respeta el operador modular declarado?
         |
         v
[Ejecución consolidada]
```

### 3.1 Candado primo: validación de función

La instrucción debe invocar un identificador funcional basado en un primo registrado:

```text
P7, P11, P13, P17, P19, P23, P29, ...
```

Cualquier llamada corrupta, no registrada o topológicamente inexistente se rechaza antes de ejecutarse:

```text
P12 -> rechazado
P15 -> rechazado
P999 no registrado -> rechazado
```

Este candado no demuestra por sí solo que el código asociado a P13 sea correcto; demuestra que la instrucción pertenece al alfabeto funcional permitido.

### 3.2 Candado circular: límite del dominio

Ninguna operación territorial puede consolidar un estado fuera del espacio asignado. En una rueda de `m` elementos, el avance modular se define como:

```text
next(x, p, m) = ((x - 1 + p) mod m) + 1
```

Por construcción, si `x` pertenece a `[1..m]`, entonces `next(x,p,m)` también pertenece a `[1..m]`.

Ejemplo para R49:

```text
next(x, 13, 49) = ((x - 1 + 13) mod 49) + 1
```

Así, el dominio formal nunca devuelve posiciones externas como:

```text
0, 50, 999, -3
```

Nota técnica: esto no elimina todos los desbordamientos de memoria posibles a nivel de implementación. Lo que elimina es el desbordamiento semántico dentro del dominio territorial, siempre que el código implemente correctamente las comprobaciones y use tipos seguros.

### 3.3 Candado de trayectoria: prueba de ejecución coherente

El resultado de una función no se acepta como dato aislado. Debe presentarse como secuencia verificable de estados intermedios:

```text
x0 -> x1 -> x2 -> ... -> xt
```

Para una instrucción `CALL Pp Rm Xx Tt`, la secuencia debe cumplir:

```text
x0 = x
para todo i: xi+1 = ((xi - 1 + p) mod m) + 1
longitud = t
```

Si un solo paso no respeta la distancia modular declarada, la trayectoria se rechaza.

---

## 4. Ejemplo práctico de validación

### Instrucción segura

```text
CALL P13 R49 X21 T7
```

Componentes:

```text
P13 -> función de desplazamiento 13 registrada en el glosario
R49 -> rueda circular de 49 posiciones
X21 -> posición inicial
T7  -> trayectoria de 7 estados
```

### Trayectoria emitida

Si contamos la posición inicial como primer estado de la trayectoria, la salida esperada es:

```text
[21, 34, 47, 11, 24, 37, 1]
```

### Auditoría de invariantes

```text
1. P13 existe en el glosario primo                  -> PASA
2. Todos los estados pertenecen a [1..49]           -> PASA
3. Cada transición avanza +13 mod 49                -> PASA
4. Longitud de cadena = 7 estados                   -> PASA
```

Comprobación explícita:

```text
21 + 13 -> 34
34 + 13 -> 47
47 + 13 -> 60 -> 11 mod 49
11 + 13 -> 24
24 + 13 -> 37
37 + 13 -> 50 -> 1 mod 49
```

---

## 5. Intentos de corrupción y rechazo

### 5.1 Corrupción evidente fuera de dominio

Salida manipulada:

```text
[21, 34, 999, 11, 24, 37, 1]
```

Resultado:

```text
RECHAZADO por Candado Circular
999 no pertenece a [1..49]
```

### 5.2 Corrupción sutil dentro del dominio

Salida manipulada:

```text
[21, 34, 40, 11, 24, 37, 1]
```

Resultado:

```text
RECHAZADO por Candado de Trayectoria
next(34, 13, 49) = 47, no 40
```

### 5.3 Función inexistente

Instrucción manipulada:

```text
CALL P12 R49 X21 T7
```

Resultado:

```text
RECHAZADO por Candado Primo
P12 no es un primo funcional registrado
```

---

## 6. Matriz honesta de alcance de seguridad

| Lo que el CTC garantiza internamente | Lo que el CTC no garantiza por sí solo |
|---|---|
| El motor puede rechazar resultados fuera del dominio formal. | No impide que alguien modifique el binario o el código fuente. |
| Toda trayectoria puede auditarse por pertenencia, cierre y reconstrucción. | No evita entradas falsas que sean geométricamente válidas. |
| Las funciones no registradas pueden ser rechazadas antes de ejecutar. | No elimina vulnerabilidades del sistema operativo huésped. |
| Reduce ambigüedad de estado y errores semánticos de dominio. | No protege contra manipulación física del hardware. |
| Permite verificación rápida de rutas sin confiar ciegamente en el resultado. | No sustituye criptografía, aislamiento de procesos ni sandboxing. |
| Facilita reproducibilidad y depuración determinista. | No garantiza ausencia de bugs en la implementación real. |

---

## 7. Relación con Proof-Carrying Code

El CTC puede entenderse como una forma territorial y modular de ejecución con prueba integrada.

En un sistema clásico de **Proof-Carrying Code**, una unidad de código debe traer una prueba de que cumple ciertas propiedades de seguridad antes de ejecutarse o aceptarse.

En CTC, la unidad computacional trae una prueba más geométrica:

```text
La salida debe demostrar que pertenece al territorio.
La trayectoria debe demostrar que respeta el operador.
El operador debe demostrar que existe en el glosario primo.
```

No se persiguen estados corruptos después del daño. Se impide la consolidación de estados que no saben reconstruir su propia trayectoria.

---

## 8. Glosario primo-funcional inicial

Este glosario es provisional. Cada primo debe asociarse a una función real, medible y testeable.

| Primo | Función candidata | Dominio sugerido |
|---:|---|---|
| P2 | duplicar / bifurcar | expansión binaria |
| P3 | triangular / combinar tres | síntesis local |
| P5 | filtrar / seleccionar | poda de estados |
| P7 | ordenar territorio circular | R7 / R49 |
| P11 | buscar vecino o resonancia | rutas locales |
| P13 | propagar trayectoria | ruedas modulares |
| P17 | medir estabilidad | control de equilibrio |
| P19 | expandir frontera | exploración paralela |
| P23 | comprimir memoria | patrones recurrentes |
| P29 | verificar error | auditoría territorial |
| P31 | comparar simetría | validación estructural |

Regla de diseño:

> Un primo no debe ser decorativo. Debe nombrar una función computacional con entrada, salida, coste y prueba de validez.

---

## 9. Implicación para Nexus / SimMat

El CTC no busca acelerar el ordenador completo ni sustituir el sistema operativo. Busca crear una capa local donde los problemas se transformen en territorios finitos verificables.

Arquitectura recomendada:

```text
Windows / Linux / Sistema huésped
        |
        v
Nexus Compute Layer
        |
        v
Prime Function Router
        |
        v
Closed Territorial Computation
        |
        v
CPU / GPU / simuladores locales
```

El beneficio no proviene de prometer invulnerabilidad absoluta, sino de reducir el espacio de estados posibles.

```text
Menos estados posibles.
Más cierre.
Más verificación.
Menos ambigüedad.
Más reproducibilidad.
```

---

## 10. Próximo paso: flujo dinámico A(t)

La evolución natural del CTC es pasar del ejemplo estático:

```text
CALL P13 R49 X21 T7
```

al flujo dinámico:

```text
A(t) = estado territorial del sistema en el tiempo t
A(t+1) = operador_primo(A(t), rueda, restricciones)
```

Cada transición `A(t) -> A(t+1)` deberá cumplir:

```text
1. función prima registrada
2. pertenencia al dominio
3. cierre modular
4. reconstrucción de trayectoria
5. registro auditable del cambio
```

Así, Nexus no solo calcula trayectorias: mantiene una historia verificable de por qué cada estado existe.

---

## 11. Frase fundacional

> El primo llama la función. La rueda limita el mundo. La posición fija el punto. La trayectoria demuestra el resultado.

Esta frase resume el Cómputo Territorial Cerrado como principio de ingeniería: no aceptar resultados por confianza, sino por pertenencia demostrada dentro de un territorio matemático finito.
