import argparse
from prometheus_client import start_http_server, Gauge
from downloader import Downloader
from file_reader import csv_file_reader

parser = argparse.ArgumentParser()

parser.add_argument("-m", "--mode", help="Set download mode")
parser.add_argument("-t", "--threads", help="Set number of threads")

args = parser.parse_args()
if args.mode:
    mode = str(args.mode)
if args.threads:
    number_of_threads = int(args.threads)


if __name__ == '__main__':

    start_http_server(8000)
    mode = "VPN"
    number_of_threads = 25
    if args.mode:
        mode = str(args.mode)
    if args.threads:
        number_of_threads = int(args.threads)

    filename, images_index = ("new-instagram.csv", "urls")
    urls = csv_file_reader(filename, images_index)
    urls = [url for url in urls if url != '']
    batch_size = 100
    urls_length = len(urls)

    print(f"Downloading with {number_of_threads} threads and {mode}")
    downloader = Downloader(mode=mode, number_of_th=number_of_threads, timeout=30, max_retry=1, downloading_path='media')
    downloader.make_directories()

    average_rate = Gauge('Average_Rate', 'Average Rate of download batch of images')
    elapsed_time = Gauge('Elapsed_Time', 'Elapsed time of downloading batch of images')
    image_per_second = Gauge('Image_Per_Second', 'Downloaded Image per Second')
    four_o_four = Gauge('Not_Found', 'Not found images')
    four_o_three = Gauge('Permission_Denied', 'Download permission denied')
    five_o_o = Gauge('Internal_Server', 'Internal Server Errors')
    not_valid = Gauge('Not_Valid', 'Not Valid urls')
    other_error = Gauge('Other_Error', 'other error')
    failed = Gauge('Failed', 'Failed to download')
    success = Gauge('Success', 'Success Downloads')
    timeout = Gauge('Timeout', 'Timed Out urls')
    total = Gauge('Total', 'Total')
    file_average_size = Gauge('File_average_size', 'Each file average size')
    file_average_time = Gauge('File_Average_Time', 'Each file spend time')

    for i in range((urls_length//batch_size)+1):
        if i == urls_length//batch_size:
            start_i, end_i = (batch_size * i, urls_length)
        else:
            start_i, end_i = (batch_size * i, batch_size * (i + 1))
        downloader.download_images(urls[start_i: end_i])
        average_rate.set(downloader.average_rate)
        elapsed_time.set(downloader.elapsed_time)
        image_per_second.set(downloader.image_per_second)
        four_o_four.set(downloader.four_o_four_count)
        four_o_three.set(downloader.four_o_three_count)
        other_error.set(downloader.other_error_count)
        failed.set(downloader.failed_count)
        success.set(downloader.success_count)
        total.set(downloader.total_count)
        timeout.set(downloader.timeout_count)
        five_o_o.set(downloader.five_o_o_count)
        not_valid.set(downloader.not_valid_count)
        file_average_size.set(downloader.file_average_size)
        file_average_time.set(downloader.file_average_time)
        downloader.clear_reports()