import csv
from typing import List, AnyStr


def csv_file_reader(filename: AnyStr, images_index: AnyStr) -> List[AnyStr]:
    with open(filename, "r") as f:
        reader = csv.DictReader(f)

        field_names = reader.fieldnames
        images_index = field_names.index(images_index)
        images_url = []
        for row in reader:
            image_url = row[field_names[images_index]]
            if len(image_url) != 0:
                images_url.append(image_url)
    return images_url


