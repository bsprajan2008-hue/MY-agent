# FAIRSHIFT — Fair Workload and Well-being Platform

> **A Fair Workload and Well-being Platform for Schools and Employee-Intensive Organisations**  
> *Preventing chronic overwork through transparent data, evidence-based conversations, and student-first priorities.*

---

## 🎯 Mission & Core Human Problem

In schools and employee-intensive sectors, dedicated professionals (especially teachers) frequently experience chronic overwork. Many teachers take on heavy after-hours preparation and grading because **they care deeply about their students and worry that students will suffer if tasks remain unfinished**. Other contributing factors include ambiguous task ownership, repetitive manual administration, uneven distribution, and reluctance to raise workload concerns.

**FAIRSHIFT** transforms workload management from subjective assumptions, surveillance, or accusations into **transparent, respectful, evidence-based collaboration**.

### Working Principles
1. **Never assume laziness or exploitation**: All workload metrics are neutral, grounded in recorded time and task ownership.
2. **Never compromise student safety or exam-critical work**: Essential student outcomes and legally mandated duties are strictly protected.
3. **Separate duty origins**: Clear demarcation between formally assigned work, voluntary extra support, emergency coverage, and unowned tasks.
4. **Non-surveillance guarantee**: Explicitly rejects keystroke logging, covert idle counters, and public ranking lists.
5. **Private reflection space**: Private teacher journal notes are isolated and strictly inaccessible to managers unless explicitly shared with informed consent.
6. **Explainable calculations**: Every capacity score and recommendation is derived from transparent weighted mathematical rules, not a black-box AI model.
7. **Deterministic reliability**: Core features, analytics, and advisories remain 100% operational even without external AI API keys or network access.

---

## 🏗️ Architecture & Tech Stack

```
fairshift/
├── app/
│   ├── config.py             # Environment configuration (.env, ports, secrets)
│   ├── database.py           # SQLite engine, schema migrations, and connection management
│   ├── models.py             # Pydantic data schemas & input validation (Zod equivalent)
│   ├── auth.py               # PBKDF2-SHA256 password hashing, HMAC-SHA256 session tokens, RBAC
│   ├── main.py               # FastAPI application with REST API endpoints & static file serving
│   ├── services/
│   │   ├── workload.py       # Transparent weighted workload algorithm & rebalancing engine
│   │   ├── experiment.py     # Safe 5-day guided workload experiment analyzer
│   │   ├── ai_insights.py    # AI Workload Advisor (Gemini API + Deterministic Fallback)
│   │   └── seed.py           # Multi-industry demo data seeder (School + Healthcare)
│   ├── static/
│   │   ├── index.html        # Enterprise Single-Page Application shell & accessible modals
│   │   ├── app.js            # Reactive UI engine, Canvas chart renderer, English/Tamil i18n
│   │   └── styles.css        # Typography, dark mode palette, high-contrast, PDF print layout
│   └── tests/
│       ├── test_workload.py  # 4 tests: Weighted formulas, overload thresholds, capacity
│       ├── test_priority.py  # 2 tests: Student-critical priority preservation & conflicts
│       ├── test_experiment.py# 1 test: 5-Day experiment synthesis & mini-experiment
│       ├── test_auth_rbac.py # 4 tests: Token tampering, PBKDF2 hashing, private notes
│       ├── test_ai_fallback.py# 3 tests: Deterministic insights, request drafts, disclaimer
│       └── test_routes.py    # 6 tests: API endpoints, RBAC enforcement, task audit logs
├── data/
│   └── fairshift.db          # Persistent SQLite database
├── run.py                    # Server startup script
├── seed.py                   # Demo database re-seeder
├── .env.example              # Environment variables template
├── .env                      # Local environment configuration
└── README.md                 # Complete documentation
```

---

## 🚀 Quick Start (Local Setup on Windows)

FAIRSHIFT runs locally with zero external network or database service dependencies:

### 1. Prerequisites
- Python 3.10+ (Python 3.13 tested)
- Modern web browser (Chrome, Edge, Firefox)

### 2. Run the Application
Open PowerShell or Command Prompt in the project directory:

