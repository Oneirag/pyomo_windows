import re
import zipfile
from io import BytesIO
from pathlib import Path
from typing import List

import httpx
from bs4 import BeautifulSoup
from ong_utils import is_windows

from pyomo_windows import logger, solver_executables, get_target_folder

if is_windows:
    import ssl

    ssl_verify = ssl.create_default_context()
else:
    ssl_verify = True


class DownloadSolvers:

    def __init__(self, target: Path | str = None):
        """
        Init the downloader. Solvers are downloaded in this folder by default, or
        under the provided folder
        :param target: the folder where models will be downloaded. It is created if it does not exit
        """
        self.target = get_target_folder(target)
        self.client = httpx.Client(verify=ssl_verify, follow_redirects=True)
        self.logger = logger

    def __download(self, url: str, destination: Path, required_files: List[str]):
        """Downloads a file and returns file contents (in memory) and file name"""
        self.logger.info(f"Downloading {url}")
        contents = list()
        with self.client.stream(method="get", url=url) as response:
            file_name = response.url.path.split("/")[-1]
            content_length = int(response.headers["Content-Length"])
            num_bytes_downloaded = 0
            for chunk in response.iter_bytes():
                contents.append(chunk)
                # download_file.write(chunk)
                num_bytes_downloaded += len(chunk)
                percent_complete = 100.0 * (num_bytes_downloaded / content_length)
                self.logger.info(f"{file_name}: {percent_complete:.2f}%")

        # res = self.client.get(url)
        file_content = BytesIO(b"".join(contents))
        # file_name = res.url.path.split("/")[-1]
        with zipfile.ZipFile(file_content) as zip:
            for name in zip.namelist():
                if any(re.match(pattern, name) for pattern in required_files):
                    destination_filename = name.split("/")[-1]
                    (destination / destination_filename).write_bytes(zip.read(name))
                else:
                    self.logger.warn(f"Skipping file: {name}")

    def download_glpk(self):
        solver = "glpk"
        url = "http://sourceforge.net/projects/winglpk/"
        url = "https://sourceforge.net/projects/winglpk/files/latest/download"
        destination = self.target / solver
        destination.mkdir(exist_ok=True)
        required_files = [
            rf".*/w64/{solver_executables[solver]}",
            r".*/w64/glpk_.*\.dll",

        ]
        self.__download(url, destination, required_files)
        self.logger.info("finished!")

    def get_download_link_github(self, github_link: str, release: str, link_filter_pattern: str) -> str:
        """
        Gets the download link of a github project
        :param github_link: something like https://github.com/<developer>/<project_name>
        :param release: the release version (p.ej. 3.14.16 for Ipot)
        :param link_filter_pattern: regular expression to apply to the releases links to get the correct link
        :return: a full download link of the zip file
        """
        if github_link.endswith("/"):
            github_link = github_link[:-1]
        url = f"{github_link}/releases/expanded_assets/releases/{release}"
        soup = BeautifulSoup(self.client.get(url), features="html.parser")
        links = soup.find_all("a")
        zips = [link for link in links if link.get("href").endswith(".zip")]
        download_path = [z.get("href") for z in zips if re.match(link_filter_pattern, z.get("href"))][0]
        download_url = f"https://github.com{download_path}"
        return download_url

    def download_ipopt(self):
        solver = "ipopt"
        download_link = self.get_download_link_github(github_link="https://github.com/coin-or/Ipopt",
                                                      release="3.14.16",
                                                      link_filter_pattern=r".*-md\.zip")

        destination = self.target / solver
        destination.mkdir(exist_ok=True)
        """All dll and executable of the bin folder"""
        required_files = [
            rf".*bin/.*\.exe",
            rf".*bin/.*\.dll",
        ]
        self.__download(download_link, destination, required_files)
        self.logger.info("finished!")

    def download_cbc(self):
        solver = "cbc"
        download_link = self.get_download_link_github(github_link="https://github.com/coin-or/Cbc",
                                                      release="2.10.12",
                                                      link_filter_pattern=r".*-windows-2022.*\.zip")

        destination = self.target / solver
        destination.mkdir(exist_ok=True)
        """All dll and executable of the bin folder"""
        required_files = [
            rf".*cbc\.exe",
        ]
        self.__download(download_link, destination, required_files)
        self.logger.info("finished!")


if __name__ == '__main__':
    downloader = DownloadSolvers()
    downloader.download_glpk()
    # downloader.download_ipopt()
    # downloader.download_cbc()
