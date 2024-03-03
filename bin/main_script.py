import sys
import os

# Obtiene la ruta absoluta al directorio donde se encuentra actualmente main_script.py
current_script_path = os.path.dirname(os.path.abspath(__file__))
# Sube un nivel en la estructura de directorios para llegar al directorio raíz del proyecto
project_root_path = os.path.join(current_script_path, '..')
# Añade el directorio raíz del proyecto a sys.path
sys.path.append(os.path.normpath(project_root_path))


##################
#### MODULE 1 ####
##################

from src.coauthors_affiliation import get_dois_from_ORCID

import requests
import json
import csv
import os
import pandas as pd

author_name = "A_LUQUE"
output_path = "results/"
generate_individual_files = False
include_timestamp = True
global_json_file = os.path.join(output_path, f'{author_name}_all_articles_extensive_data.json')

# Example usage get_combined_dois
orcid_id = "0000-0002-5817-4914" # Replace with the actual ORCID ID
query_dois = get_dois_from_ORCID.get_combined_dois(orcid_id)


##################
#### MODULE 2 ####
##################

from src.coauthors_affiliation import fetch_coauthors_data

fetch_coauthors_data.generate_global_json_file(query_dois, generate_individual_files,global_json_file)
global_df = fetch_coauthors_data.generate_global_df(global_json_file)
csv_file = global_json_file.replace('.json', '.csv')
global_df.to_csv(csv_file, index=False)

print(global_df)