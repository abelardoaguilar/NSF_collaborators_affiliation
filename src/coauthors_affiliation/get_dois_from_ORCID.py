import requests
import json
import csv
import os
import pandas as pd

def get_orcid_articles(orcid_id):
    # Replace 'YOUR_ACCESS_TOKEN' with an actual ORCID API access token if needed.
    headers = {
        'Accept': 'application/json',
        #'Authorization': 'Bearer YOUR_ACCESS_TOKEN',
    }
    
    # Construct the URL to access the ORCID record
    url = f'https://pub.orcid.org/v3.0/{orcid_id}/works'
    
    # Make the request to the ORCID API
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        dois = []
        
        # Loop through the returned works and extract the DOIs
        for work in data.get('group', []):
            for work_summary in work.get('work-summary', []):
                doi = work_summary.get('external-ids', {}).get('external-id', [])
                for id in doi:
                    if id.get('external-id-type') == 'doi':
                        dois.append(id.get('external-id-value'))
        
        return dois
    else:
        print(f'Failed to retrieve data for ORCID ID {orcid_id}. Status code: {response.status_code}')
        return []


def get_crossref_articles(orcid_id):
    """
    Retrieves a list of DOIs for publications associated with a given ORCID ID from CrossRef.

    Parameters:
    orcid_id (str): The ORCID ID of the author.

    Returns:
    list: A list of DOIs for the author's publications.
    """
    # Base URL for CrossRef API
    crossref_api_url = "https://api.crossref.org/works"
    # Parameters for the API request, filtering by ORCID ID
    params = {
        'filter': f'orcid:{orcid_id}',
        'rows': 1000  # Adjust the number of results as needed
    }
    
    # Perform the API request
    response = requests.get(crossref_api_url, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        # Extract DOIs from the items in the response
        dois = [item['DOI'] for item in data['message']['items']]
        return dois
    else:
        print(f"Error fetching data: HTTP {response.status_code}")
        return []


def get_combined_dois(orcid_id):
    orcid_dois = get_orcid_articles(orcid_id)
    crossref_dois = get_crossref_articles(orcid_id)
    combined_dois = orcid_dois + crossref_dois
    unique_dois = list(set(combined_dois))
    
    # Print summary
    print(f"DOIs for ORCID ID:{orcid_id}\n")
    print(f"Number of DOIs from ORCID: {len(orcid_dois)}")
    print(f"Number of DOIs from CrossRef: {len(crossref_dois)}")
    print(f"Total number of unique DOIs: {len(unique_dois)}")
    
    return unique_dois




