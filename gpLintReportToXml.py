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

# Variables para guardar información del archivo actual
current_file = None

# Iterar sobre las líneas del archivo
for line in lines:
    line = line.strip()
    if not line:
        continue

    # Si la línea comienza con "<file name=", crear un nuevo elemento "file"
    if line.startswith("<file name="):
        file_name = line.split('"')[1]
        current_file = SubElement(root, 'file')
        current_file.set('name', file_name)
        continue

    # Asumir que la línea tiene el formato "<error line=" línea " column=" columna " severity=" nivel " message=" mensaje " source="gplint"/>"
    parts = line.split('"')
    if len(parts) == 11:
        error = SubElement(current_file, 'error')
        error.set('line', parts[3].strip())
        error.set('column', parts[7].strip())
        error.set('severity', parts[5].strip())
        error.set('message', parts[9].strip())
        error.set('source', 'gplint')

# Convertir a string con formato bonito
xml_string = minidom.parseString(tostring(root)).toprettyxml(indent="   ")

# Escribir el informe XML en un archivo
with open('report.xml', 'w') as file:
    file.write(xml_string)