```powershell
# 1. Initialize and seed the demo database (Oakridge High School & St. Jude Clinic)
python seed.py

# 2. Run the automated test suite (20 unit tests)
python -m unittest discover -s app/tests -p "test_*.py"

# 3. Start the FAIRSHIFT web application
python run.py
```

Open your browser to:
👉 **`http://127.0.0.1:8000`**

---

## 👥 Demo Personas & Logins

You can sign in with any demo account (password: `demo123`), or click the **"Switch Persona"** buttons in the top demo banner to test instant role switching:

### A. Oakridge High School (Education Domain)
| Persona | Email | Role | Workload Pattern |
| :--- | :--- | :--- | :--- |
| **Priya Sharma** | `priya.sharma@oakridge.edu` | **Teacher** | Overloaded (135% capacity); 9.5h after-hours logged out of deep care for Year 11 exam students. |
| **Marcus Chen** | `marcus.chen@oakridge.edu` | **Teacher** | Balanced / Available (70% capacity); Math teacher ready to support departmental duties. |
| **Aisha Rahman** | `aisha.rahman@oakridge.edu` | **Teacher** | Balanced (88% capacity); Science teacher with lab safety commitments. |
| **Sarah Jenkins** | `sarah.jenkins@oakridge.edu` | **Principal (Manager)** | Oversees team workload fairness, reviews conflict requests, and authorizes rebalancing. |
| **David Miller** | `david.miller@oakridge.edu` | **Coordinator** | Manages timetable scheduling, working hours, and operational logistics. |

### B. St. Jude Community Health Clinic (Healthcare Domain)
| Persona | Email | Role | Workload Pattern |
| :--- | :--- | :--- | :--- |
| **Elena Rostova, RN** | `elena.rostova@stjudehealth.org` | **Staff Nurse** | Overloaded (118% capacity); stepped into unplanned emergency triage coverage. |
| **Dr. Aris Thorne** | `aris.thorne@stjudehealth.org` | **Physician** | Balanced clinical patient load. |
| **Maria Patel** | `maria.patel@stjudehealth.org` | **Clinic Admin (Manager)** | Reviews clinical shift allocations and compliance schedules. |

---

## 🌟 6 MVP Features Implemented

### MVP 1: Workload and Extra-Time Tracker
- Records title, description, category (`teaching`, `lesson preparation`, `assessment`, `administration`, `student support`, `meetings`, `extracurricular`, `other`).
- Formally assigned vs voluntarily accepted vs emergency work vs unclear ownership.
- Distinguishes scheduled working hours from after-hours work.
- Records underlying causes: `student_needs`, `urgent_request`, `unclear_ownership`, `quality_concern`, `insufficient_staffing`, `colleague_support`, `personal_choice`.
- **Private Notes**: Author-only reflection notes protected by server-side query isolation.

### MVP 2: Fair Workload Distribution & Transparent Scoring
Transparent weighted scoring formula:
$$\text{Projected Load} = \text{Fixed Commitments} + \sum (\text{Task Hours} \times W_{\text{urgency}}) + (0.3 \times \text{Unplanned Hours})$$

**Priority Weights ($W_{\text{urgency}}$):**
- **Critical (1.5x)**: Student safety, urgent student needs, imminent exam deadlines
- **High (1.25x)**: Essential teaching and curriculum assessment
- **Normal (1.0x)**: Routine departmental responsibilities
- **Deferrable (0.75x)**: Non-urgent tasks that can wait

**Capacity Index Categories:**
- `< 85%`: Available Capacity (healthy, can absorb support)
- `85% - 105%`: Balanced & Sustainable
- `105% - 125%`: Moderate Overload (advisory check-in recommended)
- `> 125%`: Severe Overload Risk (action required to reassign/defer)

### MVP 3: Student-First Priority & Work Boundaries
- Protects critical student safety and imminent examinations from arbitrary reassignment.
- Integrated conflict resolution generator:
  > *"I have [Task A] and [Task B] competing for [Available Hours] of planning time this week. Which should I prioritise, and can either task be safely reassigned or rescheduled?"*
- Teachers submit requests directly to leadership; managers record documented decisions.

