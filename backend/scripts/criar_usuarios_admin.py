import os
from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import hash_password

# ==============================
# 🔐 TRAVA DE SEGURANÇA
# ==============================

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise Exception("❌ DATABASE_URL não definida")

# Garante que NÃO é banco local
if "localhost" in DATABASE_URL or "127.0.0.1" in DATABASE_URL:
    raise Exception("❌ Este script NÃO pode rodar em banco local")

# Opcional: reforço para Render
if "render.com" not in DATABASE_URL:
    raise Exception("❌ DATABASE_URL não parece ser do Render")

print("✅ Banco de PRODUÇÃO detectado")

# ==============================
# 👤 DADOS DO USUÁRIO
# ==============================

EMAIL = ""
PASSWORD = ""  # depois você pode trocar no banco ou criar outro script

# ==============================
# 🚀 CRIAÇÃO DO USUÁRIO
# ==============================

def create_user():
    db = SessionLocal()

    try:
        user_exists = db.query(User).filter(User.email == EMAIL).first()

        if user_exists:
            print("⚠️ Usuário já existe")
            return

        user = User(
            email=EMAIL,
            password_hash=hash_password(PASSWORD),
            is_active=True
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        print("✅ Usuário criado com sucesso em PRODUÇÃO")
        print(f"ID: {user.id}")
        print(f"Email: {user.email}")

    finally:
        db.close()


if __name__ == "__main__":
    create_user()
