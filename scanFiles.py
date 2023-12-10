import os
import re
from datetime import datetime

def extract_date_from_filename(filename):
    date_patterns = [
        r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
        r'\d{2}-\d{2}-\d{4}',  # DD-MM-YYYY
        r'\d{4}\d{2}\d{2}',    # YYYYMMDD
        # Add more patterns as needed
    ]

    for pattern in date_patterns:
        match = re.search(pattern, filename)
        if match:
            # Return both the date string and the non-date part of the filename
            return match.group(), re.sub(pattern, '', filename)
    return None, filename

def parse_date(date_str):
    date_formats = [
        '%Y-%m-%d',
        '%d-%m-%Y',
        '%Y%m%d',
        # Add more formats as needed
    ]

    for fmt in date_formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None

def scan_folders(root_dir):
    folder_data = {}
    for dirpath, dirnames, filenames in os.walk(root_dir):
        file_info = {}
        for file in filenames:
            if file.endswith('.json') or file.endswith('.csv'):
                date_str, file_base_name = extract_date_from_filename(file)
                if date_str:
                    date_obj = parse_date(date_str)
                    if date_obj:
                        if file_base_name not in file_info:
                            file_info[file_base_name] = {'dates': [], 'type': os.path.splitext(file)[1]}
                        file_info[file_base_name]['dates'].append(date_obj)

        for key, value in file_info.items():
            value['dates'] = [min(value['dates']), max(value['dates'])]

        if file_info:
            folder_data[dirpath] = file_info

    return folder_data

def main():
    root_dir = './data/'  # Set your directory path here
    data = scan_folders(root_dir)
    for folder, files in data.items():
        print(f'Folder: {folder}')
        for file_base, info in files.items():
            print(f'File Name: {file_base}')
            print(f'Date Range: {info["dates"][0].date()} to {info["dates"][1].date()}')
            print('---------------------')

if __name__ == '__main__':
    main()
