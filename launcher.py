import json
import subprocess
import urllib.request
import urllib.error
import shutil
import tempfile
import zipfile

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

GAME_DIR = BASE_DIR / "game"
GAME_FILE = GAME_DIR / "game.exe"
VERSION_FILE = GAME_DIR / "version.json"

VERSION_URL = (
    "https://raw.githubusercontent.com/"
    "krwstar/coding-rehab-dungeon/main/version.json"
)
DOWNLOAD_URL = (
    "https://github.com/"
    "krwstar/coding-rehab-dungeon/releases/latest/download/"
    "coding-rehab-dungeon-windows.zip"
)


def has_game():
    return GAME_FILE.exists()


def has_internet():
    try:
        urllib.request.urlopen(VERSION_URL, timeout=5)
        return True
    except (
        urllib.error.URLError,
        urllib.error.HTTPError,
        TimeoutError,
    ):
        return False


def get_local_version():
    try:
        with open(VERSION_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        return data["version"]
    
    except (FileNotFoundError, KeyError, json.JSONDecodeError):
        return None


def get_remote_version():
    try:
        with urllib.request.urlopen(VERSION_URL, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))

        return data["version"]

    except(
        urllib.error.URLError,
        urllib.error.HTTPError,
        TimeoutError,
        KeyError,
        json.JSONDecodeError,
    ):
        return None


def version_tuple(version):
    return tuple(int(part) for part in version.split("."))


def check_update():
    local_version = get_local_version()
    remote_version = get_remote_version()
    
    if remote_version is None:
        return False
    if local_version is None:
        return True
    
    return version_tuple(remote_version) > version_tuple(local_version)


def update_game():
    print("게임을 다운로드하는 중...")
    
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir = Path(temp_dir)
            
            zip_path = temp_dir / "update.zip"
            extract_dir = temp_dir / "update"
            
            urllib.request.urlretrieve(
                DOWNLOAD_URL,
                zip_path,
            )
            
            print("다운로드 완료")
            print("업데이트 파일을 확인하는 중...")
            
            extract_dir.mkdir()
            
            with zipfile.ZipFile(zip_path, "r") as zip_file:
                zip_file.extractall(extract_dir)
            
            new_game_file = extract_dir / "game.exe"
            new_version_file = extract_dir / "version.json"
            
            if not new_game_file.exists():
                raise FileNotFoundError(
                    "업데이트 파일에 game.exe가 없습니다."
                )
            
            if not new_version_file.exists():
                raise FileNotFoundError(
                    "업데이트 파일에 version.json이 없습니다."
                )
            
            with open(new_version_file, "r", encoding="utf-8") as f:
                version_data = json.load(f)
            
            if "version" not in version_data:
                raise ValueError(
                    "version.json에 version 정보가 없습니다."
                )
            
            GAME_DIR.mkdir(parents=True, exist_ok=True)
            
            for item in extract_dir.iterdir():
                destination = GAME_DIR / item.name
                
                if item.is_dir():
                    shutil.copytree(
                        item,
                        destination,
                        dirs_exist_ok=True,
                    )
                else:
                    shutil.copy2(
                        item,
                        destination,
                    )
            
            print(f"업데이트 완료! 버전 {version_data['version']}")
        
        return True
    
    except (
        urllib.error.URLError,
        urllib.error.HTTPError,
        TimeoutError,
        zipfile.BadZipFile,
        FileNotFoundError,
        json.JSONDecodeError,
        ValueError,
        OSError,
    ) as e:
        print()
        print("업데이트에 실패했습니다.")
        print(f"오류: {e}")
        return False


def launch_game():
    subprocess.Popen([str(GAME_FILE)], cwd=GAME_DIR)

def main():
    online = has_internet()
    game_exists = has_game()
    
    if not online and not game_exists:
        print("게임 파일을 찾을 수 없습니다.")
        print("게임을 다운로드하려면 인터넷 연결이 필요합니다.")
        input("Enter를 눌러 종료...")
        return
    
    if not online:
        print("인터넷에 연결할 수 없습니다.")
        print("업데이트를 확인하지 않고 게임을 실행합니다.")
        launch_game()
        return
    
    if not game_exists:
        input("Enter를 눌러 게임을 다운로드...")
        
        if not update_game():
            input("Enter를 눌러 종료...")
            return
        
        launch_game()
        return
    
    if check_update():
        print("새로운 버전이 있습니다.")
        
        if not update_game():
            print("업데이트에 실패했습니다.")
            print("기존 버전으로 게임을 실행합니다.")
            input("Enter를 눌러 진행...")
    
    launch_game()

if __name__ == "__main__":
    main()