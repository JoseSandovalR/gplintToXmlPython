import os
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

# Ruta del archivo de salida de gplint
output_file = 'lint_output.txt'

# Leer la salida de gplint desde el archivo
with open(output_file, 'r') as file:
    output = file.read()

# Crear un informe XML básico
root = Element('checkstyle')
root.set('version', '4.3')

# Asumir que cada línea es un problema
lines = output.split('\n')
i = 0
while i < len(lines):
    file_path = lines[i].strip()
    if file_path:
        line_info = lines[i+1].strip().split()
        line_number = line_info[0]
        severity = line_info[1]
        message = ' '.join(line_info[2:])

        file = SubElement(root, 'file')
        file.set('name', os.path.basename(file_path))
        error = SubElement(file, 'error')
        error.set('line', line_number)
        error.set('severity', severity)
        error.set('message', message)
        error.set('source', 'gplint')

    i += 2

# Convertir a string con formato bonito
xml_string = minidom.parseString(tostring(root)).toprettyxml(indent="   ")

# Escribir el informe XML en un archivo
with open('report.xml', 'w') as file:
    file.write(xml_string)
