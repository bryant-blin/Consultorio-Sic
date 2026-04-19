from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from modelo.usuarios import db, Login, Rol, Usuario

def auth_login():
    # Consultamos todos los roles para el select
    roles = Rol.query.all()

    if request.method == 'POST':
        user_input = request.form.get('username')
        pass_input = request.form.get('password')
        rol_input = request.form.get('rol') # El ID del rol seleccionado

        # Buscamos en la tabla 'login'
        user_auth = Login.query.filter_by(usuario=user_input, id_rol=rol_input).first()

        # Validación directa
        if user_auth and user_auth.contrasena == pass_input:
            login_user(user_auth)
            return redirect(url_for('dashboard'))
        
        flash("Usuario, clave o rol incorrectos")
    
    return render_template('acceso.html', roles=roles)

def auth_logout():
    logout_user()
    return redirect(url_for('auth_login'))

def auth_registro():
    # Consultamos roles para que el usuario elija
    roles = Rol.query.all()

    if request.method == 'POST':
        correo = request.form.get('correo')
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        usuario_nick = request.form.get('username')
        clave = request.form.get('password')
        id_rol = request.form.get('rol')
        master_key = request.form.get('master_key')

        # VALIDACIÓN DE CLAVE MAESTRA
        if master_key != "30821491":
            flash("❌ Clave Maestra de Seguridad incorrecta. Registro denegado.", "error")
            return render_template('registro.html', roles=roles)

        # 1. Crear el perfil
        nuevo_usuario = Usuario(correo_electronico=correo, nombres=nombre, apellidos=apellido)
        db.session.add(nuevo_usuario)
        db.session.flush() # Para obtener el ID

        # 2. Crear las credenciales
        nuevo_login = Login(id_usuario=nuevo_usuario.id_usuario, id_rol=id_rol, usuario=usuario_nick, contrasena=clave)
        db.session.add(nuevo_login)
        db.session.commit()

        flash("¡Cuenta creada correctamente!")
        return redirect(url_for('auth_login'))
        
    return render_template('registro.html', roles=roles)

def auth_recuperar():
    if request.method == 'POST':
        email_buscado = request.form.get('email')
        nueva_clave = request.form.get('nueva_password')

        # Buscamos en Usuario porque ahí está el correo
        perfil = Usuario.query.filter_by(correo_electronico=email_buscado).first()

        if perfil and perfil.login_info:
            # Actualizamos la clave en el login vinculado
            perfil.login_info.contrasena = nueva_clave
            db.session.commit()
            flash("¡Contraseña actualizada! Ya puedes entrar con tu nueva clave.")
            return redirect(url_for('auth_login'))
        else:
            flash("El correo no está registrado en el sistema.")
            
    return render_template('recuperar.html')