import os
import shutil
import sys
import threading
import time

import requests
from requests import ConnectionError
from requests.exceptions import Timeout
import timeout_decorator
import shortuuid





data_fields = {
    'number_of_threads': 0,
    'total': 0,
    'succeeded': 0,
    'failed': 0,
    'time': 0,
    '403': 0,
    '404': 0,
    '500': 0,
    'not_valid': 0,
    'timeout': 0,
    'other_error': 0,
    'avg_rate': 0,
    'bytes_downloaded': 0,
}

socks_ports = dict(http='socks5://127.0.0.1:5566', https='socks5://127.0.0.1:5566')


class FileRequest:
    def __init__(self, url, status_code):
        self.url = url
        self.status_code = status_code
        self.time = time.ctime()


class Downloader:
    timeout_seconds = None

    def __init__(self, max_retry,
                 downloading_path,
                 timeout,
                 initial_data=data_fields,
                 mode="VPN",
                 number_of_th=25,
                 conn_establish_timeout=1):
        self.socks = socks_ports
        self.downloading_path = downloading_path
        self.timeout_seconds = timeout
        self.mode = mode
        self.__data = initial_data
        self.lock = threading.Lock()
        self.connection_establish_timeout = conn_establish_timeout if conn_establish_timeout > 1 else 1
        self.MAX_RETRY = max_retry if max_retry >= 1 else 0
        if number_of_th <= 0:
            self.logger.info("Number of threads can not be less than 1")
            sys.exit(1)
        self.number_of_threads = number_of_th
        self.initiate_url_types()

    def initiate_url_types(self):
        self.__succeeded = []
        self.__failed = []
        self.__timed_out = []
        self.__internal_server = []
        self.__not_valid = []
        self.__permission_denied = []
        self.__not_found = []
        self.__other_errors = []

    @property
    def permission_denied_urls(self):
        return [url.__dict__ for url in self.__permission_denied]

    @property
    def not_found_urls(self):
        return [url.__dict__ for url in self.__not_found]

    @property
    def succeeded_urls(self):
        return [url.__dict__ for url in self.__succeeded]

    @property
    def failed_urls(self):
        return [url.__dict__ for url in self.__failed]

    @property
    def timed_out_urls(self):
        return [url.__dict__ for url in self.__timed_out]

    @property
    def other_error_urls(self):
        return [url.__dict__ for url in self.__other_errors]

    @property
    def internal_server_error_urls(self):
        return [url.__dict__ for url in self.__internal_server]

    @property
    def not_valid_urls(self):
        return [url.__dict__ for url in self.__not_valid]

    @property
    def four_o_four_count(self):
        return self.__data['404']

    @property
    def four_o_three_count(self):
        return self.__data['403']

    @property
    def five_o_o_count(self):
        return self.__data['500']

    @property
    def not_valid_count(self):
        return self.__data['not_valid']

    @property
    def timeout_count(self):
        return self.__data['timeout']

    @property
    def other_error_count(self):
        return self.__data['other_error']

    @property
    def failed_count(self):
        return self.__data['failed']

    @property
    def success_count(self):
        return self.__data['succeeded']

    @property
    def total_count(self):
        return self.__data['total']

    @property
    def file_average_time(self):
        file_avg_time = self.elapsed_time / self.success_count if self.success_count != 0 else 0
        return round(file_avg_time, 2)

    @property
    def file_average_size(self):
        average_size_in_bytes = self.__data['bytes_downloaded'] / self.success_count if self.success_count != 0 else 0
        average_size_in_kilo_bytes = average_size_in_bytes / 1024
        return round(average_size_in_kilo_bytes, 2)

    @property
    def average_rate(self):
        return self.__data['avg_rate']

    @property
    def elapsed_time(self):
        return self.__data['time']

    @property
    def image_per_second(self):
        image_per_sec = self.success_count / self.elapsed_time if self.elapsed_time != 0 else 0
        return round(image_per_sec, 2)

    def make_directories(self):
        if not os.path.exists(self.downloading_path):
            os.makedirs(self.downloading_path)
        else:
            shutil.rmtree(self.downloading_path)
            os.makedirs(self.downloading_path)

    def download_from_a_list(self, list):
        for image_url in list:
            retry = True
            retry_counter = 0
            while retry and retry_counter <= self.MAX_RETRY:
                retry_counter += 1
                try:
                    req = self.download_file(image_url)
                    if req.status_code == 200:
                        unique_name = shortuuid.uuid()
                        image_path_name = f'./{self.downloading_path}/{unique_name}.jpeg'
                        self.lock.acquire()
                        self.__data['bytes_downloaded'] += len(req.content)
                        self.__store_succeeded_to_download_urls_path(image_path_name)
                        self.lock.release()
                        open(image_path_name, 'wb').write(req.content)
                        retry = False
                    else:
                        if retry_counter > self.MAX_RETRY:
                            self.lock.acquire()
                            self.__store_failed_to_download_urls(image_url, req.status_code)
                            self.lock.release()
                        retry = True
                    print("Downloading...")
                except Timeout:
                    self.lock.acquire()
                    self.__store_failed_to_download_urls(image_url, 'TIMEOUT')
                    self.lock.release()
                    retry = False
                except ConnectionError:
                    self.lock.acquire()
                    self.__store_failed_to_download_urls(image_url, 'NOT_VALID')
                    self.lock.release()
                    retry = False
                except:
                    if retry_counter > self.MAX_RETRY:
                        self.lock.acquire()
                        self.__store_failed_to_download_urls(image_url, 'OTHER')
                        self.lock.release()
                        retry = True

    @timeout_decorator.timeout(timeout_seconds)
    def download_file(self, file):
        if self.mode == "VPN":
            req = requests.get(file, allow_redirects=True,
                               timeout=(self.connection_establish_timeout, self.timeout_seconds))
        else:
            req = requests.get(file, allow_redirects=True,
                               proxies=self.socks,
                               timeout=(self.connection_establish_timeout, self.timeout_seconds))
        return req

    def download_images(self, images_url):

        self.__data['total'] = len(images_url)
        self.__data['number_of_threads'] = self.number_of_threads

        chunked_urls = self.__get_chunked_urls(images_url)

        start_time = time.time()

        threads = self.__start_threads(chunked_urls)
        print(f'{len(threads)} thread started.')

        for thread in threads:
            thread.join()
        execution_time = time.time() - start_time
        print(f"execution time: {execution_time}s")
        self.__data['time'] = round(execution_time, 2)
        self.__calculate_avg_rate()

    def __calculate_avg_rate(self):
        media_size = self.__data['bytes_downloaded']
        media_size_in_mbytes = media_size / (1024 * 1024)
        time = self.__data['time']
        avg_rate = (media_size_in_mbytes / time) if time != 0 else 0
        avg_rate = round(avg_rate, 2)
        self.__data['avg_rate'] = avg_rate

    def __store_failed_to_download_urls(self, url, code):
        req = FileRequest(url=url, status_code=code)
        if code == 403:
            self.__permission_denied.append(req)
            self.__data['403'] += 1
        elif code == 404:
            self.__not_found.append(req)
            self.__data['404'] += 1
        elif code == 500:
            self.__internal_server.append(req)
            self.__data['500'] += 1
        elif code == 'TIMEOUT':
            self.__timed_out.append(req)
            self.__data['timeout'] += 1
        elif code == 'NOT_VALID':
            self.__not_valid.append(req)
            self.__data['not_valid'] += 1
        else:
            self.__other_errors.append(req)
            self.__data['other_error'] += 1

        self.__failed.append(req)
        self.__data['failed'] += 1

    def __store_succeeded_to_download_urls_path(self, url):
        req = FileRequest(url=url, status_code=200)
        self.__succeeded.append(req)
        self.__data['succeeded'] += 1

    def __get_chunked_urls(self, images_url):
        chunked_urls = []
        chunk_length = len(images_url) // self.number_of_threads
        remained_urls = len(images_url) % self.number_of_threads
        for i in range(self.number_of_threads):
            chunked_urls.append([images_url[i * chunk_length: (i + 1) * chunk_length]])
        for i in range(1, remained_urls + 1):
            chunked_urls[i - 1][0].append(images_url[-i])
        return chunked_urls

    def __start_threads(self, chunked_urls):
        threads = []
        for lst in chunked_urls:
            t = threading.Thread(target=self.download_from_a_list, args=lst)
            threads.append(t)
            t.start()
        return threads

    def clear_reports(self):
        for key in self.__data.keys():
            self.__data[key] = 0
        self.initiate_url_types()
