import argparse
from prometheus_client import start_http_server, Gauge
from downloader import Downloader

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

    print(f"Downloading with {number_of_threads} threads and {mode}")

    for i in range(1000):
        downloader = Downloader(mode=mode, number_of_th=number_of_threads)
        downloader.make_directories()
        downloader.download_images()

        # s.observe(float(downloader.data['time'].replace('seconds', '')))
