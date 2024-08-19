import functions_framework
import json
import zipfile
from gcloud import storage
from googleapiclient.discovery import build
from bs4 import BeautifulSoup
import requests
import pdfplumber

@functions_framework.http
def http_triggered_function(request):
    try:

        scrape_and_upload_to_gcs_1()
        scrape_and_upload_to_gcs_2()
        scrape_and_upload_to_gcs_3()
        scrape_and_upload_to_gcs_4()
        scrape_and_upload_to_gcs_5()
        scrape_and_upload_to_gcs_6()
        scrape_and_upload_to_gcs_7()
        scrape_and_upload_to_gcs_8()
        scrape_and_upload_to_gcs_9()
        scrape_and_upload_to_gcs_10()
        # scrape_and_upload_to_gcs_11()
        # scrape_and_upload_to_gcs_12()
        # scrape_and_upload_to_gcs_13()
        # scrape_and_upload_to_gcs_14()
        # scrape_and_upload_to_gcs_15()
        # scrape_and_upload_to_gcs_16()
        # scrape_and_upload_to_gcs_17()
        # scrape_and_upload_to_gcs_18()
        # scrape_and_upload_to_gcs_19()
        
        return {
            'statusCode': 200,
            'body': json.dumps('Functions executed successfully.')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }
def storage_client():
    storage_client = storage.Client()
    bucket = storage_client.bucket("beacon-database")


def scrape_and_upload_to_gcs_1():
    from gcloud import storage
    import json
    from bs4 import BeautifulSoup
    import requests

    # URL of the page to scrape
    url = 'https://childmind.org/guide/autism-spectrum-disorder-quick-guide/'
    
    # GCS Configuration
    gcs_bucket_name = 'beacon-database'  # Replace with your GCS bucket name
    gcs_blob_name = 'asd_guide.json'  # Replace with the desired blob name

    # Set up headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # Fetch the web page using requests with headers
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the specific div by class
        target_div = soup.find('div', class_='w-full mt-16 md:px-3 md:row-span-2 xl:row-span-1')

        # Extract content from p, h2, h3, and ul tags within the specific div
        data = []
        if target_div:
            for tag in target_div.find_all(['p', 'h2', 'h3', 'ul']):
                tag_name = tag.name
                tag_content = tag.get_text(strip=True)
                
                # Handle lists separately
                if tag_name == 'ul':
                    list_items = [li.get_text(strip=True) for li in tag.find_all('li')]
                    tag_content = '\n'.join(list_items)
                
                data.append({
                    'tag': tag_name,
                    'content': tag_content
                })
        else:
            print("Target div not found")

        # Debugging: Print the length and content of the data list
        print(f"Number of items extracted: {len(data)}")
        print("Data extracted:")
        for item in data:
            print(item)

        # Convert data to JSON format
        data_json = json.dumps(data, ensure_ascii=False)

        # Google Cloud Storage Configuration
        storage_client = storage.Client()
        bucket = storage_client.bucket(gcs_bucket_name)
        blob = bucket.blob(gcs_blob_name)

        # Upload data to GCS
        try:
            blob.upload_from_string(data_json, content_type='application/json')
            print("Data successfully uploaded to GCS")

            #clearing for storage
            data_json=None
            data=None
        except Exception as e:
            print(f"Error uploading data to GCS: {e}")

    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        
