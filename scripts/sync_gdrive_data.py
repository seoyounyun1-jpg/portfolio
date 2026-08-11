#!/usr/bin/env python3
"""Google Drive의 데이터 파일을 로컬 data/{target}/ 폴더로 내려받는 수동 실행 스크립트."""

import argparse
import io
import json
import os
import sys

from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
SIZE_WARNING_THRESHOLD = 50 * 1024 * 1024  # 50MB

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(REPO_ROOT, "data")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Google Drive 파일을 data/{target}/ 폴더로 다운로드합니다."
    )
    parser.add_argument("--file-id", required=True, help="Google Drive 파일 ID")
    parser.add_argument(
        "--target", required=True, help="data/ 하위에 저장할 폴더명 (예: mission01)"
    )
    return parser.parse_args()


def build_drive_service():
    load_dotenv()
    raw_credentials = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not raw_credentials:
        sys.exit(
            "GOOGLE_SERVICE_ACCOUNT_JSON 환경변수가 설정되어 있지 않습니다. "
            ".env 파일을 확인하세요."
        )

    try:
        credentials_info = json.loads(raw_credentials)
    except json.JSONDecodeError:
        sys.exit("GOOGLE_SERVICE_ACCOUNT_JSON 값이 올바른 JSON 형식이 아닙니다.")

    credentials = service_account.Credentials.from_service_account_info(
        credentials_info, scopes=SCOPES
    )
    return build("drive", "v3", credentials=credentials)


def confirm_large_download(size_bytes, file_name):
    size_mb = size_bytes / (1024 * 1024)
    print(
        f"경고: '{file_name}' 파일 용량이 {size_mb:.1f}MB로 50MB를 초과합니다.",
        file=sys.stderr,
    )
    answer = input("계속 다운로드하시겠습니까? [y/N]: ").strip().lower()
    return answer in ("y", "yes")


def download_file(service, file_id, target_dir):
    metadata = service.files().get(fileId=file_id, fields="name, size").execute()
    file_name = metadata["name"]
    size_bytes = int(metadata.get("size", 0))

    if size_bytes > SIZE_WARNING_THRESHOLD:
        if not confirm_large_download(size_bytes, file_name):
            print("다운로드를 취소했습니다.")
            return

    os.makedirs(target_dir, exist_ok=True)
    destination_path = os.path.join(target_dir, file_name)

    request = service.files().get_media(fileId=file_id)
    with io.FileIO(destination_path, "wb") as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            if status:
                print(f"다운로드 중... {int(status.progress() * 100)}%")

    print(f"완료: {destination_path}")


def main():
    args = parse_args()
    service = build_drive_service()
    target_dir = os.path.join(DATA_DIR, args.target)
    download_file(service, args.file_id, target_dir)


if __name__ == "__main__":
    main()
