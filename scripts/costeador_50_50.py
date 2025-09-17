import os
from pprint import pprint
from pymongo import MongoClient
from dotenv import load_dotenv

# === Configuración ===
load_dotenv(dotenv_path=os.path.join("config", ".env"))
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "grupolaser")
COLLECTION_NAME = os.getenv("COLLECTION", "productos")

# === Precios de resina (ejemplo, en $/kg) ===
# ⚠️ Aquí ajustamos según tus datos reales después
PRECIOS_RESINA = {
    "PET": 1.71,
    "PP": 1.61,
    "SURLYN": 7.32,
    "MOMPRENE": 5.40,
    "CELCON": 1.82,
    "KOCETAL": 5.00,
    "ALTO IMPACTO": 2.35,
    "RESINA K": 3.60,
}

# Costos fijos de referencia (ejemplo, $/kg)
COSTO_FIJO_KG = 0.80

def conectar():
    client = MongoClient(MONGO_URI)
    return client[DB_NAME][COLLECTION_NAME]

def costeador_50_50(producto: dict):
    """
    Aplica la lógica 50/50 a un producto.
    """
    peso_g = producto.get("PESO", 0) or 0
    resina = (producto.get("MAT_1") or "").upper().strip()

    if peso_g == 0 or resina not in PRECIOS_RESINA:
        return {"error": "Producto sin peso válido o resina desconocida."}

    # Convertir a kg
    peso_kg = peso_g / 1000

    # Costos
    costo_resina = peso_kg * PRECIOS_RESINA[resina]   # 50% materia prima
    costo_fijo   = peso_kg * COSTO_FIJO_KG            # 50% costos fijos
    costo_total  = costo_resina + costo_fijo

    # Márgenes (ejemplo: 30% y 50%)
    precios_venta = {
        "30%": costo_total * 1.30,
        "50%": costo_total * 1.50,
    }

    return {
        "producto": producto.get("CVE_ART"),
        "descripcion": producto.get("DESCR"),
        "peso_g": peso_g,
        "resina": resina,
        "costo_resina": round(costo_resina, 4),
        "costo_fijo": round(costo_fijo, 4),
        "costo_total": round(costo_total, 4),
        "precios_venta": precios_venta
    }

def main():
    col = conectar()

    # Traer 5 productos con resina conocida
    cursor = col.find({"MAT_1": {"$in": list(PRECIOS_RESINA.keys())}}).limit(5)

    for prod in cursor:
        resultado = costeador_50_50(prod)
        pprint(resultado)
        print("-" * 50)

if __name__ == "__main__":
    main()