use crate::dissipative_filter::FiltroDisipativoFase;
use crate::infinite_territory::OperadorEspectralInfinito;
use crate::photosynthesis_simulator::BiomimeticEnergyTransportSimulator;

pub enum TipoFlujo {
    EspectralInfinito { escala: u128, t: f64 },
    SenalCorrupta {
        muestras: Vec<f64>,
        frecuencia_objetivo: f64,
    },
    FlujoBiomimetico {
        ruido_ambiental: Vec<f64>,
        acoplamiento_fmo: f64,
    },
}

pub struct DecimalLightRouter;

impl DecimalLightRouter {
    pub fn procesar_y_enrutar(flujo: TipoFlujo) {
        match flujo {
            TipoFlujo::EspectralInfinito { escala, t } => {
                println!("\n[ROUTER] Enrutando a Motor Espectral Infinito (HTS)");
                let operador = OperadorEspectralInfinito::new(escala, t);
                let reporte = operador.colapsar_territorio();
                println!(
                    "   -> Resonancia Espectral : {:.6} | Invariante: {:.1}",
                    reporte.resonancia_espectral, reporte.invariante_global
                );
            }
            TipoFlujo::SenalCorrupta {
                muestras,
                frecuencia_objetivo,
            } => {
                println!("\n[ROUTER] Enrutando a Filtro Disipativo de Fase (TRC)");
                let filtro = FiltroDisipativoFase::new(frecuencia_objetivo, 0.5);
                let reporte = filtro.filtrar_flujo(&muestras);
                println!(
                    "   -> Coherencia Final      : {:.6} | Inmunidad: {}",
                    reporte.coherencia_final, reporte.exito_filtro
                );
                if reporte.exito_filtro {
                    println!(
                        "   -> [✓] ÉXITO: Estructura pura extraída (Amplitud): {:.4}",
                        reporte.senal_limpia_detectada
                    );
                }
            }
            TipoFlujo::FlujoBiomimetico {
                ruido_ambiental,
                acoplamiento_fmo,
            } => {
                println!("\n[ROUTER] Enrutando a Simulador Biomimético de Transporte Energético");
                let simulador = BiomimeticEnergyTransportSimulator::new(acoplamiento_fmo);
                let reporte = simulador.simular_transporte(&ruido_ambiental);

                println!("   -> Eficiencia de Transporte : {:.2}%", reporte.eficiencia_transporte);
                println!("   -> Energía en Centro Reacción: {:.4} eV", reporte.energia_recolectada);
                println!("   -> Pérdida Térmica (Calor)  : {:.2}%", reporte.disipacion_termica);

                if reporte.exito_captura {
                    println!("   -> [✓] Canal biomimético estable bajo ruido.");
                } else {
                    println!("   -> [X] Régimen inestable: disipación dominante.");
                }
            }
        }
    }
}
