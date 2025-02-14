"""
First stage of the OCC exam data extraction pipeline.
"""

import os, sys
import json
from tqdm import tqdm

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("importing...")

from unstructured.partition.pdf import partition_pdf
from unstructured.documents.elements import NarrativeText, PageBreak

DATA_PATH='test-data/occ-test-qas'
OUTPUT_PATH='eval-data/questions/occ'

def process_occ_exam_qt_pdf(file_name):
    logger.info(f"\n\n>> Processing file: {file_name}")

    # Extract text from PDF
    file_path = os.path.join(DATA_PATH, file_name)
    elements = partition_pdf(file_path, include_page_breaks=True, strategy="hi_res")
    
    logger.info(f">> Extracted {len(elements)} elements from PDF")

    # Extract document title
    title = elements[0].text

    page_number=1
    # Extract just the body text elements
    def should_include(node):
        nonlocal page_number
        if type(node) is PageBreak:
            page_number += 1
            return False
        return(
            type(node) is NarrativeText
            and page_number > 1
            and node.text.strip() != ""
            and not node.text.startswith('Distribution of this document is illegal')
            and not node.text.startswith('Downloaded by: ')
            and not node.text.startswith('Want to earn $')
        )
    text_elements = [n.text for n in elements if should_include(n)]
    
    # Parse text into Question / Truth dictionary
    qt_groups = []
    this_group = []
    def make_group():
        nonlocal this_group, qt_groups, title, file_name
        q_part = '\n'.join(this_group)
        do_switch = file_name.endswith('Stuvia-5577353-occ-uce-practice-exam-questions-en-answers-20242025.pdf')
        return {
            'question': q_part if not do_switch else a_part,
            'truth': a_part if not do_switch else q_part,
            'source': {
                'title': title,
                'file_name': file_name
            }
        }
    
    for element in text_elements:
        if "ANSWERS" in element:
            q_part = element.split("ANSWERS")[0].strip()
            a_part = element.split("ANSWERS")[1].strip()
            this_group.append(q_part)

            qt_groups.append(make_group())
            this_group = []
        else:
            this_group.append(element)
    
    return qt_groups


def get_input_file_list():
    files = os.listdir(DATA_PATH)
    
    # Create a list to store file information
    file_info = []
    
    for file in files:
        if file.endswith('.pdf'):
            file_info.append(file)
    
    return file_info


def save_data_to_disk(data, file_name):
    logger.info(f"\n\n>> Saving data to disk: {file_name}")

    file_path = os.path.join(OUTPUT_PATH, file_name)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(data)
    print(f"Data has been saved to '{file_path}'")


if __name__ == '__main__':
    file_list = get_input_file_list()
    for file_name in tqdm(file_list, desc="Processing exam files", unit="file"):
        file_output = file_name.replace('.pdf', '.json')
        if os.path.exists(os.path.join(OUTPUT_PATH, file_output)):
            logger.info(f"Skipping file: {file_name}")
            continue

        questions = process_occ_exam_qt_pdf(file_name)
    
        save_data_to_disk(json.dumps(questions), file_output)

    #file_name = 'Stuvia-5576758-fin-uce-final-review-exam-questions-en-answers-20242025.pdf'
    #process_occ_exam_qt_pdf(file_name)