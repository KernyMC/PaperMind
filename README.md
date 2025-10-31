# 🧠 PaperMind: Biblioteca Académica Inteligente

**La evolución de la gestión bibliográfica académica**

Una herramienta revolucionaria que combina la gestión bibliográfica de Zotero con las capacidades de análisis inteligente de Paper-QA, permitiendo consultas avanzadas con IA sobre tu biblioteca académica completa.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Paper-QA](https://img.shields.io/badge/Paper--QA-v4.9.0-orange.svg)
![Version](https://img.shields.io/badge/PaperMind-v1.0-purple.svg)

## 🚀 ¿Qué es PaperMind?

PaperMind es la próxima generación de herramientas para investigadores académicos. Combina la robusta gestión bibliográfica de Zotero con la inteligencia artificial de Paper-QA para crear una experiencia de investigación completamente nueva.

### 🧠 **Inteligencia Artificial Aplicada**
- **Consultas en lenguaje natural**: Pregunta como hablarías con un colega
- **Análisis semántico avanzado**: Encuentra conexiones que no sabías que existían
- **Síntesis automática**: Combina información de múltiples fuentes
- **Razonamiento multi-hop**: Conecta ideas a través de diferentes papers

### 📚 **Biblioteca Unificada**
- **Integración dual**: Zotero + papers locales en un solo lugar
- **Metadatos enriquecidos**: Información completa automática
- **Organización inteligente**: Colecciones y etiquetas sincronizadas
- **Identificación de origen**: Transparencia total en las fuentes

## 🎯 Características Principales

### 🔗 **Gestión Automática con Zotero**
- **Descarga inteligente**: PDFs automáticos desde DOI/PMID
- **Metadatos normalizados**: Título, autores, DOI, año automático
- **Sincronización bidireccional**: Zotero ↔ PaperMind
- **Organización avanzada**: Colecciones y etiquetas preservadas

### 🤖 **Análisis Inteligente con IA**
- **Búsqueda semántica**: Sin necesidad de palabras exactas
- **Respuestas contextualizadas**: Con citaciones específicas
- **Evaluación de evidencia**: Ranking automático de relevancia
- **Síntesis multi-documento**: Combina información de múltiples fuentes

### 🎯 **Experiencia de Usuario Superior**
- **Interfaz web moderna**: Diseño intuitivo y responsivo
- **Consultas filtradas**: Por colección, etiqueta o fuente
- **Respuestas enriquecidas**: Metadatos completos y referencias
- **Feedback en tiempo real**: Estado de todas las operaciones

## 🚀 Instalación Rápida

### 1. Clonar PaperMind
```bash
git clone https://github.com/KernyMC/PaperMind.git
cd PaperMind
```

### 2. Configurar entorno
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
# Crear archivo de configuración
cp .env.example .env
```

**Edita tu archivo .env:**
```env
# OpenAI API Key (requerida para IA)
OPENAI_API_KEY=tu_openai_api_key_aqui

# Zotero API Key (requerida para sincronización)
ZOTERO_API_KEY=tu_zotero_api_key_aqui

# Directorios personalizados (opcional)
PAPERS_DIR=./zotero_papers
LOCAL_PAPERS_DIR=./mis_papers
```

### 5. ¡Lanzar PaperMind!
```bash
python app_zotero_paperqa.py
```

🌐 **Accede a:** http://localhost:7860

## 🔑 Obtener API Keys

### OpenAI API Key
1. 🌐 Ve a [OpenAI Platform](https://platform.openai.com/api-keys)
2. 🔐 Crea cuenta o inicia sesión
3. ⚡ Genera nueva API key
4. 📋 Copia la key `sk-proj-...`

### Zotero API Key
1. 🌐 Ve a [Zotero Settings](https://www.zotero.org/settings/keys)
2. 🔐 Inicia sesión en Zotero
3. 🔑 Crea private key
4. ✅ Permite acceso lectura/escritura
5. 📋 Copia la key generada

## 📖 Guía de Uso Completa

### 🔧 **Paso 1: Configuración Inicial**
```
1. 🔍 Detectar Usuario Zotero → Identifica automáticamente tu ID
2. 📚 Obtener Colecciones → Carga tus colecciones para organización
```

### ➕ **Paso 2: Alimentar tu Biblioteca**
```
Opción A: Por DOI/PMID
- Introduce: 10.1038/nature12373
- PaperMind descarga automáticamente PDF + metadatos

Opción B: Papers locales
- Coloca PDFs en: ./mis_papers/
- PaperMind los detecta automáticamente
```

### 🔄 **Paso 3: Sincronización Inteligente**
```
1. 🔄 Sincronizar Zotero → Conecta biblioteca Zotero
2. 📚 Cargar Biblioteca Completa → Incluye locales + Zotero
3. ✅ Verificar → Confirma carga exitosa
```

### 🧠 **Paso 4: Consultas con IA**
```
🎯 Haz preguntas en lenguaje natural:
- "¿Qué metodologías aparecen en mis papers de 2023?"
- "¿Cuáles son las tendencias en mi área de investigación?"
- "¿Qué papers contradicen la hipótesis X?"
```

## 💡 Ejemplos de Consultas Avanzadas

### 🔬 **Análisis Metodológico**
```
¿Qué metodologías de investigación cualitativa aparecen en mis papers de ciencias sociales?
```

### 📊 **Búsqueda de Tendencias**
```
¿Cómo ha evolucionado la investigación en IA según mis papers de los últimos 5 años?
```

### 🔍 **Análisis Comparativo**
```
¿Qué diferencias encuentras entre los enfoques metodológicos de mis papers europeos vs americanos?
```

### 🎯 **Síntesis de Conocimiento**
```
¿Cuáles son los principales hallazgos sobre CRISPR en mi colección de genética molecular?
```

### 🔗 **Conexiones Interdisciplinarias**
```
¿Qué conexiones puedes encontrar entre mis papers de psicología cognitiva y neurociencias?
```

## 📁 Arquitectura del Proyecto

```
papermind/
├── 🧠 app_zotero_paperqa.py    # Núcleo de PaperMind
├── 📦 requirements.txt         # Dependencias IA + Zotero
├── ⚙️  .env.example           # Plantilla configuración
├── 📖 README.md               # Esta documentación
├── 📄 LICENSE                 # Licencia MIT
├── 🔍 .gitignore             # Archivos ignorados
├── 📚 zotero_papers/          # Papers Zotero (auto-descarga)
├── 📁 mis_papers/            # Papers locales (manual)
└── 🔐 .env                   # Tu configuración personal
```

## 🛠️ Configuración Avanzada

### 🎛️ **Personalización de Directorios**
```env
# En tu archivo .env
PAPERS_DIR=./mi_biblioteca_zotero
LOCAL_PAPERS_DIR=./documentos_investigacion
```

### 🤖 **Modelos de IA Alternativos**
```python
# En app_zotero_paperqa.py línea ~34
self.docs = Docs(
    llm="gpt-4o",           # Modelo más potente
    summary_llm="gpt-4o"    # Para resúmenes detallados
)
```

### 🌐 **Configuración de Red**
```python
# Cambiar puerto si está ocupado
demo.launch(
    share=False, 
    server_name="localhost", 
    server_port=7861  # Puerto alternativo
)
```

## 🔧 Solución de Problemas

### ❌ **Error: API Key no encontrada**
```bash
# Verificar archivo .env
cat .env  # Linux/macOS
type .env # Windows

# Debe contener:
OPENAI_API_KEY=sk-proj-...
ZOTERO_API_KEY=...
```

### ❌ **Error: No se pueden cargar papers**
```bash
# Verificar directorios
ls -la zotero_papers/  # Linux/macOS
ls -la mis_papers/     # Linux/macOS
dir zotero_papers\     # Windows
dir mis_papers\        # Windows
```

### ❌ **Puerto ocupado**
```python
# Cambiar puerto en última línea
demo.launch(server_port=7861)
```

### ❌ **Problemas de conexión Zotero**
1. ✅ Verificar API key en Zotero.org
2. ✅ Comprobar permisos de lectura/escritura
3. ✅ Probar conexión manualmente

## 🤝 Contribuir a PaperMind

¡PaperMind es un proyecto en evolución! Tu contribución es bienvenida:

1. 🍴 **Fork** el proyecto
2. 🌿 **Crea** rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. 💾 **Commit** cambios (`git commit -am 'Agrega: nueva funcionalidad increíble'`)
4. 📤 **Push** rama (`git push origin feature/nueva-funcionalidad`)
5. 🔃 **Abre** Pull Request

### 🎯 **Áreas de Contribución**
- 🤖 Mejoras en algoritmos IA
- 🎨 Diseño de interfaz
- 📊 Nuevas funcionalidades
- 🐛 Corrección de bugs
- 📖 Documentación
- 🌐 Internacionalización

## 📊 Estadísticas del Proyecto

| Métrica | Valor |
|---------|-------|
| 🐍 **Lenguaje** | Python 3.10+ |
| 📦 **Dependencias** | 6 principales |
| 🧩 **Módulos** | 4 integrados |
| 🌐 **Interfaz** | Web (Gradio) |
| 🔗 **APIs** | OpenAI + Zotero + Crossref |
| 📈 **Versión** | v1.0 |

## 🏆 Casos de Uso Exitosos

### 👨‍🎓 **Estudiantes de Doctorado**
- Síntesis automática de literatura
- Identificación de gaps de investigación
- Análisis de metodologías emergentes

### 👩‍🔬 **Investigadores Senior**
- Review sistemáticos acelerados
- Conexiones interdisciplinarias
- Gestión de grandes corpus

### 👨‍🏫 **Profesores Universitarios**
- Preparación de cursos basada en evidencia
- Actualización curricular continua
- Mentoring estudiantil mejorado

## 📄 Licencia

PaperMind está licenciado bajo **MIT License**. Ver `LICENSE` para detalles completos.

## 🙏 Agradecimientos y Tecnologías

PaperMind no sería posible sin estas increíbles tecnologías:

- 🤖 **[Paper-QA](https://github.com/Future-House/paper-qa)** - Motor de análisis IA para papers académicos
- 📚 **[Zotero](https://www.zotero.org/)** - Gestión bibliográfica de código abierto
- 🎨 **[Gradio](https://gradio.app/)** - Interfaces web para ML/IA
- 🧠 **[OpenAI](https://openai.com/)** - Modelos de lenguaje avanzados
- 🔍 **[Crossref](https://www.crossref.org/)** - Metadatos académicos globales


</div> 
=======
⭐ **¡Si este proyecto te resulta útil, dale una estrella!** 
>>>>>>> 1ba901e4e1cf21318a3f1ba094b04cde14466dcd

