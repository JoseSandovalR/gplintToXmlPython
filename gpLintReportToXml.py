import xml.etree.ElementTree as ET
import re

def parse_line(line):
    split_line = line.split(' ', 3)
    file_path = split_line[0]
    line_col = split_line[1].split(':')
    severity = split_line[2]
    message = split_line[3].strip()

    return file_path, line_col[0], line_col[1], severity, message

def main():
    root = ET.Element('checkstyle')
    root.set('version', '4.3')

    with open('lint_output.txt', 'r') as file:
        lines = file.readlines()
        for line in lines[:-1]:  # Ignoramos la última línea
            file_path, line_num, col_num, severity, message = parse_line(line)
            file_element = ET.SubElement(root, 'file')
            file_element.set('name', file_path)

            error_element = ET.SubElement(file_element, 'error')
            error_element.set('line', line_num)
            error_element.set('column', col_num)
            error_element.set('severity', severity)
            error_element.set('message', message)
            error_element.set('source', 'gplint')

        # Añadimos el total de errores y advertencias
        total_errors = re.findall('\d+', lines[-1])
        file_element = ET.SubElement(root, 'file')
        file_element.set('name', '✖')

        error_element = ET.SubElement(file_element, 'error')
        error_element.set('line', str(len(lines) - 1))
        error_element.set('column', '0')
        error_element.set('severity', 'problems')
        error_element.set('message', f'({total_errors[0]} errors, {total_errors[1]} warnings)')
        error_element.set('source', 'gplint')

    # Escribimos el XML en un archivo
    tree = ET.ElementTree(root)
    tree.write('report.xml')

if __name__ == '__main__':
    main()
