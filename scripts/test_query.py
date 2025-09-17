import os
import argparse
from pprint import pprint

from pymongo import MongoClient
from dotenv import load_dotenv

def get_connection():
    # Carga variables desde config/.env si existe; usa defaults si no
    load_dotenv(dotenv_path=os.path.join("config", ".env"))
    uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    db_name = os.getenv("DB_NAME", "grupolaser")
    coll_name = os.getenv("COLLECTION", "productos")
    client = MongoClient(uri)
    return client[db_name][coll_name]

def parse_args():
    p = argparse.ArgumentParser(description="Lee N productos de Mongo para validar conexión")
    p.add_argument("--limit", type=int, default=5, help="Cantidad de documentos a mostrar (default 5)")
    p.add_argument("--fields", type=str, default="CVE_ART,DESCR,PESO,MAT_1,PIG",
                   help="Campos a mostrar separados por comas (sin espacios). Ej: CVE_ART,DESCR,PESO")
    return p.parse_args()

def main():
    args = parse_args()
    collection = get_connection()

    total = collection.count_documents({})
    print(f"✅ Total de documentos en 'productos': {total}")

    # Proyección de campos
    fields = [f.strip() for f in args.fields.split(",") if f.strip()]
    projection = {f: 1 for f in fields}
    # opcional: oculta _id para que sea más limpio en consola
    projection["_id"] = 0

    print(f"✅ Mostrando {args.limit} documentos con campos: {', '.join(fields)}")
    cursor = collection.find({}, projection).limit(args.limit)

    for i, doc in enumerate(cursor, start=1):
        print(f"\n— Doc #{i} —")
        pprint(doc)

if __name__ == "__main__":
    main()