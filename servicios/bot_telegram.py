import telebot
from telebot import types
from datetime import datetime, timedelta
import threading
import os
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

DetailedTelegramCalendar.months['es'] = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
DetailedTelegramCalendar.days_of_week['es'] = ["Lu", "Ma", "Mi", "Ju", "Vi", "Sa", "Do"]

class CalendarioClinica(DetailedTelegramCalendar):
    first_step = 'm'  # Iniciar directamente pidiendo el MES, ignorando el Año

def obtener_calendario():
    # Solo permitir fechas desde HOY hasta el final del año actual
    hoy = datetime.now().date()
    fin_de_ano = datetime.now().date().replace(month=12, day=31)
    return CalendarioClinica(locale='es', min_date=hoy, max_date=fin_de_ano)

# ═══════════════════════════════════════════════════════════
# FUNCIONES DE AYUDA (GENERADORES DE BOTONES)
# ═══════════════════════════════════════════════════════════

def crear_reloj():
    markup = types.InlineKeyboardMarkup(row_width=4)
    horas = ["08:00", "09:00", "10:00", "11:00", "14:00", "15:00", "16:00", "17:00"]
    botones = [types.InlineKeyboardButton(h, callback_data=f"hora_{h}") for h in horas]
    markup.add(*botones)
    return markup


# ═══════════════════════════════════════════════════════════
# FUNCIÓN PRINCIPAL DEL BOT
# ═══════════════════════════════════════════════════════════

