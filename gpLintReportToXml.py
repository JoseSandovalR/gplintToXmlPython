import xml.etree.ElementTree as ET

def process_line(line):
    line = line.strip()
    parts = line.split("  ", 1)
    if len(parts) == 2:
        loc, message = parts
        if ":" in loc:
            line, column = loc.split(":")
            return line.strip(), column.strip(), message.strip()
    return None, None, None

def process_file(file_name):
    root = ET.Element("checkstyle", version="4.3")

    with open(file_name, "r") as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        file_line = lines[i].strip()
        if file_line.startswith("/"):
            file_name = file_line
            file_elem = ET.SubElement(root, "file", name=file_name)

            i += 1
            line, column, message = process_line(lines[i])
            while line is not None:
                ET.SubElement(file_elem, "error", line=line, column=column, severity="error", message=message, source="gplint")
                i += 1
                line, column, message = process_line(lines[i])

        i += 1
        if "problems" in lines[i]:
            break

    tree = ET.ElementTree(root)
    tree.write("report.xml", xml_declaration=True, encoding="utf-8")

process_file("lint_output.txt")
