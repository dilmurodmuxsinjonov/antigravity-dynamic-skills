import json
import hashlib
import subprocess
import shutil
import re
import argparse
from pathlib import Path

# ==============================================================================
# Antigravity Dynamic Skill Manager - Sinxronizatsiya skripti (Python)
# ==============================================================================
# Ushbu skript tashqi repozitoriylardan skillarni tortib oladi va indekslaydi.
# Muallif: Antigravity AI Assistant (Jules)

DEFAULT_REPOS = [
    "https://github.com/sickn33/antigravity-awesome-skills.git",
    "https://github.com/guanyang/antigravity-skills.git",
    "https://github.com/rmyndharis/antigravity-skills.git"
]

ROOT_DIR = Path(__file__).parent.absolute()
TEMP_DIR = ROOT_DIR / ".temp_repos"
SKILLS_DIR = ROOT_DIR / "skills"
INDEX_FILE = ROOT_DIR / "skills_index.json"

def get_file_hash(filepath):
    """Faylning MD5 xeshini hisoblash."""
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
    except Exception as e:
        print(f"⚠️ Faylni o'qishda xatolik {filepath}: {e}")
        return None
    return hasher.hexdigest()

def normalize_name(name):
    """Fayl nomini solishtirish uchun normallashtirish."""
    return re.sub(r'[^a-z0-9]', '', name.lower())

def extract_description(content, filename):
    """Fayl ichidan qisqacha tavsifni ajratib olish."""
    match = re.search(r'^#+\s+(.*)', content, re.MULTILINE)
    if match:
        return match.group(1).strip()

    for line in content.splitlines():
        line = line.strip()
        if line and not line.startswith('#'):
            return line[:150] + ('...' if len(line) > 150 else '')

    return f"Skill fayli: {filename}"

def sync(repos):
    print("🔄 Sinxronizatsiya boshlandi...")

    if TEMP_DIR.exists():
        shutil.rmtree(TEMP_DIR)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    SKILLS_DIR.mkdir(parents=True, exist_ok=True)

    all_downloaded_files = []

    for i, repo_url in enumerate(repos):
        repo_path = TEMP_DIR / f"repo_{i}"
        print(f"📥 Yuklanmoqda: {repo_url}")

        try:
            subprocess.run(["git", "clone", "-q", "--depth", "1", repo_url, str(repo_path)], check=True)
        except subprocess.CalledProcessError:
            print(f"❌ Klonlashda xatolik: {repo_url}")
            continue

        if repo_path.exists():
            for md_file in repo_path.rglob("*.md"):
                if md_file.name.lower() != "readme.md":
                    all_downloaded_files.append(md_file)

    print(f"📦 Jami {len(all_downloaded_files)} ta yangi fayl topildi. Filtrlash va nusxalash...")

    existing_hashes = set()
    existing_names = set()

    for existing_file in SKILLS_DIR.rglob("*.md"):
        f_hash = get_file_hash(existing_file)
        if f_hash:
            existing_hashes.add(f_hash)
        existing_names.add(normalize_name(existing_file.name))

    new_skills_count = 0

    for file_path in all_downloaded_files:
        f_hash = get_file_hash(file_path)
        norm_name = normalize_name(file_path.name)

        if f_hash in existing_hashes or norm_name in existing_names:
            continue

        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
        except Exception:
            continue

        if not content:
            continue

        text = (file_path.name + " " + content).lower()

        category = "General"
        if re.search(r'ui|ux|tailwind|css|design|style|component|theme', text):
            category = "UI_UX"
        elif re.search(r'3d|animation|threejs|framer|motion|video|render', text):
            category = "3D_Animation"
        elif re.search(r'ai|prompt|skill|llm|agent|gpt|claude', text):
            category = "AI_MD_Skills"
        elif re.search(r'react|node|fullstack|api|dev|backend|frontend|sql|db', text):
            category = "Full_Stack_Developer"

        dest_folder = SKILLS_DIR / category
        dest_folder.mkdir(parents=True, exist_ok=True)

        dest_path = dest_folder / file_path.name
        shutil.copy2(file_path, dest_path)

        existing_hashes.add(f_hash)
        existing_names.add(norm_name)
        new_skills_count += 1

    print("📝 Indeks yangilanmoqda...")
    all_final_skills = []
    for skill_file in SKILLS_DIR.rglob("*.md"):
        if skill_file.name.lower() == "readme.md": continue

        try:
            with open(skill_file, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()

            category = skill_file.parent.name
            description = extract_description(content, skill_file.name)

            skill_obj = {
                "id": skill_file.stem,
                "name": skill_file.name,
                "category": category,
                "path": str(skill_file.relative_to(ROOT_DIR)).replace('\\', '/'),
                "description": description
            }
            all_final_skills.append(skill_obj)
        except Exception:
            continue

    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_final_skills, f, indent=4, ensure_ascii=False)

    print(f"✅ Tayyor! {new_skills_count} ta yangi skill qo'shildi.")
    print(f"📊 Jami skillar soni: {len(all_final_skills)}")

    if TEMP_DIR.exists():
        shutil.rmtree(TEMP_DIR)

    print("🎉 Operatsiya muvaffaqiyatli yakunlandi!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Antigravity Skill Manager Sync Tool")
    parser.add_argument('--repos', nargs='+', help='Sinxronizatsiya uchun repozitoriyalar ro\'yxati')
    args = parser.parse_args()

    sync(args.repos if args.repos else DEFAULT_REPOS)
