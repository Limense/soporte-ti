"""
Configuración del Sistema de Tickets
"""

# Configuración de la aplicación
APP_CONFIG = {
    'title': 'Sistema de Tickets - Soporte TI UTP',
    'icon': '🎫',
    'layout': 'wide',
    'sidebar_state': 'expanded'
}

# Configuración de la base de datos
DATABASE_CONFIG = {
    'name': 'soporte_ti.db',
    'type': 'sqlite'
}

# Categorías de tickets
CATEGORIAS_TICKETS = [
    'Hardware',
    'Software', 
    'Red',
    'Cuenta_Usuario',
    'Impresora',
    'Otro'
]

# Prioridades
PRIORIDADES = [
    'Baja',
    'Media', 
    'Alta',
    'Crítica'
]

# Estados de tickets
ESTADOS_TICKETS = [
    'Abierto',
    'En_Proceso',
    'Pendiente_Usuario',
    'Resuelto',
    'Cerrado'
]

# Tipos de equipos
TIPOS_EQUIPOS = [
    'Desktop',
    'Laptop',
    'Proyector',
    'Impresora',
    'Switch',
    'Router',
    'Monitor',
    'Otro'
]

# Estados de equipos
ESTADOS_EQUIPOS = [
    'Activo',
    'Mantenimiento',
    'Dañado',
    'Disponible',
    'Dado_de_baja'
]