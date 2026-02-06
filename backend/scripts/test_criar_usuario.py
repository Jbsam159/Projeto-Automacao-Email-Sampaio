from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import hash_password

def create_user():
    db = SessionLocal()

    try:
        email = "user1@example.com"
        password = "123"

        # Verifica se já existe
        user_exists = db.query(User).filter(User.email == email).first()
        if user_exists:
            print("⚠️ Usuário já existe")
            return

        user = User(
            email=email,
            password_hash=hash_password(password)
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        print("✅ Usuário criado com sucesso")
        print(f"ID: {user.id}")
        print(f"Email: {user.email}")
        print(f"Senha: {password}")

    finally:
        db.close()


if __name__ == "__main__":
    create_user()
