# 📚 Biblioteca Académica Unificada: Zotero + Paper-QA

Una herramienta poderosa que combina la gestión bibliográfica de Zotero con las capacidades de análisis inteligente de Paper-QA, permitiendo consultas avanzadas sobre tu biblioteca académica completa.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Paper-QA](https://img.shields.io/badge/Paper--QA-v4.9.0-orange.svg)

## 🎯 Características Principales

### 📚 **Biblioteca Unificada**
- **Integración dual**: Combina papers de Zotero + papers locales
- **Consultas simultáneas**: Una pregunta, múltiples fuentes
- **Identificación de origen**: Distingue claramente fuentes Zotero vs locales

### 🔗 **Gestión Automática con Zotero**
- **Metadatos enriquecidos**: Título, autores, DOI, año automático
- **Descarga inteligente**: PDFs automáticos desde DOI/PMID
- **Organización avanzada**: Colecciones y etiquetas de Zotero
- **Sincronización bidireccional**: Zotero ↔ Paper-QA

### 🤖 **Análisis Inteligente con Paper-QA v4**
- **Búsqueda semántica**: Encuentra información relevante sin palabras exactas
- **Respuestas contextualizadas**: Citas automáticas con páginas específicas
- **Multi-hop reasoning**: Conecta información de múltiples fuentes
- **Evaluación de evidencia**: Rankea y filtra la información más relevante

## 🚀 Instalación Rápida

### 1. Clonar el repositorio
```bash
git clone https://github.com/KernyMC/PaperMind.git
```

### 2. Crear entorno virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar API Keys
```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tus API keys
notepad .env  # Windows
nano .env     # Linux/macOS
```

**Contenido del archivo .env:**
```env
# OpenAI API Key (requerida)
OPENAI_API_KEY=tu_openai_api_key_aqui

# Zotero API Key (requerida)
ZOTERO_API_KEY=tu_zotero_api_key_aqui
```

### 5. Ejecutar la aplicación
```bash
python app_zotero_paperqa.py
```

Accede a: **http://localhost:7868**

## 🔑 Obtener API Keys

### OpenAI API Key
1. Ve a [OpenAI Platform](https://platform.openai.com/api-keys)
2. Crea una cuenta o inicia sesión
3. Genera una nueva API key
4. Copia la key que comienza con `sk-proj-...`

### Zotero API Key
1. Ve a [Zotero Settings](https://www.zotero.org/settings/keys)
2. Inicia sesión en tu cuenta Zotero
3. Crea una nueva private key
4. Permite acceso de lectura/escritura a tu biblioteca
5. Copia la key generada

## 📖 Guía de Uso

### 🔧 **Paso 1: Configuración Inicial**
1. **Detectar Usuario Zotero**: El sistema identifica automáticamente tu ID
2. **Obtener Colecciones**: Carga tus colecciones de Zotero para organización

### ➕ **Paso 2: Añadir Papers**
- **Por DOI/PMID**: Introduce identificadores para descarga automática
- **Metadatos automáticos**: Título, autores, año obtenidos de Crossref
- **Organización**: Asigna a colecciones específicas de Zotero

### 🔄 **Paso 3: Sincronización**
1. **Sincronizar Zotero**: Conecta tu biblioteca Zotero con Paper-QA
2. **Cargar Biblioteca Completa**: Incluye papers locales + Zotero
3. **Verificar carga**: Confirma que todos los papers están disponibles

### 🎯 **Paso 4: Consultas Inteligentes**
- **Preguntas naturales**: Usa lenguaje natural para tus consultas
- **Filtros avanzados**: Por colección, etiqueta o fuente
- **Respuestas enriquecidas**: Con citaciones automáticas y metadatos

## 💡 Ejemplos de Consultas

### Consultas Metodológicas
```
¿Qué metodologías de investigación aparecen en mis papers de genética?
```

### Búsquedas Temáticas
```
¿Cuáles son los principales hallazgos sobre CRISPR en mis artículos de 2023?
```

### Análisis Comparativo
```
¿Qué diferencias metodológicas hay entre mis papers cualitativos y cuantitativos?
```

### Búsquedas de Tendencias
```
¿Cómo ha evolucionado la investigación en IA según mis papers de los últimos 5 años?
```

## 📁 Estructura del Proyecto

```
biblioteca-academica-unificada/
├── app_zotero_paperqa.py      # Aplicación principal
├── requirements.txt           # Dependencias Python
├── .env.example              # Plantilla configuración
├── .gitignore               # Archivos ignorados por Git
├── README.md                # Este archivo
├── zotero_papers/           # Papers descargados de Zotero (ignorado)
├── mis_papers/             # Papers locales (ignorado)
└── .env                    # Configuración personal (ignorado)
```

## 🛠️ Configuración Avanzada

### Directorios Personalizados
Puedes personalizar las rutas en tu archivo `.env`:
```env
PAPERS_DIR=./mi_biblioteca_zotero
LOCAL_PAPERS_DIR=./mis_documentos_locales
```

### Modelos de IA Alternativos
El sistema usa `gpt-4o-mini` por defecto, pero puedes configurar otros modelos OpenAI editando la línea:
```python
self.docs = Docs(llm="gpt-4o", summary_llm="gpt-4o")  # Modelo más potente
```

## 🔍 Solución de Problemas

### Error: API Key no encontrada
```bash
# Verifica que el archivo .env existe y tiene el formato correcto
cat .env  # Linux/macOS
type .env # Windows
```

### Error: No se pueden cargar papers
```bash
# Verifica que los directorios existen
ls zotero_papers/     # Linux/macOS
ls mis_papers/        # Linux/macOS
dir zotero_papers\    # Windows
dir mis_papers\       # Windows
```

### Puerto 7868 ocupado
```python
# Cambia el puerto en la última línea del archivo
demo.launch(share=False, server_name="localhost", server_port=7869)
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 🙏 Agradecimientos

- **[Paper-QA](https://github.com/Future-House/paper-qa)**: Framework de análisis de papers con IA
- **[Zotero](https://www.zotero.org/)**: Gestión bibliográfica de código abierto
- **[Gradio](https://gradio.app/)**: Interfaz web interactiva
- **[OpenAI](https://openai.com/)**: Modelos de lenguaje avanzados

## 📊 Métricas del Proyecto

- **Lenguaje**: Python 3.10+
- **Dependencias**: 6 principales
- **Funcionalidades**: 4 módulos integrados
- **Interfaz**: Web (Gradio)
- **APIs**: OpenAI + Zotero + Crossref

---

**¿Preguntas o sugerencias?** Abre un [issue](https://github.com/tu-usuario/biblioteca-academica-unificada/issues) o contacta al desarrollador.

⭐ **¡Si este proyecto te resulta útil, dale una estrella!** 
