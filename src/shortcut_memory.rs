use crate::factory_core::ReporteAtajoMaximo;
use std::collections::HashMap;
use std::sync::Mutex;

#[derive(Debug, Clone, Hash, PartialEq, Eq)]
pub struct FirmaEstructural {
    pub huella_id: String,
    pub dimension_espacio: usize,
}

pub struct ShortcutMemory {
    cache: Mutex<HashMap<FirmaEstructural, ReporteAtajoMaximo>>,
}

impl ShortcutMemory {
    pub fn new() -> Self {
        Self {
            cache: Mutex::new(HashMap::new()),
        }
    }

    pub fn consultar(&self, firma: &FirmaEstructural) -> Option<ReporteAtajoMaximo> {
        let lock = self.cache.lock().unwrap();
        lock.get(firma).cloned()
    }

    pub fn memorizar(&self, firma: FirmaEstructural, reporte: ReporteAtajoMaximo) {
        let mut lock = self.cache.lock().unwrap();
        lock.insert(firma, reporte);
    }
}
