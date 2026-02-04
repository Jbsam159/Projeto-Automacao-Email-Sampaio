from apscheduler.schedulers.background import BackgroundScheduler
from app.core.database import SessionLocal
from app.services.cleanup_service import limpar_boletos_expirados
from app.core.logger import get_logger

logger = get_logger(__name__)
scheduler = BackgroundScheduler()

def job_limpeza():
  db = SessionLocal()
  try:
    removidos = limpar_boletos_expirados(db)
    logger.info(f"Limpeza automática executada | removidos={removidos}")
  finally:
    db.close()

def start_scheduler():
  scheduler.add_job(job_limpeza, "interval", hours=22)
  scheduler.start()
