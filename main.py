from prometheus_client import start_http_server
from file_reader import csv_file_reader
from reporter import Reporter

if __name__ == '__main__':

    start_http_server(8000)
    filename, images_index = ("new-instagram.csv", "urls")
    urls = csv_file_reader(filename, images_index)
    urls = [url for url in urls if url != '']
    batch_size = 100

    urls_length = len(urls)

    reporter = Reporter()

    for i in range((urls_length // batch_size) + 1):
        if i == urls_length // batch_size:
            start_i, end_i = (batch_size * i, urls_length)
        else:
            start_i, end_i = (batch_size * i, batch_size * (i + 1))
        reporter.download(urls[start_i: end_i])
