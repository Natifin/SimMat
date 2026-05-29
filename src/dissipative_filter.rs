pub struct FiltroDisipativoFase {
    pub frecuencia_base: f64,
    pub umbral_coherencia: f64,
}

#[derive(Debug, Clone)]
pub struct SenalColapsada {
    pub senal_limpia_detectada: f64,
    pub entropia_aniquilada: f64,
    pub coherencia_final: f64,
    pub exito_filtro: bool,
}

impl FiltroDisipativoFase {
    pub fn new(frecuencia: f64, umbral: f64) -> Self {
        Self {
            frecuencia_base: frecuencia,
            umbral_coherencia: umbral,
        }
    }

    pub fn filtrar_flujo(&self, datos_corruptos: &[f64]) -> SenalColapsada {
        let mut suma_fase_cos = 0.0;
        let mut suma_fase_sin = 0.0;
        let total_muestras = datos_corruptos.len() as f64;

        for (i, &valor) in datos_corruptos.iter().enumerate() {
            let angulo = (i as f64 * self.frecuencia_base) % (2.0 * std::f64::consts::PI);
            suma_fase_cos += valor * angulo.cos();
            suma_fase_sin += valor * angulo.sin();
        }

        let magnitud_espectral =
            ((suma_fase_cos.powi(2) + suma_fase_sin.powi(2)).sqrt() * 2.0) / total_muestras;

        let es_coherente = magnitud_espectral > self.umbral_coherencia;

        SenalColapsada {
            senal_limpia_detectada: if es_coherente { magnitud_espectral } else { 0.0 },
            entropia_aniquilada: 1.0 - magnitud_espectral,
            coherencia_final: magnitud_espectral,
            exito_filtro: es_coherente,
        }
    }
}
