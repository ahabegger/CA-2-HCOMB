import tkinter as tk
from tkinter import ttk, StringVar, BooleanVar
from PDB import download_pdb
import os


def gui():
    pdb_code = gui_pdb_selection()
    print(f"PDB Code: {pdb_code}")

    nonstandard = gui_toggables()
    print(f"Nonstandard: {nonstandard}")

    structure = gui_structure()
    print(f"Structure: {structure}")

    return pdb_code, nonstandard, structure


def gui_pdb_selection():
    # Create the main window
    root = tk.Tk()
    root.title("PDB2LatticePy - Model Input Options")

    # Create a Notebook widget
    nb = ttk.Notebook(root)

    # Section 1 Model Input
    frame1 = ttk.Frame(nb)
    nb.add(frame1, text="1. PDB Code")

    pdb_code_input = tk.StringVar()

    # Contents of Section 1
    tk.Label(frame1, text="Input Valid PDB Code").pack(fill='x', padx=5, pady=2)
    tk.Entry(frame1, textvariable=pdb_code_input).pack(fill='x', padx=5, pady=2)

    def check_pdb_in_folder(code, folder='PDB_Files'):
        # Construct the full path to the file
        file_path = os.path.join(folder, f"{code}.pdb")
        # Check if this file exists in the specified folder
        return os.path.isfile(file_path)

    def sec1frame1_save(pdb_code):
        if download_pdb(pdb_code):
            print("Successful Downloaded")
        else:
            print("Invalid Code")

        if check_pdb_in_folder(pdb_code):
            root.destroy()

    # Button Defined
    btn = tk.Button(frame1, text='Submit', command=lambda: sec1frame1_save(pdb_code_input.get()))
    btn.pack(side='bottom')

    # Section 1 Model Input
    frame2 = ttk.Frame(nb)
    nb.add(frame2, text="2. Preloaded Protein")

    # Dropdown menu for Lattice Type selection
    preloaded_proteins = StringVar(frame2)
    preloaded_proteins.set("Select Preloaded Protein")
    preloaded_proteins_options = [
        "1A80 = HIV CAPSID C-TERMINAL DOMAIN",
        "1MBS = HARBOR SEAL MYOGLOBIN",
        "3FXC = FERREDOXIN FROM SPIRULINA PLATENSIS",
        "4CTS = CITRATE SYNTHASE FROM SUS SCROFA",
        "5RXN = RUBREDOXIN FROM CLOSTRIDIUM PASTEURIANUM"
    ]
    tk.OptionMenu(frame2, preloaded_proteins, *preloaded_proteins_options).pack(fill='x', padx=5, pady=2)

    def sec1frame2_save(pdb_code):
        if check_pdb_in_folder(pdb_code):
            print(f"{pdb_code} Found in Files")
            root.destroy()

    # Button Defined
    btn = tk.Button(frame2, text='Submit', command=lambda: sec1frame2_save(preloaded_proteins.get()[:4]))
    btn.pack(side='bottom')

    # Section 1 Model Input
    frame3 = ttk.Frame(nb)
    nb.add(frame3, text="3. PDB File Text Input")

    custom_pdb_file_input = StringVar()

    tk.Label(frame3, text="Paste PDB File Text Input Here").pack(fill='x', padx=5, pady=2)
    tk.Entry(frame3, textvariable=custom_pdb_file_input).pack(fill='x', padx=5, pady=2)

    def sec1frame3_save(custom_pdb_file):
        code = "custom"
        with open('PDB_Files/custom.pdb', 'w') as file:
            file.write(custom_pdb_file)
        if check_pdb_in_folder(code):
            print(f"{code} Found in Files")
            root.destroy()

    # Button Defined
    btn = tk.Button(frame3, text='Submit', command=lambda: sec1frame3_save(custom_pdb_file_input.get()))
    btn.pack(side='bottom')

    # Pack the Notebook last so it fills the root window
    nb.pack(expand=True, fill='both')

    # Set a fixed size for the window
    root.geometry('700x250')

    root.mainloop()

    if len(custom_pdb_file_input.get()) > 20:
        return "custom"
    elif len(pdb_code_input.get()) > 2:
        return pdb_code_input.get()
    else:
        return preloaded_proteins.get()[:4]


def gui_toggables():
    root = tk.Tk()
    root.title("PDB2LatticePy - Toggable Options")

    # Create StringVar instances for different options
    nonstandard_input = BooleanVar()

    tk.Checkbutton(root, text="Include Non-Standard Amino Acids", variable=nonstandard_input).pack(fill='x', padx=5,
                                                                                                   pady=2)

    # Button Defined
    btn = tk.Button(root, text='Submit', command=root.destroy)
    btn.pack(side='bottom')

    # Set a fixed size for the window
    root.geometry('700x300')

    # Run the main window loop
    root.mainloop()

    nonstandard = nonstandard_input.get()

    return nonstandard


def gui_structure():
    # Create the main window
    root = tk.Tk()
    root.title("PDB2LatticePy - Structure Options")

    # Dropdown menu for Lattice Type selection
    structure = StringVar(root)
    structure.set("Select a Structure")
    structure_options = [
        "DEFAULT STRUCTURE",
        "1-DIMENSIONAL CUBIC LATTICE STRUCTURE"
        #"3-DIMENSIONAL CUBIC LATTICE STRUCTURE",
        #"TETRAHEDERAL LATTICE STRUCTURE"
    ]
    tk.OptionMenu(root, structure, *structure_options).pack(fill='x', padx=5, pady=2)

    # Button Defined
    btn = tk.Button(root, text='Submit', command=root.destroy)
    btn.pack(side='bottom')

    # Set a fixed size for the window
    root.geometry('700x350')

    root.mainloop()

    return structure.get()


if __name__ == "__main__":
    gui()
