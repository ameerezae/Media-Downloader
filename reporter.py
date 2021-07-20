from downloader import Downloader
from prometheus_client import Gauge
import os


def get_env(var_name, default_value='', required=False):
    if type(var_name) != str or type(default_value) != str:
        return ValueError("var_name and default_value must be string")
    var_val = os.environ.get(var_name, default_value).strip()
    if var_val == "" and required:
        return ValueError(var_name + " not found in envirenment variables")
    return var_val


def get_downloader_config():
    return {
        "mode": get_env("DOWNLOADER_MODE", required=True),
        "timeout": float(get_env("REQUEST_TIMEOUT", required=True)),
        "number_of_th": int(get_env("DOWNLOADER_THREAD_NO", required=True)),
        "downloading_path": get_env("DOWNLOADING_PATH", required=True),
        "max_retry": int(get_env("DOWNLOADER_MAX_RETRY", required=True)),
        "conn_establish_timeout": float(get_env("CONNECTION_ESTABLISHMENT_TIMEOUT", required=True)),
    }


class Reporter:

    def __init__(self):
        self.average_rate = Gauge('Average_Rate', 'Average Rate of download batch of images')
        self.elapsed_time = Gauge('Elapsed_Time', 'Elapsed time of downloading batch of images')
        self.image_per_second = Gauge('Image_Per_Second', 'Downloaded Image per Second')
        self.four_o_four = Gauge('Not_Found', 'Not found images')
        self.four_o_three = Gauge('Permission_Denied', 'Download permission denied')
        self.five_o_o = Gauge('Internal_Server', 'Internal Server Errors')
        self.not_valid = Gauge('Not_Valid', 'Not Valid urls')
        self.other_error = Gauge('Other_Error', 'other error')
        self.failed = Gauge('Failed', 'Failed to download')
        self.success = Gauge('Success', 'Success Downloads')
        self.timeout = Gauge('Timeout', 'Timed Out urls')
        self.total = Gauge('Total', 'Total')
        self.file_average_size = Gauge('File_average_size', 'Each file average size')
        self.file_average_time = Gauge('File_Average_Time', 'Each file spend time')
        self.__downloader = None

    @property
    def downloader(self):
        if not self.__downloader:
            config = get_downloader_config()
            self.__downloader = Downloader(**config)

        return self.__downloader

    def __set_gauges(self):
        self.average_rate.set(self.downloader.average_rate)
        self.elapsed_time.set(self.downloader.elapsed_time)
        self.image_per_second.set(self.downloader.image_per_second)
        self.four_o_four.set(self.downloader.four_o_four_count)
        self.four_o_three.set(self.downloader.four_o_three_count)
        self.other_error.set(self.downloader.other_error_count)
        self.failed.set(self.downloader.failed_count)
        self.success.set(self.downloader.success_count)
        self.total.set(self.downloader.total_count)
        self.timeout.set(self.downloader.timeout_count)
        self.five_o_o.set(self.downloader.five_o_o_count)
        self.not_valid.set(self.downloader.not_valid_count)
        self.file_average_size.set(self.downloader.file_average_size)
        self.file_average_time.set(self.downloader.file_average_time)

    def download(self, urls):
        self.downloader.download_images(urls)
        self.__set_gauges()
        self.downloader.clear_reports()
