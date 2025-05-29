"""
Script para inicializar la base de datos con datos de ejemplo
"""

import sqlite3
from datetime import datetime

def crear_base_datos():
    """Crear base de datos y tablas iniciales"""
    
    conn = sqlite3.connect('soporte_ti.db')
    cursor = conn.cursor()
    
    # Crear tablas
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
    
    conn.commit()
    conn.close()
    print("✅ Base de datos creada exitosamente")

if __name__ == "__main__":
    crear_base_datos()