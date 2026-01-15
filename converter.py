import os
import json
import requests
from bs4 import BeautifulSoup

def pdf_to_json(pdf_path, output_json_path):
    """
    Convert PDF to JSON using GROBID REST API directly.
    This is more reliable than using the grobid-client library.
    """
    # Check if GROBID server is running
    try:
        response = requests.get("http://localhost:8070/api/isalive", timeout=5)
        if response.status_code != 200 or response.text.strip() != "true":
            raise Exception("GROBID server is not responding correctly")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Cannot connect to GROBID server at http://localhost:8070. "
                       f"Make sure Docker is running with GROBID container. Error: {e}")
    
    print(f"Processing {pdf_path}...")
    
    # Use GROBID REST API directly
    url = "http://localhost:8070/api/processFulltextDocument"
    
    with open(pdf_path, 'rb') as pdf_file:
        files = {'input': pdf_file}
        params = {
            'generateIDs': '1',
            'consolidateHeader': '1',
            'consolidateCitations': '0',
            'includeRawCitations': '0',
            'includeRawAffiliations': '0',
            'segmentSentences': '0'
        }
        
        response = requests.post(url, files=files, data=params, timeout=60)
    
    if response.status_code != 200:
        raise Exception(f"GROBID processing failed with status {response.status_code}: {response.text[:200]}")
    
    xml_content = response.text
    
    if not xml_content or len(xml_content) < 100:
        raise Exception(f"Invalid XML response from GROBID (too short): {xml_content[:100]}")
    
    print(f"Received XML from GROBID ({len(xml_content)} characters)")
    
    # 2. Parse XML to JSON using BeautifulSoup
    soup = BeautifulSoup(xml_content, 'xml')
    
    document_data = {
        "title": "",
        "authors": [],
        "abstract": "",
        "sections": []
    }

    # Extract Title
    title_tag = soup.find('title', type='main')
    if title_tag:
        document_data['title'] = title_tag.text

    # Extract Authors
    authors = []
    source_desc = soup.find('sourceDesc')
    if source_desc:
        for author in source_desc.find_all('author'):
            pers_name = author.find('persName')
            if pers_name:
                forename = pers_name.find('forename')
                surname = pers_name.find('surname')
                name_parts = []
                if forename: name_parts.append(forename.text)
                if surname: name_parts.append(surname.text)
                if name_parts:
                    authors.append(" ".join(name_parts))
    
    document_data['authors'] = authors

    # Extract Abstract
    abstract_tag = soup.find('abstract')
    if abstract_tag:
        document_data['abstract'] = abstract_tag.text.strip()

    # Extract Sections (Headings + Paragraphs)
    # GROBID usually puts body content in <body> -> <div>
    body = soup.find('body')
    if body:
        for div in body.find_all('div'):
            head = div.find('head')
            heading = head.text if head else "No Heading"
            
            paragraphs = []
            for p in div.find_all('p'):
                paragraphs.append(p.text)
            
            if paragraphs:
                document_data['sections'].append({
                    "heading": heading,
                    "content": "\n".join(paragraphs)
                })

    # 3. Save to JSON file
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(document_data, f, indent=4)
        
    print(f"Saved JSON to {output_json_path}")
    print(f"  - Title: {document_data['title'][:50] if document_data['title'] else 'N/A'}...")
    print(f"  - Authors: {len(document_data['authors'])}")
    print(f"  - Abstract: {'✓' if document_data['abstract'] else '✗'}")
    print(f"  - Sections: {len(document_data['sections'])}")
    
    return document_data

if __name__ == "__main__":
    # Test run
    pdf_file = "paper.pdf"  # Replace with your PDF name
    if os.path.exists(pdf_file):
        pdf_to_json(pdf_file, "paper_data.json")
    else:
        print(f"Please place a '{pdf_file}' in this folder to test.")