### MVP 4: Safe Five-Day Workload Experiment
- Guided 5-day daily observation log.
- Employees record: extra task, time spent, why taken on, feared consequence if it waited, and actual observed outcome in hindsight.
- Synthesizes:
  - Most common root causes of extra work
  - Total extra hours discovered
  - Candidate tasks for delegation, checklists, or rescheduling
  - Fear vs reality outcome reflections
  - **One safe, small next mini-experiment** (e.g. testing structured verbal rubrics instead of exhaustive handwritten notes)
- Employees have complete data agency: can skip questions and permanently delete experiment records.

### MVP 5: Respectful Request and Grievance Channel
- Structured submission for:
  - Prioritisation clarification
  - Operational assistance
  - Non-urgent task reassignment
  - Recurring workload imbalance
  - Confidential concern (routed to authorized handler)
- Full audit event logging for all sensitive managerial actions.

### MVP 6: AI Workload Advisor & Safety Protocols
Four evidence-based advisory modes:
1. **Summarise My Logs**: Synthesizes key time drivers and after-hours patterns.
2. **Draft Respectful Request**: Generates collaborative, non-accusatory messages for manager review.
3. **Review Questions**: Proposes evidence-based questions for 1-on-1 check-ins.
4. **Rebalancing Advisory**: Analyzes team distribution to find safe reallocation opportunities.

**AI Safety Principles:**
- Strict server-side RBAC: only authorized data is accessible.
- **Informed Consent**: Private reflection notes are excluded by default; only included if user explicitly checks the consent toggle.
- **Deterministic Fallback**: If `GEMINI_API_KEY` is not provided, the advisor runs transparent deterministic rules producing structured advisories.
- **Human Review Mandatory**: All recommendations include an explicit disclaimer stating human review and mutual consent are required.

---

## 🌐 Multilingual & Accessibility

- **Languages Supported**: English and Tamil (`தமிழ்`) with instant language switching.
- **High-Contrast Accessibility Mode**: Keyboard-friendly navigation, enhanced borders, and accessible color contrast.
- **Print / PDF Layout**: Clean CSS `@media print` stylesheet removing navigation chrome for high-fidelity printable executive reports.
- **Data Export**: One-click download of personal workload records as standard CSV.

---

## 🧪 Automated Test Suite

Run the full automated test suite:

```powershell
python -m unittest discover -s app/tests -p "test_*.py"
```

### Test Coverage Summary:
- **`test_workload.py`** (4 tests): Verifies weighted formulas, Priya's overload ratio (>100%), Marcus's healthy capacity (<100%), and team distribution sorting.
- **`test_priority.py`** (2 tests): Validates student-critical task preservation and conflict request syntax.
- **`test_experiment.py`** (1 test): Verifies 5-day reflection aggregation, root causes, and safe mini-experiment generation.
- **`test_auth_rbac.py`** (4 tests): Tests PBKDF2 password hashing, HMAC-SHA256 session token verification, token tampering rejection, and private note isolation.
- **`test_ai_fallback.py`** (3 tests): Tests deterministic AI fallback without external API keys, request drafting, and mandatory review disclaimers.
- **`test_routes.py`** (6 tests): Validates API route handlers, Pydantic input models, time log accumulators, task creation, request resolution, and human-approved reassignments.

**Total**: 20 tests passing in < 1 second.

---

## 🔒 Security & Privacy Governance

1. **Authentication**: PBKDF2-HMAC-SHA256 with unique cryptographic salts, stored securely in SQLite.
2. **Session Security**: HMAC-SHA256 signed session tokens with expiration and HttpOnly/SameSite cookie semantics.
3. **Access Control**: Server-side role checks (`teacher`, `manager`, `coordinator`) on every endpoint.
4. **Tenant Isolation**: Every database query enforces `org_id` boundaries.
5. **Private Notes Confidentiality**: `private_note` fields are filtered at the database query level and never transmitted to managers or unauthorized peers.
6. **No Real PII**: Seed data consists entirely of fictional demonstration profiles.

---

## 📄 License & Ethical Usage
FAIRSHIFT is designed as an open, ethical platform for employee well-being and equitable workload management in educational and healthcare institutions.
