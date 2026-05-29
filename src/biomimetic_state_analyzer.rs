use crate::photosynthesis_simulator::BiomimeticEnergyTransportSimulator;
use std::fs;

pub struct BiomimeticSweepConfig {
    pub acoplamiento_inicio: f64,
    pub acoplamiento_fin: f64,
    pub acoplamiento_paso: f64,
    pub amplitud_inicio: f64,
    pub amplitud_fin: f64,
    pub amplitud_paso: f64,
    pub muestras: usize,
}

#[derive(Debug, Clone)]
pub struct BiomimeticSweepResult {
    pub acoplamiento_fmo: f64,
    pub amplitud_ruido: f64,
    pub eficiencia_transporte: f64,
    pub energia_recolectada: f64,
    pub disipacion_termica: f64,
    pub exito_captura: bool,
}

pub struct BiomimeticStateAnalyzer;

impl BiomimeticStateAnalyzer {
    pub fn ejecutar_barrido(config: &BiomimeticSweepConfig) -> Vec<BiomimeticSweepResult> {
        let mut resultados = Vec::new();

        let mut acoplamiento = config.acoplamiento_inicio;
        while acoplamiento <= config.acoplamiento_fin + 1e-9 {
            let simulador = BiomimeticEnergyTransportSimulator::new(acoplamiento);

            let mut amplitud_ruido = config.amplitud_inicio;
            while amplitud_ruido <= config.amplitud_fin + 1e-9 {
                let mut ruido = vec![0.0; config.muestras];
                for (i, slot) in ruido.iter_mut().enumerate() {
                    *slot = (i as f64 * 12.34).sin() * amplitud_ruido;
                }

                let reporte = simulador.simular_transporte(&ruido);
                resultados.push(BiomimeticSweepResult {
                    acoplamiento_fmo: acoplamiento,
                    amplitud_ruido,
                    eficiencia_transporte: reporte.eficiencia_transporte,
                    energia_recolectada: reporte.energia_recolectada,
                    disipacion_termica: reporte.disipacion_termica,
                    exito_captura: reporte.exito_captura,
                });

                amplitud_ruido += config.amplitud_paso;
            }

            acoplamiento += config.acoplamiento_paso;
        }

        resultados
    }

    pub fn guardar_csv(path: &str, resultados: &[BiomimeticSweepResult]) -> std::io::Result<()> {
        let mut out = String::from(
            "acoplamiento_fmo,amplitud_ruido,eficiencia_transporte,energia_recolectada,disipacion_termica,exito_captura\n",
        );

        for r in resultados {
            out.push_str(&format!(
                "{:.3},{:.3},{:.6},{:.6},{:.6},{}\n",
                r.acoplamiento_fmo,
                r.amplitud_ruido,
                r.eficiencia_transporte,
                r.energia_recolectada,
                r.disipacion_termica,
                r.exito_captura
            ));
        }

        if let Some(parent) = std::path::Path::new(path).parent() {
            fs::create_dir_all(parent)?;
        }
        fs::write(path, out)
    }
}
