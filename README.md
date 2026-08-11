# Portfolio

데이터 분석/사이드 프로젝트 기록용 포트폴리오 저장소입니다.

## 폴더 구조

```
portfolio/
├── README.md
├── .gitignore
├── .env.example
├── missions/              # 미션 기록 (md 파일, 직접 작성)
├── projects/               # 프로젝트 기록 (md 파일, 직접 작성)
├── data/                   # 분석에 사용한 데이터 (Google Drive에서 스크립트로 동기화)
│   ├── 미션01/                # missions/미션01 대응 데이터
│   └── 사이드프로젝트01/       # projects/사이드프로젝트01 대응 데이터
└── scripts/
    └── sync_gdrive_data.py # Google Drive 데이터 다운로드 스크립트
```

- `missions/`, `projects/`: 학습 기록/프로젝트 회고 등을 마크다운으로 직접 작성해서 넣는 공간입니다.
- `data/`: 각 미션·프로젝트에서 사용한 데이터 파일을 담는 공간이며, 파일은 커밋하지 않고 `scripts/sync_gdrive_data.py`로 각자 로컬에서 내려받아 채웁니다. 자동화 워크플로는 없고 필요할 때 수동으로 실행합니다.

## Google Drive 연동 설정

`sync_gdrive_data.py`는 Google Drive API(서비스 계정 인증)를 사용해 지정한 파일을 내려받습니다.

### 1. Google Cloud 서비스 계정 발급

1. [Google Cloud Console](https://console.cloud.google.com/)에서 프로젝트를 생성(또는 기존 프로젝트 선택)합니다.
2. `API 및 서비스 > 라이브러리`에서 **Google Drive API**를 검색해 활성화합니다.
3. `API 및 서비스 > 사용자 인증 정보 > 사용자 인증 정보 만들기 > 서비스 계정`으로 서비스 계정을 생성합니다.
4. 생성된 서비스 계정 상세 화면에서 `키 > 키 추가 > 새 키 만들기 > JSON`을 선택해 JSON 키 파일을 다운로드합니다.
5. 다운로드한 JSON 파일 안의 `client_email` 값을 확인합니다.

### 2. Drive 폴더/파일 공유

- Google Drive에서 데이터가 있는 폴더(또는 파일)를 우클릭 → 공유에서, 위에서 확인한 서비스 계정 이메일(`client_email`)을 **뷰어** 권한으로 추가합니다.
- 서비스 계정과 공유되지 않은 파일은 API로 접근할 수 없습니다.

### 3. .env 설정

1. `.env.example`을 복사해 `.env` 파일을 만듭니다.

   ```bash
   cp .env.example .env
   ```

2. 다운로드한 JSON 키 파일의 **전체 내용을 한 줄로** `GOOGLE_SERVICE_ACCOUNT_JSON`에 넣습니다.

   ```
   GOOGLE_SERVICE_ACCOUNT_JSON={"type":"service_account","project_id":"...","private_key":"...","client_email":"...", ...}
   ```

   `.env`는 `.gitignore`에 포함되어 있어 커밋되지 않습니다.

### 4. 의존성 설치

```bash
pip install -r requirements.txt
```

## 사용법: scripts/sync_gdrive_data.py

Google Drive 파일 ID와 저장할 `data/` 하위 폴더명을 인자로 받아 원본 파일명 그대로 다운로드합니다. 파일이 50MB를 초과하면 경고 후 계속 진행할지 확인합니다.

```bash
python scripts/sync_gdrive_data.py --file-id <GOOGLE_DRIVE_FILE_ID> --target 미션01
```

```bash
python scripts/sync_gdrive_data.py --file-id <GOOGLE_DRIVE_FILE_ID> --target 사이드프로젝트01
```

파일은 `data/{target}/원본파일명` 경로에 저장됩니다.

> 파일 ID는 Google Drive 공유 링크(`https://drive.google.com/file/d/여기가_파일_ID/view`)에서 확인할 수 있습니다.
