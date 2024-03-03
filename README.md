# NSF_collaborators_affiliation
Temporary repo to develop a Python package with the purpose of creating a table with the information of coauthors, needed for NSF grant proposals

## Proposed structure

```
proyecto/
│
├── bin/
│   └── script_principal.py  # Script principal que utiliza funciones de los módulos
│
├── src/
│   └── coauthors_affiliation/
│       ├── __init__.py
│       ├── get_dois_from_ORCID.py
│       ├── fetch_coauthors_data.py
│       └── final_formatting.py
│
├── data/
│   └── ...  # Datos utilizados o generados por el proyecto
│
└── results/
    └── ...  # Resultados generados por el proyecto
```