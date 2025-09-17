import os
import requests
from pprint import pprint
from pymongo import MongoClient
from dotenv import load_dotenv

# === Configuración ===
load_dotenv(dotenv_path=os.path.join("config", ".env"))
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "grupolaser")
COLLECTION_NAME = os.getenv("COLLECTION", "productos")

# === Precios de resina en USD/kg ===
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

COSTO_FIJO_KG = 0.80  # USD/kg

def get_exchange_rate():
    """Obtiene el tipo de cambio USD/MXN desde Banxico."""
    url = "https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF43718/datos/oportuno"
    token = "f6ceeb3d882a3552fe75cf86bdbcacee2d3e594169ec5853a81ff5f127460f3a"
    headers = {"Bmx-Token": token}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return float(data["bmx"]["series"][0]["datos"][0]["dato"])
    except Exception as e:
        print("⚠️ Error al obtener tipo de cambio:", e)
        return 20.0  # valor por defecto si falla

def conectar():
    client = MongoClient(MONGO_URI)
    return client[DB_NAME][COLLECTION_NAME]

def calcular_costos(producto, tc_usd):
    peso_g = producto.get("PESO", 0) or 0
    resina = (producto.get("MAT_1") or "").upper().strip()
    lin_prod = (producto.get("LIN_PROD") or "").upper().strip()

    if peso_g == 0 or resina not in PRECIOS_RESINA:
        return {"error": "Producto sin peso válido o resina desconocida."}

    # Convertir a kg
    peso_kg = peso_g / 1000

    # Costo en USD
    costo_resina_usd = peso_kg * PRECIOS_RESINA[resina]
    costo_fijo_usd   = peso_kg * COSTO_FIJO_KG
    costo_total_usd  = costo_resina_usd + costo_fijo_usd

    # Convertir a MXN
    costo_total_mxn = costo_total_usd * tc_usd

    # Márgenes según tipo
    if lin_prod.startswith("BOT"):
        margenes = [0.20, 0.30, 0.40]
    elif lin_prod.startswith("TAP"):
        margenes = [0.60, 0.70, 0.80]
    else:
        margenes = [0.30]  # default

    precios = {}
    for m in margenes:
        pv = costo_total_mxn * (1 + m)
        rent = (pv - costo_total_mxn) / costo_total_mxn
        precios[f"{int(m*100)}%"] = {
            "precio_venta": round(pv, 4),
            "rentabilidad": f"{rent*100:.2f}%"
        }

    return {
        "producto": producto.get("CVE_ART"),
        "descripcion": producto.get("DESCR"),
        "lin_prod": lin_prod,
        "peso_g": peso_g,
        "resina": resina,
        "costo_total_usd": round(costo_total_usd, 4),
        "costo_total_mxn": round(costo_total_mxn, 4),
        "precios": precios
    }

def main():
    col = conectar()
    tc = get_exchange_rate()
    print(f"💱 Tipo de cambio actual: 1 USD = {tc:.2f} MXN")

    # Tomamos un producto con resina conocida
    producto = col.find_one({"MAT_1": {"$in": list(PRECIOS_RESINA.keys())}})
    if not producto:
        print("⚠️ No se encontró producto con resina conocida.")
        return

    resultado = calcular_costos(producto, tc)
    pprint(resultado)

if __name__ == "__main__":
    main()