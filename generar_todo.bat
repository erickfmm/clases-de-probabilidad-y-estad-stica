@echo off
echo ============================================================
echo Generando todas las presentaciones desde clases/**/*.yml
echo ============================================================
echo.

echo [1/2] Generando presentaciones LaTeX/PDF...
echo ------------------------------------------------------------
python generate_slides.py
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Fallo al generar PDFs
    pause
    exit /b 1
)

echo.
echo [2/2] Generando presentaciones PowerPoint...
echo ------------------------------------------------------------
python generate_pptx.py
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Fallo al generar PPTX
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Proceso completado exitosamente!
echo.
echo Archivos generados:
echo   - PDFs en:  pdfs/[materia]/
echo   - PPTXs en: pptx/[materia]/
echo   - TEXs en:  slides/
echo ============================================================
pause
