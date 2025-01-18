# run.py
from datetime import date, time, timedelta
from app import create_app, db
from app.models import Slot
from app.routes.main import create_50min_slots  # Função auxiliar para gerar intervalos

app = create_app()

def auto_create_slots():
    """
    Exemplo simples que cria slots para a semana atual (segunda a sábado)
    nos horários: 08:00-12:00 e 14:00-18:00, a cada 50 minutos.
    """
    with app.app_context():
        base_date = date.today()
        end_date = base_date + timedelta(days=7)  # Gera para 1 semana
        current_day = base_date
        created_count = 0

        while current_day <= end_date:
            # weekday(): segunda = 0 até sábado = 5 (domingo = 6, ignorado)
            if current_day.weekday() < 6:
                created_count += create_50min_slots(current_day, time(8, 0), time(12, 0))
                created_count += create_50min_slots(current_day, time(14, 0), time(18, 0))
            current_day += timedelta(days=1)

        db.session.commit()
        print(f"[auto_create_slots] Slots criados/atualizados: {created_count}")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("[run.py] Banco de dados criado com sucesso!")
        # Descomente a linha abaixo se quiser gerar os slots automaticamente ao iniciar:
        # auto_create_slots()
    app.run(host='0.0.0.0', port=5000, debug=True)
