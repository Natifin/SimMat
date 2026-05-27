use std::time::Instant;

pub trait DominioMatematico {
    fn identificar_idioma(&self) -> String;
    fn verificar_conservacion(&self, muestra: &[u8]) -> bool;
    fn aplicar_interferencia(&self, fase: usize, muestra: &[u8]) -> f64;
    fn total_fases_permitidas(&self) -> usize;
}

#[derive(Debug, Clone)]
pub struct ReporteAtajoMaximo {
    pub idioma_detectado: String,
    pub rutas_totales: usize,
    pub rutas_aniquiladas: usize,
    pub coherencia_optima: f64,
    pub solucion_fase: usize,
    pub tiempo_procesamiento_ns: u128,
}

pub struct UniversalShortcutEngine;

impl UniversalShortcutEngine {
    pub fn procesar<D: DominioMatematico>(problema: &D, flujo: &[u8]) -> ReporteAtajoMaximo {
        let t0 = Instant::now();
        let idioma = problema.identificar_idioma();

        let cumple_invariante = problema.verificar_conservacion(flujo);
        let penalizacion_inicial = if cumple_invariante { 1.0 } else { 0.05 };

        let total_rutas = problema.total_fases_permitidas();
        let mut rutas_aniquiladas = 0usize;

        let mut max_coherencia = -1.0;
        let mut fase_optima = 0usize;

        for fase in 0..total_rutas {
            let mut amplitud = penalizacion_inicial * problema.aplicar_interferencia(fase, flujo);

            if amplitud < 0.1 {
                rutas_aniquiladas += 1;
                amplitud = 0.0;
            }

            if amplitud > max_coherencia {
                max_coherencia = amplitud;
                fase_optima = fase;
            }
        }

        ReporteAtajoMaximo {
            idioma_detectado: idioma,
            rutas_totales: total_rutas,
            rutas_aniquiladas,
            coherencia_optima: max_coherencia,
            solucion_fase: fase_optima,
            tiempo_procesamiento_ns: t0.elapsed().as_nanos(),
        }
    }
}

pub struct MatrixDomain {
    pub dimension: usize,
    pub traza_teorica: i32,
    pub autovalores_candidatos: Vec<Vec<i32>>,
}

impl DominioMatematico for MatrixDomain {
    fn identificar_idioma(&self) -> String {
        format!(
            "Álgebra Matricial Simétrica (Dim {}x{})",
            self.dimension, self.dimension
        )
    }

    fn verificar_conservacion(&self, _muestra: &[u8]) -> bool {
        self.traza_teorica % 2 == 0
    }

    fn aplicar_interferencia(&self, fase: usize, _muestra: &[u8]) -> f64 {
        if fase >= self.autovalores_candidatos.len() {
            return 0.0;
        }

        let suma_autovalores: i32 = self.autovalores_candidatos[fase].iter().sum();

        if suma_autovalores == self.traza_teorica {
            1.0
        } else {
            0.01
        }
    }

    fn total_fases_permitidas(&self) -> usize {
        self.autovalores_candidatos.len()
    }
}

pub struct GraphDomain {
    pub total_nodos: usize,
    pub rutas_candidatas: Vec<Vec<usize>>,
    pub nodo_destino: usize,
}

impl DominioMatematico for GraphDomain {
    fn identificar_idioma(&self) -> String {
        format!("Topología de Redes Complejas ({} Nodos)", self.total_nodos)
    }

    fn verificar_conservacion(&self, _muestra: &[u8]) -> bool {
        self.nodo_destino > 0
    }

    fn aplicar_interferencia(&self, fase: usize, _muestra: &[u8]) -> f64 {
        if fase >= self.rutas_candidatas.len() {
            return 0.0;
        }
        let ruta = &self.rutas_candidatas[fase];

        if ruta.is_empty() {
            return 0.0;
        }

        let llega_a_destino = ruta.last() == Some(&self.nodo_destino);
        if !llega_a_destino {
            return 0.0;
        }

        1.0 / (ruta.len() as f64)
    }

    fn total_fases_permitidas(&self) -> usize {
        self.rutas_candidatas.len()
    }
}
