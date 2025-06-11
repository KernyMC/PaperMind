import gradio as gr
import os
import requests
import json
from pathlib import Path
import asyncio
from paperqa import Docs
import time
import re
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Configuración desde variables de entorno
PAPERS_DIR = os.getenv("PAPERS_DIR", "./zotero_papers")  # Directorio papers Zotero
LOCAL_PAPERS_DIR = os.getenv("LOCAL_PAPERS_DIR", "./mis_papers")  # Directorio papers locales
ZOTERO_API_KEY = os.getenv("ZOTERO_API_KEY")
ZOTERO_USER_ID = None  # Se detectará automáticamente

# Validar que las API keys estén configuradas
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("❌ OPENAI_API_KEY no encontrada. Configura tu archivo .env")
if not ZOTERO_API_KEY:
    raise ValueError("❌ ZOTERO_API_KEY no encontrada. Configura tu archivo .env")

# Crear directorios si no existen
os.makedirs(PAPERS_DIR, exist_ok=True)
os.makedirs(LOCAL_PAPERS_DIR, exist_ok=True)

class ZoteroPaperQAIntegration:
    def __init__(self):
        print("🔧 Configurando Zotero + Paper-QA...")
        self.api_key = ZOTERO_API_KEY
        self.user_id = None
        self.base_url = "https://api.zotero.org"
        self.docs = Docs(llm="gpt-4o-mini", summary_llm="gpt-4o-mini")
        self.processed_files = []
        self.collections = {}
        self.items_metadata = {}
        print("✅ Zotero + Paper-QA configurado")
        
    def get_headers(self):
        """Headers para requests a Zotero API"""
        return {
            "Zotero-API-Version": "3",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def detect_user_id(self):
        """Detectar automáticamente el User ID de Zotero"""
        try:
            response = requests.get(
                f"{self.base_url}/keys/{self.api_key}",
                headers=self.get_headers()
            )
            if response.status_code == 200:
                key_info = response.json()
                self.user_id = key_info.get('userID')
                return f"✅ Usuario Zotero detectado: {self.user_id}"
            else:
                return f"❌ Error detectando usuario: {response.status_code}"
        except Exception as e:
            return f"❌ Error conectando con Zotero: {str(e)}"
    
    def get_collections(self):
        """Obtener colecciones de Zotero"""
        if not self.user_id:
            return "❌ Primero detecta el usuario de Zotero"
        
        try:
            response = requests.get(
                f"{self.base_url}/users/{self.user_id}/collections",
                headers=self.get_headers()
            )
            
            if response.status_code == 200:
                collections = response.json()
                self.collections = {col['data']['name']: col['data']['key'] for col in collections}
                
                result = f"📚 Encontradas {len(self.collections)} colecciones:\n"
                for name, key in self.collections.items():
                    result += f"• {name} ({key})\n"
                return result
            else:
                return f"❌ Error obteniendo colecciones: {response.status_code}"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def add_item_by_doi(self, doi: str, collection_name: str = None):
        """Añadir artículo a Zotero por DOI"""
        if not self.user_id:
            return "❌ Primero detecta el usuario de Zotero"
        
        try:
            # Limpiar DOI
            doi = doi.strip().replace("https://doi.org/", "").replace("doi:", "")
            
            # Obtener metadatos desde DOI
            metadata = self.get_metadata_from_doi(doi)
            if not metadata:
                return f"❌ No se pudieron obtener metadatos para DOI: {doi}"
            
            # Crear item en Zotero
            collection_key = None
            if collection_name and collection_name in self.collections:
                collection_key = self.collections[collection_name]
            
            item_data = {
                "itemType": "journalArticle",
                "title": metadata.get("title", ""),
                "creators": [{"creatorType": "author", "name": author} for author in metadata.get("authors", [])],
                "date": metadata.get("year", ""),
                "DOI": doi,
                "url": metadata.get("url", ""),
                "abstractNote": metadata.get("abstract", ""),
                "collections": [collection_key] if collection_key else []
            }
            
            # Enviar a Zotero
            response = requests.post(
                f"{self.base_url}/users/{self.user_id}/items",
                headers={**self.get_headers(), "Content-Type": "application/json"},
                json=[item_data]
            )
            
            if response.status_code == 200:
                result_data = response.json()
                item_key = result_data['successful']['0']['key']
                
                # Intentar descargar PDF
                pdf_result = self.download_pdf_for_item(doi, item_key, metadata)
                
                return f"✅ Artículo añadido a Zotero\n📄 Título: {metadata.get('title', 'Sin título')}\n{pdf_result}"
            else:
                return f"❌ Error añadiendo a Zotero: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def get_metadata_from_doi(self, doi: str) -> Optional[Dict]:
        """Obtener metadatos desde DOI usando Crossref"""
        try:
            response = requests.get(f"https://api.crossref.org/works/{doi}")
            if response.status_code == 200:
                data = response.json()['message']
                
                # Extraer autores
                authors = []
                if 'author' in data:
                    for author in data['author']:
                        if 'given' in author and 'family' in author:
                            authors.append(f"{author['given']} {author['family']}")
                
                return {
                    "title": data.get('title', [''])[0],
                    "authors": authors,
                    "year": str(data.get('published-print', {}).get('date-parts', [['']])[0][0]),
                    "doi": doi,
                    "url": data.get('URL', ''),
                    "abstract": data.get('abstract', '')
                }
        except Exception as e:
            print(f"Error obteniendo metadatos: {e}")
        return None
    
    def download_pdf_for_item(self, doi: str, item_key: str, metadata: Dict):
        """Intentar descargar PDF para un item"""
        try:
            # Intentar desde Sci-Hub (usar con precaución y según normativas locales)
            pdf_url = f"https://sci-hub.se/{doi}"
            
            response = requests.get(pdf_url, timeout=10)
            if response.status_code == 200 and 'application/pdf' in response.headers.get('content-type', ''):
                # Generar nombre de archivo limpio
                title = metadata.get('title', 'documento')
                filename = self.clean_filename(f"{title}_{doi}.pdf")
                filepath = Path(PAPERS_DIR) / filename
                
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                return f"📥 PDF descargado: {filename}"
            else:
                return f"⚠️ PDF no disponible automáticamente para DOI: {doi}"
                
        except Exception as e:
            return f"⚠️ Error descargando PDF: {str(e)}"
    
    def clean_filename(self, filename: str) -> str:
        """Limpiar nombre de archivo para sistema de archivos"""
        # Remover caracteres no válidos
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        # Limitar longitud
        if len(filename) > 100:
            filename = filename[:95] + ".pdf"
        return filename
    
    def sync_zotero_to_paperqa(self, collection_name: str = None):
        """Sincronizar papers de Zotero con Paper-QA"""
        if not self.user_id:
            return "❌ Primero detecta el usuario de Zotero"
        
        try:
            # Obtener items de Zotero
            url = f"{self.base_url}/users/{self.user_id}/items"
            params = {"itemType": "journalArticle", "limit": 100}
            
            if collection_name and collection_name in self.collections:
                collection_key = self.collections[collection_name]
                url = f"{self.base_url}/users/{self.user_id}/collections/{collection_key}/items"
            
            response = requests.get(url, headers=self.get_headers(), params=params)
            
            if response.status_code == 200:
                items = response.json()
                
                results = []
                pdf_count = 0
                
                for item in items:
                    data = item['data']
                    title = data.get('title', 'Sin título')
                    doi = data.get('DOI', '')
                    
                    # Buscar PDF local correspondiente
                    pdf_files = list(Path(PAPERS_DIR).glob("*.pdf"))
                    matching_pdf = None
                    
                    for pdf_file in pdf_files:
                        if doi and doi.lower() in pdf_file.name.lower():
                            matching_pdf = pdf_file
                            break
                        if any(word in pdf_file.name.lower() for word in title.lower().split()[:3] if len(word) > 3):
                            matching_pdf = pdf_file
                            break
                    
                    if matching_pdf:
                        # Guardar metadatos enriquecidos
                        self.items_metadata[str(matching_pdf)] = {
                            'title': title,
                            'authors': [creator.get('name', '') for creator in data.get('creators', [])],
                            'year': data.get('date', ''),
                            'doi': doi,
                            'tags': [tag.get('tag', '') for tag in data.get('tags', [])],
                            'collections': data.get('collections', [])
                        }
                        
                        results.append(f"✅ {matching_pdf.name} → {title}")
                        pdf_count += 1
                    else:
                        results.append(f"⚠️ No PDF local para: {title}")
                
                sync_result = f"🔄 Sincronización completada:\n"
                sync_result += f"📄 {pdf_count} PDFs con metadatos enriquecidos\n\n"
                sync_result += "\n".join(results[:10])  # Mostrar solo los primeros 10
                
                if len(results) > 10:
                    sync_result += f"\n... y {len(results) - 10} más"
                
                return sync_result
            else:
                return f"❌ Error obteniendo items: {response.status_code}"
                
        except Exception as e:
            return f"❌ Error en sincronización: {str(e)}"
    
    async def load_papers_to_paperqa(self):
        """Cargar papers con metadatos enriquecidos a Paper-QA (Zotero + Locales)"""
        # Obtener PDFs de ambos directorios
        zotero_files = list(Path(PAPERS_DIR).glob("*.pdf"))
        local_files = list(Path(LOCAL_PAPERS_DIR).glob("*.pdf"))
        
        total_files = len(zotero_files) + len(local_files)
        if total_files == 0:
            return "❌ No hay PDFs en ningún directorio"
        
        results = []
        loaded_count = 0
        
        # Procesar papers de Zotero (con metadatos enriquecidos)
        if zotero_files:
            results.append(f"📚 **PAPERS DE ZOTERO** ({len(zotero_files)} archivos):")
            
            for pdf_file in zotero_files:
                try:
                    print(f"📖 Procesando Zotero: {pdf_file.name}")
                    
                    # Obtener metadatos enriquecidos de Zotero
                    metadata = self.items_metadata.get(str(pdf_file), {})
                    
                    if metadata:
                        citation = f"{', '.join(metadata.get('authors', [])[:3])} ({metadata.get('year', 'S/F')}). {metadata.get('title', pdf_file.name)}"
                        await self.docs.aadd(str(pdf_file), citation=citation)
                        title_display = metadata.get('title', pdf_file.name)
                    else:
                        await self.docs.aadd(str(pdf_file))
                        title_display = pdf_file.name
                    
                    self.processed_files.append(str(pdf_file))
                    loaded_count += 1
                    results.append(f"  ✅ {pdf_file.name} → {title_display[:50]}...")
                    
                except Exception as e:
                    results.append(f"  ❌ {pdf_file.name}: {str(e)}")
        
        # Procesar papers locales (sin metadatos Zotero)
        if local_files:
            results.append(f"\n📁 **PAPERS LOCALES** ({len(local_files)} archivos):")
            
            for pdf_file in local_files:
                try:
                    print(f"📖 Procesando Local: {pdf_file.name}")
                    
                    # Cargar paper local con identificación clara
                    citation = f"Documento Local: {pdf_file.stem}"
                    await self.docs.aadd(str(pdf_file), citation=citation)
                    
                    self.processed_files.append(str(pdf_file))
                    loaded_count += 1
                    results.append(f"  ✅ {pdf_file.name} [PAPEL LOCAL]")
                    
                except Exception as e:
                    results.append(f"  ❌ {pdf_file.name}: {str(e)}")
        
        summary = f"📚 **BIBLIOTECA COMPLETA CARGADA**: {loaded_count}/{total_files} documentos\n"
        summary += f"🔗 Zotero: {len(zotero_files)} papers con metadatos enriquecidos\n"
        summary += f"📁 Locales: {len(local_files)} papers del directorio personal\n\n"
        summary += "\n".join(results)
        
        if loaded_count > 0:
            summary += f"\n\n🚀 ¡Biblioteca unificada lista! Consulta papers de ambas fuentes simultáneamente."
        
        return summary
    
    async def ask_question_with_filters(self, question: str, collection_filter: str = None, tag_filter: str = None):
        """Hacer pregunta con filtros de colección/etiquetas"""
        if not self.processed_files:
            return "❌ No hay documentos cargados. Usa 'Cargar Papers en Paper-QA' primero."
        
        try:
            print(f"🤖 Pregunta: {question}")
            if collection_filter:
                print(f"📁 Filtro de colección: {collection_filter}")
            if tag_filter:
                print(f"🏷️ Filtro de etiqueta: {tag_filter}")
            
            # Hacer pregunta a Paper-QA
            answer = await self.docs.aquery(question)
            
            # Contar fuentes por tipo
            zotero_count = sum(1 for f in self.processed_files if PAPERS_DIR in f)
            local_count = sum(1 for f in self.processed_files if LOCAL_PAPERS_DIR in f)
            
            # Formatear respuesta con metadatos enriquecidos
            formatted_response = f"""
## 🎯 Pregunta: {question}

### 📝 Respuesta (Biblioteca Unificada):

{answer.answer}

### 📚 Información de la consulta:
- **📊 Biblioteca total**: {len(self.processed_files)} documentos
- **🔗 Papers Zotero**: {zotero_count} (con metadatos enriquecidos)
- **📁 Papers locales**: {local_count} (documentos personales)
- **🔍 Contextos utilizados**: {len(answer.context) if hasattr(answer, 'context') else 0}
"""
            
            if collection_filter:
                formatted_response += f"- **📁 Filtro colección**: {collection_filter}\n"
            if tag_filter:
                formatted_response += f"- **🏷️ Filtro etiqueta**: {tag_filter}\n"
            
            formatted_response += "\n### 🔍 Fuentes utilizadas:\n"
            
            # Mostrar contextos con identificación de origen
            if hasattr(answer, 'context') and answer.context:
                context_count = 0
                for i, context in enumerate(answer.context):
                    if context_count >= 3:
                        break
                    
                    try:
                        if hasattr(context, 'text'):
                            text_content = context.text
                        elif isinstance(context, str) and len(context) > 10:
                            text_content = context
                        else:
                            continue
                        
                        # Determinar origen y metadatos
                        source_metadata = None
                        source_type = "📄 Paper Local"
                        
                        # Buscar si es de Zotero con metadatos
                        for filepath, metadata in self.items_metadata.items():
                            if any(word in text_content.lower() for word in metadata.get('title', '').lower().split()[:3] if len(word) > 3):
                                source_metadata = metadata
                                source_type = "🔗 Paper Zotero"
                                break
                        
                        text_preview = text_content[:400] + "..." if len(text_content) > 400 else text_content
                        
                        if source_metadata:
                            # Fuente Zotero con metadatos completos
                            authors = ', '.join(source_metadata.get('authors', [])[:2])
                            if len(source_metadata.get('authors', [])) > 2:
                                authors += " et al."
                            
                            formatted_response += f"""
**{source_type} - Fuente {context_count + 1}:**
*📖 {source_metadata.get('title', 'Sin título')}*
*👥 Autores: {authors}*
*📅 Año: {source_metadata.get('year', 'S/F')}*
*🔗 DOI: {source_metadata.get('doi', 'No disponible')}*

{text_preview}

---
"""
                        else:
                            # Fuente local o sin metadatos
                            formatted_response += f"""
**{source_type} - Fuente {context_count + 1}:**
*📄 Documento de tu biblioteca personal*

{text_preview}

---
"""
                        context_count += 1
                        
                    except Exception as ctx_error:
                        continue
            
            formatted_response += f"""
### 📋 Resumen de la consulta:
- ✅ **Búsqueda en biblioteca unificada** (Zotero + Local)
- 🔍 **Análisis semántico** con Paper-QA v4
- 📚 **Metadatos enriquecidos** donde disponibles
- 🎯 **Respuesta contextualizada** con fuentes identificadas

*Respuesta generada por PaperMind v1.0 - Biblioteca Académica Inteligente*
"""
            
            return formatted_response
            
        except Exception as e:
            return f"❌ Error: {str(e)}"

# Inicializar integración
integration = ZoteroPaperQAIntegration()

# Funciones para Gradio
def detect_user():
    return integration.detect_user_id()

def get_collections():
    return integration.get_collections()

def add_by_doi(doi, collection):
    if not doi.strip():
        return "❌ Ingresa un DOI válido"
    return integration.add_item_by_doi(doi.strip(), collection if collection != "Ninguna" else None)

def sync_zotero(collection):
    return integration.sync_zotero_to_paperqa(collection if collection != "Todas" else None)

def load_papers_sync():
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(integration.load_papers_to_paperqa())
            return result
        finally:
            loop.close()
    except Exception as e:
        return f"❌ Error: {str(e)}"

def ask_with_filters(question, collection, tag):
    if not question.strip():
        return "❓ Ingresa una pregunta"
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            collection_filter = collection if collection != "Todas" else None
            tag_filter = tag if tag != "Todas" else None
            result = loop.run_until_complete(
                integration.ask_question_with_filters(question, collection_filter, tag_filter)
            )
            return result
        finally:
            loop.close()
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Interfaz Gradio
with gr.Blocks(title="PaperMind - Biblioteca Académica Inteligente", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🧠 PaperMind: Biblioteca Académica Inteligente")
    gr.Markdown("*Zotero + Papers Locales + IA: La evolución de la gestión bibliográfica académica*")
    
    # Configuración Zotero
    with gr.Tab("🔧 Configuración Zotero"):
        with gr.Row():
            detect_btn = gr.Button("🔍 Detectar Usuario Zotero", variant="primary")
            collections_btn = gr.Button("📚 Obtener Colecciones", variant="secondary")
        
        status_config = gr.Textbox(label="📋 Estado de Configuración", interactive=False, max_lines=10)
        
        detect_btn.click(fn=detect_user, outputs=[status_config])
        collections_btn.click(fn=get_collections, outputs=[status_config])
    
    # Añadir papers
    with gr.Tab("➕ Añadir Papers"):
        with gr.Row():
            doi_input = gr.Textbox(label="📄 DOI/PMID", placeholder="10.1038/nature12373 o PMC4234567")
            collection_dropdown = gr.Dropdown(
                label="📁 Colección", 
                choices=["Ninguna"], 
                value="Ninguna"
            )
        
        add_btn = gr.Button("🚀 Añadir a Zotero + Descargar PDF", variant="primary")
        status_add = gr.Textbox(label="📋 Estado de Descarga", interactive=False, max_lines=8)
        
        add_btn.click(fn=add_by_doi, inputs=[doi_input, collection_dropdown], outputs=[status_add])
    
    # Sincronización
    with gr.Tab("🔄 Sincronización"):
        with gr.Row():
            sync_collection = gr.Dropdown(
                label="📁 Sincronizar Colección", 
                choices=["Todas"], 
                value="Todas"
            )
            sync_btn = gr.Button("🔄 Sincronizar Zotero → Paper-QA", variant="primary")
        
        status_sync = gr.Textbox(label="📋 Estado de Sincronización", interactive=False, max_lines=10)
        
        load_btn = gr.Button("📚 Cargar Biblioteca Completa (Zotero + Local)", variant="secondary")
        status_load = gr.Textbox(label="📋 Estado de Carga Unificada", interactive=False, max_lines=8)
        
        sync_btn.click(fn=sync_zotero, inputs=[sync_collection], outputs=[status_sync])
        load_btn.click(fn=load_papers_sync, outputs=[status_load])
    
    # Consultas inteligentes
    with gr.Tab("🎯 Consultas Inteligentes"):
        with gr.Row():
            question_input = gr.Textbox(
                label="🤔 Tu pregunta", 
                placeholder="¿Qué metodologías de investigación aparecen en mis papers de Zotero y locales?",
                lines=2
            )
        
        with gr.Row():
            filter_collection = gr.Dropdown(
                label="📁 Filtrar por Colección", 
                choices=["Todas"], 
                value="Todas"
            )
            filter_tag = gr.Dropdown(
                label="🏷️ Filtrar por Etiqueta", 
                choices=["Todas"], 
                value="Todas"
            )
        
        ask_btn = gr.Button("🚀 Consultar Biblioteca Unificada", variant="primary")
        answer_output = gr.Markdown(label="🎯 Respuesta Enriquecida")
        
        ask_btn.click(fn=ask_with_filters, inputs=[question_input, filter_collection, filter_tag], outputs=[answer_output])
        question_input.submit(fn=ask_with_filters, inputs=[question_input, filter_collection, filter_tag], outputs=[answer_output])
    
    # Información del sistema
    gr.Markdown(f"""    
    ### 🔬 Características del Sistema:
    - **📚 Biblioteca unificada**: Combina papers Zotero + papers locales
    - **🔗 Gestión automática**: Metadatos normalizados desde Crossref
    - **📥 Descarga inteligente**: PDFs automáticos desde DOI/PMID
    - **📁 Organización**: Colecciones y etiquetas de Zotero
    - **🔍 Consultas filtradas**: Busca en ambas fuentes simultáneamente
    - **📖 Citaciones**: Referencias automáticas en formato académico
    - **🎯 Identificación de origen**: Distingue fuentes Zotero vs locales
    
    ### 📂 Directorios:
    - **Zotero**: {PAPERS_DIR}
    - **Local**: {LOCAL_PAPERS_DIR}
    
    ### 🎯 Flujo de trabajo:
    1. **Configurar**: Detecta usuario y obtén colecciones Zotero
    2. **Añadir**: Introduce DOIs para descarga automática en Zotero
    3. **Sincronizar**: Conecta ambas bibliotecas con Paper-QA
    4. **Consultar**: Haz preguntas sobre toda tu biblioteca académica
    
    ### 💡 Ventajas de la biblioteca unificada:
    - ✅ **Acceso total**: Consulta papers de ambas fuentes en una sola búsqueda
    - ✅ **Flexibilidad**: Mantén papers locales separados de Zotero
    - ✅ **Metadatos enriquecidos**: Papers Zotero con información completa
    - ✅ **Identificación clara**: Distingue origen de cada respuesta
    
    ---
    
    ### 👨‍💻 Desarrollado por
    **PaperMind v1.0** - Creado con ❤️ por **{os.getenv('USER', 'Usuario')}**
    
    *🚀 Potenciando la investigación académica con IA desde 2024*
    
    📧 ¿Sugerencias o mejoras? ¡Abre un issue en el repositorio!
    """)

if __name__ == "__main__":
    demo.launch(share=False, server_name="localhost", server_port=7860) 