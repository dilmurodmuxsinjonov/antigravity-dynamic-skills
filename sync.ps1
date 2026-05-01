# ==============================================================================
# Antigravity Dynamic Skill Manager - Sinxronizatsiya va Tozalash Skripti
# ==============================================================================
# Ushbu skript Githubdan AI skillarni (bilimlarni) yuklab oladi, dublikatlarni 
# o'chiradi va ularni toifalarga ajratgan holda mahalliy baza yaratadi.

$ErrorActionPreference = "Continue"

# 1. Manba repozitoriylari (Github)
$Repos = @(
    "https://github.com/sickn33/antigravity-awesome-skills.git",
    "https://github.com/guanyang/antigravity-skills.git",
    "https://github.com/rmyndharis/antigravity-skills.git"
)

# 2. Papka va fayl manzillarini aniqlash
$RootDir = Get-Location
$TempDir = Join-Path $RootDir ".temp_repos"       # Vaqtinchalik yuklash papkasi
$SkillsDir = Join-Path $RootDir "skills"          # Asosiy skillar papkasi
$IndexFile = Join-Path $RootDir "skills_index.json" # AI uchun indeks fayli

# 3. Eski ma'lumotlarni tozalash va yangi papkalar yaratish
if (Test-Path $TempDir) { Remove-Item -Recurse -Force $TempDir }
if (Test-Path $SkillsDir) { Remove-Item -Recurse -Force $SkillsDir }

New-Item -ItemType Directory -Force -Path $TempDir | Out-Null
New-Item -ItemType Directory -Force -Path $SkillsDir | Out-Null

$AllFiles = @()

Write-Host "🔄 Sinxronizatsiya boshlandi..." -ForegroundColor Cyan

# 4. Repozitoriylarni klonlash (Clone) va fayllarni yig'ish
$i = 0
foreach ($repoUrl in $Repos) {
    $repoPath = Join-Path $TempDir "repo_$i"
    Write-Host "📥 Yuklanmoqda: $repoUrl"
    
    # Git yordamida repozitoriyni vaqtincha papkaga yuklash
    git clone -q $repoUrl $repoPath
    
    if (Test-Path $repoPath) {
        # Faqat .md (Markdown) fayllarni qidirib topish
        $mdFiles = Get-ChildItem -Path $repoPath -Filter "*.md" -Recurse -File
        foreach ($f in $mdFiles) {
            # README fayllarni hisobga olmaymiz
            if ($f.Name.ToLower() -ne "readme.md") {
                $AllFiles += $f
            }
        }
    }
    $i++
}

Write-Host "📦 Jami $($AllFiles.Count) ta .md fayl topildi. Filtrlash boshlandi..." -ForegroundColor Yellow

# 5. Dublikatlarni o'chirish va Toifalash mantiqi
$ContentHashes = @{} # Fayl ichidagi matn xeshlari (MD5)
$FileNames = @{}     # Fayl nomlari ro'yxati
$UniqueSkills = @()  # Noyob (unique) skillar to'plami

foreach ($file in $AllFiles) {
    $content = Get-Content $file.FullName -Raw -ErrorAction SilentlyContinue
    if (-not $content) { continue }
    
    # Faylning MD5 xeshini olish (mutloq o'xshashlikni aniqlash uchun)
    $hash = (Get-FileHash -Path $file.FullName -Algorithm MD5).Hash
    $normalizedName = $file.Name.ToLower() -replace '[^a-z0-9]',''
    
    # Agar ushbu xesh yoki nom avval uchramagan bo'lsa, uni bazaga qo'shamiz
    if (-not $ContentHashes.ContainsKey($hash) -and -not $FileNames.ContainsKey($normalizedName)) {
        $ContentHashes[$hash] = $true
        $FileNames[$normalizedName] = $true
        
        $text = ($file.Name + " " + $content).ToLower()
        
        # Kalit so'zlar asosida toifalarga (category) ajratish
        $category = "General"
        if ($text -match 'ui|ux|tailwind|css|design') { $category = "UI_UX" }
        elseif ($text -match '3d|animation|threejs|framer') { $category = "3D_Animation" }
        elseif ($text -match 'ai|prompt|\.md|skill') { $category = "AI_MD_Skills" }
        elseif ($text -match 'react|node|fullstack|api|dev') { $category = "Full_Stack_Developer" }
        
        $destFolder = Join-Path $SkillsDir $category
        if (-not (Test-Path $destFolder)) { New-Item -ItemType Directory -Force -Path $destFolder | Out-Null }
        
        # Faylni o'z toifasiga ko'ra ko'chirib o'tkazish
        $destPath = Join-Path $destFolder $file.Name
        Copy-Item -Path $file.FullName -Destination $destPath -Force
        
        # AI uchun ma'lumotlar obyektini yaratish
        $skillObj = @{
            id = $file.Name.Replace('.md','')
            name = $file.Name
            category = $category
            path = "skills/$category/$($file.Name)"
            description = "Antigravity Skill: $($file.Name)"
        }
        $UniqueSkills += $skillObj
    }
}

# 6. Markazlashgan indeks faylini yaratish (JSON)
$UniqueSkills | ConvertTo-Json -Depth 5 | Out-File -FilePath $IndexFile -Encoding utf8

Write-Host "✅ Tozalandi! Jami $($UniqueSkills.Count) ta noyob skill saqlab qolindi." -ForegroundColor Green
# Vaqtinchalik papkani o'chirish
Remove-Item -Recurse -Force $TempDir
Write-Host "🎉 Sinxronizatsiya muvaffaqiyatli yakunlandi!" -ForegroundColor Cyan
