import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io
import os

# Configuración de la página
st.set_page_config(
    page_title="Sistema de Tickets - Soporte TI UTP",
    page_icon="🎫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Base de datos SQLite (se crea automáticamente)
DB_NAME = 'soporte_ti.db'

def conectar_bd():
    """Conectar a la base de datos SQLite"""
    return sqlite3.connect(DB_NAME)

def inicializar_bd():
    """Crear tablas si no existen"""
    conn = conectar_bd()
    cursor = conn.cursor()
    
    # Tabla de tickets
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
        usuario_solicitante TEXT NOT NULL,
        email TEXT NOT NULL,
        categoria TEXT NOT NULL,
        prioridad TEXT NOT NULL,
        titulo TEXT NOT NULL,
        descripcion TEXT NOT NULL,
        estado TEXT DEFAULT 'Abierto',
        tecnico_asignado TEXT DEFAULT 'Sin asignar',
        solucion TEXT DEFAULT '',
        fecha_cierre DATETIME,
        sede TEXT DEFAULT 'Lima Sur'
    )
    ''')
    
    # Tabla de inventario
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS inventario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo_equipo TEXT UNIQUE NOT NULL,
        tipo_equipo TEXT NOT NULL,
        marca TEXT NOT NULL,
        modelo TEXT NOT NULL,
        numero_serie TEXT UNIQUE,
        ubicacion TEXT NOT NULL,
        estado TEXT DEFAULT 'Activo',
        responsable TEXT,
        fecha_adquisicion DATE,
        observaciones TEXT
    )
    ''')
    
    # Tabla de técnicos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tecnicos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        especialidad TEXT,
        telefono TEXT,
        email TEXT,
        estado TEXT DEFAULT 'Activo'
    )
    ''')
    
    # Insertar datos iniciales si las tablas están vacías
    cursor.execute('SELECT COUNT(*) FROM tecnicos')
    if cursor.fetchone()[0] == 0:
        tecnicos_data = [
            ('Juan Pérez', 'Hardware y Redes', '999-111-001', 'juan.perez@utp.edu.pe', 'Activo'),
            ('María García', 'Software y Sistemas', '999-111-002', 'maria.garcia@utp.edu.pe', 'Activo'),
            ('Carlos López', 'Infraestructura TI', '999-111-003', 'carlos.lopez@utp.edu.pe', 'Activo'),
            ('Ana Rodríguez', 'Soporte General', '999-111-004', 'ana.rodriguez@utp.edu.pe', 'Activo')
        ]
        cursor.executemany(
            'INSERT INTO tecnicos (nombre, especialidad, telefono, email, estado) VALUES (?, ?, ?, ?, ?)',
            tecnicos_data
        )
    
    cursor.execute('SELECT COUNT(*) FROM inventario')
    if cursor.fetchone()[0] == 0:
        inventario_data = [
            ('PC-LAB-001', 'Desktop', 'HP', 'EliteDesk 800', 'HP001234', 'Laboratorio 1', 'Activo', 'Prof. Roberto Silva', '2023-01-15', 'Equipo en buen estado'),
            ('PC-LAB-002', 'Desktop', 'Dell', 'OptiPlex 7090', 'DL001235', 'Laboratorio 1', 'Activo', 'Prof. Roberto Silva', '2023-01-15', 'Equipo nuevo'),
            ('PROJ-AUL-001', 'Proyector', 'Epson', 'EB-X41', 'EP001236', 'Aula 201', 'Activo', 'Prof. Carmen Torres', '2022-08-20', 'Mantenimiento trimestral'),
            ('IMP-ADM-001', 'Impresora', 'Canon', 'ImageClass MF3010', 'CN001237', 'Administración', 'Activo', 'Secretaria Ana', '2022-06-10', 'Cambio de tóner reciente'),
            ('LAP-MOB-001', 'Laptop', 'Lenovo', 'ThinkPad E14', 'LN001238', 'Soporte Móvil', 'Activo', 'Técnico Juan', '2023-03-01', 'Para soporte en campo')
        ]
        cursor.executemany(
            'INSERT INTO inventario (codigo_equipo, tipo_equipo, marca, modelo, numero_serie, ubicacion, estado, responsable, fecha_adquisicion, observaciones) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            inventario_data
        )
    
    cursor.execute('SELECT COUNT(*) FROM tickets')
    if cursor.fetchone()[0] == 0:
        tickets_data = [
            ('Prof. Roberto Silva', 'roberto.silva@utp.edu.pe', 'Hardware', 'Alta', 'PC no enciende en Lab 1', 'La computadora PC-LAB-001 no enciende al presionar el botón de power. Se escucha un sonido extraño al conectar.', 'En_Proceso', 'Juan Pérez', 'Revisando fuente de poder'),
            ('Carmen Torres', 'carmen.torres@utp.edu.pe', 'Hardware', 'Media', 'Proyector sin imagen', 'El proyector del aula 201 enciende pero no muestra imagen. Cable HDMI conectado correctamente.', 'Abierto', 'Carlos López', ''),
            ('Ana Secretaria', 'ana.sec@utp.edu.pe', 'Impresora', 'Baja', 'Impresora no imprime', 'La impresora Canon de administración no responde a trabajos de impresión. Luz roja parpadeante.', 'Pendiente_Usuario', 'María García', 'Esperando cambio de cartucho'),
            ('Estudiante Mario', 'mario.est@utp.edu.pe', 'Software', 'Media', 'No puede acceder al sistema académico', 'Error al intentar ingresar credenciales en el portal académico. Mensaje de usuario no encontrado.', 'Abierto', 'Ana Rodríguez', ''),
            ('Prof. Luis Mendoza', 'luis.mendoza@utp.edu.pe', 'Red', 'Crítica', 'Sin conexión a internet en aula 305', 'Toda el aula 305 sin acceso a internet. Afecta clase en curso con 30 estudiantes.', 'En_Proceso', 'Carlos López', 'Verificando switch de red')
        ]
        cursor.executemany(
            'INSERT INTO tickets (usuario_solicitante, email, categoria, prioridad, titulo, descripcion, estado, tecnico_asignado, solucion) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
            tickets_data
        )
    
    conn.commit()
    conn.close()

def ejecutar_query(query, params=None, fetch=True):
    """Ejecutar query en la base de datos"""
    try:
        conn = conectar_bd()
        cursor = conn.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if fetch:
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
            result = [dict(zip(columns, row)) for row in rows]
        else:
            conn.commit()
            result = cursor.rowcount
        
        conn.close()
        return result
    except Exception as e:
        st.error(f"Error en la consulta: {e}")
        return None

def obtener_tecnicos():
    """Obtener lista de técnicos activos"""
    query = "SELECT nombre FROM tecnicos WHERE estado = 'Activo'"
    result = ejecutar_query(query)
    return [row['nombre'] for row in result] if result else []

def crear_ticket(datos):
    """Crear nuevo ticket en la base de datos"""
    query = """
    INSERT INTO tickets (usuario_solicitante, email, categoria, prioridad, titulo, descripcion, tecnico_asignado)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    params = (
        datos['usuario'], datos['email'], datos['categoria'], 
        datos['prioridad'], datos['titulo'], datos['descripcion'], 
        datos['tecnico']
    )
    return ejecutar_query(query, params, fetch=False)

def obtener_tickets(filtro_estado=None):
    """Obtener tickets con filtros opcionales"""
    if filtro_estado:
        query = "SELECT * FROM tickets WHERE estado = ? ORDER BY fecha_creacion DESC"
        return ejecutar_query(query, (filtro_estado,))
    else:
        query = "SELECT * FROM tickets ORDER BY fecha_creacion DESC"
        return ejecutar_query(query)

def actualizar_ticket(ticket_id, estado, solucion=None, tecnico=None):
    """Actualizar estado y solución de un ticket"""
    fecha_cierre = datetime.now().isoformat() if estado in ['Resuelto', 'Cerrado'] else None
    
    query = """
    UPDATE tickets 
    SET estado = ?, solucion = ?, tecnico_asignado = ?, fecha_cierre = ?
    WHERE id = ?
    """
    params = (estado, solucion or '', tecnico or 'Sin asignar', fecha_cierre, ticket_id)
    return ejecutar_query(query, params, fetch=False)

def obtener_inventario():
    """Obtener inventario completo"""
    query = "SELECT * FROM inventario ORDER BY codigo_equipo"
    return ejecutar_query(query)

def agregar_equipo(datos):
    """Agregar nuevo equipo al inventario"""
    query = """
    INSERT INTO inventario (codigo_equipo, tipo_equipo, marca, modelo, numero_serie, 
                          ubicacion, estado, responsable, fecha_adquisicion, observaciones)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    params = (
        datos['codigo'], datos['tipo'], datos['marca'], datos['modelo'],
        datos['serie'], datos['ubicacion'], datos['estado'], datos['responsable'],
        datos['fecha'], datos['observaciones']
    )
    return ejecutar_query(query, params, fetch=False)

def obtener_metricas():
    """Obtener métricas del dashboard"""
    queries = {
        'total_tickets': "SELECT COUNT(*) as total FROM tickets",
        'tickets_abiertos': "SELECT COUNT(*) as total FROM tickets WHERE estado IN ('Abierto', 'En_Proceso')",
        'tickets_cerrados_hoy': """
            SELECT COUNT(*) as total FROM tickets 
            WHERE DATE(fecha_cierre) = DATE('now') AND estado IN ('Resuelto', 'Cerrado')
        """,
        'tickets_por_estado': """
            SELECT estado, COUNT(*) as cantidad FROM tickets 
            GROUP BY estado ORDER BY cantidad DESC
        """,
        'tickets_por_categoria': """
            SELECT categoria, COUNT(*) as cantidad FROM tickets 
            GROUP BY categoria ORDER BY cantidad DESC
        """,
        'tickets_por_tecnico': """
            SELECT tecnico_asignado, COUNT(*) as cantidad FROM tickets 
            WHERE tecnico_asignado != 'Sin asignar'
            GROUP BY tecnico_asignado ORDER BY cantidad DESC
        """
    }
    
    metricas = {}
    for key, query in queries.items():
        result = ejecutar_query(query)
        metricas[key] = result
    
    return metricas

def mostrar_dashboard():
    """Dashboard principal con métricas"""
    st.header("📊 Dashboard de Soporte TI")
    
    metricas = obtener_metricas()
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total = metricas['total_tickets'][0]['total'] if metricas['total_tickets'] else 0
        st.metric("📋 Total Tickets", total)
    
    with col2:
        abiertos = metricas['tickets_abiertos'][0]['total'] if metricas['tickets_abiertos'] else 0
        st.metric("🔴 Tickets Abiertos", abiertos)
    
    with col3:
        cerrados_hoy = metricas['tickets_cerrados_hoy'][0]['total'] if metricas['tickets_cerrados_hoy'] else 0
        st.metric("✅ Cerrados Hoy", cerrados_hoy)
    
    with col4:
        if total > 0:
            porcentaje_resueltos = round((total - abiertos) / total * 100, 1)
        else:
            porcentaje_resueltos = 0
        st.metric("📈 % Resolución", f"{porcentaje_resueltos}%")
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Tickets por Estado")
        if metricas['tickets_por_estado']:
            df_estado = pd.DataFrame(metricas['tickets_por_estado'])
            fig = px.pie(df_estado, names='estado', values='cantidad', 
                        color_discrete_sequence=px.colors.qualitative.Set3)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📋 Tickets por Categoría")
        if metricas['tickets_por_categoria']:
            df_categoria = pd.DataFrame(metricas['tickets_por_categoria'])
            fig = px.bar(df_categoria, x='categoria', y='cantidad',
                        color='cantidad', color_continuous_scale='Blues')
            st.plotly_chart(fig, use_container_width=True)
    
    # Carga de trabajo por técnico
    st.subheader("👨‍💻 Carga de Trabajo por Técnico")
    if metricas['tickets_por_tecnico']:
        df_tecnico = pd.DataFrame(metricas['tickets_por_tecnico'])
        fig = px.bar(df_tecnico, x='tecnico_asignado', y='cantidad',
                    title="Tickets Asignados por Técnico")
        st.plotly_chart(fig, use_container_width=True)

def crear_nuevo_ticket():
    """Formulario para crear nuevo ticket"""
    st.header("📝 Crear Nuevo Ticket de Soporte")
    
    with st.form("nuevo_ticket"):
        col1, col2 = st.columns(2)
        
        with col1:
            usuario = st.text_input("👤 Usuario Solicitante *", placeholder="Ej: Prof. Juan Pérez")
            email = st.text_input("📧 Email *", placeholder="juan.perez@utp.edu.pe")
            categoria = st.selectbox("📂 Categoría *", 
                                   ["Hardware", "Software", "Red", "Cuenta_Usuario", "Impresora", "Otro"])
        
        with col2:
            prioridad = st.selectbox("⚡ Prioridad *", 
                                   ["Baja", "Media", "Alta", "Crítica"])
            tecnico = st.selectbox("👨‍🔧 Técnico Asignado", 
                                 ["Sin asignar"] + obtener_tecnicos())
            titulo = st.text_input("📋 Título del Problema *", 
                                 placeholder="Descripción breve del problema")
        
        descripcion = st.text_area("📝 Descripción Detallada *", 
                                 placeholder="Explique el problema con detalle...",
                                 height=100)
        
        submitted = st.form_submit_button("🎫 Crear Ticket", type="primary")
        
        if submitted:
            if usuario and email and titulo and descripcion:
                datos_ticket = {
                    'usuario': usuario,
                    'email': email,
                    'categoria': categoria,
                    'prioridad': prioridad,
                    'titulo': titulo,
                    'descripcion': descripcion,
                    'tecnico': tecnico
                }
                
                if crear_ticket(datos_ticket):
                    st.success("✅ Ticket creado exitosamente!")
                    st.balloons()
                else:
                    st.error("❌ Error al crear el ticket")
            else:
                st.error("⚠️ Por favor complete todos los campos obligatorios (*)")

def gestionar_tickets():
    """Gestión y seguimiento de tickets"""
    st.header("📋 Gestión de Tickets")
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    with col1:
        filtro_estado = st.selectbox("Filtrar por Estado", 
                                   ["Todos", "Abierto", "En_Proceso", "Pendiente_Usuario", "Resuelto", "Cerrado"])
    
    # Obtener tickets
    if filtro_estado == "Todos":
        tickets = obtener_tickets()
    else:
        tickets = obtener_tickets(filtro_estado)
    
    if tickets:
        for ticket in tickets:
            with st.expander(f"🎫 #{ticket['id']} - {ticket['titulo']} ({ticket['estado']})"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**Usuario:** {ticket['usuario_solicitante']}")
                    st.write(f"**Email:** {ticket['email']}")
                    st.write(f"**Categoría:** {ticket['categoria']}")
                    st.write(f"**Prioridad:** {ticket['prioridad']}")
                    st.write(f"**Fecha:** {ticket['fecha_creacion']}")
                    st.write(f"**Descripción:** {ticket['descripcion']}")
                    if ticket['solucion']:
                        st.write(f"**Solución:** {ticket['solucion']}")
                
                with col2:
                    estados = ["Abierto", "En_Proceso", "Pendiente_Usuario", "Resuelto", "Cerrado"]
                    estado_actual = ticket['estado']
                    indice_estado = estados.index(estado_actual) if estado_actual in estados else 0
                    
                    nuevo_estado = st.selectbox(f"Estado #{ticket['id']}", 
                                              estados,
                                              index=indice_estado,
                                              key=f"estado_{ticket['id']}")
                    
                    tecnicos_list = ["Sin asignar"] + obtener_tecnicos()
                    tecnico_actual = ticket['tecnico_asignado']
                    indice_tecnico = tecnicos_list.index(tecnico_actual) if tecnico_actual in tecnicos_list else 0
                    
                    nuevo_tecnico = st.selectbox(f"Técnico #{ticket['id']}", 
                                               tecnicos_list,
                                               index=indice_tecnico,
                                               key=f"tecnico_{ticket['id']}")
                    
                    solucion = st.text_area(f"Solución #{ticket['id']}", 
                                          value=ticket['solucion'] or "",
                                          key=f"solucion_{ticket['id']}")
                    
                    if st.button(f"Actualizar #{ticket['id']}", key=f"btn_{ticket['id']}"):
                        if actualizar_ticket(ticket['id'], nuevo_estado, solucion, nuevo_tecnico):
                            st.success("✅ Ticket actualizado")
                            st.rerun()
    else:
        st.info("📭 No hay tickets para mostrar")

def gestionar_inventario():
    """Gestión de inventario de equipos TI"""
    st.header("💻 Inventario de Equipos TI")
    
    tab1, tab2 = st.tabs(["📋 Ver Inventario", "➕ Agregar Equipo"])
    
    with tab1:
        inventario = obtener_inventario()
        if inventario:
            df = pd.DataFrame(inventario)
            st.dataframe(df, use_container_width=True)
            
            # Botón para exportar
            if st.button("📥 Exportar a Excel"):
                buffer = io.BytesIO()
                df.to_excel(buffer, index=False)
                st.download_button(
                    label="💾 Descargar Excel",
                    data=buffer.getvalue(),
                    file_name=f"inventario_ti_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    
    with tab2:
        with st.form("nuevo_equipo"):
            col1, col2 = st.columns(2)
            
            with col1:
                codigo = st.text_input("🏷️ Código de Equipo *", placeholder="PC-LAB-001")
                tipo = st.selectbox("💻 Tipo de Equipo *", 
                                  ["Desktop", "Laptop", "Proyector", "Impresora", "Switch", "Router", "Monitor", "Otro"])
                marca = st.text_input("🏭 Marca *", placeholder="HP, Dell, Lenovo...")
                modelo = st.text_input("📱 Modelo *", placeholder="EliteDesk 800")
                serie = st.text_input("🔢 Número de Serie", placeholder="ABC123456")
            
            with col2:
                ubicacion = st.text_input("📍 Ubicación *", placeholder="Laboratorio 1, Aula 201...")
                estado = st.selectbox("⚡ Estado *", 
                                    ["Activo", "Mantenimiento", "Dañado", "Disponible", "Dado_de_baja"])
                responsable = st.text_input("👤 Responsable", placeholder="Prof. Juan Pérez")
                fecha_adq = st.date_input("📅 Fecha de Adquisición")
                observaciones = st.text_area("📝 Observaciones")
            
            if st.form_submit_button("➕ Agregar Equipo", type="primary"):
                if codigo and tipo and marca and modelo and ubicacion:
                    datos_equipo = {
                        'codigo': codigo,
                        'tipo': tipo,
                        'marca': marca,
                        'modelo': modelo,
                        'serie': serie,
                        'ubicacion': ubicacion,
                        'estado': estado,
                        'responsable': responsable,
                        'fecha': fecha_adq,
                        'observaciones': observaciones
                    }
                    
                    if agregar_equipo(datos_equipo):
                        st.success("✅ Equipo agregado al inventario!")
                    else:
                        st.error("❌ Error al agregar equipo")
                else:
                    st.error("⚠️ Complete los campos obligatorios (*)")

def mostrar_reportes():
    """Módulo de reportes y estadísticas"""
    st.header("📊 Reportes y Estadísticas")
    
    # Reportes disponibles
    tipo_reporte = st.selectbox("Seleccionar Reporte", 
                               ["Resumen General", "Tickets por Período", "Rendimiento por Técnico", "Inventario por Estado"])
    
    if tipo_reporte == "Resumen General":
        st.subheader("📋 Resumen General del Sistema")
        
        metricas = obtener_metricas()
        
        # Tabla resumen
        if metricas['tickets_por_estado']:
            df_resumen = pd.DataFrame(metricas['tickets_por_estado'])
            st.write("**Tickets por Estado:**")
            st.dataframe(df_resumen, use_container_width=True)
        
        # Inventario resumen
        inventario = obtener_inventario()
        if inventario:
            df_inv = pd.DataFrame(inventario)
            st.write("**Resumen de Inventario:**")
            resumen_inv = df_inv.groupby(['tipo_equipo', 'estado']).size().reset_index(name='cantidad')
            st.dataframe(resumen_inv, use_container_width=True)

def main():
    # Inicializar base de datos
    inicializar_bd()
    
    # Header
    st.title("🎫 Sistema de Tickets - Soporte TI UTP")
    st.markdown("**Universidad Tecnológica del Perú - Lima Sur**")
    st.markdown("---")
    
    # Sidebar
    st.sidebar.title("📋 Menú de Navegación")
    st.sidebar.markdown("**Desarrollado por:** Andry Diego")
    pagina = st.sidebar.selectbox(
        "Seleccionar módulo:",
        ["🏠 Dashboard", "📝 Crear Ticket", "📋 Gestionar Tickets", "💻 Inventario TI", "📊 Reportes"]
    )
    
    # Routing de páginas
    if pagina == "🏠 Dashboard":
        mostrar_dashboard()
    elif pagina == "📝 Crear Ticket":
        crear_nuevo_ticket()
    elif pagina == "📋 Gestionar Tickets":
        gestionar_tickets()
    elif pagina == "💻 Inventario TI":
        gestionar_inventario()
    elif pagina == "📊 Reportes":
        mostrar_reportes()

if __name__ == "__main__":
    main()