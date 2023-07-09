import os
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

# Ruta del archivo de salida de gplint
output_file = 'lint_output.txt'

# Leer la salida de gplint desde el archivo
with open(output_file, 'r') as file:
    output = file.readlines()

# Crear un informe XML básico
root = Element('checkstyle')
root.set('version', '4.3')

# Asumir que cada línea es un problema
for line in output:
    line = line.strip()
    if line:
        # Asumir que la línea tiene el formato "ruta_archivo linea:columna nivel mensaje"
        parts = line.split('  ')
        file_path = parts[0]
        line_info = parts[1].split(':')
        line_number = line_info[0]
        severity = line_info[1].strip()
        message = ' '.join(parts[2:]).strip()

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
