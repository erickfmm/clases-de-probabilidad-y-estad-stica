# 🎓 Generador Automático de Presentaciones Educativas

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![PowerPoint](https://img.shields.io/badge/PowerPoint-.pptx-orange.svg)
![LaTeX](https://img.shields.io/badge/LaTeX-Beamer-brightgreen.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

Sistema automatizado para generar presentaciones en **PowerPoint (.pptx)** y **LaTeX Beamer (PDF)** a partir de archivos YAML estructurados. Diseñado para el Ministerio de Educación.

## 📋 Características

- ✅ Generación automática de presentaciones PowerPoint (.pptx)
- ✅ Generación automática de presentaciones LaTeX Beamer (PDF)
- ✅ Soporte para múltiples materias/cursos
- ✅ Plantillas personalizables con temas educativos
- ✅ Organización automática de archivos por materia
- ✅ Tipos de contenido enriquecidos (ejemplos, fórmulas, tablas, gráficos)
- ✅ Procesamiento por lotes de múltiples archivos

## 📁 Estructura del Proyecto

```
autogenerator-of-ppt/
├── clases/                              # Contenido de las clases en YAML
│   ├── probabilidad y estadistica/
│   │   ├── 0-introduccion.yml
│   │   ├── 1-tablas_graficos.yml
│   │   ├── 2-medidas_posicion.yml
│   │   └── 3-reglas_probabilidades.yml
│   └── programacion_e_informatica/
│       ├── 0-introduccion_conceptos_basicos.yml
│       ├── 1-fundamentos_programacion.yml
│       └── ...
├── temarios/                            # Temarios organizados por materia
│   ├── probabilidad_y_estadistica.yml
│   └── programacion_e_informatica.yml
├── pptx/                                # Presentaciones PowerPoint generadas
│   ├── probabilidad y estadistica/
│   └── programacion_e_informatica/
├── pdfs/                                # PDFs LaTeX generados
│   ├── probabilidad y estadistica/
│   └── programacion_e_informatica/
├── generate_slides.py                   # Generador LaTeX/PDF
├── generate_pptx.py                     # Generador PowerPoint
├── template.tex                         # Template LaTeX Beamer
├── generar_todo.bat                     # Script para generar todo
├── run.bat                              # Script para LaTeX/PDF
├── run_pptx.bat                         # Script para PowerPoint
└── pyproject.toml                       # Configuración del proyecto
```

## 🚀 Instalación

### Requisitos del Sistema

- **Python >= 3.9**
- **LaTeX** (TeX Live o MiKTeX) - _opcional, solo para generar PDFs_

### Instalar Dependencias

#### Opción 1: Usando uv (recomendado)

```bash
# Instalar uv
pip install uv

# Sincronizar dependencias
uv sync
```

#### Opción 2: Usando pip

```bash
pip install pyyaml jinja2 python-pptx
```

## 💻 Uso

### Generar TODO (PowerPoint + PDF)

**Windows:**
```cmd
generar_todo.bat
```

**Manual:**
```bash
python generate_slides.py    # Genera LaTeX/PDF
python generate_pptx.py       # Genera PowerPoint
```

### Solo PowerPoint

**Windows:**
```cmd
run_pptx.bat
```

**Manual:**
```bash
# Generar todas las presentaciones
python generate_pptx.py

# Generar archivo específico
python generate_pptx.py "clases/probabilidad y estadistica/0-introduccion.yml"

# Generar todos los archivos de una materia
python generate_pptx.py "clases/probabilidad y estadistica/*.yml"

# Especificar directorio de salida
python generate_pptx.py -o mi_carpeta "clases/*.yml"
```

### Solo LaTeX/PDF

**Windows:**
```cmd
run.bat
```

**Manual:**
```bash
# Generar todas las presentaciones
python generate_slides.py

# Generar archivo específico
python generate_slides.py "clases/probabilidad y estadistica/1-tablas_graficos.yml"

# Generar todos los archivos de una materia
python generate_slides.py "clases/programacion_e_informatica/*.yml"

# Especificar directorios de salida
python generate_slides.py -o slides -p pdfs
```

## 📝 Formato de Archivos YAML

### Estructura Básica

```yaml
tema: "Título Principal del Tema"
subtitulo: "Subtítulo descriptivo (opcional)"

diapositivas:
  - titulo: "Título de la Diapositiva"
    contenido:
      - "Viñeta de texto simple"
      - tipo: "ejemplo"
        texto: "Contenido del ejemplo"
      - tipo: "formula"
        texto: "$E = mc^2$"
```

### Tipos de Contenido Disponibles

| Tipo | Descripción | Ejemplo |
|------|-------------|---------|
| `string` | Viñeta simple | `- "Texto aquí"` |
| `ejemplo` | Bloque de ejemplo destacado | `tipo: "ejemplo"` |
| `formula` | Fórmula matemática centrada | `tipo: "formula"` |
| `calculo` | Ecuaciones alineadas | `tipo: "calculo"` |
| `nota` | Bloque de alerta/aviso | `tipo: "nota"` |
| `problema` | Bloque de problema | `tipo: "problema"` |
| `solucion` | Bloque de solución con pasos | `tipo: "solucion"` |
| `tabla` | Tabla con encabezados | `tipo: "tabla"` |
| `componentes` | Lista de componentes | `tipo: "componentes"` |
| `grafico_barras` | Gráfico de barras | Ver GUIA_GRAFICOS.md |
| `grafico_lineas` | Gráfico de líneas | Ver GUIA_GRAFICOS.md |
| `grafico_circular` | Gráfico circular (pie) | Ver GUIA_GRAFICOS.md |
| `grafico_dispersion` | Gráfico de dispersión | Ver GUIA_GRAFICOS.md |

### Ejemplo Completo

```yaml
tema: "Introducción a la Probabilidad"
subtitulo: "Conceptos Fundamentales"

diapositivas:
  - titulo: "¿Qué es la Probabilidad?"
    contenido:
      - "Medida de incertidumbre de eventos"
      - "Valores entre 0 y 1"
      - tipo: "formula"
        texto: "$P(A) = \\frac{\\text{casos favorables}}{\\text{casos totales}}$"
      
  - titulo: "Ejemplo Práctico"
    contenido:
      - tipo: "problema"
        texto: "¿Cuál es la probabilidad de sacar un as de un mazo de 52 cartas?"
      - tipo: "solucion"
        pasos:
          - "Casos favorables: 4 ases"
          - "Casos totales: 52 cartas"
          - "$P(\\text{as}) = \\frac{4}{52} = \\frac{1}{13}$"
```

## 📊 Gráficos

Para información detallada sobre cómo crear gráficos, consulta:
- **[GUIA_GRAFICOS.md](GUIA_GRAFICOS.md)** - Guía completa de gráficos
- **[GUIA_RAPIDA_PPTX.md](GUIA_RAPIDA_PPTX.md)** - Guía rápida de PowerPoint

## 🎨 Personalización

### Template LaTeX

Edita `template.tex` para cambiar:
- Tema de Beamer: `\usetheme{Madrid}`
- Esquema de colores: `\usecolortheme{default}`
- Fuentes y estilos

### Colores PowerPoint

Edita `generate_pptx.py` en la sección `COLORES`:

```python
COLORES = {
    'primario': RGBColor(41, 128, 185),
    'secundario': RGBColor(231, 76, 60),
    'acento': RGBColor(46, 204, 113),
    # ...
}
```

## 📚 Materias Disponibles

### Probabilidad y Estadística
- Introducción
- Tablas y Gráficos
- Medidas de Posición
- Reglas de Probabilidades

### Programación e Informática
- Introducción y Conceptos Básicos
- Fundamentos de Programación
- Estructuras de Datos y Modularidad
- Arquitectura de Software
- Integración con el Mundo Real

## 🛠️ Desarrollo

```bash
# Instalar con dependencias de desarrollo
uv sync --all-extras

# Formatear código
black generate_slides.py generate_pptx.py

# Linting
ruff check generate_slides.py generate_pptx.py
```

## 📖 Documentación Adicional

- **[crear_clases_desde_temario.instructions.md](.github/instructions/crear_clases_desde_temario.instructions.md)** - Guía completa del esquema YAML
- **[README_PPTX.md](README_PPTX.md)** - Documentación específica de PowerPoint

## 🤝 Contribuir

Para agregar nuevas materias o clases:

1. Crea un directorio en `clases/[nombre-materia]/`
2. Agrega archivos `.yml` siguiendo el esquema documentado
3. Ejecuta `generar_todo.bat` o los scripts individuales
4. Las presentaciones se generarán automáticamente

## 📄 Licencia

Proyecto educativo con licencia MIT, abierto para todo uso.

---

**Desarrollado con ❤️ para la educación**
