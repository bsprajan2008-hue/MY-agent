import uuid
from datetime import datetime, timedelta
from app.database import get_db, init_db
from app.auth import hash_password

def seed_database():
    init_db()
    with get_db() as conn:
        cursor = conn.cursor()

        # Clean existing demo tables
        cursor.execute("DELETE FROM experiment_entries;")
        cursor.execute("DELETE FROM experiments;")
        cursor.execute("DELETE FROM workload_requests;")
        cursor.execute("DELETE FROM time_logs;")
        cursor.execute("DELETE FROM reassignment_records;")
        cursor.execute("DELETE FROM audit_events;")
        cursor.execute("DELETE FROM tasks;")
        cursor.execute("DELETE FROM users;")
        cursor.execute("DELETE FROM departments;")
        cursor.execute("DELETE FROM organisation_settings;")
        cursor.execute("DELETE FROM organisations;")

        # ----------------------------------------------------
        # 1. ORGANISATION 1: Oakridge High School (School)
        # ----------------------------------------------------
        org_school_id = "org-oakridge-high"
        cursor.execute("""
            INSERT INTO organisations (id, name, industry)
            VALUES (?, ?, ?)
        """, (org_school_id, "Oakridge High School", "school"))

        cursor.execute("""
            INSERT INTO organisation_settings (id, org_id, standard_weekly_hours, enable_anonymous_feedback_threshold, default_language)
            VALUES (?, ?, ?, ?, ?)
        """, (str(uuid.uuid4()), org_school_id, 35.0, 3, "en"))

        # Departments
        dept_english = "dept-oak-english"
        dept_math = "dept-oak-math"
        dept_science = "dept-oak-science"
        dept_admin = "dept-oak-admin"

        cursor.execute("INSERT INTO departments (id, org_id, name) VALUES (?, ?, ?)", (dept_english, org_school_id, "English & Humanities"))
        cursor.execute("INSERT INTO departments (id, org_id, name) VALUES (?, ?, ?)", (dept_math, org_school_id, "Mathematics & Computing"))
        cursor.execute("INSERT INTO departments (id, org_id, name) VALUES (?, ?, ?)", (dept_science, org_school_id, "Sciences"))
        cursor.execute("INSERT INTO departments (id, org_id, name) VALUES (?, ?, ?)", (dept_admin, org_school_id, "Administration & Student Care"))

        # Users
        pw = hash_password("demo123")

        # Priya Sharma (Teacher - Experiencing overwork out of dedication)
        user_priya_id = "user-priya-sharma"
        cursor.execute("""
            INSERT INTO users (id, org_id, department_id, name, email, password_hash, role, avatar_url, weekly_target_hours, contracted_teaching_periods, preferred_language)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_priya_id, org_school_id, dept_english, "Priya Sharma", "priya.sharma@oakridge.edu", pw, "teacher", "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=150", 35.0, 22, "en"))

        # Marcus Chen (Teacher - Healthy capacity, available to support)
        user_marcus_id = "user-marcus-chen"
        cursor.execute("""
            INSERT INTO users (id, org_id, department_id, name, email, password_hash, role, avatar_url, weekly_target_hours, contracted_teaching_periods, preferred_language)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_marcus_id, org_school_id, dept_math, "Marcus Chen", "marcus.chen@oakridge.edu", pw, "teacher", "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150", 35.0, 18, "en"))

        # Aisha Rahman (Teacher - Balanced workload)
        user_aisha_id = "user-aisha-rahman"
        cursor.execute("""
            INSERT INTO users (id, org_id, department_id, name, email, password_hash, role, avatar_url, weekly_target_hours, contracted_teaching_periods, preferred_language)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_aisha_id, org_school_id, dept_science, "Aisha Rahman", "aisha.rahman@oakridge.edu", pw, "teacher", "https://images.unsplash.com/photo-1580489944761-15a19d654956?w=150", 35.0, 20, "en"))

        # Sarah Jenkins (Principal / Manager)
        user_sarah_id = "user-sarah-jenkins"
        cursor.execute("""
            INSERT INTO users (id, org_id, department_id, name, email, password_hash, role, avatar_url, weekly_target_hours, contracted_teaching_periods, preferred_language)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_sarah_id, org_school_id, dept_admin, "Sarah Jenkins", "sarah.jenkins@oakridge.edu", pw, "manager", "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=150", 40.0, 4, "en"))

        # David Miller (Staffing & Timetable Coordinator)
        user_david_id = "user-david-miller"
        cursor.execute("""
            INSERT INTO users (id, org_id, department_id, name, email, password_hash, role, avatar_url, weekly_target_hours, contracted_teaching_periods, preferred_language)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_david_id, org_school_id, dept_admin, "David Miller", "david.miller@oakridge.edu", pw, "coordinator", "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150", 37.5, 8, "en"))

        # Tasks for Oakridge High School
        today = datetime.now()
        due_tomorrow = (today + timedelta(days=1)).strftime("%Y-%m-%d")
        due_in_3_days = (today + timedelta(days=3)).strftime("%Y-%m-%d")
        due_next_week = (today + timedelta(days=7)).strftime("%Y-%m-%d")
        due_in_2_weeks = (today + timedelta(days=14)).strftime("%Y-%m-%d")

        # Priya's Tasks (Demonstrating heavy load, voluntary assessment & lesson prep for student benefit)
        p_tasks = [
            (
                "task-priya-1", org_school_id, dept_english, "Grade Year 11 Diagnostic Mock Essays",
                "Grading 64 comprehensive practice essays with personalized line-by-line developmental feedback before state exams.",
                "assessment", user_priya_id, user_sarah_id, "[]", 8.0, 9.5, due_tomorrow, "critical", "in_progress", 0,
                "voluntarily_taken", 0, "student_needs", "I worry students will fail Section B unless each essay has detailed notes."
            ),
            (
                "task-priya-2", org_school_id, dept_english, "Year 9 Differentiated Lesson Material Prep",
                "Creating tiered reading comprehension worksheets for mixed-ability learners.",
                "lesson preparation", user_priya_id, user_sarah_id, "[]", 6.0, 4.0, due_in_3_days, "high", "in_progress", 0,
                "voluntarily_taken", 1, "student_needs", "Standard textbook leaves struggling readers behind without scaffolded slides."
            ),
            (
                "task-priya-3", org_school_id, dept_english, "Literacy Remediation Catch-up Clinic",
                "Voluntary after-school reading intervention for 12 struggling readers.",
                "student support", user_priya_id, user_priya_id, "[]", 4.0, 3.5, due_next_week, "high", "in_progress", 1,
                "voluntarily_taken", 0, "student_needs", "Essential for students who missed foundational literacy periods."
            ),
            (
                "task-priya-4", org_school_id, dept_english, "Department Textbook Inventory & Condition Audit",
                "Count and log physical textbook barcodes across classrooms 301-306.",
                "administration", user_priya_id, user_david_id, "[]", 4.5, 0.0, due_in_2_weeks, "deferrable", "pending", 0,
                "formally_assigned", 1, "none", "Non-urgent admin task that could easily wait until term break."
            ),
            (
                "task-priya-5", org_school_id, dept_english, "Staff Wellbeing & Pastoral Care Meeting",
                "Weekly pastoral coordination meeting for designated form tutors.",
                "meetings", user_priya_id, user_sarah_id, "[]", 2.0, 2.0, due_in_3_days, "normal", "in_progress", 1,
                "formally_assigned", 1, "none", None
            ),
            (
                "task-priya-6", org_school_id, dept_english, "English Drama Club Rehearsal Coordination",
                "Facilitating after-school stage rehearsals without a designated co-advisor.",
                "extracurricular", user_priya_id, None, "[]", 3.5, 3.5, due_next_week, "normal", "in_progress", 1,
                "unclear_owner", 0, "unclear_ownership", "Nobody else stepped forward to supervise the club so I felt compelled."
            )
        ]

        for t in p_tasks:
            cursor.execute("""
                INSERT INTO tasks (
                    id, org_id, department_id, title, description, category,
                    assigned_to_id, assigned_by_id, collaborators, estimated_duration_hours,
                    actual_duration_hours, due_date, priority, status, is_recurring,
                    assignment_type, completed_within_scheduled_hours, extra_work_reason, private_note
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, t)

        # Marcus's Tasks (Healthy capacity, math teacher ready to help)
        m_tasks = [
            (
                "task-marcus-1", org_school_id, dept_math, "Year 10 Algebra Problem Set Review",
                "Standard weekly homework check and solution rubric distribution.",
                "assessment", user_marcus_id, user_sarah_id, "[]", 3.0, 2.5, due_in_3_days, "normal", "in_progress", 1,
                "formally_assigned", 1, "none", None
            ),
            (
                "task-marcus-2", org_school_id, dept_math, "Calculus Lesson Plans Week 6",
                "Prepare interactive slides and Desmos graph simulations.",
                "lesson preparation", user_marcus_id, user_sarah_id, "[]", 4.0, 3.0, due_next_week, "normal", "in_progress", 0,
                "formally_assigned", 1, "none", None
            ),
            (
                "task-marcus-3", org_school_id, dept_math, "Faculty Tech Support & Smartboard Calibration",
                "Routine check of interactive projectors in wing B.",
                "administration", user_marcus_id, user_david_id, "[]", 2.0, 1.5, due_in_2_weeks, "deferrable", "pending", 0,
                "formally_assigned", 1, "none", "Available to assist colleagues with digital workflow automations."
            )
        ]
        for t in m_tasks:
            cursor.execute("""
                INSERT INTO tasks (
                    id, org_id, department_id, title, description, category,
                    assigned_to_id, assigned_by_id, collaborators, estimated_duration_hours,
                    actual_duration_hours, due_date, priority, status, is_recurring,
                    assignment_type, completed_within_scheduled_hours, extra_work_reason, private_note
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, t)

        # Aisha's Tasks (Balanced science teacher)
        a_tasks = [
            (
                "task-aisha-1", org_school_id, dept_science, "Chemistry Lab Chemical Inventory & Safety Log",
                "Mandatory quarterly hazardous chemical audit as per regional school regulations.",
                "administration", user_aisha_id, user_sarah_id, "[]", 5.0, 4.0, due_in_3_days, "critical", "in_progress", 0,
                "formally_assigned", 1, "none", None
            ),
            (
                "task-aisha-2", org_school_id, dept_science, "Biology Field Trip Permission Forms Collection",
                "Collate parent signatures and student dietary requirements for marsh ecology trip.",
                "student support", user_aisha_id, user_david_id, "[]", 3.0, 2.0, due_next_week, "normal", "in_progress", 0,
                "formally_assigned", 1, "none", None
            )
        ]
        for t in a_tasks:
            cursor.execute("""
                INSERT INTO tasks (
                    id, org_id, department_id, title, description, category,
                    assigned_to_id, assigned_by_id, collaborators, estimated_duration_hours,
                    actual_duration_hours, due_date, priority, status, is_recurring,
                    assignment_type, completed_within_scheduled_hours, extra_work_reason, private_note
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, t)

        # Time Logs for Priya (Past 7 days showing 9.5 hours of after-hours work)
        p_logs = [
            ("log-p-1", org_school_id, "task-priya-1", user_priya_id, (today - timedelta(days=1)).strftime("%Y-%m-%d"), 3.5, 1, "student_needs", "Grading essay drafts at home until 9:30 PM"),
            ("log-p-2", org_school_id, "task-priya-1", user_priya_id, (today - timedelta(days=2)).strftime("%Y-%m-%d"), 3.0, 1, "student_needs", "Annotating grammar rubrics over weekend"),
            ("log-p-3", org_school_id, "task-priya-2", user_priya_id, (today - timedelta(days=3)).strftime("%Y-%m-%d"), 2.0, 0, "routine", "During scheduled planning block"),
            ("log-p-4", org_school_id, "task-priya-3", user_priya_id, (today - timedelta(days=4)).strftime("%Y-%m-%d"), 2.5, 1, "student_needs", "Staying late with ESL students"),
            ("log-p-5", org_school_id, "task-priya-5", user_priya_id, (today - timedelta(days=5)).strftime("%Y-%m-%d"), 2.0, 0, "routine", "Pastoral team session"),
            ("log-p-6", org_school_id, "task-priya-6", user_priya_id, (today - timedelta(days=6)).strftime("%Y-%m-%d"), 2.0, 1, "unclear_ownership", "Supervising auditorium drama practice")
        ]
        for l in p_logs:
            cursor.execute("""
                INSERT INTO time_logs (id, org_id, task_id, user_id, log_date, duration_hours, is_after_hours, reason, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, l)

        # Marcus's Logs
        m_logs = [
            ("log-m-1", org_school_id, "task-marcus-1", user_marcus_id, (today - timedelta(days=2)).strftime("%Y-%m-%d"), 2.5, 0, "routine", "During planning period"),
            ("log-m-2", org_school_id, "task-marcus-2", user_marcus_id, (today - timedelta(days=4)).strftime("%Y-%m-%d"), 3.0, 0, "routine", "Lesson prep completed before 4:00 PM")
        ]
        for l in m_logs:
            cursor.execute("""
                INSERT INTO time_logs (id, org_id, task_id, user_id, log_date, duration_hours, is_after_hours, reason, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, l)

        # Workload Requests (Student-First Priority Workflow Example)
        cursor.execute("""
            INSERT INTO workload_requests (
                id, org_id, user_id, assigned_to_manager_id, request_type,
                task_a_id, task_b_id, available_time_hours, message,
                access_scope, status, manager_response, resolved_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "req-priya-1", org_school_id, user_priya_id, user_sarah_id, "clarification",
            "task-priya-1", "task-priya-4", 4.0,
            "I have Grade Year 11 Diagnostic Mock Essays (critical for upcoming exam preparation) and Department Textbook Inventory (deferrable routine administration) competing for my available planning block of 4 hours this Thursday. Which should I prioritise, and can the textbook inventory be reassigned or deferred to term break?",
            "manager_only", "resolved",
            "Priya, excellent call. Please prioritize the Year 11 Diagnostic Essays without question. I have deferred the textbook inventory until next month, and David Miller will arrange for an administrative assistant to assist. Thank you for flagging this proactively.",
            (today - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        ))

        # 5-Day Guided Experiment for Priya
        exp_id = "exp-priya-oct"
        cursor.execute("""
            INSERT INTO experiments (id, org_id, user_id, start_date, end_date, status, summary_json)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            exp_id, org_school_id, user_priya_id,
            (today - timedelta(days=5)).strftime("%Y-%m-%d"),
            today.strftime("%Y-%m-%d"),
            "completed", None
        ))

        exp_entries = [
            (str(uuid.uuid4()), exp_id, user_priya_id, 1, "Personalized handwriting commentary on 32 practice quizzes", "assessment", 2.5, "student_needs", "Worry students won't improve unless I write full paragraph feedback on every page.", "Students quickly read the overall score; many did not read full margin paragraphs.", "streamline"),
            (str(uuid.uuid4()), exp_id, user_priya_id, 2, "Reorganizing shared reading cupboard", "administration", 1.5, "unclear_ownership", "Worry books will go missing if not sorted immediately.", "No classes needed the cupboard on Tuesday; task could have waited.", "delegate"),
            (str(uuid.uuid4()), exp_id, user_priya_id, 3, "Hand-making differentiated graphic organizers", "lesson preparation", 2.0, "quality_concern", "Fear that standard worksheets are insufficient for visual learners.", "Students found the visual diagrams very helpful, but a reusable digital template would save 1.5h next time.", "streamline"),
            (str(uuid.uuid4()), exp_id, user_priya_id, 4, "Drafting individual parent catch-up emails", "student support", 2.0, "student_needs", "Worry parents feel disconnected before parent-teacher conferences.", "Parents appreciated it, but an aggregated bi-weekly newsletter bullet would convey the same key points.", "reschedule"),
            (str(uuid.uuid4()), exp_id, user_priya_id, 5, "Staying behind to pack up stage props after drama club", "extracurricular", 1.5, "unclear_ownership", "Nobody else was in the auditorium to lock up.", "Student council leaders could have been entrusted with checklist sign-off.", "delegate")
        ]
        for ee in exp_entries:
            cursor.execute("""
                INSERT INTO experiment_entries (
                    id, experiment_id, user_id, day_number, task_title, category,
                    hours_spent, extra_work_cause, perceived_consequence, actual_outcome, candidate_action
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, ee)

        # Audit Events
        cursor.execute("""
            INSERT INTO audit_events (id, org_id, actor_id, actor_role, action, target_type, target_id, details_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            str(uuid.uuid4()), org_school_id, user_sarah_id, "manager", "resolve_workload_request", "workload_request", "req-priya-1",
            '{"action": "Approved deferral of Department Textbook Inventory for Priya Sharma"}'
        ))


        # ----------------------------------------------------
        # 2. ORGANISATION 2: St. Jude Community Clinic (Healthcare)
        # ----------------------------------------------------
        org_health_id = "org-st-jude-clinic"
        cursor.execute("""
            INSERT INTO organisations (id, name, industry)
            VALUES (?, ?, ?)
        """, (org_health_id, "St. Jude Community Health Clinic", "healthcare"))

        cursor.execute("""
            INSERT INTO organisation_settings (id, org_id, standard_weekly_hours, enable_anonymous_feedback_threshold, default_language)
            VALUES (?, ?, ?, ?, ?)
        """, (str(uuid.uuid4()), org_health_id, 37.5, 3, "en"))

        dept_nursing = "dept-health-nursing"
        dept_physicians = "dept-health-physicians"
        dept_clinic_admin = "dept-health-admin"

        cursor.execute("INSERT INTO departments (id, org_id, name) VALUES (?, ?, ?)", (dept_nursing, org_health_id, "Inpatient & Urgent Nursing"))
        cursor.execute("INSERT INTO departments (id, org_id, name) VALUES (?, ?, ?)", (dept_physicians, org_health_id, "Medical Staff"))
        cursor.execute("INSERT INTO departments (id, org_id, name) VALUES (?, ?, ?)", (dept_clinic_admin, org_health_id, "Clinical Operations & Compliance"))

        # Users
        user_elena_id = "user-elena-rostova"
        cursor.execute("""
            INSERT INTO users (id, org_id, department_id, name, email, password_hash, role, avatar_url, weekly_target_hours, contracted_teaching_periods, preferred_language)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_elena_id, org_health_id, dept_nursing, "Elena Rostova, RN", "elena.rostova@stjudehealth.org", pw, "teacher", "https://images.unsplash.com/photo-1594824813637-293623f99d63?w=150", 37.5, 12, "en"))

        user_aris_id = "user-aris-thorne"
        cursor.execute("""
            INSERT INTO users (id, org_id, department_id, name, email, password_hash, role, avatar_url, weekly_target_hours, contracted_teaching_periods, preferred_language)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_aris_id, org_health_id, dept_physicians, "Dr. Aris Thorne", "aris.thorne@stjudehealth.org", pw, "teacher", "https://images.unsplash.com/photo-1622253692010-333f2da6031d?w=150", 40.0, 10, "en"))

        user_maria_id = "user-maria-patel"
        cursor.execute("""
            INSERT INTO users (id, org_id, department_id, name, email, password_hash, role, avatar_url, weekly_target_hours, contracted_teaching_periods, preferred_language)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_maria_id, org_health_id, dept_clinic_admin, "Maria Patel", "maria.patel@stjudehealth.org", pw, "manager", "https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?w=150", 40.0, 0, "en"))

        # Healthcare Tasks
        h_tasks = [
            ("task-elena-1", org_health_id, dept_nursing, "Post-Operative Patient Vitals & Medication Handover", "Administer prescribed IV antibiotics and document vitals for 8 recovery patients.", "student support", user_elena_id, user_maria_id, "[]", 6.0, 6.0, due_tomorrow, "critical", "in_progress", 1, "formally_assigned", 1, "none", "Critical patient safety protocol"),
            ("task-elena-2", org_health_id, dept_nursing, "Unplanned Emergency Triage Shift Coverage", "Stepping in to cover 3 hours of triage desk due to surge in urgent respiratory cases.", "administration", user_elena_id, user_maria_id, "[]", 3.5, 3.5, due_tomorrow, "high", "in_progress", 0, "emergency_work", 0, "insufficient_staffing", "Patient triage could not be left unattended"),
            ("task-elena-3", org_health_id, dept_nursing, "Quarterly Sharps Disposal & Sterilization Logs", "Non-urgent compliance cataloging for utility wing.", "administration", user_elena_id, user_maria_id, "[]", 4.0, 0.0, due_in_2_weeks, "deferrable", "pending", 0, "formally_assigned", 1, "none", "Routine compliance check that can be rescheduled")
        ]
        for t in h_tasks:
            cursor.execute("""
                INSERT INTO tasks (
                    id, org_id, department_id, title, description, category,
                    assigned_to_id, assigned_by_id, collaborators, estimated_duration_hours,
                    actual_duration_hours, due_date, priority, status, is_recurring,
                    assignment_type, completed_within_scheduled_hours, extra_work_reason, private_note
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, t)

if __name__ == "__main__":
    seed_database()
    print("FAIRSHIFT database seeded successfully with School and Healthcare demo datasets.")
