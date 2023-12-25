import nglview


def view_pdb(pdb_file):
    view = nglview.show_structure_file(pdb_file)
    nglview.write_html(f'Diagrams/{pdb_file.split("/")[1].split(".")[0]}.html', view)
    return view
