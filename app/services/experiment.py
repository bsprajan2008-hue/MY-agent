from typing import Dict, List, Any
from app.database import get_db

def summarize_experiment(experiment_id: str, user_id: str) -> Dict[str, Any]:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM experiments
            WHERE id = ? AND user_id = ?
        """, (experiment_id, user_id))
        exp = cursor.fetchone()
        if not exp:
            return {}

        cursor.execute("""
            SELECT * FROM experiment_entries
            WHERE experiment_id = ? AND user_id = ?
            ORDER BY day_number ASC, created_at ASC
        """, (experiment_id, user_id))
        entries = cursor.fetchall()

    total_extra_hours = sum(e["hours_spent"] for e in entries)
    
    # Count causes
    causes_count = {}
    for e in entries:
        c = e["extra_work_cause"]
        causes_count[c] = causes_count.get(c, 0) + 1

    sorted_causes = sorted(causes_count.items(), key=lambda x: x[1], reverse=True)
    most_common_causes = [{"cause": c, "count": count} for c, count in sorted_causes]

    # Find tasks with unclear ownership
    unclear_ownership_tasks = [
        {"day": e["day_number"], "task": e["task_title"], "hours": e["hours_spent"], "cause": e["extra_work_cause"]}
        for e in entries if "unclear" in e["extra_work_cause"].lower() or e["extra_work_cause"] == "unclear_ownership"
    ]

    # Delegation or rescheduling candidates
    candidate_delegation_tasks = [
        {"day": e["day_number"], "task": e["task_title"], "action": e["candidate_action"], "hours": e["hours_spent"]}
        for e in entries if e["candidate_action"] in ("delegate", "reschedule", "streamline")
    ]

    # Perceived concerns vs actual observed outcomes
    reflections = []
    for e in entries:
        if e.get("perceived_consequence") or e.get("actual_outcome"):
            reflections.append({
                "task": e["task_title"],
                "feared_consequence": e.get("perceived_consequence") or "Fear that student learning would suffer immediately.",
                "observed_outcome": e.get("actual_outcome") or "Task was completed through personal sacrifice; team was unaware of the strain.",
                "candidate_action": e["candidate_action"]
            })

    # Propose one small, safe next experiment
    primary_cause = sorted_causes[0][0] if sorted_causes else "routine overload"
    if "student" in primary_cause.lower() or "quality" in primary_cause.lower():
        safe_next_experiment = (
            "Safe Mini-Experiment: Next week, for one non-exam assessment, test providing structured verbal feedback "
            "or a rubric checklist instead of exhaustive handwritten notes, saving an estimated 2-3 hours while testing "
            "if student understanding remains equivalent."
        )
    elif "unclear" in primary_cause.lower() or "staffing" in primary_cause.lower():
        safe_next_experiment = (
            "Safe Mini-Experiment: Next week, before starting an unassigned administrative task, spend 2 minutes asking "
            "in the department channel: 'Is there a designated owner for this task, or can we split the 45-minute setup?'"
        )
    else:
        safe_next_experiment = (
            "Safe Mini-Experiment: Set an intentional 15-minute boundary on non-critical end-of-day wrap-up on Tuesday and Thursday, "
            "recording whether any urgent priority is genuinely affected."
        )

    summary = {
        "experiment_id": experiment_id,
        "status": exp["status"],
        "total_days_logged": len(set(e["day_number"] for e in entries)),
        "total_entries": len(entries),
        "total_extra_hours_recorded": round(total_extra_hours, 1),
        "most_common_causes": most_common_causes,
        "unclear_ownership_tasks": unclear_ownership_tasks,
        "candidate_delegation_tasks": candidate_delegation_tasks,
        "reflections": reflections,
        "safe_next_experiment": safe_next_experiment,
        "tentative_pattern_disclaimer": "These findings are observational reflection patterns based on your 5-day logs, not clinical or formal performance diagnoses. Safety-critical and legally required duties must always be maintained."
    }

    return summary
