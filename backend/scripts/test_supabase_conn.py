from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql+psycopg2://postgres:_!.jdTW/mTT7-cD@db.jrdjwscfnriqboqyvgoq.supabase.co:5432/postgres?sslmode=require"

try:
  engine = create_engine(DATABASE_URL)

  with engine.connect() as connection:
    result = connection.execute(text("SELECT 1"))
    print("✅ Conexão com banco funcionando!")
    print("Resultado:", result.scalar())

except Exception as e:
  print("❌ Erro ao conectar no banco:")
  print(e)