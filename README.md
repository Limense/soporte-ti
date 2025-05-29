# 🎫 Sistema de Tickets - Soporte TI UTP

Sistema de gestión de tickets de soporte técnico.

## 🚀 Características

- ✅ **Dashboard con métricas en tiempo real**
- ✅ **Creación y gestión de tickets**
- ✅ **Sistema de inventario de equipos TI**
- ✅ **Asignación de técnicos**
- ✅ **Reportes exportables a Excel**
- ✅ **Seguimiento de estados y SLA**

## 📋 Requisitos

- Python 3.8 o superior
- Streamlit
- Pandas
- Plotly
- openpyxl

## 🔧 Instalación

1. **Clonar o descargar el proyecto**
```bash
git clone <repository_url>
cd sistema_tickets
```

2. **Crear entorno virtual**
```bash
python -m venv venv
```

3. **Activar entorno virtual**
```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

4. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

## ▶️ Ejecución

```bash
streamlit run app.py
```

El sistema estará disponible en: `http://localhost:8501`

## 👤 Desarrollador

**Andry Emilio Diego**
- Email: andriy.diego@outlook.com
- LinkedIn: [linkedin.com/in/andriydiego](https://linkedin.com/in/andriydiego)
- GitHub: [github.com/Limense](https://github.com/Limense)

## 📊 Funcionalidades

### Dashboard
- Métricas principales de tickets
- Gráficos de estado y categorías
- Carga de trabajo por técnico

### Gestión de Tickets
- Crear nuevos tickets
- Asignar técnicos
- Actualizar estados
- Seguimiento de soluciones

### Inventario TI
- Registrar equipos
- Control de ubicaciones
- Estados de equipos
- Exportar reportes

## 🗄️ Base de Datos

El sistema utiliza SQLite para simplicidad y portabilidad. La base de datos se crea automáticamente en el primer uso con datos de ejemplo.
