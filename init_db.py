from database import engine, Base

# Șterge toate tabelele
Base.metadata.drop_all(bind=engine)
print("Toate tabelele au fost șterse.")
