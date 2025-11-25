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
    
    # Guardar archivo .tex
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(contenido_latex)
    
    print(f"✓ Archivo LaTeX generado: {output_path}")


def compilar_latex(archivo_tex):
    """
    Compila un archivo LaTeX a PDF usando pdflatex.
    
    Args:
        archivo_tex (str): Ruta al archivo .tex
        
    Returns:
        bool: True si la compilación fue exitosa
    """
    try:
        # Ejecutar pdflatex dos veces para referencias cruzadas
        for i in range(2):
            resultado = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', archivo_tex],
                capture_output=True,
                text=True,
                check=False
            )
        
        if resultado.returncode == 0:
            print(f"✓ PDF generado exitosamente: {Path(archivo_tex).with_suffix('.pdf')}")
            return True
        else:
            print(f"⚠ Error al compilar {archivo_tex}")
            print(resultado.stdout[-500:] if len(resultado.stdout) > 500 else resultado.stdout)
            return False
            
    except FileNotFoundError:
        print("⚠ pdflatex no encontrado. Instala una distribución LaTeX (TeX Live, MiKTeX, etc.)")
        print("  Solo se generarán los archivos .tex")
        return False


def procesar_tema(archivo_yaml, template_path, output_dir, compilar=True):
    """
    Procesa un tema completo: carga YAML, genera LaTeX y opcionalmente compila.
    
    Args:
        archivo_yaml (str): Ruta al archivo YAML del tema
        template_path (str): Ruta al template LaTeX
        output_dir (str): Directorio de salida
        compilar (bool): Si se debe intentar compilar a PDF
    """
    print(f"\n→ Procesando: {Path(archivo_yaml).name}")
    
    # Cargar datos
    datos = cargar_yaml(archivo_yaml)
    
    # Generar nombre de salida
    nombre_base = Path(archivo_yaml).stem
    output_tex = Path(output_dir) / f"{nombre_base}.tex"
    
    # Crear directorio de salida si no existe
    Path(output_dir).mkdir(exist_ok=True)
    
    # Generar LaTeX
    generar_latex(datos, template_path, output_tex)
    
    # Compilar a PDF si se solicita
    if compilar:
        compilar_latex(str(output_tex))


def main():
    """Función principal del script."""
    # Configurar parser de argumentos
    parser = argparse.ArgumentParser(
        description='Generador de Diapositivas - Probabilidad y Estadística',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python generate_slides.py                           # Procesa archivos por defecto
  python generate_slides.py archivo.yml               # Procesa un archivo específico
  python generate_slides.py archivo1.yml archivo2.yml # Procesa múltiples archivos
  python generate_slides.py *.yml                     # Procesa todos los .yml (usando glob)
  python generate_slides.py clases/**/*.yml           # Procesa todos los .yml en subdirectorios
  python generate_slides.py -o pdfs archivo.yml       # Especifica directorio de salida
  python generate_slides.py -t mi_template.tex *.yml  # Usa un template personalizado
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
        help='Directorio de salida para los archivos generados (default: slides/)'
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
    clases_dir = directorio_base / "clases" / "probabilidad y estadistica"
    
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
        # Archivos por defecto
        temas = [
            clases_dir / "0-introduccion.yml",
            clases_dir / "1-tablas_graficos.yml",
            clases_dir / "2-medidas_posicion.yml",
            clases_dir / "3-reglas_probabilidades.yml"
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
            procesar_tema(tema, template_path, output_dir, compilar=True)
            procesados += 1
        else:
            print(f"⚠ Advertencia: No se encontró {tema}")
    
    print("\n" + "=" * 60)
    print(f"✓ Proceso completado. {procesados} archivo(s) procesado(s).")
    print(f"  Revisa el directorio: {output_dir}")
    print("=" * 60)


if __name__ == "__main__":
    main()
