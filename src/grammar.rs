use std::fmt;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum IdiomaDecimal {
    RotacionalPuro,
    EspejoDirecto,
    BicanalParalelo,
    MulticanalComplejo,
}

impl fmt::Display for IdiomaDecimal {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            IdiomaDecimal::RotacionalPuro => write!(f, "Rotacional Puro (Rueda Única)"),
            IdiomaDecimal::EspejoDirecto => write!(f, "Espejo Directo (Rebote sobre Eje 9)"),
            IdiomaDecimal::BicanalParalelo => write!(f, "Bicanal Paralelo (Vías Entrelazadas)"),
            IdiomaDecimal::MulticanalComplejo => write!(f, "Multicanal Complejo"),
        }
    }
}

#[derive(Debug, Clone)]
pub struct FichaLinguistica {
    pub p: u32,
    pub periodo_longitud: usize,
    pub idioma: IdiomaDecimal,
    pub total_canales: usize,
    pub vocabulario_madre: Vec<Vec<u8>>,
    pub espejo_activo: bool,
    pub atractor_dominante: String,
}

pub struct DecimalLightGrammar;

impl DecimalLightGrammar {
    pub fn traducir_territorio(p: u32) -> FichaLinguistica {
        let mut restos_cubiertos = vec![false; p as usize];
        let mut vocabulario = Vec::new();

        for num in 1..p {
            if !restos_cubiertos[num as usize] {
                let mut mapa_restos = vec![0u8; (p + 1) as usize];
                let mut resto = num % p;
                let mut periodo = Vec::new();

                while resto != 0 && mapa_restos[resto as usize] == 0 {
                    mapa_restos[resto as usize] = 1;
                    restos_cubiertos[resto as usize] = true;
                    resto *= 10;
                    periodo.push((resto / p) as u8 + b'0');
                    resto %= p;
                }

                if !periodo.is_empty() {
                    vocabulario.push(periodo);
                }
            }
        }

        let total_canales = vocabulario.len();
        let periodo_longitud = vocabulario.first().map(|v| v.len()).unwrap_or(0);

        let idioma = match (total_canales, periodo_longitud) {
            (1, _) => IdiomaDecimal::RotacionalPuro,
            (_, 2) => IdiomaDecimal::EspejoDirecto,
            (2, _) => IdiomaDecimal::BicanalParalelo,
            _ => IdiomaDecimal::MulticanalComplejo,
        };

        let espejo_activo = vocabulario
            .first()
            .map(|bloque| Self::validar_espejo_9(bloque))
            .unwrap_or(false);

        let atractor_dominante = match idioma {
            IdiomaDecimal::RotacionalPuro => String::from("Desplazamiento Cíclico Isótropo"),
            IdiomaDecimal::EspejoDirecto => String::from("Simetría Bilateral de Eje Central (9)"),
            IdiomaDecimal::BicanalParalelo => format!("Salto de Cauce Dual Modulo {}", p % 3),
            IdiomaDecimal::MulticanalComplejo => {
                format!("Dispersión Reticular de Canales ({})", total_canales)
            }
        };

        FichaLinguistica {
            p,
            periodo_longitud,
            idioma,
            total_canales,
            vocabulario_madre: vocabulario,
            espejo_activo,
            atractor_dominante,
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
