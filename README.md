# edu-dashboard

A minimal self-hosted academic dashboard for tracking your university study plan, weighted average, and graduation projection.

![screenshot placeholder](https://placeholder.co/800x400?text=edu-dashboard)

## Features

- **Live grade tracking** — click any grade in the table to edit it; changes save instantly
- **Weighted average** — supports custom per-exam CFU weights (e.g. lowest-grade weighting rules)
- **Simulator** — "what if I get X on this exam?" recalculates your average in real time
- **Graduation projection** — calculates the minimum average needed on remaining exams to hit your target
- **Auto-refresh** — page re-fetches data every 30s; open on multiple devices and they stay in sync
- **Status badges** — click to cycle: `Not done → Upcoming → Submitted → Pending grade → Graded`

## Quick Start

**Requirements:** Python 3 (no extra packages).

```bash
git clone https://github.com/cmdhro/edu-dashboard
cd edu-dashboard

# 1. Create your config
cp config.example.json config.json

# 2. Create your study plan
cp data.example.json data.json

# 3. Run
python3 server.py
# → http://localhost:8800
```

Edit `config.json` and `data.json` with your data (see below), then open the browser.

## Configuration

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
| `total_cfu` | Total credits required for your degree |
| `target_media` | Weighted average you're aiming for |
| `thesis_bonus` | Bonus points added to your base grade at graduation (0 if none) |

### `data.json`

An array of exam objects. Each exam:

```json
{
  "nome": "Machine Learning",
  "cfu": 9,
  "voto": null,
  "data": "15/07/2025",
  "status": "next",
  "anno": 1,
  "note": "optional free text",
  "special_cfu": null
}
```

| Field | Type | Description |
|---|---|---|
| `nome` | string | Course name |
| `cfu` | number | Credits |
| `voto` | number \| null | Grade (18–30), or `null` if not yet taken |
| `data` | string \| null | Exam date as `"DD/MM/YYYY"`, or `null` |
| `status` | string | See status values below |
| `anno` | number | Academic year (1, 2, …) — used for grouping |
| `note` | string | Optional notes shown in the table |
| `special_cfu` | number \| null | Override CFU weight in the average calculation (see below) |

#### Status values

| Value | Meaning |
|---|---|
| `todo` | Not yet taken |
| `next` | Upcoming — has a set date |
| `sent` | Project/work submitted, waiting for oral/grade |
| `wait` | Taken but not yet officially recorded |
| `done` | Officially graded and recorded |

> You can also click the badge in the dashboard to cycle through statuses.

#### `special_cfu` — custom weighting

Some universities apply a rule where the lowest grade in your career is weighted differently (e.g. counts for fewer credits in the average calculation). Set `special_cfu` on that exam:

```json
{
  "nome": "That one exam you bombed",
  "cfu": 9,
  "voto": 22,
  "status": "done",
  "special_cfu": 4
}
```

This exam will count as 4 CFU (not 9) in the weighted average. All other calculations use the real `cfu` value.

## Changing the port

```bash
PORT=9000 python3 server.py
```

## Docker

```bash
cp config.example.json config.json
cp data.example.json data.json
# edit both files, then:
docker compose up -d
```

To change the port: `PORT=9000 docker compose up -d`

## Updating grades

**From the dashboard** (recommended): click any `—` in the Grade column, type the grade, press Enter.

**From the terminal** (e.g. via SSH on a server): edit `data.json` directly. The dashboard picks up changes within 30 seconds.

## File structure

```
edu-dashboard/
├── index.html            # frontend (single file, no build step)
├── server.py             # ~30-line HTTP server (GET static + POST data.json/config.json)
├── config.json           # your personal config (gitignored)
├── data.json             # your study plan (gitignored)
├── config.example.json   # template
├── data.example.json     # template
└── docker-compose.yml    # optional
```

`config.json` and `data.json` are in `.gitignore` — your personal data never ends up in version control.

## Self-hosting permanently (Linux systemd)

```bash
# On your server, inside the project directory:
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

Made by [cmdhro](https://github.com/cmdhro)
