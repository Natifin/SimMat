use std::time::Instant;

#[derive(Debug, Clone)]
pub struct EstadoOnda {
    pub canal: String,
    pub fase: usize,
    pub amplitud_coherencia: f64,
}

#[derive(Debug, Clone)]
pub struct ReporteColapso {
    pub canal_estable: String,
    pub fase_estable: usize,
    pub niveles_evaluados: usize,
    pub rutas_canceladas: usize,
    pub tiempo_colapso_ns: u128,
    pub coherencia_final: f64,
}

pub struct QuantumLikeSimulator;

impl QuantumLikeSimulator {
    pub fn colapsar_flujo(
        flujo_observado: &[u8],
        _p: u32,
        canales_territorio: &[(String, Vec<u8>)],
    ) -> ReporteColapso {
        let t0 = Instant::now();
        let huella_len = usize::min(16, flujo_observado.len());
        let huella = &flujo_observado[..huella_len];

        let mut mejor_estado = EstadoOnda {
            canal: String::from("Desconocido"),
            fase: 0,
            amplitud_coherencia: -1.0,
        };

        let mut niveles_evaluados = 0usize;
        let mut rutas_canceladas = 0usize;

        for (canal, bloque) in canales_territorio {
            if bloque.is_empty() {
                continue;
            }

            let penalizacion_espejo = if bloque.len() % 2 == 0 && !Self::validar_espejo_9(bloque) {
                0.5
            } else {
                1.0
            };

            for fase in 0..bloque.len() {
                niveles_evaluados += 1;
                let mut amplitud = 1.0 * penalizacion_espejo;

                for (i, b) in huella.iter().enumerate() {
                    if *b != bloque[(fase + i) % bloque.len()] {
                        amplitud *= 0.1;
                    }
                }

                if amplitud < 0.1 {
                    rutas_canceladas += 1;
                }

                if amplitud > mejor_estado.amplitud_coherencia {
                    mejor_estado = EstadoOnda {
                        canal: canal.clone(),
                        fase,
                        amplitud_coherencia: amplitud,
                    };
                }
            }
        }

        ReporteColapso {
            canal_estable: mejor_estado.canal,
            fase_estable: mejor_estado.fase,
            niveles_evaluados,
            rutas_canceladas,
            tiempo_colapso_ns: t0.elapsed().as_nanos(),
            coherencia_final: mejor_estado.amplitud_coherencia.max(0.0),
        }
    }

    fn validar_espejo_9(bloque: &[u8]) -> bool {
        if bloque.is_empty() || bloque.len() % 2 != 0 {
            return false;
        }
        let mitad = bloque.len() / 2;
        for i in 0..mitad {
            if (bloque[i] - b'0') + (bloque[i + mitad] - b'0') != 9 {
                return false;
            }
        }
        true
    }
}
