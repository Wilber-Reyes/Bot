import mysql.connector
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Configuración
TOKEN = '8082658597:AAF2rLA-oxA-YxhO5i-X_IAZYIHivmOcBM8'  # Token de tu bot
MYSQL_HOST = 'localhost'  # Dirección de tu servidor MySQL
MYSQL_USER = 'root'  # Usuario de MySQL
MYSQL_PASSWORD = 'R57606795'  # Contraseña de MySQL
MYSQL_DATABASE = 'asistencia'  # Nombre de la base de datos

# Crear la base de datos y la tabla si no existen
def create_db():
    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD
    )
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DATABASE}")
    cursor.execute('''CREATE TABLE IF NOT EXISTS asistencia (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id INT NOT NULL,
                        username VARCHAR(50) NOT NULL,
                        fecha DATETIME NOT NULL
                    )''')
    conn.commit()
    cursor.close()
    conn.close()

# Comando /start
async def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    await update.message.reply_text(f'Hola {user.first_name}, soy tu asistente para registrar la asistencia.\nComanda /registrar para registrar tu entrada.')

# Comando /registrar
async def registrar(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    user_id = user.id
    username = user.username
    fecha = update.message.date.strftime('%Y-%m-%d %H:%M:%S')  # Formato de la fecha

    # Conexión a la base de datos MySQL
    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )
    cursor = conn.cursor()
    
    # Insertar los datos de la asistencia
    cursor.execute("INSERT INTO asistencia (user_id, username, fecha) VALUES (%s, %s, %s)", (user_id, username, fecha))
    conn.commit()
    cursor.close()
    conn.close()

    await update.message.reply_text(f'Asistencia registrada correctamente para {user.first_name}.')

# Comando /reporte
async def reporte(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )
    cursor = conn.cursor()

    # Obtener el reporte de asistencias
    cursor.execute("SELECT username, fecha FROM asistencia ORDER BY fecha DESC")
    rows = cursor.fetchall()
    
    if rows:
        reporte_msg = "Asistencias registradas:\n"
        for row in rows:
            reporte_msg += f"Usuario: {row[0]}, Fecha: {row[1]}\n"
    else:
        reporte_msg = "No hay registros de asistencia disponibles."
    
    cursor.close()
    conn.close()

    await update.message.reply_text(reporte_msg)

# Función principal para iniciar el bot
def main():
    create_db()  # Crear la base de datos y la tabla si no e
