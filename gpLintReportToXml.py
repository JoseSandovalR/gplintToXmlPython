import os
import re
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

# Ruta del archivo de salida de gplint
output_file = 'lint_output.txt'

# Leer la salida de gplint desde el archivo
with open(output_file, 'r') as file:
    output = file.readlines()

# Expresión regular para analizar las líneas de error
pattern = r'(?P<file_path>.+)\n\s+(?P<line>\d+:\d+)\s+(?P<severity>\w+)\s+(?P<message>.+)'

# Crear un informe XML básico
root = Element('checkstyle')
root.set('version', '4.3')

# Asumir que cada línea es un problema
for line in output:
    match = re.match(pattern, line)
    if match:
        file_path = match.group('file_path').strip()
        line_info = match.group('line').split(':')
        line_number = line_info[0]
        severity = match.group('severity').strip()
        message = match.group('message').strip()

        file = SubElement(root, 'file')
        file.set('name', os.path.basename(file_path))
        error = SubElement(file, 'error')
        error.set('line', line_number)
        error.set('severity', severity)
        error.set('message', message)
        error.set('source', 'gplint')

# Convertir a string con formato bonito
xml_string = minidom.parseString(tostring(root)).toprettyxml(indent="   ")

# Escribir el informe XML en un archivo
with open('report.xml', 'w') as file:
    file.write(xml_string)
