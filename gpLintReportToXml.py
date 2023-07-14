import xml.etree.ElementTree as ET

def process_file(file_name):
    root = ET.Element("checkstyle", version="4.3")

    with open(file_name, "r") as f:
        lines = f.readlines()

    file_elem = None
    for line in lines:
        line = line.strip()
        if line.startswith("/"):
            file_name = line
            file_elem = ET.SubElement(root, "file", name=file_name)
        elif line.startswith("✖"):
            problems_line = line.split(" ")[1:]
            problems_count = problems_line[0]
            problems_message = " ".join(problems_line[1:])
            root.set("errors", problems_count)
            root.set("warnings", "0")
            root.set("version", "4.3")
            root.set("timestamp", "")
            root.set("severity", "")
            root.set("name", "")
            root.set("totalerrors", problems_count)
            root.set("totalwarnings", "0")
            root.set("totalfixes", "")
            root.set("fixableerrors", "")
            root.set("fixablewarnings", "")
            root.set("fixable", "")
            root.set("configlocation", "")
        elif line.startswith("   ") and "error" in line:
            parts = line.split("  ")
            loc = parts[0].strip()
            message = " ".join(parts[1:])
            line, column = loc.split(":")
            error_elem = ET.SubElement(file_elem, "error", line=line.strip(), column=column.strip(), severity="error", message=message.strip(), source="gplint")
        else:
            continue

    tree = ET.ElementTree(root)
    output_file = file_name.replace(".txt", ".xml")
    tree.write(output_file, xml_declaration=True, encoding="utf-8")

process_file("lint_output.txt")

<<<<<<< HEAD
=======
process_file("lint_output.txt")
>>>>>>> parent of 74d9ddb (aakskjsakas)
