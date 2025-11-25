"""
Script para generar diapositivas LaTeX desde archivos YAML.

Este script lee archivos YAML con contenido de temas de Probabilidad y Estadística,
y genera presentaciones en formato LaTeX Beamer usando un template.
"""

import yaml
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import subprocess
import sys
import argparse
import glob


def cargar_yaml(archivo_yaml):
    """
    Carga un archivo YAML y retorna su contenido.
    
    Args:
        archivo_yaml (str): Ruta al archivo YAML
        
    Returns:
        dict: Contenido del archivo YAML
    """
    with open(archivo_yaml, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def generar_latex(datos_yaml, template_path, output_path):
    """
    Genera un archivo LaTeX usando Jinja2.
    
    Args:
        datos_yaml (dict): Datos del tema desde YAML
        template_path (str): Ruta al template LaTeX
        output_path (str): Ruta donde guardar el archivo .tex generado
    """
    # Configurar Jinja2 con delimitadores personalizados para LaTeX
    env = Environment(
        loader=FileSystemLoader(Path(template_path).parent),
        block_start_string='<<%',
        block_end_string='%>>',
        variable_start_string='<<',
        variable_end_string='>>',
        comment_start_string='<<#',
        comment_end_string='#>>',
        trim_blocks=True,
        lstrip_blocks=True
    )
    
    template = env.get_template(Path(template_path).name)
    
    # Renderizar template con los datos
    contenido_latex = template.render(**datos_yaml)
    
    # Crear directorio de salida si no existe
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Guardar archivo .tex
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(contenido_latex)
    
    print(f"✓ Archivo LaTeX generado: {output_path}")


def compilar_latex(archivo_tex, output_pdf_dir=None):
    """
    Compila un archivo LaTeX a PDF usando pdflatex.
    
    Args:
        archivo_tex (str): Ruta al archivo .tex
        output_pdf_dir (str): Directorio donde colocar el PDF final (opcional)
        
    Returns:
        bool: True si la compilación fue exitosa
    """
    import shutil
    
    archivo_tex = Path(archivo_tex).resolve()
    directorio_trabajo = archivo_tex.parent
    
    try:
        # Ejecutar pdflatex dos veces para referencias cruzadas
        print(f"  Compilando con pdflatex...")
        for i in range(2):
            resultado = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', str(archivo_tex.name)],
                capture_output=True,
                text=True,
                check=False,
                encoding='utf-8',
                errors='replace',
                cwd=str(directorio_trabajo)
            )
            
            if i == 0 and resultado.returncode != 0:
                print(f"⚠ Error en primera compilación de {archivo_tex.name}")
                break
        
        pdf_generado = directorio_trabajo / archivo_tex.with_suffix('.pdf').name
        
        if pdf_generado.exists():
            # Si se especificó un directorio de salida diferente, copiar el PDF
            if output_pdf_dir:
                output_pdf_dir = Path(output_pdf_dir)
                output_pdf_dir.mkdir(parents=True, exist_ok=True)
                pdf_destino = output_pdf_dir / pdf_generado.name
                
                if pdf_destino.exists():
                    pdf_destino.unlink()
                
                shutil.copy2(str(pdf_generado), str(pdf_destino))
                print(f"✓ PDF generado exitosamente: {pdf_destino}")
            else:
                print(f"✓ PDF generado exitosamente: {pdf_generado}")
            
            # Limpiar archivos auxiliares
            for ext in ['.aux', '.log', '.out', '.nav', '.snm', '.toc']:
                aux_file = directorio_trabajo / f"{archivo_tex.stem}{ext}"
                if aux_file.exists():
                    try:
                        aux_file.unlink()
                    except:
                        pass
            
            return True
        else:
            print(f"⚠ Error: No se generó el PDF para {archivo_tex.name}")
            if resultado.returncode != 0:
                # Buscar el archivo .log para más detalles
                log_file = directorio_trabajo / f"{archivo_tex.stem}.log"
                if log_file.exists():
                    print(f"  Ver detalles en: {log_file}")
            return False
            
    except FileNotFoundError:
        print("⚠ pdflatex no encontrado. Instala una distribución LaTeX (TeX Live, MiKTeX, etc.)")
        print("  Solo se generarán los archivos .tex")
        return False
    except Exception as e:
        print(f"⚠ Error inesperado al compilar: {e}")
        return False


def procesar_tema(archivo_yaml, template_path, output_dir, pdf_dir=None, compilar=True):
    """
    Procesa un tema completo: carga YAML, genera LaTeX y opcionalmente compila.
    
    Args:
        archivo_yaml (str): Ruta al archivo YAML del tema
        template_path (str): Ruta al template LaTeX
        output_dir (str): Directorio de salida para .tex
        pdf_dir (str): Directorio de salida para .pdf (si es diferente)
        compilar (bool): Si se debe intentar compilar a PDF
    """
    archivo_yaml = Path(archivo_yaml).resolve()
    print(f"\n→ Procesando: {archivo_yaml}")
    
    # Cargar datos
    datos = cargar_yaml(archivo_yaml)
    
    # Determinar estructura de directorios
    try:
        directorio_base = Path(__file__).parent.resolve()
        clases_base = directorio_base / "clases"
        
        if archivo_yaml.is_relative_to(clases_base):
            relative_path = archivo_yaml.parent.relative_to(clases_base)
        else:
            relative_path = Path(".")
    except (ValueError, AttributeError):
        relative_path = Path(".")
    
    # Generar rutas de salida manteniendo estructura
    nombre_base = archivo_yaml.stem
    tex_output_dir = Path(output_dir) / relative_path
    output_tex = tex_output_dir / f"{nombre_base}.tex"
    
    # Generar LaTeX
    generar_latex(datos, template_path, output_tex)
    
    # Compilar a PDF si se solicita
    if compilar:
        # Determinar directorio de salida del PDF
        if pdf_dir:
            pdf_output_dir = Path(pdf_dir) / relative_path
        else:
            pdf_output_dir = tex_output_dir
        
        compilar_latex(str(output_tex), pdf_output_dir)


