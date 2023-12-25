import requests


def download_pdb(pdb_id):
    """
    Download a PDB file given the PDB ID.

    Args:
    pdb_id (str): The ID of the PDB record.
    """
    # Construct the URL
    url = f'https://files.rcsb.org/download/{pdb_id}.pdb'

    # Send a request to the URL
    response = requests.get(url)

    # If the request was successful
    if response.status_code == 200:
        # The destination file path (you may want to customize this)
        file_path = f'PDB_Files/{pdb_id}.pdb'

        # Write the response content (the PDB file) to a local file
        with open(file_path, 'wb') as file:
            file.write(response.content)
        return True
    else:
        print(f'Error downloading {pdb_id}.pdb. Status code: {response.status_code}')
        return False
