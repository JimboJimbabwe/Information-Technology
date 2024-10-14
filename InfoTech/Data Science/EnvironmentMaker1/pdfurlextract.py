import PyPDF2
import json

def extract_links_from_pdf(pdf_path):
    links = []

    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)

        for page in reader.pages:
            if '/Annots' in page:
                for annot in page['/Annots']:
                    obj = annot.get_object()
                    if '/A' in obj and '/URI' in obj['/A']:
                        links.append(obj['/A']['/URI'])

    return links

def save_links_to_json(links, output_file):
    with open(output_file, 'w') as file:
        json.dump(links, file, indent=2)

def main():
    pdf_path = r'C:\Users\james\PycharmProjects\JSONMakerWebTwo\Network Testing Ports - Bug Bounty.pdf'
    output_file = 'extracted_links.json'

    links = extract_links_from_pdf(pdf_path)

    if links:
        save_links_to_json(links, output_file)
        print(f"Extracted {len(links)} links and saved them to {output_file}")
    else:
        print("No links were found in the PDF.")

if __name__ == "__main__":
    main()