mod biomimetic_state_analyzer;
mod dissipative_filter;
mod factory_core;
mod grammar;
mod infinite_territory;
mod photosynthesis_simulator;
mod quantum_inspired;
mod router;
mod shortcut_memory;

use biomimetic_state_analyzer::{BiomimeticStateAnalyzer, BiomimeticSweepConfig};
use router::{DecimalLightRouter, TipoFlujo};

fn main() {
    println!("=================================================================");
    println!("     DECIMAL_LIGHT ROUTER v0.1 — ECOSISTEMA DE CONTROL CRÍTICO    ");
    println!("=================================================================");

    let mut datos_industriales = vec![0.0; 1000];
    for (i, slot) in datos_industriales.iter_mut().enumerate() {
        let senal_pura = (i as f64 * 0.5).sin();
        let ruido_caotico = ((i * i) as f64 * 45.67).cos() * 8.0;
        *slot = senal_pura + ruido_caotico;
    }
    let flujo_telemetria = TipoFlujo::SenalCorrupta {
        muestras: datos_industriales,
        frecuencia_objetivo: 0.5,
    };
    DecimalLightRouter::procesar_y_enrutar(flujo_telemetria);

    let flujo_infinito = TipoFlujo::EspectralInfinito {
        escala: 1_000_000_000_000u128,
        t: 0.922,
    };
    DecimalLightRouter::procesar_y_enrutar(flujo_infinito);

    let mut ruido_termico_hoja = vec![0.0; 1000];
    for (i, slot) in ruido_termico_hoja.iter_mut().enumerate() {
        *slot = (i as f64 * 12.34).sin() * 2.5;
    }

    println!("\n[SITUACIÓN] Modelado biomimético de transferencia fotónica de clorofila.");
    println!(
        "-> Fluctuaciones térmicas moleculares inyectadas: {}",
        ruido_termico_hoja.len()
    );

    let flujo_fotosintesis = TipoFlujo::FlujoBiomimetico {
        ruido_ambiental: ruido_termico_hoja,
        acoplamiento_fmo: 0.5,
    };

    let cronometro_bio = std::time::Instant::now();
    DecimalLightRouter::procesar_y_enrutar(flujo_fotosintesis);
    println!("-> Tiempo de Cómputo Biomimético: {:?}", cronometro_bio.elapsed());



    println!("
[ESCENARIO 4] BARRIDO DE ESTADOS BIOMIMÉTICOS");
    println!("Nota: análisis computacional exploratorio; no valida fotosíntesis artificial real.");
    let config = BiomimeticSweepConfig {
        acoplamiento_inicio: 0.1,
        acoplamiento_fin: 2.0,
        acoplamiento_paso: 0.1,
        amplitud_inicio: 0.1,
        amplitud_fin: 5.0,
        amplitud_paso: 0.1,
        muestras: 1000,
    };

    let resultados = BiomimeticStateAnalyzer::ejecutar_barrido(&config);
    let _ = BiomimeticStateAnalyzer::guardar_csv("results/biomimetic_sweep_v0_1.csv", &resultados);

    let mut best = &resultados[0];
    let mut energia_max = f64::MIN;
    let mut disip_min = f64::MAX;
    let mut exitos = 0usize;

    for r in &resultados {
        if r.eficiencia_transporte > best.eficiencia_transporte {
            best = r;
        }
        if r.energia_recolectada > energia_max {
            energia_max = r.energia_recolectada;
        }
        if r.disipacion_termica < disip_min {
            disip_min = r.disipacion_termica;
        }
        if r.exito_captura {
            exitos += 1;
        }
    }

    println!("-> Mejor combinación        : acoplamiento={:.2}, amplitud_ruido={:.2}", best.acoplamiento_fmo, best.amplitud_ruido);
    println!("-> Eficiencia máxima        : {:.4}%", best.eficiencia_transporte);
    println!("-> Energía máxima           : {:.6}", energia_max);
    println!("-> Disipación mínima        : {:.6}%", disip_min);
    println!("-> Configuraciones exitosas : {}", exitos);
    println!("-> CSV                      : results/biomimetic_sweep_v0_1.csv");

    println!("=================================================================");
}
