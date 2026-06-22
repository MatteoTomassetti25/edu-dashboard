<div align="center">

# 📊 edu-dashboard

**A minimal self-hosted dashboard to track your university career.**  
Weighted average, graduation projection, grade simulator — all in one static page.

[![Python](https://img.shields.io/badge/python-3.x-blue?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)
[![Self-hosted](https://img.shields.io/badge/self--hosted-yes-orange?style=flat-square)]()
[![No dependencies](https://img.shields.io/badge/dependencies-none-lightgrey?style=flat-square)]()



</div>

---

## ✨ Features

| | |
|---|---|
| 📝 **Inline grade editing** | Click any grade in the table to edit it — saves instantly to `data.json` |
| ⚖️ **Weighted average** | Supports `special_cfu` overrides for per-exam weighting rules |
| 🔮 **Grade simulator** | "What if I get X on this exam?" — recalculates your average in real time |
| 🎯 **Graduation projection** | Minimum average needed on remaining exams to hit your target |
| 🔄 **Auto-refresh** | Re-fetches data every 30s — open on multiple devices and stay in sync |
| 🏷️ **Status badges** | Click to cycle: `Not done → Upcoming → Submitted → Pending → Graded` |
| 🐳 **Docker ready** | One-command deploy with `docker compose up` |
| 🔒 **Private by design** | `config.json` and `data.json` are gitignored — your data stays local |

---

## 🚀 Quick Start

> **Requirements:** Python 3 only. No packages to install.

```bash
git clone https://github.com/MatteoTomassetti25/edu-dashboard
cd edu-dashboard

cp config.example.json config.json   # edit with your info
cp data.example.json   data.json     # edit with your courses

python3 server.py
# → http://localhost:8800
```

---

## ⚙️ Configuration

### `config.json`

```json
{
  "student_name": "Your Name",
  "matricola": "123456",
  "university": "Your University",
  "degree": "MSc Computer Science",
  "total_cfu": 120,
  "target_media": 27.3,
  "thesis_bonus": 10
}
```

| Field | Description |
|---|---|
| `total_cfu` | Total credits required to graduate |
| `target_media` | Weighted average you're aiming for |
| `thesis_bonus` | Bonus points added at graduation (0 if none) |

---

### `data.json`

An array of exam objects:

```json
[
  {
    "nome": "Machine Learning",
    "cfu": 9,
    "voto": null,
    "data": "15/07/2025",
    "status": "next",
    "anno": 1,
    "note": "",
    "special_cfu": null
  }
]
```

#### Fields

| Field | Type | Description |
|---|---|---|
| `nome` | `string` | Course name |
| `cfu` | `number` | Credits |
| `voto` | `number \| null` | Grade (18–30), or `null` if not yet taken |
| `data` | `string \| null` | Exam date `"DD/MM/YYYY"`, or `null` |
| `status` | `string` | See table below |
| `anno` | `number` | Year group for display (1, 2, …) |
| `note` | `string` | Free text shown in the table |
| `special_cfu` | `number \| null` | CFU override for weighted average (see below) |

#### Status values

| Value | Meaning | Badge color |
|---|---|---|
| `todo` | Not yet taken | grey |
| `next` | Upcoming exam, date set | orange |
| `sent` | Project submitted, awaiting grade | blue |
| `wait` | Taken but not officially recorded | yellow |
| `done` | Officially graded | green |

> **Tip:** You can also click the badge in the dashboard to cycle through statuses.

#### `special_cfu` — custom weighting

Some universities apply rules where the lowest grade in your career is weighted differently in the average.  
Set `special_cfu` on that exam to override its weight:

```json
{
  "nome": "That one hard exam",
  "cfu": 9,
  "voto": 22,
  "status": "done",
  "special_cfu": 4
}
```

The exam counts as **4 CFU** (not 9) in the weighted average. All other values (display, CFU progress) use the real `cfu`.

---

## 🐳 Docker

```bash
cp config.example.json config.json
cp data.example.json   data.json
# edit both, then:
docker compose up -d
```

Custom port: `PORT=9000 docker compose up -d`

---

## 🖥️ Permanent self-hosting (Linux systemd)

```bash
mkdir -p ~/.config/systemd/user

cat > ~/.config/systemd/user/edu-dashboard.service << EOF
[Unit]
Description=edu-dashboard
After=network.target

[Service]
ExecStart=python3 /path/to/edu-dashboard/server.py
WorkingDirectory=/path/to/edu-dashboard
Restart=always

[Install]
WantedBy=default.target
EOF

systemctl --user enable --now edu-dashboard
```

---

## 📁 Project structure

```
edu-dashboard/
├── index.html            # frontend — single file, zero build step
├── server.py             # ~30 lines, no extra packages
├── config.json           # your personal config  ← gitignored
├── data.json             # your study plan        ← gitignored
├── config.example.json   # template
├── data.example.json     # template
└── docker-compose.yml
```

---

## 🔧 Updating grades

**From the dashboard** *(recommended)*  
Click any `—` in the Grade column → type the grade → Enter.

**From the terminal** *(e.g. over SSH)*  
Edit `data.json` directly. The dashboard picks up changes within 30 seconds.

---

<div align="center">

Made with ☕ by [MatteoTomassetti25](https://github.com/MatteoTomassetti25)

</div>
