C:\Users\erick.merino\AppData\Roaming\Python\Python313\Scripts\uv sync
C:\Users\erick.merino\AppData\Roaming\Python\Python313\Scripts\uv run generate_slides.py "clases\probabilidad y estadistica\*.yml" -o slides -t template.tex
cd pdfs
call convertir_latex.bat
cd ..