import requests
import json
import csv
import os
import pandas as pd

def fetch_article_data(doi):
    """
    Fetches article data from CrossRef using DOI.
    """
    url = f"https://api.crossref.org/works/{doi}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed to fetch data for DOI: {doi}")
        return None

def extract_author_data(article_data):
    """
    Extracts author data from CrossRef article data.
    """
    authors = article_data['message']['author']
    author_data = []
    for author in authors:
        author_info = {
            'given_name': author.get('given', ''),
            'family_name': author.get('family', ''),
            'affiliation': []
        }
        if 'affiliation' in author:
            if isinstance(author['affiliation'], list):
                for affiliation in author['affiliation']:
                    if isinstance(affiliation, str):
                        author_info['affiliation'].append(affiliation)
                    elif isinstance(affiliation, dict) and 'name' in affiliation:
                        author_info['affiliation'].append(affiliation['name'])
            elif isinstance(author['affiliation'], str):
                author_info['affiliation'].append(author['affiliation'])
        author_data.append(author_info)
    return author_data

def save_article_data_to_json(article_data, author_data, doi):
    """
    Saves article data and author data to a JSON file.
    """
    article_message = article_data.get('message', {})
    
    title = article_message.get('title', [''])[0]
    
    container_title = article_message.get('container-title', [])
    journal = container_title[0] if container_title else ''
    
    publication_date = ''
    if 'published-online' in article_message:
        date_parts = article_message['published-online'].get('date-parts', [[]])
        if date_parts:
            publication_date = date_parts[0][0]

    filename = f'article_data_{doi.replace("/", "_")}.json'
    
    data_to_save = {
        'article': {
            'title': title,
            'journal': journal,
            'doi': doi,
            'publication_date': publication_date
        },
        'authors': author_data
    }

    with open(filename, 'w') as f:
        json.dump(data_to_save, f, indent=4)


def generate_global_json_file(dois, generate_individual_files, global_json_file):
    all_articles_data = []

    for doi in dois:
        article_data = fetch_article_data(doi)
        if article_data:
            author_data = extract_author_data(article_data)
            print(f"Authors data for DOI {doi}:")
            for author in author_data:
                print(f"Name: {author['given_name']} {author['family_name']}")
                print(f"Affiliation(s): {', '.join(author['affiliation']) if author['affiliation'] else 'Not available'}")
                print()
            print()
            if generate_individual_files:
                save_article_data_to_json(article_data, author_data, doi)
            if 'message' in article_data and 'title' in article_data['message'] and 'container-title' in article_data['message'] and 'published-online' in article_data['message']:
                all_articles_data.append({
                    'doi': doi,
                    'article_data': {
                        'title': article_data['message']['title'][0],
                        'journal': article_data['message']['container-title'][0],
                        'doi': doi,
                        'publication_date': article_data['message']['published-online']['date-parts'][0][0]
                    },
                    'author_data': author_data
                })

    with open(global_json_file, 'w') as f:
        json.dump(all_articles_data, f, indent=4)


def generate_global_df(global_json_file):
    # Read the contents of the global_json_file
    with open(global_json_file, 'r') as f:
        data = json.load(f)

    # Create an empty list to store the rows
    rows = []

    # Iterate over the data and create a row for each article+author combination
    for article_data in data:
        doi = article_data['doi']
        title = article_data['article_data']['title']
        journal = article_data['article_data']['journal']
        publication_date = article_data['article_data']['publication_date']
        authors = article_data['author_data']

        for author in authors:
            given_name = author['given_name']
            family_name = author['family_name']
            affiliation = ', '.join(author['affiliation']) if author['affiliation'] else 'Not available'

            row = {
                'DOI': doi,
                'Title': title,
                'Journal': journal,
                'Publication Date': publication_date,
                'Given Name': given_name,
                'Family Name': family_name,
                'Affiliation': affiliation
            }

            rows.append(row)

    # Create the dataframe
    df = pd.DataFrame(rows)

    return df
