@echo off
echo ============================================================
echo Generando PDFs desde archivos LaTeX en slides/
echo ============================================================
echo.

cd /d "%~dp0"

for %%f in (..\slides\*.tex) do (
    echo Compilando %%~nf.tex...
    C:/Users/erick.merino/AppData/Local/Programs/MiKTeX/miktex/bin/x64/pdflatex -interaction=nonstopmode -output-directory=. "%%f"
    if exist "%%~nf.pdf" (
        echo   [OK] %%~nf.pdf generado
    ) else (
        echo   [ERROR] No se pudo generar %%~nf.pdf
    )
    echo.
)

echo.
echo Limpiando archivos auxiliares...
del *.aux *.log *.out *.nav *.snm *.toc 2>nul

echo.
echo ============================================================
echo Proceso completado! Los PDFs estan en la carpeta pdfs/
echo ============================================================
pause
