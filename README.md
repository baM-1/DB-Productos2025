# DB-Productos2025

Proyecto de **Grupo Laser** para centralizar, consultar y costear productos de botellas y tapas/tapones mediante un sistema híbrido en **Python + MongoDB**.

## 🚀 Objetivo
Implementar un **costeador 50/50** (50% resina + 50% costos fijos) conectado a una base de datos de productos reales.  
El sistema permite:
- Importar productos desde Excel a MongoDB.
- Consultar productos con scripts en Python.
- Calcular costos, márgenes y rentabilidad con precios de resina en USD y tipo de cambio Banxico.

## ⚙️ Stack Tecnológico
- **Python 3.12**
- **MongoDB 8.x**
- **Pandas** para manejo de Excel.
- **PyMongo** para conexión a la DB.
- **Requests** para tipo de cambio (API Banxico).
- **VS Code** + **iTerm2 (Fish Shell)** para desarrollo.

## 📊 Funcionalidades actuales
- Cargar la DB desde Excel (`import_xlsx_to_mongo.py`).
- Consultar documentos (`test_query.py`).
- Calcular costos 50/50 (`costeador_50_50.py`).
- Prototipo con tipo de cambio en tiempo real y márgenes dinámicos (`costeador_prototipo.py`).

## 🛠️ Instalación

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/baM-1/DB-Productos2025.git
   cd DB-Productos2025
