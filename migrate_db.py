from principal import app, db
from sqlalchemy import text

def migrate():
    with app.app_context():
        print("Iniciando migración de base de datos...")
        try:
            # Añadir la columna id_transaccion si no existe
            db.session.execute(text('ALTER TABLE facturacion ADD COLUMN IF NOT EXISTS id_transaccion VARCHAR(50);'))
            
            # Añadir fecha_registro a historial_medico
            db.session.execute(text('ALTER TABLE historial_medico ADD COLUMN IF NOT EXISTS fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP;'))
            
            # Añadir estado_cierre a facturacion
            db.session.execute(text('ALTER TABLE facturacion ADD COLUMN IF NOT EXISTS estado_cierre BOOLEAN DEFAULT FALSE;'))
            
            # Añadir estado_cierre a historial_medico
            db.session.execute(text('ALTER TABLE historial_medico ADD COLUMN IF NOT EXISTS estado_cierre BOOLEAN DEFAULT FALSE;'))
            
            # Crear la nueva tabla pago_detalle si no existe
            db.create_all()
            
            db.session.commit()
            print("¡Migración completada con éxito!")
        except Exception as e:
            db.session.rollback()
            print(f"Error durante la migración: {e}")

if __name__ == "__main__":
    migrate()