def scrape_and_upload_to_gcs_2():
    import json
    from bs4 import BeautifulSoup
    import requests
    from gcloud import storage
    from google.api_core.exceptions import GoogleAPIError
    import os

    # Step 1: Fetch the web page
    url = 'https://www.mayoclinic.org/diseases-conditions/autism-spectrum-disorder/symptoms-causes/syc-20352928'
    response = requests.get(url)
    html_content = response.text

    # Step 2: Parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the contentbox div
    contentbox_div = soup.find('div', class_='contentbox')

    # Initialize an empty list to store data
    data = []

    # Only proceed if the contentbox_div is found
    if contentbox_div:
        # Start from the next sibling of contentbox_div
        for div in contentbox_div.find_all_next('div', recursive=False):
            # Break if a div with class 'requestappt' is encountered
            if 'requestappt' in div.get('class', []):
                break

            # Extract content from p, h2, h3, and ul tags within the div
            for tag in div.find_all(['p', 'h2', 'h3', 'ul']):
                tag_name = tag.name
                tag_content = tag.get_text(strip=True)
                
                # Handle lists separately
                if tag_name == 'ul':
                    list_items = [li.get_text(strip=True) for li in tag.find_all('li')]
                    tag_content = '\n'.join(list_items)
                
                data.append({
                    'tag': tag_name,
                    'content': tag_content
                })

    # Step 3: Convert data to JSON format
    data_json = json.dumps(data, ensure_ascii=False)

    # Step 4: Google Cloud Storage (GCS) Configuration
    gcs_bucket_name = 'beacon-database'
    gcs_key = 'asd_symptoms.json'

    # Initialize Google Cloud Storage client
    storage_client = storage.Client()

    try:
        # Upload JSON file to GCS
        bucket = storage_client.get_bucket(gcs_bucket_name)
        blob = bucket.blob(gcs_key)
        blob.upload_from_string(data_json, content_type='application/json')
        print("Data successfully uploaded to GCS")

        #clearing for storage
        data_json=None
        data=None
    except GoogleAPIError as e:
        print(f"Failed to upload to GCS: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
        
def scrape_and_upload_to_gcs_3():
    import json
    from bs4 import BeautifulSoup
    import requests
    from gcloud import storage
    from google.api_core.exceptions import GoogleAPIError

    # Step 1: Fetch the web page
    url = 'https://autism.org/what-is-autism/'
    response = requests.get(url)
    html_content = response.text

    # Step 2: Parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all div elements with the specified classes
    data = []
    divs1 = soup.find_all('div', class_='fusion-text fusion-text-1')
    divs2 = soup.find_all('div', class_='fusion-text fusion-text-2')

    # Extract content from the first class
    for div in divs1:
        div_content = div.get_text(strip=True)
        data.append({
            'class': 'fusion-text-1',
            'content': div_content
        })

    # Extract content from the second class
    for div in divs2:
        div_content = div.get_text(strip=True)
        data.append({
            'class': 'fusion-text-2',
            'content': div_content
        })

    # Convert data to JSON format
    data_json = json.dumps(data, ensure_ascii=False)

    # Step 3: Google Cloud Storage (GCS) Configuration
    gcs_bucket_name = 'beacon-database'
    gcs_key = 'autism_info.json'

    # Initialize Google Cloud Storage client
    storage_client = storage.Client()

    try:
        # Upload JSON data to GCS
        bucket = storage_client.get_bucket(gcs_bucket_name)
        blob = bucket.blob(gcs_key)
        blob.upload_from_string(data_json, content_type='application/json')
        print("Data successfully uploaded to GCS")

        #clearing for storage
        data_json=None
        data=None
    except GoogleAPIError as e:
        print(f"Failed to upload to GCS: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    
def scrape_and_upload_to_gcs_4():
    import json
    from bs4 import BeautifulSoup
    import requests
    import pdfplumber
    from gcloud import storage
    from google.api_core.exceptions import GoogleAPIError

    # Step 1: Download the PDF
    url = "https://portal.ct.gov/-/media/dph/cyshcn/ct-collaborative-autism-services-resource-directory.pdf"
    response = requests.get(url)
    
    # Save to /tmp directory in Lambda
    pdf_path = "/tmp/resource_directory.pdf"
    with open(pdf_path, "wb") as file:
        file.write(response.content)

    # Step 2: Extract Data from the PDF
    def extract_text_from_pdf(pdf_path):
        text_data = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text_data.extend(page.extract_text().split('\n'))
        return text_data

    pdf_text_lines = extract_text_from_pdf(pdf_path)

    # Step 3: Parse Data
    def parse_text(lines):
        parsed_data = []
        entry = {}
        for line in lines:
            if line.strip() == '':  # Assuming a blank line indicates a new entry
                if entry:
                    parsed_data.append(entry)
                    entry = {}
            else:
                if "Organization:" in line:
                    if entry:  # Save the previous entry if it exists
                        parsed_data.append(entry)
                    entry = {"organization": line.replace("Organization:", "").strip()}
                elif "Contact:" in line:
                    entry["contact_info"] = line.replace("Contact:", "").strip()
                elif "Services:" in line:
                    entry["services"] = line.replace("Services:", "").strip()
                else:
                    # Handle additional lines or append to existing entry fields
                    if "additional_info" in entry:
                        entry["additional_info"] += " " + line.strip()
                    else:
                        entry["additional_info"] = line.strip()
        if entry:
            parsed_data.append(entry)
        return parsed_data

    structured_data = parse_text(pdf_text_lines)

    # Convert structured data to JSON
    json_data = json.dumps(structured_data, ensure_ascii=False, indent=4)

    # Step 4: Google Cloud Storage (GCS) Configuration
    gcs_bucket_name = 'beacon-database'
    gcs_key = 'autism_services_resource_directory.json'

    # Initialize Google Cloud Storage client
    storage_client = storage.Client()

    try:
        # Upload JSON data to GCS
        bucket = storage_client.get_bucket(gcs_bucket_name)
        blob = bucket.blob(gcs_key)
        blob.upload_from_string(json_data, content_type='application/json')
        print("Data successfully uploaded to GCS")

        #clearing for storage
        data=None
        structured_data=None
        pdf_text_lines=None

    except GoogleAPIError as e:
        print(f"Failed to upload to GCS: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def scrape_and_upload_to_gcs_5():
    import json
    from bs4 import BeautifulSoup
    import requests
    from gcloud import storage
    from google.api_core.exceptions import GoogleAPIError

    # Fetch the webpage content
    url = 'https://www.connecticutchildrens.org/specialties-conditions/developmental-behavioral-pediatrics/autism-spectrum-disorder-asd'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract data
    data = []

    # Function to clean the text content
    def clean_text(text):
        return text.strip()  # Clean up the text content

    # Find and extract all <p> tags
    for tag in soup.find_all('p'):
        text_content = clean_text(tag.get_text(strip=True))
        data.append({
            'tag': tag.name,
            'content': text_content
        })

    # Convert data to JSON format
    json_data = json.dumps(data, ensure_ascii=False, indent=4)

    # Google Cloud Storage (GCS) Configuration
    gcs_bucket_name = 'beacon-database'
    gcs_key = 'autism_spectrum_disorder.json'

    # Initialize Google Cloud Storage client
    storage_client = storage.Client()

    try:
        # Upload JSON data to GCS
        bucket = storage_client.get_bucket(gcs_bucket_name)
        blob = bucket.blob(gcs_key)
        blob.upload_from_string(json_data, content_type='application/json')
        print("Data successfully uploaded to GCS")

        #clearing for storage
        data=None
        json_data=None
    except GoogleAPIError as e:
        print(f"Failed to upload to GCS: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def scrape_and_upload_to_gcs_6():
    import json
    from bs4 import BeautifulSoup
    import requests
    from gcloud import storage
    from google.api_core.exceptions import GoogleAPIError

    # Step 1: Fetch the web page
    url = 'https://www.healthline.com/health/autism#support'
    response = requests.get(url)
    html_content = response.text

    # Step 2: Parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract content from the specified class
    data = []
    divs = soup.find_all('div', class_='css-1avyp1d')

    for div in divs:
        div_content = div.get_text(strip=True)
        data.append({
            'content': div_content
        })

    # Convert data to JSON format
    data_json = json.dumps(data, ensure_ascii=False, indent=4)

    # Google Cloud Storage (GCS) Configuration
    gcs_bucket_name = 'beacon-database'
    gcs_key = 'autism_support.json'

    # Initialize Google Cloud Storage client
    storage_client = storage.Client()

    try:
        # Upload JSON data to GCS
        bucket = storage_client.get_bucket(gcs_bucket_name)
        blob = bucket.blob(gcs_key)
        blob.upload_from_string(data_json, content_type='application/json')
        print("Data successfully uploaded to GCS")

        #clearing for storage
        data=None
        data_json=None
    except GoogleAPIError as e:
        print(f"Failed to upload to GCS: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def scrape_and_upload_to_gcs_7():
    import json
    from bs4 import BeautifulSoup
    import requests
    from gcloud import storage
    from google.api_core.exceptions import GoogleAPIError

    # List of URLs to scrape
    URLs = [
        'https://www.birth23.org/programs/?town&program_type',
        'https://www.birth23.org/programs/page/2/?town&program_type'
    ]

    # Define User-Agent string
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    def extract_program_info(div):
        """Extract program information from a div block."""
        title = div.find('h3').get_text(strip=True) if div.find('h3') else 'No Title'
        category = div.find('div', class_='program-block-categories').get_text(strip=True) if div.find('div', class_='program-block-categories') else 'No Category'
        
        # Extract contact email
        contact_div = div.find('div', class_='program-block-contact')
        contact_email = 'No Contact Email'
        if contact_div:
            email_link = contact_div.find('a')
            if email_link and 'href' in email_link.attrs:
                contact_email = email_link.attrs['href'].replace('mailto:', '')
            else:
                contact_email = contact_div.get_text(strip=True)
        
        # Extract phone number
        phone_number = div.find('div', class_='program-block-phone').get_text(strip=True) if div.find('div', class_='program-block-phone') else 'No Phone Number'
        
        return {
            'title': title,
            'category': category,
            'contact_email': contact_email,
            'phone_number': phone_number
        }

    # Data extraction
    all_programs = []

    # Iterate over each URL
    for URL in URLs:
        print(f'Scraping {URL}')
        try:
            response = requests.get(URL, headers=HEADERS)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # Print the page title for debugging
                print(f'Page Title: {soup.title.string}')

                # Define block to scrape
                blocks = soup.find_all('div', class_='loop-program program-block program-post')

                # Check if any blocks are found
                if not blocks:
                    print(f'No blocks found on {URL}.')
                    continue

                # Extract data
                for block in blocks:
                    program_info = extract_program_info(block)
                    all_programs.append(program_info)

                print(f'Data extracted from {URL}.')
            else:
                print(f'Failed to retrieve {URL} with status code: {response.status_code}')
        except Exception as e:
            print(f'An error occurred while scraping {URL}: {e}')

    # Convert data to JSON format
    json_data = json.dumps(all_programs, ensure_ascii=False, indent=4)

    # Google Cloud Storage (GCS) Configuration
    gcs_bucket_name = 'beacon-database'
    gcs_file_name = 'birth_to_3_programs.json'

    # Initialize Google Cloud Storage client
    storage_client = storage.Client()

    try:
        # Upload JSON data to GCS
        bucket = storage_client.get_bucket(gcs_bucket_name)
        blob = bucket.blob(gcs_file_name)
        blob.upload_from_string(json_data, content_type='application/json')
        print("Data successfully uploaded to GCS")

        #clearing for storage
        all_programs=None
        json_data=None
    except GoogleAPIError as e:
        print(f"Failed to upload to GCS: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def scrape_and_upload_to_gcs_8():
    import json
    from googleapiclient.discovery import build
    from gcloud import storage
    from google.api_core.exceptions import GoogleAPIError
    from datetime import datetime

    # Configuration
    API_KEY = '***'  # Replace with your Google API Key
    CALENDAR_ID = 'ctfoodbank.events@gmail.com'  # Replace with your public calendar ID

    # Create the Google Calendar service object
    service = build('calendar', 'v3', developerKey=API_KEY)

    # Fetch events from the public calendar
    now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    events_result = service.events().list(calendarId=CALENDAR_ID, timeMin=now,
                                        singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])

    # Prepare data for JSON
    data = []

    for event in events:
        # Extract event details
        event_data = {
            'id': event.get('id'),
            'summary': event.get('summary', ''),
            'start': event.get('start', {}).get('dateTime', event.get('start', {}).get('date', '')),
            'end': event.get('end', {}).get('dateTime', event.get('end', {}).get('date', '')),
            'description': event.get('description', ''),
            'location': event.get('location', ''),
            'creator': event.get('creator', {}).get('email', '')
        }
        data.append(event_data)

    # Convert data to JSON format
    json_data = json.dumps(data, ensure_ascii=False, indent=4)

    # Google Cloud Storage (GCS) Configuration
    gcs_bucket_name = 'beacon-database'
    gcs_file_name = 'calendar_events.json'

    # Initialize Google Cloud Storage client
    storage_client = storage.Client()

    try:
        # Upload JSON data to GCS
        bucket = storage_client.get_bucket(gcs_bucket_name)
        blob = bucket.blob(gcs_file_name)
        blob.upload_from_string(json_data, content_type='application/json')
        print("Data successfully uploaded to GCS")

        #clearing for storage
        data=None
        json_data=None
    except GoogleAPIError as e:
        print(f"Failed to upload to GCS: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def scrape_and_upload_to_gcs_9():
    import json
    from bs4 import BeautifulSoup
    import requests
    from gcloud import storage
    from google.api_core.exceptions import GoogleAPIError

    # Fetch the web page
    url = 'https://www.cdc.gov/autism/data-research/?CDC_AAref_Val=https://www.cdc.gov/ncbddd/autism/data.html'
    response = requests.get(url)
    html_content = response.text

    # Parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Function to extract text content from a given div section
    def extract_text_content(section_div):
        content = []
        for tag in section_div.find_all(['p', 'h2', 'h3', 'ul', 'a']):
            tag_name = tag.name
            if tag_name == 'a':
                tag_content = tag.get_text(strip=True)
                href = tag.get('href', '')
                content.append({
                    'tag': tag_name,
                    'content': tag_content,
                    'href': href
                })
            else:
                tag_content = tag.get_text(strip=True)
                if tag_name == 'ul':
                    list_items = [li.get_text(strip=True) for li in tag.find_all('li')]
                    tag_content = '\n'.join(list_items)
                content.append({
                    'tag': tag_name,
                    'content': tag_content
                })
        return content

    # Function to extract table data from a given div section
    def extract_table_content(section_div):
        table_data = []
        table = section_div.find('table')
        if table:
            headers = [th.get_text(strip=True) for th in table.find_all('th')]
            for row in table.find_all('tr')[1:]:  # Skip the header row
                columns = row.find_all('td')
                if len(columns) > 0:
                    row_data = {}
                    for i, column in enumerate(columns):
                        row_data[headers[i]] = column.get_text(strip=True)
                    table_data.append(row_data)
        return table_data

    # Find and extract data from the specified sections
    data = []
    section1_div = soup.find('div', class_='dfe-section', attrs={'data-section': 'cdc_data_surveillance_section_1'})
    if section1_div:
        section1_content = extract_text_content(section1_div)
        data.append({
            'section': 'cdc_data_surveillance_section_1',
            'content': section1_content
        })

    section2_div = soup.find('div', class_='dfe-section', attrs={'data-section': 'cdc_data_surveillance_section_2'})
    if section2_div:
        section2_content = extract_table_content(section2_div)
        data.append({
            'section': 'cdc_data_surveillance_section_2',
            'content': section2_content
        })

    # Debugging: Print the length and content of the data list
    print(f"Number of sections extracted: {len(data)}")
    print("Data extracted:")
    for section in data:
        print(section)

    # Convert data to JSON format
    data_json = json.dumps(data, ensure_ascii=False, indent=4)

    # Google Cloud Storage (GCS) Configuration
    gcs_bucket_name = 'beacon-database'
    gcs_file_name = 'cdc_autism_data.json'

    # Initialize Google Cloud Storage client
    storage_client = storage.Client()

    try:
        # Upload JSON data to GCS
        bucket = storage_client.get_bucket(gcs_bucket_name)
        blob = bucket.blob(gcs_file_name)
        blob.upload_from_string(data_json, content_type='application/json')
        print("Data successfully uploaded to GCS")

        #clearing for storage
        content=None
        table_data=None
        data=None
        data_json=None
    except GoogleAPIError as e:
        print(f"Failed to upload to GCS: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def scrape_and_upload_to_gcs_10():
    import json
    from bs4 import BeautifulSoup
    import requests
    from gcloud import storage
    from google.api_core.exceptions import GoogleAPIError

    # Fetch the webpage content
    url = 'https://portal.ct.gov/oca/miscellaneous/miscellaneous/resources/resource-list'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Initialize data list
    data = []

    # Function to parse items and descriptions from the siblings
    def parse_items_and_descriptions(start_ul):
        items = []
        descriptions = []
        ul = start_ul

        while ul:
            for li in ul.find_all('li'):
                link = li.find('a')
                link_text = link.get_text(strip=True) if link else ''
                link_href = link['href'] if link else ''
                items.append({
                    'text': link_text,
                    'href': link_href
                })
            
            # Find the next description <p> tag
            next_p = ul.find_next_sibling('p', style='text-align: justify;')
            if next_p:
                descriptions.append(next_p.get_text(strip=True))
            
            # Move to the next <ul> if it exists
            ul = next_p.find_next_sibling('ul', style='list-style-type: disc;') if next_p else None

        return items, descriptions

    # Extract data
    heading = None
    for tag in soup.find_all(['p', 'ul']):
        if tag.name == 'p' and 'margin-bottom: 0in;' in tag.get('style', ''):
            if heading:
                # Save previous heading's data before starting a new one
                data.append({
                    'title': heading['title'],
                    'items': heading['items'],
                    'descriptions': heading['descriptions']
                })

            # Start a new heading
            heading = {
                'title': tag.get_text(strip=True),
                'items': [],
                'descriptions': []
            }

            # Parse items and descriptions starting from the next sibling <ul>
            next_ul = tag.find_next_sibling('ul', style='list-style-type: disc;')
            if next_ul:
                heading['items'], heading['descriptions'] = parse_items_and_descriptions(next_ul)
        
    # Append the last heading
    if heading:
        data.append({
            'title': heading['title'],
            'items': heading['items'],
            'descriptions': heading['descriptions']
        })

    # Convert data to JSON format
    json_data = json.dumps(data, ensure_ascii=False, indent=4)

    # Google Cloud Storage (GCS) Configuration
    gcs_bucket_name = 'beacon-database'
    gcs_file_name = 'connecticut_resource_directory.json'

    # Initialize Google Cloud Storage client
    storage_client = storage.Client()

    try:
        # Upload JSON data to GCS
        bucket = storage_client.get_bucket(gcs_bucket_name)
        blob = bucket.blob(gcs_file_name)
        blob.upload_from_string(json_data, content_type='application/json')
        print("Data successfully uploaded to GCS")

        #clearing for storage
        items=None
        descriptions=None
        data=None
        json_data=None
    except GoogleAPIError as e:
        print(f"Failed to upload to GCS: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def scrape_and_upload_to_gcs_11():
    import json
    from bs4 import BeautifulSoup
    import requests
    from gcloud import storage
    from google.api_core.exceptions import GoogleAPIError

    # URL of the website to scrape
    URL = 'https://www.thediaperbank.org/diaper-connections/'

    # Send a GET request to the website
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Define blocks to scrape
    blocks = [
        {'class': 'et_pb_column et_pb_column_2_3 et_pb_column_1 et_pb_css_mix_blend_mode_passthrough et-last-child'},
        {'class': 'et_pb_column et_pb_column_2_3 et_pb_column_2 et_pb_css_mix_blend_mode_passthrough'},
        {'class': 'et_pb_column et_pb_column_2_3 et_pb_column_5 et_pb_css_mix_blend_mode_passthrough et-last-child'}
    ]

    documents = []

    for block in blocks:
        for div in soup.find_all('div', class_=block['class']):
            # Extracting text from the div
            text = div.get_text(strip=True)
            # Adding text to the documents list
            documents.append({'text': text})

    # Convert documents to JSON format
    json_data = json.dumps(documents, ensure_ascii=False, indent=4)

    # Google Cloud Storage (GCS) Configuration
    gcs_bucket_name = 'beacon-database'
    gcs_file_name = 'diaper_connections.json'

    # Initialize Google Cloud Storage client
    storage_client = storage.Client()

    try:
        # Upload JSON data to GCS
        bucket = storage_client.get_bucket(gcs_bucket_name)
        blob = bucket.blob(gcs_file_name)
        blob.upload_from_string(json_data, content_type='application/json')
        print("Data successfully uploaded to GCS")

        #clearing for storage
        documents=None
        json_data=None
    except GoogleAPIError as e:
        print(f"Failed to upload to GCS: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def scrape_and_upload_to_gcs_12():
    import json
    from bs4 import BeautifulSoup
    import requests
    from gcloud import storage
    from google.api_core.exceptions import GoogleAPIError

    # Fetch the webpage content
    url = "https://portal.ct.gov/dds/supports-and-services/family-support-and-services?language=en_US"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract data
    data = []

    # Find all divs with the specified class
    for div in soup.find_all('div', class_='cg-c-lead-story__body col'):
        block_content = div.get_text(strip=True, separator=' ')
        list_items = [li.get_text(strip=True) for li in div.find_all('li')]
        
        # Combine the block content with list items
        combined_content = {
            'block_content': block_content,
            'list_items': list_items
        }
        data.append(combined_content)

    # Convert data to JSON format
    json_data = json.dumps(data, ensure_ascii=False, indent=4)

    # Google Cloud Storage (GCS) Configuration
    gcs_bucket_name = 'beacon-database'
    gcs_file_name = 'family_support_and_services.json'

    # Initialize Google Cloud Storage client
    storage_client = storage.Client()

    try:
        # Upload JSON data to GCS
        bucket = storage_client.get_bucket(gcs_bucket_name)
        blob = bucket.blob(gcs_file_name)
        blob.upload_from_string(json_data, content_type='application/json')
        print("Data successfully uploaded to GCS")

        #clearing for storage
        data=None
        json_data=None
    except GoogleAPIError as e:
        print(f"Failed to upload to GCS: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def scrape_and_upload_to_gcs_13():
    import json
    from bs4 import BeautifulSoup
    import requests
    from gcloud import storage
    from google.api_core.exceptions import GoogleAPIError

    # Step 1: Fetch the web page
    url = 'https://kidshealth.org/en/parents/milestones.html'
    response = requests.get(url)
    html_content = response.text

    # Step 2: Parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all div elements with the class 'cmp-container'
    data = []
    divs = soup.find_all('div', class_='cmp-container')

    for div in divs:
        div_content = div.get_text(strip=True)
        data.append({
            'content': div_content
        })

    # Convert data to JSON format
    data_json = json.dumps(data, ensure_ascii=False)

    # Google Cloud Storage (GCS) Configuration
    gcs_bucket_name = 'beacon-database'
    gcs_file_name = 'milestones.json'

    # Initialize Google Cloud Storage client
    storage_client = storage.Client()

    try:
        # Upload JSON data to GCS
        bucket = storage_client.get_bucket(gcs_bucket_name)
        blob = bucket.blob(gcs_file_name)
        blob.upload_from_string(data_json, content_type='application/json')
        print("Data successfully uploaded to GCS")

        #clearing for storage
        data=None
        data_json=None
    except GoogleAPIError as e:
        print(f"Failed to upload to GCS: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def scrape_and_upload_to_gcs_14():
    import json
    from bs4 import BeautifulSoup
    import requests
    from gcloud import storage
    from google.api_core.exceptions import GoogleAPIError

    # Fetch the web page
    url = 'https://www.nimh.nih.gov/health/topics/autism-spectrum-disorders-asd'
    response = requests.get(url)
    html_content = response.text

    # Parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the specific div by ID and class
    target_div = soup.find('div', id='main_content', class_='areanav-true sidebar-true')

    # Extract content from p, h2, h3, ul, and a tags within the specific div
    data = []
    if target_div:
        for tag in target_div.find_all(['p', 'h2', 'h3', 'ul', 'a']):
            tag_name = tag.name
            if tag_name == 'a':
                tag_content = tag.get_text(strip=True)
                href = tag.get('href', '')
                data.append({
                    'tag': tag_name,
                    'content': tag_content,
                    'href': href
                })
            else:
                tag_content = tag.get_text(strip=True)
                if tag_name == 'ul':
                    list_items = [li.get_text(strip=True) for li in tag.find_all('li')]
                    tag_content = '\n'.join(list_items)
                data.append({
                    'tag': tag_name,
                    'content': tag_content
                })
    else:
        print("Target div not found")

    # Debugging: Print the length and content of the data list
    print(f"Number of items extracted: {len(data)}")
    print("Data extracted:")
    for item in data:
        print(item)

    # Convert data to JSON format
    data_json = json.dumps(data, ensure_ascii=False, indent=4)

    # Google Cloud Storage (GCS) Configuration
    gcs_bucket_name = 'beacon-database'
    gcs_file_name = 'nimh_asd.json'

    # Initialize Google Cloud Storage client
    storage_client = storage.Client()

    try:
        # Upload JSON data to GCS
        bucket = storage_client.get_bucket(gcs_bucket_name)
        blob = bucket.blob(gcs_file_name)
        blob.upload_from_string(data_json, content_type='application/json')
        print("Data successfully uploaded to GCS")

        #clearing for storage
        data=None
        data_json=None
    except GoogleAPIError as e:
        print(f"Failed to upload to GCS: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def scrape_and_upload_to_gcs_15():
    import json
    from bs4 import BeautifulSoup
    import requests
    from gcloud import storage
    from google.api_core.exceptions import GoogleAPIError

    # Fetch the web page
    url = 'https://www.autismspeaks.org/signs-autism'
    response = requests.get(url)
    html_content = response.text

    # Parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the specific div by class
    target_divs = soup.find_all('div', class_='basic-block')

    # Extract content from p, h2, h3, ul, and a tags within the specific divs
    data = []
    for target_div in target_divs:
        section_data = []
        for tag in target_div.find_all(['p', 'h2', 'h3', 'ul', 'a']):
            tag_name = tag.name
            if tag_name == 'a':
                tag_content = tag.get_text(strip=True)
                href = tag.get('href', '')
                section_data.append({
                    'tag': tag_name,
                    'content': tag_content,
                    'href': href
                })
            else:
                tag_content = tag.get_text(strip=True)
                if tag_name == 'ul':
                    list_items = [li.get_text(strip=True) for li in tag.find_all('li')]
                    tag_content = '\n'.join(list_items)
                section_data.append({
                    'tag': tag_name,
                    'content': tag_content
                })
        if section_data:
            data.append(section_data)

    # Debugging: Print the length and content of the data list
    print(f"Number of sections extracted: {len(data)}")
    print("Data extracted:")
    for section in data:
        print(section)

    # Convert data to JSON format
    data_json = json.dumps(data, ensure_ascii=False, indent=4)

    # Google Cloud Storage (GCS) Configuration
    gcs_bucket_name = 'beacon-database'
    gcs_file_name = 'signs_autism.json'

    # Initialize Google Cloud Storage client
    storage_client = storage.Client()

    try:
        # Upload JSON data to GCS
        bucket = storage_client.get_bucket(gcs_bucket_name)
        blob = bucket.blob(gcs_file_name)
        blob.upload_from_string(data_json, content_type='application/json')
        print("Data successfully uploaded to GCS")

        #clearing for storage
        data=None
        data_json=None
    except GoogleAPIError as e:
        print(f"Failed to upload to GCS: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def scrape_and_upload_to_gcs_16():
    import json
    from bs4 import BeautifulSoup
    import requests
    from gcloud import storage
    from google.api_core.exceptions import GoogleAPIError

    # URL of the webpage to scrape
    url = 'https://ctserc.org/services'

    # Make an HTTP GET request to the webpage
    response = requests.get(url)

    # Parse the HTML content of the webpage
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the div with the id 'serc-services'
    services_div = soup.find('div', id='serc-services')

    # Extract text from the div
    services_text = services_div.get_text(strip=True) if services_div else 'Div with id "serc-services" not found.'

    # Prepare the data
    data = {
        'source_url': url,
        'content': services_text
    }

    # Convert data to JSON format
    json_data = json.dumps(data, ensure_ascii=False, indent=4)

    # Google Cloud Storage (GCS) configuration
    gcs_bucket_name = 'beacon-database'
    gcs_file_name = 'state_education_resource_center.json'

    # Initialize Google Cloud Storage client
    storage_client = storage.Client()

    try:
        # Upload JSON data to GCS
        bucket = storage_client.get_bucket(gcs_bucket_name)
        blob = bucket.blob(gcs_file_name)
        blob.upload_from_string(json_data, content_type='application/json')
        print("Data successfully uploaded to GCS")

        #clearing for storage
        data=None
        json_data=None
    except GoogleAPIError as e:
        print(f"Failed to upload to GCS: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def scrape_and_upload_to_gcs_17():
    import json
    from bs4 import BeautifulSoup
    import requests
    from gcloud import storage
    from google.api_core.exceptions import GoogleAPIError

    # URL of the website to scrape
    URL = 'https://portal.ct.gov/dss/archived-folder/temporary-family-assistance---tfa'

    # Send a GET request to the website
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Define block to scrape
    block_class = 'content'

    # Extract the content from the specified block
    content_div = soup.find('div', class_=block_class)
    if content_div:
        text = content_div.get_text(strip=True)
    else:
        text = 'Content not found.'

    # Convert data to JSON format
    data = {
        'content': text
    }
    json_data = json.dumps(data, ensure_ascii=False, indent=4)

    # Google Cloud Storage (GCS) configuration
    gcs_bucket_name = 'beacon-database'
    gcs_file_name = 'temporary_family_assistance.json'

    # Initialize Google Cloud Storage client
    storage_client = storage.Client()

    try:
        # Upload JSON data to GCS
        bucket = storage_client.get_bucket(gcs_bucket_name)
        blob = bucket.blob(gcs_file_name)
        blob.upload_from_string(json_data, content_type='application/json')
        print("Data successfully uploaded to GCS")

        #clearing for storage
        data=None
        json_data=None
    except GoogleAPIError as e:
        print(f"Failed to upload to GCS: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def scrape_and_upload_to_gcs_18():
    import json
    from bs4 import BeautifulSoup
    import requests
    from gcloud import storage
    from google.api_core.exceptions import GoogleAPIError

    # URL of the webpage to scrape
    url = 'https://portal.ct.gov/dph/wic/wic'

    # Send a GET request to the website
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract data
    data = []

    # Define the styles to target
    target_styles = [
        'margin: 0in 0in 0pt;',
        'text-align: left;'
    ]

    # Find and extract <p> and <div> tags with the specified styles
    for style in target_styles:
        for tag in soup.find_all(['p', 'div'], style=style):
            text_content = tag.get_text(strip=True)
            data.append({
                'tag': tag.name,
                'style': style,
                'content': text_content
            })

    # Convert data to JSON format
    json_data = json.dumps(data, ensure_ascii=False, indent=4)

    # Google Cloud Storage (GCS) configuration
    gcs_bucket_name = 'beacon-database'
    gcs_file_name = 'women_infants_children.json'

    # Initialize Google Cloud Storage client
    storage_client = storage.Client()

    try:
        # Upload JSON data to GCS
        bucket = storage_client.get_bucket(gcs_bucket_name)
        blob = bucket.blob(gcs_file_name)
        blob.upload_from_string(json_data, content_type='application/json')
        print("Data successfully uploaded to GCS")

        #clearing for storage
        data=None
        json_data=None
    except GoogleAPIError as e:
        print(f"Failed to upload to GCS: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def scrape_and_upload_to_gcs_19():
    import requests
    from google.cloud import storage
    import json
    # Step 1: Fetch Data
    url = 'https://www.211childcare.org/providers.json'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")
    
    # Step 2: Upload to Google Cloud Storage
    client = storage.Client()
    bucket_name = 'beacon-database'  # Your bucket name
    destination_blob_name = 'providers.json'
    
    bucket = client.get_bucket(bucket_name)
    json_data = json.dumps(data)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(json_data, content_type='application/json')
    
    print(f"Data successfully uploaded to {bucket_name}/{destination_blob_name}")

    #clearning for storage
    json_data=None
    data=None