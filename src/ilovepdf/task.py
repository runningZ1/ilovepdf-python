from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from urllib.parse import unquote

from .errors import ApiError, Error, Errors
from .file import File
from .ilovepdf import Ilovepdf
from .request_payload.form_url_encoded import FormUrlEncoded
from .servers import START_SERVER
from .extra_upload_params.base import Base as ExtraUploadParamsBase


@dataclass
class DownloadInfo:
    output_filename: Optional[str] = None
    output_file: Optional[bytes] = None
    output_filetype: Optional[str] = None


class Task(Ilovepdf):
    API_PARAMS: List[str] = []

    def __init__(self, public_key: str, secret_key: str, make_start: bool = False) -> None:
        super().__init__(public_key, secret_key)
        self.task_id: Optional[str] = None
        if not hasattr(self, "tool"):
            self.tool = None
        self.packaged_filename: Optional[str] = None
        self.output_filename: Optional[str] = None
        self.ignore_errors = True
        self.ignore_password = True
        self.try_pdf_repair = True
        self._files: List[File] = []
        self._meta_values: Dict[str, Any] = {}
        self._download_info = DownloadInfo()
        self._result: Optional[Any] = None
        self._chained_task = not make_start
        if make_start:
            response = self.perform_start_request()
            self.worker_server = f"https://{response.body['server']}"
            self.task_id = response.body["task"]

    @property
    def result(self):
        return self._result

    def chained_task(self) -> bool:
        return self._chained_task

    def next(self, next_tool: str) -> "Task":
        body = {
            "v": self.api_version,
            "task": self.task_id,
            "tool": next_tool,
        }
        encoded = FormUrlEncoded(body).extract_to_str()
        try:
            response = self.send_request("post", "task/next", {"body": encoded})
            no_task_present = "task" not in response.body or not response.body.get("task")
            if no_task_present:
                raise Errors.StartError(response, custom_msg="No task assigned on chained start")
        except ApiError as exc:
            raise Errors.StartError(exc.http_response, custom_msg="Error on start chained task")

        next_task = self.new_task(next_tool, make_start=False)
        next_task.worker_server = self.worker_server
        next_task.task_id = response.body["task"]

        for server_filename, filename in response.body.get("files", {}).items():
            next_task.files.append(File(server_filename, filename))
        return next_task

    def assign_meta_value(self, key: str, value: Any) -> None:
        self._meta_values[key] = value

    @property
    def files(self) -> List[File]:
        return self._files

    def add_file(self, filepath: str, extra_upload_params: Optional[ExtraUploadParamsBase] = None) -> File:
        if not os.path.isfile(filepath):
            raise ValueError(f"No file exists in '{filepath}'")
        file = self.perform_upload_request(filepath, extra_upload_params)
        self._files.append(file)
        return file

    def add_file_from_url(self, url: str, extra_upload_params: Optional[ExtraUploadParamsBase] = None) -> File:
        file = self.perform_upload_url_request(url, extra_upload_params)
        self._files.append(file)
        return file

    def download(self, path: Optional[str] = None, create_directory: bool = False) -> bool:
        self.download_file()
        if path:
            path = os.fspath(path)
            if path.endswith("/"):
                path = path[:-1]
        else:
            path = "."
        destination = os.path.join(path, self._download_info.output_filename or "")
        if create_directory:
            os.makedirs(path, exist_ok=True)
        with open(destination, "wb") as file_handle:
            file_handle.write(self._download_info.output_file or b"")
        return True

    def blob(self) -> Optional[bytes]:
        self.download_file()
        return self._download_info.output_file

    @property
    def download_info(self) -> DownloadInfo:
        return self._download_info

    def status(self):
        return self.query_task_status(self.worker_server, self.task_id)

    def execute(self):
        self._result = self.perform_process_request()
        return self._result

    def delete(self):
        return self.send_request("delete", f"task/{self.task_id}")

    def delete_file(self, file: File) -> bool:
        if file.deleted():
            raise Error("File was already deleted")
        file_was_found = any(f.server_filename == file.server_filename for f in self.files)
        if not file_was_found:
            raise Error("File to delete not found")
        response = self.perform_deletefile_request(file)
        if response.success():
            file.mark_as_deleted()
            self._files = [f for f in self._files if f.server_filename != file.server_filename]
        else:
            raise ApiError(response, custom_msg="No error occurred but response was not successful when deleting the desired file")
        return True

    def enable_file_encryption(self, enable: bool, new_encrypt_key: Optional[str] = None) -> None:
        if self.files:
            raise Error("Encryption mode cannot be assigned after uploading the files")
        super().enable_file_encryption(enable, new_encrypt_key)

    def download_file(self) -> bool:
        response = self.perform_filedownload_request()
        content_disposition = response.headers.get("content-disposition")
        filename = self._parse_filename_from_content_disposition(content_disposition)
        self._download_info.output_filename = filename
        self._download_info.output_file = response.raw_body
        self._download_info.output_filetype = os.path.splitext(filename or "")[1]
        return True

    def perform_deletefile_request(self, file: File):
        body = {
            "task": self.task_id,
            "server_filename": file.server_filename,
            "v": self.api_version,
        }
        return self.send_request("delete", f"upload/{self.task_id}/{file.server_filename}", {"body": body})

    def perform_filedownload_request(self):
        return self.send_request("get", f"download/{self.task_id}", {"body": {"v": self.api_version}})

    def perform_process_request(self):
        body = {
            "task": self.task_id,
            "tool": self.tool,
            "packaged_filename": self.packaged_filename,
            "output_filename": self.output_filename,
            "ignore_errors": self.ignore_errors,
            "ignore_password": self.ignore_password,
            "try_pdf_repair": self.try_pdf_repair,
            "meta": self._meta_values,
            "v": self.api_version,
        }
        body.update(self.file_submit_params())
        body.update(self.extract_api_params())
        return self.send_request("post", "process", {"body": body})

    def perform_start_request(self):
        body = {"v": self.api_version}
        encoded = FormUrlEncoded(body).extract_to_str()
        response = self.send_request("get", f"start/{self.tool}", {"body": encoded})
        if "server" not in response.body or not response.body.get("server"):
            raise Errors.StartError(response, custom_msg="No server assigned on start")
        return response

    def perform_upload_request(self, filepath: str, tool_additional_params: Optional[ExtraUploadParamsBase] = None):
        file_handle = open(filepath, "rb")
        try:
            body: Dict[str, Any] = {
                "multipart": True,
                "v": self.api_version,
                "task": self.task_id,
                "file": file_handle,
            }
            if isinstance(tool_additional_params, ExtraUploadParamsBase):
                body.update(tool_additional_params.get_values())
            response = self.send_request("post", "upload", {"body": body})
        finally:
            file_handle.close()
        return self.get_file_from_response(response.body, filepath)

    def perform_upload_url_request(self, url: str, tool_additional_params: Optional[ExtraUploadParamsBase] = None):
        body: Dict[str, Any] = {
            "multipart": True,
            "v": self.api_version,
            "task": self.task_id,
            "cloud_file": url,
        }
        if isinstance(tool_additional_params, ExtraUploadParamsBase):
            body.update(tool_additional_params.get_values())
        response = self.send_request("post", "upload", {"body": body})
        return self.get_file_from_response(response.body, url)

    def file_submit_params(self) -> Dict[str, Any]:
        files_payload: Dict[str, Any] = {"files": {}}
        for idx, f in enumerate(self.files):
            files_payload["files"][str(idx)] = f.file_options()
        return files_payload

    def extract_api_params(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        for param_name in self.API_PARAMS:
            result[param_name] = getattr(self, param_name, None)
        return result

    def get_file_from_response(self, response_body: Dict[str, Any], file_path_or_url: str) -> File:
        filename = os.path.basename(file_path_or_url)
        file = File(response_body.get("server_filename"), filename)
        if response_body.get("pdf_pages"):
            file.pdf_pages = response_body.get("pdf_pages")
        if response_body.get("pdf_page_number"):
            file.pdf_page_number = int(response_body.get("pdf_page_number"))
        if response_body.get("pdf_forms"):
            file.pdf_forms = response_body.get("pdf_forms")
        return file

    def _parse_filename_from_content_disposition(self, content_disposition: Optional[str]) -> Optional[str]:
        if not content_disposition:
            return None
        if "filename*=" in content_disposition:
            parts = content_disposition.split("filename*=")
            if len(parts) > 1:
                value = parts[1]
                if "''" in value:
                    value = value.split("''", 1)[1]
                return unquote(value.replace('"', ""))
        if "filename=" in content_disposition:
            value = content_disposition.split("filename=")[-1]
            return value.replace('"', "").strip()
        return None
