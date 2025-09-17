import pandas as pd
from pymongo import MongoClient

def import_xlsx_to_mongo(xlsx_path, mongo_uri, db_name, collection_name, drop=False):
    df = pd.read_excel(xlsx_path)
    print("✅ Columnas detectadas:", list(df.columns))
    print("✅ Filas detectadas:", len(df))

    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    if drop:
        print("🗑️ Limpiando colección antes de importar...")
        collection.drop()

    # Convertir NaN a None
    df = df.where(pd.notnull(df), None)

    records = df.to_dict(orient='records')
    if not records:
        print("⚠️ No hay registros para importar.")
        return

    result = collection.insert_many(records)
    print(f"✅ Importados {len(result.inserted_ids)} documentos en MongoDB.")

if __name__ == "__main__":
    import_xlsx_to_mongo(
        xlsx_path="/Users/bam/Documents/WorkWork/GrupoLaser/DB-Productos2025/data/raw/DB-Productos-Raw.xlsx",
        mongo_uri="mongodb://localhost:27017/",
        db_name="grupolaser",
        collection_name="productos",
        drop=True   # 👈 para limpiar antes de importar
    )