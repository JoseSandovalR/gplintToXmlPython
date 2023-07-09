import os
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

# Ruta del archivo de salida de gplint
output_file = 'lint_output.txt'

# Leer la salida de gplint desde el archivo
with open(output_file, 'r') as file:
    lines = file.readlines()

# Crear un informe XML básico
root = Element('checkstyle')
root.set('version', '4.3')

# Variables para almacenar la ruta del archivo y el número de línea
file_path = ''
line_number = ''

# Iterar sobre las líneas del archivo
for line in lines:
    line = line.strip()
    if not line:
        continue

    # Si la línea contiene una ruta de archivo, guardarla
    if os.path.isfile(line):
        file_path = line
        continue

    # Asumir que la línea tiene el formato "linea:columna nivel mensaje"
    parts = line.split(' ', maxsplit=3)
    if len(parts) == 4:
        line_number, _, severity, message = parts

        file = SubElement(root, 'file')
        file.set('name', os.path.basename(file_path))
        error = SubElement(file, 'error')
        error.set('line', line_number.strip())
        error.set('column', '0')
        error.set('severity', severity.strip())
        error.set('message', message.strip())
        error.set('source', 'gplint')

# Convertir a string con formato bonito
xml_string = minidom.parseString(tostring(root)).toprettyxml(indent="   ")

# Escribir el informe XML en un archivo
with open('report.xml', 'w') as file:
    file.write(xml_string)
