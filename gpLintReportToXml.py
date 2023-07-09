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
        parts = line.split(' ', maxsplit=2)
        if len(parts) == 3:
            file_location, line_column, message = parts
            file_parts = file_location.split(':')
            if len(file_parts) == 2:
                file_path, _ = file_parts
                line, column = line_column.split(':')

                file = SubElement(root, 'file')
                file.set('name', os.path.basename(file_path.strip()))
                error = SubElement(file, 'error')
                error.set('line', line.strip())
                error.set('column', column.strip())
                error.set('severity', 'error')
                error.set('message', message.strip())
                error.set('source', 'gplint')

# Convertir a string con formato bonito
xml_string = minidom.parseString(tostring(root)).toprettyxml(indent="   ")

# Escribir el informe XML en un archivo
with open('report.xml', 'w') as file:
    file.write(xml_string)

