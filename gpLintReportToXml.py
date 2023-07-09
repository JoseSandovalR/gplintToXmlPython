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
for line in output.split('\n'):
    line = line.strip()
    if line:
        # Asumir que la línea tiene el formato "ruta_archivo:linea:columna:nivel:mensaje"
        parts = line.split(':', maxsplit=4)
        if len(parts) >= 5:
            file = SubElement(root, 'file')
            file.set('name', os.path.basename(parts[0].strip()))
            error = SubElement(file, 'error')
            error.set('line', parts[1].strip())
            error.set('column', parts[2].strip())
            error.set('severity', parts[3].strip())
            error.set('message', parts[4].strip())
            error.set('source', 'gplint')

# Convertir a string con formato bonito
xml_string = minidom.parseString(tostring(root)).toprettyxml(indent="   ")

# Escribir el informe XML en un archivo
with open('report.xml', 'w') as file:
    file.write(xml_string)
)