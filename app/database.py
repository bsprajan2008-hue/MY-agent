import sqlite3
import json
from contextlib import contextmanager
from app.config import DATABASE_PATH

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@contextmanager
def get_db():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = dict_factory
    conn.execute("PRAGMA foreign_keys = ON;")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        cursor = conn.cursor()
        
        # 1. Organisations
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS organisations (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            industry TEXT NOT NULL DEFAULT 'school',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # 2. Departments
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS departments (
            id TEXT PRIMARY KEY,
            org_id TEXT NOT NULL,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (org_id) REFERENCES organisations(id) ON DELETE CASCADE
        );
        """)

        # 3. Users
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            org_id TEXT NOT NULL,
            department_id TEXT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('teacher', 'manager', 'coordinator')),
            avatar_url TEXT,
            weekly_target_hours REAL DEFAULT 35.0,
            contracted_teaching_periods INTEGER DEFAULT 22,
            preferred_language TEXT DEFAULT 'en',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (org_id) REFERENCES organisations(id) ON DELETE CASCADE,
            FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE SET NULL
        );
        """)

        # 4. Tasks
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY,
            org_id TEXT NOT NULL,
            department_id TEXT,
            title TEXT NOT NULL,
            description TEXT,
            category TEXT NOT NULL CHECK(category IN ('teaching', 'lesson preparation', 'assessment', 'administration', 'student support', 'meetings', 'extracurricular', 'other')),
            assigned_to_id TEXT,
            assigned_by_id TEXT,
            collaborators TEXT, -- JSON array of user IDs
            estimated_duration_hours REAL NOT NULL DEFAULT 1.0,
            actual_duration_hours REAL NOT NULL DEFAULT 0.0,
            due_date TEXT NOT NULL,
            priority TEXT NOT NULL CHECK(priority IN ('critical', 'high', 'normal', 'deferrable')),
            status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending', 'in_progress', 'completed', 'delegated', 'cancelled')),
            is_recurring INTEGER DEFAULT 0,
            assignment_type TEXT NOT NULL DEFAULT 'formally_assigned' CHECK(assignment_type IN ('formally_assigned', 'voluntarily_taken', 'emergency_work', 'unclear_owner')),
            completed_within_scheduled_hours INTEGER DEFAULT 1,
            extra_work_reason TEXT DEFAULT 'none',
            private_note TEXT, -- strictly visible only to author/assignee
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (org_id) REFERENCES organisations(id) ON DELETE CASCADE,
            FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE SET NULL,
            FOREIGN KEY (assigned_to_id) REFERENCES users(id) ON DELETE SET NULL,
            FOREIGN KEY (assigned_by_id) REFERENCES users(id) ON DELETE SET NULL
        );
        """)

        # 5. Time Logs
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS time_logs (
            id TEXT PRIMARY KEY,
            org_id TEXT NOT NULL,
            task_id TEXT,
            user_id TEXT NOT NULL,
            log_date TEXT NOT NULL,
            duration_hours REAL NOT NULL,
            is_after_hours INTEGER DEFAULT 0,
            reason TEXT DEFAULT 'routine',
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (org_id) REFERENCES organisations(id) ON DELETE CASCADE,
            FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE SET NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """)

        # 6. Workload Requests & Concerns
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS workload_requests (
            id TEXT PRIMARY KEY,
            org_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            assigned_to_manager_id TEXT,
            request_type TEXT NOT NULL CHECK(request_type IN ('clarification', 'assistance', 'reassignment', 'recurring_imbalance', 'confidential_concern')),
            task_a_id TEXT,
            task_b_id TEXT,
            available_time_hours REAL,
            message TEXT NOT NULL,
            access_scope TEXT DEFAULT 'manager_only' CHECK(access_scope IN ('manager_only', 'designated_confidential_handler', 'coordinator')),
            status TEXT DEFAULT 'submitted' CHECK(status IN ('submitted', 'under_review', 'resolved', 'reassigned')),
            manager_response TEXT,
            resolved_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (org_id) REFERENCES organisations(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (assigned_to_manager_id) REFERENCES users(id) ON DELETE SET NULL,
            FOREIGN KEY (task_a_id) REFERENCES tasks(id) ON DELETE SET NULL,
            FOREIGN KEY (task_b_id) REFERENCES tasks(id) ON DELETE SET NULL
        );
        """)

        # 7. Five-Day Guided Experiments
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS experiments (
            id TEXT PRIMARY KEY,
            org_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT,
            status TEXT DEFAULT 'active' CHECK(status IN ('active', 'completed', 'archived')),
            summary_json TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (org_id) REFERENCES organisations(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """)

        # 8. Experiment Entries (Day 1 - 5)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS experiment_entries (
            id TEXT PRIMARY KEY,
            experiment_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            day_number INTEGER NOT NULL CHECK(day_number BETWEEN 1 AND 5),
            task_title TEXT NOT NULL,
            category TEXT NOT NULL,
            hours_spent REAL NOT NULL,
            extra_work_cause TEXT NOT NULL,
            perceived_consequence TEXT,
            actual_outcome TEXT,
            candidate_action TEXT DEFAULT 'keep' CHECK(candidate_action IN ('delegate', 'reschedule', 'streamline', 'keep')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (experiment_id) REFERENCES experiments(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """)

        # 9. Audit Events
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_events (
            id TEXT PRIMARY KEY,
            org_id TEXT NOT NULL,
            actor_id TEXT NOT NULL,
            actor_role TEXT NOT NULL,
            action TEXT NOT NULL,
            target_type TEXT NOT NULL,
            target_id TEXT NOT NULL,
            details_json TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (org_id) REFERENCES organisations(id) ON DELETE CASCADE,
            FOREIGN KEY (actor_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """)

        # 10. Reassignment Records
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS reassignment_records (
            id TEXT PRIMARY KEY,
            org_id TEXT NOT NULL,
            task_id TEXT NOT NULL,
            previous_user_id TEXT,
            new_user_id TEXT NOT NULL,
            reassigned_by_id TEXT NOT NULL,
            reason TEXT NOT NULL,
            approved_by_human INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (org_id) REFERENCES organisations(id) ON DELETE CASCADE,
            FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE,
            FOREIGN KEY (previous_user_id) REFERENCES users(id) ON DELETE SET NULL,
            FOREIGN KEY (new_user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (reassigned_by_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """)

        # 11. Organisation Settings
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS organisation_settings (
            id TEXT PRIMARY KEY,
            org_id TEXT UNIQUE NOT NULL,
            standard_weekly_hours REAL DEFAULT 35.0,
            enable_anonymous_feedback_threshold INTEGER DEFAULT 5,
            default_language TEXT DEFAULT 'en',
            working_days_json TEXT DEFAULT '["Monday","Tuesday","Wednesday","Thursday","Friday"]',
            notifications_json TEXT DEFAULT '{"email_reminders":true,"weekly_digest":true}',
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (org_id) REFERENCES organisations(id) ON DELETE CASCADE
        );
        """)

        # Indexes for fast querying & security isolation
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_org_user ON tasks(org_id, assigned_to_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_status_due ON tasks(status, due_date);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_timelogs_org_user_date ON time_logs(org_id, user_id, log_date);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_requests_org_user ON workload_requests(org_id, user_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_audit_org_created ON audit_events(org_id, created_at);")

if __name__ == "__main__":
    init_db()
    print("FAIRSHIFT database initialized successfully.")
