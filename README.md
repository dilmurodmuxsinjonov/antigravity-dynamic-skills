# 🚀 Antigravity Dynamic Skill Manager

Ushbu loyiha **Antigravity AI** (yoki har qanday agentic AI) uchun "Lazy Loading" arxitekturasini ta'minlab beruvchi mahalliylashtirilgan bilimlar bazasi boshqaruvchisidir.

## 🌟 Maqsad
AI tizimlariga minglab `.md` (Markdown) formatidagi bilimlarni (skills) birdaniga yuklash AI'ning token limitlarini (credit limit) juda tez tugatib yuboradi. Ushbu menejer barcha bilimlarni kompyuterning o'zida saqlaydi va AI'ga faqat kerakli bo'lgan bilimni aynan kerakli vaqtda "qidirib topish" va "o'qish" imkonini beradi. 

Bu usul orqali **token xarajatlari 90% gacha tejaladi** va AI'ning ishlash tezligi oshadi.

## ✨ Xususiyatlar
- **🔍 Avtomatik Sinxronizatsiya**: Eng mashhur Github skill repozitoriylaridan (sickn33, guanyang, rmyndharis) ma'lumotlarni avtomatik tortib oladi.
- **🛡️ Aqlli Tozalash (Deduplication)**: MD5 xeshlash algoritmi yordamida bir xil yoki mutloq o'xshash bilimlarni o'chirib yuboradi.
- **📂 Toifalarga ajratish**: Barcha bilimlar avtomatik ravishda `Full Stack`, `UI/UX`, `3D Animation`, `AI Skills` kabi papkalarga saralanadi.
- **🧠 AI Brain Integration**: Antigravity Brain tizimi bilan integratsiya qilingan (Indekslash mexanizmi).

## 🛠️ O'rnatish va Ishga tushirish

1. Ushbu repozitoriyni klonlang:
   ```bash
   git clone https://github.com/dilmurodmuxsinjonov/antigravity-dynamic-skills.git
   ```
2. Terminalni (PowerShell) oching va sinxronizatsiyani ishga tushiring:
   ```powershell
   powershell -ExecutionPolicy Bypass -File .\sync.ps1
   ```

## 📂 Loyiha Strukturasi
- `skills/`: Tozalangan va saralangan barcha `.md` fayllar.
- `skills_index.json`: AI uchun mo'ljallangan markazlashgan qidiruv indeksi.
- `sync.ps1`: PowerShell yordamida yozilgan asosiy sinxronizatsiya va filtrlash skripti.

## 🤝 Hissa qo'shish
Loyihani yanada takomillashtirish bo'yicha takliflaringiz bo'lsa, "Pull Request" yuboring yoki "Issue" oching.

---
*Created by Antigravity AI Assistant.*