def iniciar_bot_sic(app, db, Cita, Historial_Medico):
    # Token dinámico: Usa variable de entorno o el token manual como respaldo
    TOKEN = os.environ.get('TELEGRAM_TOKEN', "8758265776:AAHRTZh5HbsjrvWZSaNpiygoZHnRR4h4ANE")
    ADMIN_CHAT_ID = os.environ.get('ADMIN_CHAT_ID', "@SistemaSIC_bot")

    # ═══════════════════════════════════════════════════════════
    # 📝 CONFIGURACIÓN DE TEXTOS (CAMBIA LOS MENSAJES AQUÍ)
    # ═══════════════════════════════════════════════════════════
    MSJ = {
        "bienvenida": "👋 ¡Hola! Bienvenido, espero que te encuentres bien.\n\nPor favor ingresa tu número de *Cédula de Identidad*:",
        "no_encontrado": "🔍 No te encontré en el sistema. Para registrarte, por favor escribe tu *Nombre y Apellido* completo:",
        "preguntar_edad": "¿Cuántos *años* tienes?",
        "preguntar_telefono": "Ingresa tu número de *teléfono*:",
        "registro_exito": "🎊 ¡Registro exitoso! ¿Deseas agendar tu primera cita?",
        "error_registro": "❌ Error al registrarte vamos a intentarlo de nuevo:",
        "hola_paciente": "✅ ¡Hola como estas *{nombre}*!\n¿Qué deseas hacer?",
        "seleccionar_paso": "Selecciona el *{paso}*:",
        "fecha_seleccionada": "📅 Fecha: *{fecha}*",
        "preguntar_hora": "⏰ Escribe la *hora* que deseas para tu cita (ejemplo: 4:30 o 10):\n\n_Luego podrás elegir si es AM o PM._",
        "preguntar_ampm": "🕒 ¿La hora es *{hora}* AM o PM?",
        "preguntar_motivo": "¿Cuál es el *motivo* de tu consulta?",
        "horario_ocupado": "❌ Lo sentimos, ese horario (*{hora}*) ya está ocupado.\nPor favor vuelve a seleccionar una hora diferente.",
        "cita_agendada": "✅ *¡espere un momento por favor....!*\n\n📅 Fecha: {fecha}\n⏰ Hora: {hora}\n💡 Motivo: {motivo}\n\nEscribe /micita para ver o cancelar tu cita.",
        "error_agendar": "❌ Error al agendar:",
        "cancelar_operacion": "Operación cancelada. Escribe /start cuando lo necesites.",
        "sesion_expirada": "⚠️ Sesión expirada o no iniciada. Por favor usa /start.",
        "cita_cancelada_paciente": "✅ Tu cita del {fecha} a las {hora} ha sido *cancelada*.\nEscribe /start si necesitas algo más.",
        "no_permiso_cancelar": "🚫 No tienes permiso para cancelar esta cita.",
        "no_citas_activas": "📭 No tienes citas activas agendadas.",
        "detalle_mi_cita": "📋 *Tu próxima cita:*\n\n📅 Fecha: {fecha}\n⏰ Hora: {hora}\n💡 Motivo: {motivo}\nEstado: *{estado}*",
        "btn_cancelar_cita": "❌ Cancelar esta cita",
        "staff_nueva_cita": "📅 *Nueva Cita (vía Bot):*\n👤 {nombre}\n🗓️ {fecha} a las {hora}\n💡 Motivo: {motivo}",
        "staff_cita_cancelada": "⚠️ *Cita cancelada por el paciente:*\n👤 {nombre}\n📅 {fecha} a las {hora}",
        "resumen_datos": "📝 *RESUMEN DE TUS DATOS:*\n\n👤 *Nombre:* {nombre}\n🪪 *Cédula:* {cedula}\n🎂 *Edad:* {edad} años\n📞 *Teléfono:* {telefono}\n\n¿Los datos son correctos?",
        "confirmar_registro": "✅ Confirmar y Registrar",
        "cambiar_nombre": "✏️ Cambiar Nombre",
        "cambiar_edad": "✏️ Cambiar Edad",
        "cambiar_telefono": "✏️ Cambiar Teléfono",
        "cambiar_cedula": "✏️ Cambiar Cédula"
    }
    # ═══════════════════════════════════════════════════════════
    
    class BotExceptionHandler(telebot.ExceptionHandler):
        def handle(self, exception):
            print(f"[AVISO] Aviso del Bot: Micro-corte de red detectado y recuperado ({str(exception)[:40]}...)")
            return True
            
    bot = telebot.TeleBot(TOKEN, exception_handler=BotExceptionHandler())

    global bot_global, admin_id_global
    bot_global = bot
    admin_id_global = ADMIN_CHAT_ID

    print(f"[OK] SIC_Bot CONECTADO EXITOSAMENTE...")
    user_states = {}

    # ══════════════════════════════════
    # COMANDOS ESPECIALES (STAFF)
    # ══════════════════════════════════

    @bot.message_handler(commands=['id'])
    def get_id(message):
        bot.reply_to(message, f"Tu ID de Chat es: `{message.chat.id}`\n\nCopia este número y ponlo en ADMIN_CHAT_ID del archivo bot_telegram.py", parse_mode='Markdown')

    @bot.message_handler(commands=['hoy'])
    def get_today_appointments(message):
        chat_id = message.chat.id
        with app.app_context():
            hoy = datetime.now().date()
            citas_hoy = Cita.query.filter(db.func.date(Cita.fecha_cita) == hoy).order_by(Cita.fecha_cita.asc()).all()
            if not citas_hoy:
                bot.send_message(chat_id, "✅ No hay citas agendadas para hoy.")
                return
            respuesta = f"📅 *CITAS PARA HOY ({hoy}):*\n\n"
            for c in citas_hoy:
                hora = c.fecha_cita.strftime('%H:%M')
                respuesta += f"⏰ {hora} — {c.nombre_paciente} {c.apellido_paciente} ({c.estado})\n"
            bot.send_message(chat_id, respuesta, parse_mode='Markdown')

    @bot.message_handler(commands=['micita'])
    def ver_mi_cita(message):
        chat_id = message.chat.id
        with app.app_context():
            cita = Cita.query.filter_by(id_bot_sic=chat_id).filter(
                Cita.fecha_cita >= datetime.now(),
                Cita.estado != 'Cancelada'
            ).order_by(Cita.fecha_cita.asc()).first()

            if not cita:
                bot.send_message(chat_id, MSJ["no_citas_activas"])
                return

            fecha = cita.fecha_cita.strftime('%d/%m/%Y')
            hora = cita.fecha_cita.strftime('%H:%M')
            texto = MSJ["detalle_mi_cita"].format(
                fecha=fecha, hora=hora, motivo=cita.motivo or '---', estado=cita.estado
            )
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(
                MSJ["btn_cancelar_cita"], callback_data=f"cancelar_cita_{cita.id_cita}"
            ))
            bot.send_message(chat_id, texto, parse_mode='Markdown', reply_markup=markup)

    # ══════════════════════════════════
    # CALLBACKS (BOTONES INLINE)
    # ══════════════════════════════════

    @bot.callback_query_handler(func=CalendarioClinica.func())
    def cal(c):
        chat_id = c.message.chat.id
        result, key, step = obtener_calendario().process(c.data)
        if not result and key:
            pasos_es = {"year": "Año", "month": "Mes", "day": "Día"}
            paso_actual = pasos_es.get(LSTEP[step], LSTEP[step])
            bot.edit_message_text(MSJ["seleccionar_paso"].format(paso=paso_actual),
                                  chat_id, c.message.message_id, 
                                  reply_markup=key, parse_mode='Markdown')
        elif result:
            if chat_id in user_states:
                user_states[chat_id]['datos']['fecha'] = str(result)
                user_states[chat_id]['step'] = 'WAITING_TIME'
                bot.edit_message_text(MSJ["fecha_seleccionada"].format(fecha=result),
                                      chat_id, c.message.message_id, parse_mode='Markdown')
                bot.send_message(chat_id, MSJ["preguntar_hora"], parse_mode='Markdown')
            else:
                bot.send_message(chat_id, MSJ["sesion_expirada"])

    @bot.callback_query_handler(func=lambda call: True)
    def responder_clicks(call):
        chat_id = call.message.chat.id
        if call.data.startswith("cancelar_cita_"):
            id_cita = int(call.data.split("_")[-1])
            with app.app_context():
                cita = Cita.query.get(id_cita)
                if cita and str(cita.id_bot_sic) == str(chat_id):
                    cita.estado = 'Cancelada'
                    db.session.commit()
                    fecha = cita.fecha_cita.strftime('%d/%m/%Y')
                    hora = cita.fecha_cita.strftime('%H:%M')
                    bot.answer_callback_query(call.id, "Anulada")
                    bot.edit_message_text(
                        MSJ["cita_cancelada_paciente"].format(fecha=fecha, hora=hora),
                        chat_id, call.message.message_id, parse_mode='Markdown'
                    )
                    notificar_staff(MSJ["staff_cita_cancelada"].format(
                        nombre=f"{cita.nombre_paciente} {cita.apellido_paciente}", fecha=fecha, hora=hora
                    ))
                else:
                    bot.answer_callback_query(call.id, MSJ["no_permiso_cancelar"])
            return

        if call.data.startswith("hora_"):
            hora_seleccionada = call.data.split("_")[1]
            bot.answer_callback_query(call.id, "OK")
            if chat_id in user_states:
                user_states[chat_id]['datos']['hora'] = hora_seleccionada
                user_states[chat_id]['step'] = 'WAITING_MOTIVO'
                bot.edit_message_text(f"⏰ Hora: *{hora_seleccionada}*",
                                      chat_id, call.message.message_id, parse_mode='Markdown')
                bot.send_message(chat_id, MSJ["preguntar_motivo"], parse_mode='Markdown')
            else:
                bot.send_message(chat_id, MSJ["sesion_expirada"])
            return

        # ════════════════════════════════════
        # CALLBACKS DE CONFIRMACIÓN DE REGISTRO
        # ════════════════════════════════════
        if chat_id not in user_states: return
        state = user_states[chat_id]

        if call.data == "conf_si":
            bot.answer_callback_query(call.id, "Registrando...")
            try:
                # Doble validación de seguridad de la edad (Rango 0-120)
                edad_val = int(state['datos']['edad'])
                if edad_val < 0 or edad_val > 120:
                    raise ValueError("Edad fuera de rango")

                with app.app_context():
                    nuevo = Historial_Medico(
                        cedula=str(state['datos']['cedula']).strip(),
                        nombre_paciente=state['datos']['nombre_completo'],
                        edad=edad_val,
                        telefono=state['datos']['telefono']
                    )
                    db.session.add(nuevo)
                    db.session.commit()
                    state['datos']['nombre'] = state['datos']['nombre_completo']
                    state['step'] = 'SHOW_MENU'
                    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
                    markup.add("📅 Agendar Cita", "❌ Salir")
                    bot.edit_message_text("✅ Datos guardados correctamente.", chat_id, call.message.message_id)
                    bot.send_message(chat_id, MSJ["registro_exito"], reply_markup=markup)
            except Exception as e:
                db.session.rollback()
                print(f"[ERROR REGISTRO BOT]: {e}")
                bot.send_message(chat_id, 
                    "⚠️ *No se pudo completar el registro.*\n\n"
                    "Es posible que los datos sea incorrectos o que la Cédula ya exista.\n"
                    "Por favor, revisa tus datos o inténtalo de nuevo con /start.", 
                    parse_mode='Markdown')
                if chat_id in user_states:
                    del user_states[chat_id]

        elif call.data == "conf_no":
            bot.answer_callback_query(call.id, "Cancelado")
            bot.edit_message_text(MSJ["cancelar_operacion"], chat_id, call.message.message_id)
            del user_states[chat_id]

        elif call.data == "edit_nombre":
            state['step'] = 'WAITING_NAME'
            bot.edit_message_text("✏️ Escribe de nuevo tu *Nombre y Apellido*:", chat_id, call.message.message_id, parse_mode='Markdown')

        elif call.data == "edit_cedula":
            state['step'] = 'WAITING_CEDULA'
            bot.edit_message_text("✏️ Escribe de nuevo tu *Cédula*:", chat_id, call.message.message_id, parse_mode='Markdown')

        elif call.data == "edit_edad":
            state['step'] = 'WAITING_AGE'
            bot.edit_message_text("✏️ Escribe de nuevo tu *Edad*:", chat_id, call.message.message_id, parse_mode='Markdown')

        elif call.data == "edit_tel":
            state['step'] = 'WAITING_PHONE'
            bot.edit_message_text("✏️ Escribe de nuevo tu *Teléfono*:", chat_id, call.message.message_id, parse_mode='Markdown')
        
        elif call.data.startswith("ampm_"):
            # Procesar selección AM/PM
            tipo = call.data.split("_")[1] # am o pm
            bot.answer_callback_query(call.id, "Hora confirmada")
            if chat_id in user_states:
                hora_temp = user_states[chat_id]['datos']['hora_temp']
                h, m = map(int, hora_temp.split(":"))
                
                # Convertir a 24h
                if tipo == "pm" and h < 12: h += 12
                if tipo == "am" and h == 12: h = 0
                
                hora_final = f"{h:02d}:{m:02d}"
                
                # --- VALIDACIÓN DE HORA PASADA (AJUSTADO A VENEZUELA UTC-4) ---
                fecha_sel = user_states[chat_id]['datos']['fecha']
                obj_fecha_hora = datetime.strptime(f"{fecha_sel} {hora_final}", "%Y-%m-%d %H:%M")
                
                ahora_venezuela = datetime.now() - timedelta(hours=4)
                print(f"DEBUG: Cliente eligio {obj_fecha_hora} | Servidor cree que es {ahora_venezuela}")

                if obj_fecha_hora < ahora_venezuela:
                    bot.answer_callback_query(call.id, "⚠️ Hora inválida") # Detener el círculo de carga
                    bot.send_message(chat_id, "⚠️ *Esta hora ya ha pasado para el día de hoy.* ⏰\nPor favor, selecciona una hora diferente.", parse_mode='Markdown')
                    user_states[chat_id]['step'] = 'WAITING_TIME'
                    bot.send_message(chat_id, "⏰ Escribe de nuevo la hora que deseas (ejemplo: 4:30):")
                    return # Importante retornar para no avanzar al siguiente paso
                # -----------------------------------------------------------

                user_states[chat_id]['datos']['hora'] = hora_final
                user_states[chat_id]['step'] = 'WAITING_MOTIVO'
                
                sufijo = "AM" if tipo == "am" else "PM"
                bot.edit_message_text(f"⏰ Hora confirmada: *{hora_temp} {sufijo}*",
                                      chat_id, call.message.message_id, parse_mode='Markdown')
                bot.send_message(chat_id, MSJ["preguntar_motivo"], parse_mode='Markdown')
            else:
                bot.send_message(chat_id, MSJ["sesion_expirada"])
            return

    # ══════════════════════════════════
    # FLUJO DE CONVERSACIÓN
    # ══════════════════════════════════

    @bot.message_handler(commands=['start', 'help'])
    def send_welcome(message):
        chat_id = message.chat.id
        user_states[chat_id] = {'step': 'WAITING_CEDULA', 'datos': {}}
        bot.send_message(chat_id, MSJ["bienvenida"], parse_mode='Markdown')

    @bot.message_handler(func=lambda message: True)
    def handle_messages(message):
        chat_id = message.chat.id
        texto = message.text.strip()

        if chat_id not in user_states:
            send_welcome(message)
            return

        state = user_states[chat_id]
        step = state['step']

        with app.app_context():

            # ════════════════════════════════════
            # 0. COMANDOS GLOBALES DE INTERRUPCIÓN
            # ════════════════════════════════════
            if texto in ["❌ Cancelar", "❌ Salir", "/start", "/cancel"]:
                bot.send_message(chat_id, MSJ["cancelar_operacion"],
                                 reply_markup=types.ReplyKeyboardRemove())
                if chat_id in user_states:
                    del user_states[chat_id]
                return

            # PASO 1: VALIDAR CÉDULA
            if step == 'WAITING_CEDULA':
                if not texto.isdigit():
                    bot.send_message(chat_id, "⚠️ La cédula debe contener solo números. Por favor, ingrésala de nuevo:")
                    return
                paciente = Historial_Medico.query.filter_by(cedula=texto).first()
                state['datos']['cedula'] = texto
                if paciente:
                    state['datos']['nombre'] = paciente.nombre_paciente
                    state['step'] = 'SHOW_MENU'
                    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
                    markup.add("📅 Agendar Cita", "❌ Salir")
                    bot.send_message(chat_id,
                        MSJ["hola_paciente"].format(nombre=paciente.nombre_paciente),
                        reply_markup=markup, parse_mode='Markdown')
                else:
                    state['step'] = 'WAITING_NAME'
                    bot.send_message(chat_id, MSJ["no_encontrado"], parse_mode='Markdown')

            # PASO 2: REGISTRO NUEVO PACIENTE
            elif step == 'WAITING_NAME':
                state['datos']['nombre_completo'] = texto
                state['step'] = 'WAITING_AGE'
                bot.send_message(chat_id, MSJ["preguntar_edad"], parse_mode='Markdown')

            elif step == 'WAITING_AGE':
                if not texto.isdigit() or int(texto) > 120 or int(texto) < 0:
                    bot.send_message(chat_id, "⚠️ Por favor ingresa una *edad válida* (número entre 0 y 120):", parse_mode='Markdown')
                    return
                state['datos']['edad'] = int(texto)
                state['step'] = 'WAITING_PHONE'
                bot.send_message(chat_id, MSJ["preguntar_telefono"], parse_mode='Markdown')

            elif step == 'WAITING_PHONE':
                state['datos']['telefono'] = texto
                state['step'] = 'WAITING_CONFIRMATION'
                
                # Generar botones de edición
                markup = types.InlineKeyboardMarkup(row_width=2)
                btn_si = types.InlineKeyboardButton(MSJ["confirmar_registro"], callback_data="conf_si")
                btn_no = types.InlineKeyboardButton("❌ Cancelar", callback_data="conf_no")
                btn_e_nom = types.InlineKeyboardButton(MSJ["cambiar_nombre"], callback_data="edit_nombre")
                btn_e_ced = types.InlineKeyboardButton(MSJ["cambiar_cedula"], callback_data="edit_cedula")
                btn_e_eda = types.InlineKeyboardButton(MSJ["cambiar_edad"], callback_data="edit_edad")
                btn_e_tel = types.InlineKeyboardButton(MSJ["cambiar_telefono"], callback_data="edit_tel")
                
                markup.add(btn_si)
                markup.add(btn_e_nom, btn_e_ced)
                markup.add(btn_e_eda, btn_e_tel)
                markup.add(btn_no)

                resumen = MSJ["resumen_datos"].format(
                    nombre=state['datos']['nombre_completo'],
                    cedula=state['datos']['cedula'],
                    edad=state['datos']['edad'],
                    telefono=state['datos']['telefono']
                )
                bot.send_message(chat_id, resumen, reply_markup=markup, parse_mode='Markdown')

            elif step == 'WAITING_CONFIRMATION':
                # Si el usuario escribe algo en lugar de usar botones
                bot.send_message(chat_id, "Por favor, usa los botones anteriores para confirmar o editar tus datos.")
                return

            # PASO 3: MENÚ PRINCIPAL
            elif texto in ["📅 Agendar Cita", "si", "sí", "agendar", "Si", "Sí", "Agendar"]:
                state['step'] = 'WAITING_DATE'
                calendar, cal_step = obtener_calendario().build()
                pasos_es = {"year": "Año", "month": "Mes", "day": "Día"}
                paso_inicial = pasos_es.get(LSTEP[cal_step], LSTEP[cal_step])
                bot.send_message(chat_id, MSJ["seleccionar_paso"].format(paso=paso_inicial),
                                 reply_markup=calendar, parse_mode='Markdown')

            # PASO 4: FECHA (fallback texto)
            elif step == 'WAITING_DATE':
                try:
                    datetime.strptime(texto, '%Y-%m-%d')
                    state['datos']['fecha'] = texto
                    state['step'] = 'WAITING_TIME'
                    bot.send_message(chat_id, MSJ["preguntar_hora"], parse_mode='Markdown')
                except ValueError:
                    bot.send_message(chat_id, "Formato inválido. Usa el calendario.")

            # PASO 5: HORA (Procesamiento inteligente)
            elif step == 'WAITING_TIME':
                # Limpiar texto de espacios y caracteres extra
                t = texto.lower().replace(" ", "").replace(".", "")
                
                # Formatear: ej "430" -> "4:30", "10" -> "10:00"
                solo_nums = "".join([c for c in t if c.isdigit()])
                
                if not solo_nums:
                    bot.send_message(chat_id, "⚠️ Por favor ingresa una hora válida (ej: 4:30 o 430)")
                    return
                
                if len(solo_nums) <= 2: # "4" o "10"
                    h, m = solo_nums, "00"
                elif len(solo_nums) == 3: # "430"
                    h, m = solo_nums[0], solo_nums[1:]
                else: # "1030"
                    h, m = solo_nums[:2], solo_nums[2:]
                
                h_int = int(h)
                m_int = int(m)
                
                if h_int > 12 or m_int > 59:
                    bot.send_message(chat_id, "⚠️ Por favor ingresa una hora en formato 12h (1-12) seguida de los minutos.")
                    return
                
                hora_formateada = f"{h_int:02d}:{m_int:02d}"
                state['datos']['hora_temp'] = hora_formateada
                state['step'] = 'WAITING_AMPM'
                
                # Botones AM / PM
                markup = types.InlineKeyboardMarkup()
                markup.add(
                    types.InlineKeyboardButton("☀️ AM", callback_data="ampm_am"),
                    types.InlineKeyboardButton("🌙 PM", callback_data="ampm_pm")
                )
                
                bot.send_message(chat_id, MSJ["preguntar_ampm"].format(hora=hora_formateada), 
                                 reply_markup=markup, parse_mode='Markdown')

            elif step == 'WAITING_AMPM':
                bot.send_message(chat_id, "Por favor selecciona AM o PM en los botones de arriba.")
                return

            # PASO 6: MOTIVO Y GUARDADO FINAL
            elif step == 'WAITING_MOTIVO':
                state['datos']['motivo'] = texto
                try:
                    obj_fecha = datetime.strptime(
                        f"{state['datos']['fecha']} {state['datos']['hora']}", '%Y-%m-%d %H:%M'
                    )

                    # --- VALIDACIÓN EXTRA DE SEGURIDAD (UTC-4) ---
                    ahora_venezuela = datetime.now() - timedelta(hours=4)
                    if obj_fecha < ahora_venezuela:
                        bot.send_message(chat_id, "❌ *Lo sentimos, el tiempo ha pasado.* \nPor favor, inicia de nuevo con /start para elegir una hora válida.", parse_mode='Markdown')
                        if chat_id in user_states:
                            del user_states[chat_id]
                        return
                    # ---------------------------------------------

                    # ⚠️ VALIDACIÓN DE CONFLICTO
                    conflicto = Cita.query.filter_by(fecha_cita=obj_fecha).first()
                    if conflicto:
                        bot.send_message(chat_id,
                            MSJ["horario_ocupado"].format(hora=state['datos']['hora']),
                            parse_mode='Markdown')
                        state['step'] = 'WAITING_DATE'
                        calendar, cal_step = obtener_calendario().build()
                        bot.send_message(chat_id, f"Selecciona otra fecha:", reply_markup=calendar)
                        return

                    n_p = state['datos']['nombre'].split(" ")
                    nueva_cita = Cita(
                        nombre_paciente=n_p[0],
                        apellido_paciente=" ".join(n_p[1:]) if len(n_p) > 1 else "S/A",
                        cedula=state['datos']['cedula'],
                        fecha_cita=obj_fecha,
                        motivo=state['datos']['motivo'],
                        estado='Pendiente',
                        id_bot_sic=chat_id
                    )
                    db.session.add(nueva_cita)
                    db.session.commit()

                    motivo_cita = state['datos'].get('motivo', '---').strip()

                    bot.send_message(chat_id,
                        MSJ["cita_agendada"].format(
                            fecha=state['datos']['fecha'], 
                            hora=state['datos']['hora'], 
                            motivo=motivo_cita
                        ),
                        parse_mode='Markdown', reply_markup=types.ReplyKeyboardRemove())

                    notificar_staff(MSJ["staff_nueva_cita"].format(
                        nombre=state['datos']['nombre'],
                        fecha=state['datos']['fecha'],
                        hora=state['datos']['hora'],
                        motivo=motivo_cita
                    ))
                    del user_states[chat_id]

                except Exception as e:
                    db.session.rollback()
                    bot.send_message(chat_id, f"{MSJ['error_agendar']} {e}")

    bot.infinity_polling()


# ═══════════════════════════════════════════════════════════
# FUNCIONES GLOBALES DE NOTIFICACIÓN
# ═══════════════════════════════════════════════════════════
bot_global = None
admin_id_global = None

def notificar_staff(mensaje):
    """Notifica al administrador de la clínica."""
    if bot_global and admin_id_global and str(admin_id_global).lstrip('-').isdigit():
        try:
            bot_global.send_message(admin_id_global, mensaje, parse_mode='Markdown')
        except Exception as e:
            print(f"[BOT] Error notificando staff: {e}")

def notificar_paciente(chat_id, mensaje):
    """Notifica a un paciente específico por su Chat ID de Telegram."""
    if bot_global and chat_id:
        try:
            bot_global.send_message(chat_id, mensaje, parse_mode='Markdown')
        except Exception as e:
            print(f"[BOT] Error notificando paciente {chat_id}: {e}")

def start_bot_thread(app, db, Cita, Historial_Medico):
    bot_thread = threading.Thread(target=iniciar_bot_sic, args=(app, db, Cita, Historial_Medico))
    bot_thread.daemon = True
    bot_thread.start()
