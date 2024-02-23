import requests
from bs4 import BeautifulSoup
from ebooklib import epub

def fetch_and_convert_to_epub(url, epub_file_name):
    # Fetch the page
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses

    # Parse the HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Clean the HTML here (remove or alter parts as necessary)
    # This step will vary greatly depending on the structure of your documentation
    # For simplicity, let's just extract the main content assuming it's within a <main> tag
    main_content = soup.find('main')
    if main_content is None:
        main_content = soup  # Fallback to the whole soup if <main> is not found

    # Create an ePub book
    book = epub.EpubBook()

    # Add basic book information (customize as needed)
    book.set_identifier('id123456')
    book.set_title('Documentation Page')
    book.set_language('en')

    # Convert the main content to a string and create an ePub HTML file
    epub_content = epub.EpubHtml(title='Main Content', file_name='content.xhtml', lang='en')
    epub_content.content = str(main_content)

    # Add the HTML file to the book
    book.add_item(epub_content)

    # Define the book structure
    book.toc = (epub_content,)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Set the book's spine
    book.spine = ['nav', epub_content]

    # Write the ePub file
    epub.write_epub(epub_file_name, book, {})

# Example usage
url = 'https://eips.ethereum.org/EIPS/eip-1'
fetch_and_convert_to_epub(url, 'documentation_page.epub')