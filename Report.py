def create_report(pdb_code):
    title = ""
    with open(f"PDB_Files/{pdb_code}.pdb") as file:
        for line in file:
            if "TITLE" in line:
                title += line

    input_diagram = ""
    with open(f"Diagrams/{pdb_code}.html") as file:
        for line in file:
            input_diagram += line
    input_diagram = input_diagram.split("body>")[1][:-2]

    output_diagram = ""
    with open(f"Diagrams/{pdb_code}_modified.html") as file:
        for line in file:
            output_diagram += line
    output_diagram = output_diagram.split("body>")[1][:-2]

    changes = ""
    with open(f"Modified_PDB_Files/{pdb_code}_modified.pdb") as file:
        for line in file:
            if "REMARK" in line:
                changes += '<p>' + line + '</p>\n'

    top = f"<!DOCTYPE html>\n" \
          f"<html lang=\"en\">\n" \
          f"<head>\n" \
          f"   <meta charset=\"UTF-8\">\n" \
          f"   <title>{pdb_code} Transformation</title>\n" \
          f'<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" ' \
          f'integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" ' \
          f'crossorigin="anonymous">\n' \
          f"</head>\n" \
          f"<body>\n" \
          f"<h1>PDB2LatticePy Report</h1>\n" \
          f"<h2>{pdb_code} M2M Transformation</h2>\n"
    for part in title.replace('TITLE', '').split('\n'):
        top += f"<h2>{part}</h2>\n"
    top += f"<h3>Input Model</h3>\n"

    bottom = '</body>\n<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" ' \
             'integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" ' \
             'crossorigin="anonymous"></script>\n</html> '

    middle = '<h3>Changes</h3>\n' \
             f'{changes.replace("REMARK", "")}\n' \
             '<h3>Output Model</h3>\n'

    code = top + input_diagram + middle + output_diagram + bottom
    with open(f"Reports/{pdb_code}_transformation.html", 'w') as file:
        file.write(code)


if __name__ == "__main__":
    create_report("3FXC")