def main():
    """Función principal del script."""
    # Configurar parser de argumentos
    parser = argparse.ArgumentParser(
        description='Generador de Diapositivas - Probabilidad y Estadística',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python generate_slides.py                              # Procesa TODOS los .yml en clases/**/
  python generate_slides.py archivo.yml                  # Procesa un archivo específico
  python generate_slides.py archivo1.yml archivo2.yml    # Procesa múltiples archivos
  python generate_slides.py clases/**/*.yml              # Procesa todos en clases (explícito)
  python generate_slides.py "clases/probabilidad y estadistica/*.yml"  # Solo probabilidad
  python generate_slides.py "clases/programacion_e_informatica/*.yml"  # Solo programación
  python generate_slides.py -p pdfs archivo.yml          # PDFs en carpeta pdfs/ (con subdirectorios)
  python generate_slides.py -o slides -p pdfs            # Especifica directorios de salida
  python generate_slides.py -t mi_template.tex           # Usa template personalizado

Estructura de salida:
  - Archivos .tex siempre van a: slides/
  - Archivos .pdf van a: pdfs/[materia]/ (mantiene estructura de clases/)
        """
    )
    parser.add_argument(
        'archivos',
        nargs='*',
        help='Archivos YAML a procesar. Soporta patrones con * (ej: *.yml, clases/*.yml)'
    )
    parser.add_argument(
        '-o', '--output',
        dest='output_dir',
        default=None,
        help='Directorio de salida para los archivos .tex generados (default: slides/)'
    )
    parser.add_argument(
        '-p', '--pdf-dir',
        dest='pdf_dir',
        default=None,
        help='Directorio de salida para los archivos .pdf (default: pdfs/)'
    )
    parser.add_argument(
        '-t', '--template',
        dest='template',
        default=None,
        help='Ruta al archivo template LaTeX (default: template.tex)'
    )
    
    args = parser.parse_args()
    
    # Configuración
    directorio_base = Path(__file__).parent
    template_path = Path(args.template) if args.template else directorio_base / "template.tex"
    output_dir = Path(args.output_dir) if args.output_dir else directorio_base / "slides"
    pdf_dir = Path(args.pdf_dir) if args.pdf_dir else directorio_base / "pdfs"
    clases_dir = directorio_base / "clases"
    
    # Determinar qué archivos procesar
    if args.archivos:
        # Expandir patrones con glob
        temas = []
        for patron in args.archivos:
            # Si el patrón contiene *, expandirlo
            if '*' in patron or '?' in patron:
                archivos_encontrados = glob.glob(patron, recursive=True)
                temas.extend([Path(f) for f in archivos_encontrados if f.endswith(('.yml', '.yaml'))])
            else:
                # Archivo directo
                temas.append(Path(patron))
    else:
        # Buscar todos los archivos .yml en clases/**/*
        temas = list(clases_dir.glob('**/*.yml'))
        if not temas:
            # Fallback a archivos por defecto de probabilidad y estadística
            prob_dir = clases_dir / "probabilidad y estadistica"
            temas = [
                prob_dir / "0-introduccion.yml",
                prob_dir / "1-tablas_graficos.yml",
                prob_dir / "2-medidas_posicion.yml",
                prob_dir / "3-reglas_probabilidades.yml"
            ]
    
    print("=" * 60)
    print("Generador de Diapositivas - Probabilidad y Estadística")
    print("=" * 60)
    
    # Verificar que existe el template
    if not template_path.exists():
        print(f"✗ Error: No se encontró el template en {template_path}")
        sys.exit(1)
    
    # Verificar que hay archivos para procesar
    if not temas:
        print("✗ Error: No se encontraron archivos YAML para procesar")
        print("Usa --help para ver ejemplos de uso")
        sys.exit(1)
    
    # Procesar cada tema
    procesados = 0
    for tema in temas:
        if tema.exists():
            procesar_tema(tema, template_path, output_dir, pdf_dir, compilar=True)
            procesados += 1
        else:
            print(f"⚠ Advertencia: No se encontró {tema}")
    
    print("\n" + "=" * 60)
    print(f"✓ Proceso completado. {procesados} archivo(s) procesado(s).")
    print(f"  Archivos .tex generados en: {output_dir}/[materia]/")
    print(f"  Archivos .pdf generados en: {pdf_dir}/[materia]/")
    print("=" * 60)


if __name__ == "__main__":
    main()
