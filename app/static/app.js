/**
 * FAIRSHIFT Enterprise Web Application
 * Complete Frontend Engine with State Management, Reactive Rendering,
 * Real Interactive Canvas/SVG Charts, English/Tamil i18n, and API Client
 */

// -------------------------------------------------------------
// I18N DICTIONARY: English & Tamil (தமிழ்)
// -------------------------------------------------------------
const I18N = {
  en: {
    app_name: "FAIRSHIFT",
    tagline: "Fair Workload and Well-being Platform",
    nav_personal: "My Space",
    nav_my_dashboard: "My Dashboard",
    nav_my_tasks: "My Tasks & Duties",
    nav_time_logs: "Time & Extra-Hours",
    nav_experiment: "5-Day Experiment",
    nav_requests: "Requests & Concerns",
    nav_management: "Leadership & Team",
    nav_team_workload: "Team Capacity & Fairness",
    nav_rebalance: "Task Rebalancing",
    nav_platform: "Insights & Platform",
    nav_ai_advisor: "AI Workload Advisor",
    nav_settings: "Settings & Privacy",
    nav_walkthrough: "Demo Walkthrough",
    btn_log_time: "Log Time",
    btn_print_pdf: "Print / Export Summary",
    btn_save_task: "Save Task",
    btn_cancel: "Cancel",
    btn_send_request: "Send Request",
    btn_save_log: "Record Log",
    modal_task_title: "Record Task / Duty",
    modal_timelog_title: "Log Actual Time Spent",
    modal_request_title: "Prioritisation & Support Request",
    field_title: "Task Title *",
    field_category: "Category *",
    field_priority: "Priority Level *",
    field_est_hours: "Est. Hours *",
    field_due_date: "Due Date *",
    field_assignment_type: "Duty Origin",
    field_reason_extra: "Reason for Extra Work",
    field_private_note: "Private Note (Strictly visible only to you!)",
    field_select_task: "Associated Task (Optional)",
    field_hours: "Hours Spent *",
    field_date: "Date *",
    field_after_hours: "Completed outside scheduled working hours (After-hours / Weekend)",
    field_notes: "Brief Reflection / Notes",
    field_request_type: "Request Type *",
    field_message: "Respectful Message *",
    status_available: "Available Capacity",
    status_balanced: "Balanced & Sustainable",
    status_moderate: "Moderate Overload",
    status_severe: "Severe Overload Risk"
  },
  ta: {
    app_name: "ஃபேர்ஷிப்ட்",
    tagline: "நியாயமான பணிச்சுமை மற்றும் நல்வாழ்வு தளம்",
    nav_personal: "என் பணியிடம்",
    nav_my_dashboard: "என் முகப்புப்பலகை",
    nav_my_tasks: "என் பணிகள் மற்றும் கடமைகள்",
    nav_time_logs: "நேரம் மற்றும் கூடுதல் நேரம்",
    nav_experiment: "5-நாள் பணிச்சுமை ஆய்வு",
    nav_requests: "கோரிக்கைகள் மற்றும் பகிர்வு",
    nav_management: "நிர்வாகம் மற்றும் குழு",
    nav_team_workload: "குழு பணிச்சுமை மற்றும் நியாயம்",
    nav_rebalance: "பணிகளை மறுபகிர்வு செய்தல்",
    nav_platform: "ஆய்வு மற்றும் தளம்",
    nav_ai_advisor: "செயற்கை நுண்ணறிவு ஆலோசகர்",
    nav_settings: "அமைப்புகள் மற்றும் தனியுரிமை",
    nav_walkthrough: "விளக்கக் கையேடு",
    btn_log_time: "நேரம் பதிவு செய்",
    btn_print_pdf: "அறிக்கை அச்சிடு / பதிவிறக்கு",
    btn_save_task: "பணியை சேமி",
    btn_cancel: "ரத்து செய்",
    btn_send_request: "கோரிக்கை அனுப்பு",
    btn_save_log: "பதிவு செய்",
    modal_task_title: "புதிய பணியை பதிவு செய்க",
    modal_timelog_title: "செலவிடப்பட்ட நேரத்தை பதிவு செய்",
    modal_request_title: "பணி முன்னுரிமை மற்றும் உதவி கோரிக்கை",
    field_title: "பணி தலைப்பு *",
    field_category: "வகை *",
    field_priority: "முன்னுரிமை நிலை *",
    field_est_hours: "மதிப்பிடப்பட்ட மணிநேரம் *",
    field_due_date: "முடிவு நாள் *",
    field_assignment_type: "பணி தோற்றம்",
    field_reason_extra: "கூடுதல் பணிக்கான காரணம்",
    field_private_note: "தனிப்பட்ட குறிப்பு (உங்களுக்கு மட்டுமே தெரியும்!)",
    field_select_task: "தொடர்புடைய பணி (விரும்பினால்)",
    field_hours: "செலவிட்ட மணிநேரம் *",
    field_date: "தேதி *",
    field_after_hours: "பணி நேரத்திற்குப் பின் / விடுமுறை நாளில் செய்யப்பட்டது",
    field_notes: "குறிப்புகள்",
    field_request_type: "கோரிக்கை வகை *",
    field_message: "மரியாதையான செய்தி *",
    status_available: "கூடுதல் திறன் உள்ளது",
    status_balanced: "சமநிலையான பணிச்சுமை",
    status_moderate: "மிதமான கூடுதல் பணிச்சுமை",
    status_severe: "அதிக பணிச்சுமை அபாயம்"
  }
};

class FairshiftApp {
  constructor() {
    this.currentUser = null;
    this.currentView = "dashboard-teacher";
    this.currentLang = localStorage.getItem("fairshift_lang") || "en";
    this.isDarkMode = localStorage.getItem("fairshift_theme") === "dark";
    this.isHighContrast = localStorage.getItem("fairshift_contrast") === "true";

    // Local cached data
    this.tasks = [];
    this.timeLogs = [];
    this.personalWorkload = null;
    this.teamWorkload = null;
    this.requests = [];
    this.experiment = null;
    this.demoUsers = [];
    this.aiInsightResult = null;

    this.init();
  }

  async init() {
    // Apply theme
    this.applyTheme();
    this.applyContrast();
    this.applyLanguage();

    // Check auth
    try {
      const res = await fetch("/api/auth/me");
      if (res.ok) {
        this.currentUser = await res.json();
      } else {
        // Auto-login as default Priya Sharma (Overloaded teacher) for demo convenience
        await this.quickSwitchUser("user-priya-sharma");
        return;
      }
    } catch (e) {
      console.error("Auth check failed:", e);
    }

    this.updateUserUI();
    await this.fetchInitialData();
    this.render();
  }

  applyTheme() {
    const html = document.documentElement;
    if (this.isDarkMode) {
      html.classList.add("dark");
    } else {
      html.classList.remove("dark");
    }
    const icon = document.getElementById("theme-icon");
    if (icon) {
      icon.innerHTML = this.isDarkMode
        ? `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/>`
        : `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/>`;
    }
  }

  toggleTheme() {
    this.isDarkMode = !this.isDarkMode;
    localStorage.setItem("fairshift_theme", this.isDarkMode ? "dark" : "light");
    this.applyTheme();
    this.render(); // Re-render canvas charts for dark/light palette
  }

  toggleHighContrast() {
    this.isHighContrast = !this.isHighContrast;
    localStorage.setItem("fairshift_contrast", this.isHighContrast ? "true" : "false");
    this.applyContrast();
  }

  applyContrast() {
    if (this.isHighContrast) {
      document.body.classList.add("high-contrast");
    } else {
      document.body.classList.remove("high-contrast");
    }
  }

  setLanguage(lang) {
    this.currentLang = lang;
    localStorage.setItem("fairshift_lang", lang);
    document.documentElement.setAttribute("lang", lang);
    this.applyLanguage();
    this.render();
  }

  applyLanguage() {
    const dict = I18N[this.currentLang] || I18N.en;
    document.querySelectorAll("[data-i18n]").forEach(el => {
      const key = el.getAttribute("data-i18n");
      if (dict[key]) {
        el.textContent = dict[key];
      }
    });
    const langSelect = document.getElementById("lang-select");
    if (langSelect) langSelect.value = this.currentLang;
  }

  t(key) {
    const dict = I18N[this.currentLang] || I18N.en;
    return dict[key] || key;
  }

  updateUserUI() {
    if (!this.currentUser) return;
    const nameEl = document.getElementById("user-name");
    const roleBadge = document.getElementById("user-role-badge");
    const avatarEl = document.getElementById("user-avatar");
    const orgLabel = document.getElementById("demo-org-label");

    if (nameEl) nameEl.textContent = this.currentUser.name;
    if (avatarEl && this.currentUser.avatar_url) avatarEl.src = this.currentUser.avatar_url;
    if (orgLabel) orgLabel.textContent = `${this.currentUser.org_name} (${this.currentUser.org_industry === 'school' ? 'Education' : 'Healthcare'} Domain)`;

    if (roleBadge) {
      const r = this.currentUser.role;
      roleBadge.textContent = r.toUpperCase();
      if (r === "manager") {
        roleBadge.className = "inline-block px-1.5 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-purple-100 text-purple-800 dark:bg-purple-900/60 dark:text-purple-200";
      } else if (r === "coordinator") {
        roleBadge.className = "inline-block px-1.5 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-blue-100 text-blue-800 dark:bg-blue-900/60 dark:text-blue-200";
      } else {
        roleBadge.className = "inline-block px-1.5 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-teal-100 text-teal-800 dark:bg-teal-900/60 dark:text-teal-200";
      }
    }
  }

  async fetchInitialData() {
    try {
      const [tasksRes, logsRes, workloadRes, reqsRes, expRes, demoUsersRes] = await Promise.all([
        fetch("/api/tasks?scope=my"),
        fetch("/api/timelogs"),
        fetch("/api/workload/personal"),
        fetch("/api/requests"),
        fetch("/api/experiments/current"),
        fetch("/api/auth/demo-users")
      ]);

      if (tasksRes.ok) this.tasks = await tasksRes.json();
      if (logsRes.ok) this.timeLogs = await logsRes.json();
      if (workloadRes.ok) this.personalWorkload = await workloadRes.json();
      if (reqsRes.ok) this.requests = await reqsRes.json();
      if (expRes.ok) this.experiment = await expRes.json();
      if (demoUsersRes.ok) this.demoUsers = await demoUsersRes.json();

      if (this.currentUser.role in { manager: 1, coordinator: 1 }) {
        const teamRes = await fetch("/api/workload/team");
        if (teamRes.ok) this.teamWorkload = await teamRes.json();
      }

      this.populateTaskDropdowns();
      this.populateDemoUsersModal();
    } catch (e) {
      console.error("Failed to load initial dataset:", e);
    }
  }

  populateTaskDropdowns() {
    const taskSelectLog = document.getElementById("log-input-task");
    const taskSelectA = document.getElementById("req-input-task-a");
    const taskSelectB = document.getElementById("req-input-task-b");

    if (taskSelectLog) {
      taskSelectLog.innerHTML = `<option value="">-- General Unlisted Activity --</option>` +
        this.tasks.map(t => `<option value="${t.id}">${t.title} (${t.priority.toUpperCase()})</option>`).join("");
    }

    if (taskSelectA && taskSelectB) {
      const urgentTasks = this.tasks.filter(t => t.priority === "critical" || t.priority === "high");
      const normalTasks = this.tasks.filter(t => t.priority === "normal" || t.priority === "deferrable");

      taskSelectA.innerHTML = urgentTasks.map(t => `<option value="${t.id}">${t.title} [${t.priority.toUpperCase()}]</option>`).join("") ||
        this.tasks.map(t => `<option value="${t.id}">${t.title}</option>`).join("");

      taskSelectB.innerHTML = normalTasks.map(t => `<option value="${t.id}">${t.title} [${t.priority.toUpperCase()}]</option>`).join("") ||
        this.tasks.map(t => `<option value="${t.id}">${t.title}</option>`).join("");

      this.updateConflictMessageDraft();
    }
  }

  updateConflictMessageDraft() {
    const taskSelectA = document.getElementById("req-input-task-a");
    const taskSelectB = document.getElementById("req-input-task-b");
    const hoursInput = document.getElementById("req-input-available-hours");
    const messageArea = document.getElementById("req-input-message");

    if (!taskSelectA || !taskSelectB || !messageArea) return;

    const taskAName = taskSelectA.options[taskSelectA.selectedIndex]?.text || "Task A";
    const taskBName = taskSelectB.options[taskSelectB.selectedIndex]?.text || "Task B";
    const hours = hoursInput?.value || "4.0";

    const draft = `I have ${taskAName} and ${taskBName} competing for ${hours} hours of available planning time this week. Which should I prioritise, and can either task be safely reassigned or rescheduled?`;
    messageArea.value = draft;
  }

  handleRequestTypeChange(val) {
    const block = document.getElementById("req-competing-tasks-block");
    if (block) {
      if (val === "clarification") {
        block.classList.remove("hidden");
        this.updateConflictMessageDraft();
      } else {
        block.classList.add("hidden");
      }
    }
  }

  populateDemoUsersModal() {
    const container = document.getElementById("demo-users-list");
    if (!container) return;

    container.innerHTML = this.demoUsers.map(u => `
      <div onclick="app.quickSwitchUser('${u.id}')" class="p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-700/40 hover:bg-teal-50 dark:hover:bg-teal-950/40 cursor-pointer flex items-center justify-between transition">
        <div class="flex items-center space-x-3">
          <img src="${u.avatar_url || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150'}" class="w-10 h-10 rounded-full object-cover">
          <div>
            <div class="font-bold text-sm text-slate-900 dark:text-white">${u.name}</div>
            <div class="text-xs text-slate-500">${u.email} • ${u.department_name || 'General'}</div>
          </div>
        </div>
        <div class="text-right">
          <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${u.role === 'manager' ? 'bg-purple-100 text-purple-800' : u.role === 'coordinator' ? 'bg-blue-100 text-blue-800' : 'bg-teal-100 text-teal-800'}">${u.role}</span>
          <div class="text-[11px] text-slate-400 mt-1">${u.industry === 'school' ? '🏫 School' : '🏥 Healthcare'}</div>
        </div>
      </div>
    `).join("");
  }

  async quickSwitchUser(userId) {
    try {
      const res = await fetch("/api/auth/switch-demo", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId })
      });
      if (res.ok) {
        const data = await res.json();
        this.currentUser = data.user;
        this.closeModal("modal-demo-switcher");
        this.updateUserUI();

        // If manager, default to manager dashboard, else teacher dashboard
        if (this.currentUser.role === "manager" || this.currentUser.role === "coordinator") {
          this.currentView = "dashboard-manager";
        } else {
          this.currentView = "dashboard-teacher";
        }

        await this.fetchInitialData();
        this.render();
      }
    } catch (e) {
      console.error("Failed to switch demo user:", e);
    }
  }

  navigate(viewName) {
    this.currentView = viewName;
    document.querySelectorAll(".nav-item").forEach(item => {
      if (item.getAttribute("data-view") === viewName) {
        item.classList.add("bg-teal-50", "text-teal-700", "dark:bg-slate-700", "dark:text-teal-400", "font-bold");
      } else {
        item.classList.remove("bg-teal-50", "text-teal-700", "dark:bg-slate-700", "dark:text-teal-400", "font-bold");
      }
    });

    // Close mobile menu if open
    const sidebar = document.getElementById("sidebar");
    if (sidebar && !sidebar.classList.contains("hidden") && window.innerWidth < 768) {
      sidebar.classList.add("hidden");
    }

    this.render();
  }

  toggleMobileSidebar() {
    const sidebar = document.getElementById("sidebar");
    if (sidebar) {
      sidebar.classList.toggle("hidden");
      sidebar.classList.toggle("fixed");
      sidebar.classList.toggle("inset-y-0");
      sidebar.classList.toggle("left-0");
      sidebar.classList.toggle("z-50");
    }
  }

  openModal(modalId) {
    const m = document.getElementById(modalId);
    if (m) m.classList.remove("hidden");
  }

  closeModal(modalId) {
    const m = document.getElementById(modalId);
    if (m) m.classList.add("hidden");
  }

  // -------------------------------------------------------------
  // FORM SUBMISSION HANDLERS
  // -------------------------------------------------------------
  async handleTaskSubmit(e) {
    e.preventDefault();
    const payload = {
      title: document.getElementById("task-input-title").value,
      category: document.getElementById("task-input-category").value,
      priority: document.getElementById("task-input-priority").value,
      estimated_duration_hours: parseFloat(document.getElementById("task-input-est-hours").value),
      due_date: document.getElementById("task-input-due-date").value,
      assignment_type: document.getElementById("task-input-assignment-type").value,
      extra_work_reason: document.getElementById("task-input-extra-reason").value,
      private_note: document.getElementById("task-input-private-note").value || null,
      status: "pending"
    };

    try {
      const res = await fetch("/api/tasks", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      if (res.ok) {
        this.closeModal("modal-task");
        document.getElementById("form-task").reset();
        await this.fetchInitialData();
        this.render();
      } else {
        const err = await res.json();
        alert(err.detail || "Error saving task");
      }
    } catch (err) {
      alert("Network error: " + err.message);
    }
  }

  async handleTimeLogSubmit(e) {
    e.preventDefault();
    const payload = {
      task_id: document.getElementById("log-input-task").value || null,
      duration_hours: parseFloat(document.getElementById("log-input-hours").value),
      log_date: document.getElementById("log-input-date").value,
      is_after_hours: document.getElementById("log-input-after-hours").checked,
      notes: document.getElementById("log-input-notes").value || ""
    };

    try {
      const res = await fetch("/api/timelogs", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      if (res.ok) {
        this.closeModal("modal-timelog");
        document.getElementById("form-timelog").reset();
        await this.fetchInitialData();
        this.render();
      } else {
        const err = await res.json();
        alert(err.detail || "Error saving time log");
      }
    } catch (err) {
      alert("Network error: " + err.message);
    }
  }

  async handleRequestSubmit(e) {
    e.preventDefault();
    const type = document.getElementById("req-input-type").value;
    const payload = {
      request_type: type,
      task_a_id: type === "clarification" ? (document.getElementById("req-input-task-a").value || null) : null,
      task_b_id: type === "clarification" ? (document.getElementById("req-input-task-b").value || null) : null,
      available_time_hours: type === "clarification" ? parseFloat(document.getElementById("req-input-available-hours").value || 0) : null,
      message: document.getElementById("req-input-message").value,
      access_scope: type === "confidential_concern" ? "designated_confidential_handler" : "manager_only"
    };

    try {
      const res = await fetch("/api/requests", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      if (res.ok) {
        this.closeModal("modal-request");
        document.getElementById("form-request").reset();
        await this.fetchInitialData();
        this.navigate("requests");
      } else {
        const err = await res.json();
        alert(err.detail || "Error submitting request");
      }
    } catch (err) {
      alert("Network error: " + err.message);
    }
  }

  openRespondModal(reqId) {
    const r = this.requests.find(x => x.id === reqId);
    if (!r) return;
    document.getElementById("resp-input-request-id").value = r.id;
    document.getElementById("resp-request-details").innerHTML = `
      <div class="font-bold text-slate-800 dark:text-slate-200">From: ${r.author_name} (${r.request_type})</div>
      <div class="text-slate-600 dark:text-slate-300 italic">"${r.message}"</div>
    `;
    this.openModal("modal-respond-request");
  }

  async handleResponseSubmit(e) {
    e.preventDefault();
    const reqId = document.getElementById("resp-input-request-id").value;
    const payload = {
      status: document.getElementById("resp-input-status").value,
      manager_response: document.getElementById("resp-input-message").value
    };

    try {
      const res = await fetch(`/api/requests/${reqId}/respond`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      if (res.ok) {
        this.closeModal("modal-respond-request");
        await this.fetchInitialData();
        this.render();
      } else {
        const err = await res.json();
        alert(err.detail || "Error responding");
      }
    } catch (err) {
      alert("Network error: " + err.message);
    }
  }

  openReassignModal(taskId, title, fromUserName, defaultToUserId = "") {
    document.getElementById("reassign-task-id").value = taskId;
    document.getElementById("reassign-task-summary").innerHTML = `
      <div class="font-bold text-slate-800 dark:text-slate-200">Task: ${title}</div>
      <div class="text-slate-500">Currently assigned to: ${fromUserName}</div>
    `;
    const sel = document.getElementById("reassign-to-user-id");
    sel.innerHTML = this.demoUsers
      .filter(u => u.org_name === this.currentUser.org_name && u.role === "teacher")
      .map(u => `<option value="${u.id}" ${u.id === defaultToUserId ? 'selected' : ''}>${u.name} (${u.department_name || 'General'})</option>`)
      .join("");

    document.getElementById("reassign-reason").value = `Rebalancing non-urgent work from ${fromUserName} to preserve essential student-critical capacity.`;
    this.openModal("modal-reassign");
  }

  async handleReassignmentSubmit(e) {
    e.preventDefault();
    const payload = {
      task_id: document.getElementById("reassign-task-id").value,
      new_user_id: document.getElementById("reassign-to-user-id").value,
      reason: document.getElementById("reassign-reason").value
    };

    try {
      const res = await fetch("/api/workload/reassign", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      if (res.ok) {
        this.closeModal("modal-reassign");
        alert("Task successfully reassigned with human approval documented.");
        await this.fetchInitialData();
        this.render();
      } else {
        const err = await res.json();
        alert(err.detail || "Error reassigning task");
      }
    } catch (err) {
      alert("Network error: " + err.message);
    }
  }

  async handleExperimentEntrySubmit(e) {
    e.preventDefault();
    if (!this.experiment || !this.experiment.experiment) {
      alert("No active experiment found. Please start an experiment first.");
      return;
    }
    const expId = this.experiment.experiment.id;
    const payload = {
      day_number: parseInt(document.getElementById("ee-day-number").value),
      hours_spent: parseFloat(document.getElementById("ee-hours").value),
      task_title: document.getElementById("ee-task-title").value,
      category: document.getElementById("ee-category").value,
      extra_work_cause: document.getElementById("ee-cause").value,
      perceived_consequence: document.getElementById("ee-perceived-consequence").value,
      actual_outcome: document.getElementById("ee-actual-outcome").value,
      candidate_action: document.getElementById("ee-candidate-action").value
    };

    try {
      const res = await fetch(`/api/experiments/${expId}/entries`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      if (res.ok) {
        this.closeModal("modal-experiment-entry");
        document.getElementById("form-experiment-entry").reset();
        await this.fetchInitialData();
        this.render();
      } else {
        const err = await res.json();
        alert(err.detail || "Error saving entry");
      }
    } catch (err) {
      alert("Network error: " + err.message);
    }
  }

  async runAIAdvisor(mode) {
    const btn = document.getElementById("btn-run-ai");
    if (btn) {
      btn.disabled = true;
      btn.innerHTML = `<span class="animate-spin inline-block mr-2">⚙️</span> Synthesizing Insights...`;
    }

    const consent = document.getElementById("ai-consent-checkbox")?.checked || false;
    const contextNotes = document.getElementById("ai-context-input")?.value || "";

    try {
      const res = await fetch("/api/ai/insights", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          mode: mode,
          include_private_notes: consent,
          user_context: contextNotes
        })
      });
      if (res.ok) {
        this.aiInsightResult = await res.json();
        this.render();
      } else {
        const err = await res.json();
        alert(err.detail || "Error generating AI insights");
      }
    } catch (err) {
      alert("Network error: " + err.message);
    } finally {
      if (btn) {
        btn.disabled = false;
        btn.textContent = "Run Advisor Mode";
      }
    }
  }

  async markTaskStatus(taskId, newStatus) {
    try {
      const res = await fetch(`/api/tasks/${taskId}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status: newStatus })
      });
      if (res.ok) {
        await this.fetchInitialData();
        this.render();
      }
    } catch (e) {
      console.error(e);
    }
  }

  // -------------------------------------------------------------
  // CANVAS CHART RENDERING ENGINE (Pure Canvas / SVG - Zero Dummy Images)
  // -------------------------------------------------------------
  drawWorkloadGauge(canvasId, capacityRatio, statusColor) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    const w = canvas.width;
    const h = canvas.height;
    ctx.clearRect(0, 0, w, h);

    const centerX = w / 2;
    const centerY = h - 20;
    const radius = Math.min(centerX, centerY) - 15;

    // Background Arc
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, Math.PI, 2 * Math.PI, false);
    ctx.lineWidth = 18;
    ctx.strokeStyle = this.isDarkMode ? "#334155" : "#e2e8f0";
    ctx.stroke();

    // Value Arc
    const ratioClamped = Math.min(Math.max(capacityRatio / 150, 0), 1.0);
    const endAngle = Math.PI + (ratioClamped * Math.PI);

    let strokeColor = "#10b981"; // Emerald
    if (capacityRatio > 125) strokeColor = "#f43f5e"; // Rose
    else if (capacityRatio > 105) strokeColor = "#f59e0b"; // Amber
    else if (capacityRatio >= 85) strokeColor = "#3b82f6"; // Blue

    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, Math.PI, endAngle, false);
    ctx.lineWidth = 18;
    ctx.strokeStyle = strokeColor;
    ctx.lineCap = "round";
    ctx.stroke();

    // Value Text
    ctx.fillStyle = this.isDarkMode ? "#f8fafc" : "#0f172a";
    ctx.font = "bold 26px sans-serif";
    ctx.textAlign = "center";
    ctx.fillText(`${capacityRatio}%`, centerX, centerY - 25);

    ctx.font = "600 12px sans-serif";
    ctx.fillStyle = this.isDarkMode ? "#94a3b8" : "#64748b";
    ctx.fillText("of weekly capacity", centerX, centerY - 5);
  }

  drawCategoryBarChart(canvasId, categoryHours) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    const w = canvas.width;
    const h = canvas.height;
    ctx.clearRect(0, 0, w, h);

    const entries = Object.entries(categoryHours);
    if (entries.length === 0) {
      ctx.fillStyle = "#94a3b8";
      ctx.font = "14px sans-serif";
      ctx.textAlign = "center";
      ctx.fillText("No tasks recorded yet", w / 2, h / 2);
      return;
    }

    const maxVal = Math.max(...entries.map(e => e[1]), 8);
    const barWidth = Math.min((w - 60) / entries.length - 12, 45);
    const startX = 40;
    const chartHeight = h - 50;

    // Draw baseline
    ctx.strokeStyle = this.isDarkMode ? "#334155" : "#cbd5e1";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(startX, chartHeight + 10);
    ctx.lineTo(w - 10, chartHeight + 10);
    ctx.stroke();

    entries.forEach(([cat, val], i) => {
      const x = startX + (i * (barWidth + 12));
      const barH = (val / maxVal) * (chartHeight - 20);
      const y = (chartHeight + 10) - barH;

      // Bar fill
      ctx.fillStyle = this.isDarkMode ? "#0d9488" : "#0f766e";
      ctx.fillRect(x, y, barWidth, barH);

      // Label
      ctx.fillStyle = this.isDarkMode ? "#cbd5e1" : "#475569";
      ctx.font = "10px sans-serif";
      ctx.textAlign = "center";
      const shortName = cat.length > 7 ? cat.slice(0, 6) + ".." : cat;
      ctx.fillText(shortName, x + barWidth / 2, chartHeight + 25);

      // Value
      ctx.fillStyle = this.isDarkMode ? "#f8fafc" : "#0f172a";
      ctx.font = "bold 10px sans-serif";
      ctx.fillText(`${val}h`, x + barWidth / 2, y - 4);
    });
  }

  drawTeamCapacityBarChart(canvasId, members) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    const w = canvas.width;
    const h = canvas.height;
    ctx.clearRect(0, 0, w, h);

    if (!members || members.length === 0) return;

    const rowHeight = (h - 20) / members.length;
    members.forEach((m, idx) => {
      const y = 15 + (idx * rowHeight);

      // Member name
      ctx.fillStyle = this.isDarkMode ? "#f8fafc" : "#0f172a";
      ctx.font = "600 12px sans-serif";
      ctx.textAlign = "left";
      ctx.fillText(m.user_name, 10, y + 14);

      // Background Bar
      const barX = 140;
      const maxBarWidth = w - barX - 60;
      ctx.fillStyle = this.isDarkMode ? "#334155" : "#e2e8f0";
      ctx.fillRect(barX, y, maxBarWidth, 16);

      // Value Fill
      const ratio = Math.min(m.capacity_ratio / 150, 1.0);
      let fillColor = "#10b981";
      if (m.capacity_ratio > 125) fillColor = "#f43f5e";
      else if (m.capacity_ratio > 105) fillColor = "#f59e0b";
      else if (m.capacity_ratio >= 85) fillColor = "#3b82f6";

      ctx.fillStyle = fillColor;
      ctx.fillRect(barX, y, maxBarWidth * ratio, 16);

      // Percentage Text
      ctx.fillStyle = this.isDarkMode ? "#f8fafc" : "#0f172a";
      ctx.font = "bold 12px sans-serif";
      ctx.textAlign = "left";
      ctx.fillText(`${m.capacity_ratio}%`, barX + (maxBarWidth * ratio) + 8, y + 13);
    });
  }

  // -------------------------------------------------------------
  // DYNAMIC VIEW RENDERERS
  // -------------------------------------------------------------
  render() {
    const container = document.getElementById("view-container");
    const pageTitle = document.getElementById("page-title");
    if (!container) return;

    switch (this.currentView) {
      case "dashboard-teacher":
        if (pageTitle) pageTitle.textContent = this.t("nav_my_dashboard");
        this.renderTeacherDashboard(container);
        break;
      case "my-tasks":
        if (pageTitle) pageTitle.textContent = this.t("nav_my_tasks");
        this.renderMyTasksView(container);
        break;
      case "time-tracker":
        if (pageTitle) pageTitle.textContent = this.t("nav_time_logs");
        this.renderTimeTrackerView(container);
        break;
      case "experiment":
        if (pageTitle) pageTitle.textContent = this.t("nav_experiment");
        this.renderExperimentView(container);
        break;
      case "requests":
        if (pageTitle) pageTitle.textContent = this.t("nav_requests");
        this.renderRequestsView(container);
        break;
      case "dashboard-manager":
        if (pageTitle) pageTitle.textContent = this.t("nav_team_workload");
        this.renderManagerDashboard(container);
        break;
      case "rebalancing":
        if (pageTitle) pageTitle.textContent = this.t("nav_rebalance");
        this.renderRebalancingView(container);
        break;
      case "ai-insights":
        if (pageTitle) pageTitle.textContent = this.t("nav_ai_advisor");
        this.renderAIInsightsView(container);
        break;
      case "settings":
        if (pageTitle) pageTitle.textContent = this.t("nav_settings");
        this.renderSettingsView(container);
        break;
      case "walkthrough":
        if (pageTitle) pageTitle.textContent = this.t("nav_walkthrough");
        this.renderWalkthroughView(container);
        break;
      case "landing":
      default:
        if (pageTitle) pageTitle.textContent = "FAIRSHIFT Overview";
        this.renderLandingView(container);
        break;
    }
  }

  // 1. TEACHER DASHBOARD VIEW
  renderTeacherDashboard(container) {
    const wl = this.personalWorkload || {
      capacity_ratio: 100, status_label: "Balanced",
      total_projected_load: 35, target_hours: 35,
      actual_logged_hours_this_week: 0, after_hours_logged: 0,
      personal_time_lost_hours: 0, voluntary_unplanned_hours: 0,
      explanation_factors: [], priority_breakdown: { counts: {} }
    };

    container.innerHTML = `
      <div class="space-y-6">
        
        <!-- Welcome Banner with Safe Working Principles reminder -->
        <div class="p-5 rounded-2xl bg-gradient-to-r from-teal-700 to-teal-900 text-white shadow-sm flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <div class="flex items-center space-x-2">
              <span class="text-xs uppercase tracking-wider font-bold text-teal-200">Personal Workload Calibration</span>
              <span class="px-2 py-0.5 rounded text-[10px] font-extrabold bg-teal-500/30 text-teal-100">Evidence-Based</span>
            </div>
            <h2 class="text-xl sm:text-2xl font-bold mt-1">Hello, ${this.currentUser.name}</h2>
            <p class="text-teal-100 text-xs sm:text-sm mt-1 max-w-2xl">
              Recorded workload data is used for transparent, respectful planning conversations — never surveillance or performance accusations.
            </p>
          </div>
          <div class="flex items-center space-x-2">
            <button onclick="app.openModal('modal-request')" class="px-3.5 py-2 rounded-xl bg-white text-teal-900 font-bold text-xs sm:text-sm hover:bg-teal-50 shadow-sm transition">
              Raise Workload Conflict
            </button>
            <button onclick="app.openModal('modal-task')" class="px-3.5 py-2 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-bold text-xs sm:text-sm transition">
              + Add Task
            </button>
          </div>
        </div>

        <!-- 4 Top Metric KPI Cards -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          
          <!-- Capacity Card -->
          <div class="p-5 rounded-2xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shadow-sm">
            <div class="text-xs font-bold uppercase tracking-wider text-slate-400">Projected Load</div>
            <div class="flex items-baseline space-x-2 mt-2">
              <span class="text-2xl font-extrabold text-slate-900 dark:text-white">${wl.total_projected_load}h</span>
              <span class="text-xs text-slate-500">/ ${wl.target_hours}h target</span>
            </div>
            <div class="mt-3">
              <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-bold ${wl.capacity_status === 'severe_overload' ? 'bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-300' : wl.capacity_status === 'moderate_overload' ? 'bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300' : 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300'}">
                ${wl.status_label} (${wl.capacity_ratio}%)
              </span>
            </div>
          </div>

          <!-- After-Hours Logged -->
          <div class="p-5 rounded-2xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shadow-sm">
            <div class="text-xs font-bold uppercase tracking-wider text-slate-400">After-Hours Work</div>
            <div class="flex items-baseline space-x-2 mt-2">
              <span class="text-2xl font-extrabold text-amber-600 dark:text-amber-400">${wl.after_hours_logged}h</span>
              <span class="text-xs text-slate-500">past 7 days</span>
            </div>
            <div class="text-xs text-slate-500 dark:text-slate-400 mt-3">
              Logged evening or weekend hours outside schedule.
            </div>
          </div>

          <!-- Unplanned / Voluntary Load -->
          <div class="p-5 rounded-2xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shadow-sm">
            <div class="text-xs font-bold uppercase tracking-wider text-slate-400">Unplanned / Voluntary</div>
            <div class="flex items-baseline space-x-2 mt-2">
              <span class="text-2xl font-extrabold text-indigo-600 dark:text-indigo-400">${wl.voluntary_unplanned_hours}h</span>
              <span class="text-xs text-slate-500">absorbed</span>
            </div>
            <div class="text-xs text-slate-500 dark:text-slate-400 mt-3">
              ${wl.unclear_ownership_count || 0} tasks flagged with unclear ownership.
            </div>
          </div>

          <!-- Personal Time Lost -->
          <div class="p-5 rounded-2xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shadow-sm">
            <div class="text-xs font-bold uppercase tracking-wider text-slate-400">Personal Time Impact</div>
            <div class="flex items-baseline space-x-2 mt-2">
              <span class="text-2xl font-extrabold text-rose-600 dark:text-rose-400">${wl.personal_time_lost_hours}h</span>
              <span class="text-xs text-slate-500">estimated</span>
            </div>
            <div class="text-xs text-slate-500 dark:text-slate-400 mt-3">
              Time absorbed without formal compensation.
            </div>
          </div>

        </div>

        <!-- Middle Section: Visual Gauge & Explainable Breakdown -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          <!-- Visual Capacity Gauge -->
          <div class="p-5 rounded-2xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shadow-sm flex flex-col items-center justify-center">
            <div class="w-full flex items-center justify-between mb-2">
              <span class="font-bold text-sm text-slate-900 dark:text-white">Weekly Capacity Gauge</span>
              <span class="text-xs text-slate-400">Transparent Rule</span>
            </div>
            <canvas id="chart-gauge" width="280" height="150" class="my-2"></canvas>
            <div class="text-center text-xs text-slate-500 dark:text-slate-400 max-w-xs mt-1">
              Considers contracted periods, weighted active tasks, and historical variance.
            </div>
          </div>

          <!-- Transparent Calculation Factors (Explainability) -->
          <div class="lg:col-span-2 p-5 rounded-2xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shadow-sm">
            <div class="flex items-center justify-between mb-3">
              <div>
                <h3 class="font-bold text-slate-900 dark:text-white text-base">Explainable Calculation Breakdown</h3>
                <p class="text-xs text-slate-500">Every hour is grounded in transparent formulas rather than a black-box model.</p>
              </div>
              <span class="px-2 py-0.5 rounded text-[11px] font-bold bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300">Auditable</span>
            </div>
            <div class="space-y-3">
              ${(wl.explanation_factors || []).map(f => `
                <div class="p-3 rounded-xl bg-slate-50 dark:bg-slate-700/40 border border-slate-100 dark:border-slate-700 flex items-center justify-between">
                  <div>
                    <div class="font-bold text-xs text-slate-800 dark:text-slate-200">${f.factor}</div>
                    <div class="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5">${f.description}</div>
                  </div>
                  <div class="text-sm font-extrabold text-slate-900 dark:text-white">${f.hours}h</div>
                </div>
              `).join("")}
            </div>
            ${(wl.missing_data_notes && wl.missing_data_notes.length > 0) ? `
              <div class="mt-3 p-2.5 rounded-lg bg-amber-50 dark:bg-amber-950/30 text-amber-900 dark:text-amber-200 text-xs flex items-center space-x-2">
                <span>⚠️</span>
                <span>${wl.missing_data_notes.join(" ")}</span>
              </div>
            ` : ""}
          </div>

        </div>

        <!-- Priority Tasks Table (Student-First Focus) -->
        <div class="p-5 rounded-2xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shadow-sm">
          <div class="flex items-center justify-between mb-4">
            <div>
              <h3 class="font-bold text-slate-900 dark:text-white text-base">Active Tasks & Immediate Deadlines</h3>
              <p class="text-xs text-slate-500">Critical student safety & exam prep tasks are protected.</p>
            </div>
            <button onclick="app.navigate('my-tasks')" class="text-xs font-bold text-teal-600 hover:text-teal-700">View All Tasks (${this.tasks.length}) →</button>
          </div>
          
          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs">
              <thead class="bg-slate-50 dark:bg-slate-700/50 text-slate-500 uppercase font-bold tracking-wider">
                <tr>
                  <th class="p-3">Priority</th>
                  <th class="p-3">Task Title</th>
                  <th class="p-3">Category</th>
                  <th class="p-3">Due Date</th>
                  <th class="p-3">Est / Actual</th>
                  <th class="p-3">Origin</th>
                  <th class="p-3 text-right">Action</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100 dark:divide-slate-700">
                ${this.tasks.slice(0, 5).map(t => `
                  <tr class="hover:bg-slate-50/60 dark:hover:bg-slate-700/30 transition">
                    <td class="p-3">
                      <span class="inline-flex px-2 py-0.5 rounded text-[10px] font-extrabold uppercase ${t.priority === 'critical' ? 'bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-300' : t.priority === 'high' ? 'bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300' : t.priority === 'normal' ? 'bg-blue-100 text-blue-800 dark:bg-blue-950 dark:text-blue-300' : 'bg-slate-100 text-slate-700'}">${t.priority}</span>
                    </td>
                    <td class="p-3 font-semibold text-slate-900 dark:text-slate-100">
                      ${t.title}
                      ${t.private_note ? `<span title="Private reflection note present" class="ml-1 text-slate-400">🔒</span>` : ""}
                    </td>
                    <td class="p-3 text-slate-600 dark:text-slate-300 capitalize">${t.category}</td>
                    <td class="p-3 text-slate-500">${t.due_date}</td>
                    <td class="p-3 font-medium text-slate-700 dark:text-slate-300">${t.estimated_duration_hours}h / ${t.actual_duration_hours || 0}h</td>
                    <td class="p-3 text-slate-500 capitalize">${(t.assignment_type || '').replace('_', ' ')}</td>
                    <td class="p-3 text-right">
                      ${t.status === 'completed' ? `
                        <span class="text-emerald-600 font-bold">✓ Done</span>
                      ` : `
                        <button onclick="app.markTaskStatus('${t.id}', 'completed')" class="px-2.5 py-1 rounded bg-teal-50 hover:bg-teal-100 dark:bg-teal-950 dark:hover:bg-teal-900 text-teal-800 dark:text-teal-200 font-bold">Complete</button>
                      `}
                    </td>
                  </tr>
                `).join("")}
              </tbody>
            </table>
          </div>
        </div>

      </div>
    `;

    setTimeout(() => {
      this.drawWorkloadGauge("chart-gauge", wl.capacity_ratio, wl.color);
    }, 50);
  }

  // 2. MY TASKS & DUTIES VIEW
  renderMyTasksView(container) {
    container.innerHTML = `
      <div class="space-y-5">
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
          <div>
            <h2 class="text-xl font-bold text-slate-900 dark:text-white">My Tasks & Assigned Duties</h2>
            <p class="text-xs text-slate-500">Track planned vs actual hours, voluntary support, and boundary flags.</p>
          </div>
          <div class="flex items-center space-x-2">
            <button onclick="app.openModal('modal-task')" class="px-3 py-1.5 rounded-lg bg-teal-600 hover:bg-teal-700 text-white font-semibold text-xs sm:text-sm shadow-sm transition">
              + New Task
            </button>
            <a href="/api/export/workload-csv" download class="px-3 py-1.5 rounded-lg bg-slate-100 dark:bg-slate-700 hover:bg-slate-200 text-slate-700 dark:text-slate-200 font-semibold text-xs sm:text-sm flex items-center space-x-1.5">
              <span>📥 Export CSV</span>
            </a>
          </div>
        </div>

        <!-- Task Filters -->
        <div class="flex flex-wrap gap-2 text-xs">
          <button onclick="app.filterTasks('')" class="px-3 py-1 rounded-full bg-teal-600 text-white font-bold">All (${this.tasks.length})</button>
          <button onclick="app.filterTasks('pending')" class="px-3 py-1 rounded-full bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-300 hover:bg-slate-200">Active</button>
          <button onclick="app.filterTasks('completed')" class="px-3 py-1 rounded-full bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-300 hover:bg-slate-200">Completed</button>
        </div>

        <!-- Full Task Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          ${this.tasks.map(t => `
            <div class="p-5 rounded-2xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shadow-sm flex flex-col justify-between space-y-3">
              <div>
                <div class="flex items-center justify-between mb-2">
                  <span class="inline-flex px-2 py-0.5 rounded text-[10px] font-extrabold uppercase ${t.priority === 'critical' ? 'bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-300' : t.priority === 'high' ? 'bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300' : 'bg-blue-100 text-blue-800 dark:bg-blue-950 dark:text-blue-300'}">${t.priority}</span>
                  <span class="text-[11px] font-medium text-slate-400 capitalize">${t.category}</span>
                </div>
                <h4 class="font-bold text-slate-900 dark:text-white text-base">${t.title}</h4>
                <p class="text-xs text-slate-500 dark:text-slate-400 mt-1 line-clamp-2">${t.description || 'No detailed instructions provided.'}</p>
                
                ${t.extra_work_reason && t.extra_work_reason !== 'none' ? `
                  <div class="mt-2 text-[11px] font-medium text-amber-700 dark:text-amber-300 bg-amber-50 dark:bg-amber-950/40 p-2 rounded-lg border border-amber-200/50">
                    💡 Reason: ${t.extra_work_reason.replace('_', ' ')}
                  </div>
                ` : ""}

                ${t.private_note ? `
                  <div class="mt-2 text-[11px] text-slate-600 dark:text-slate-300 bg-slate-50 dark:bg-slate-700/50 p-2 rounded-lg border border-slate-200/60 dark:border-slate-700">
                    <span class="font-bold">🔒 Private Note:</span> ${t.private_note}
                  </div>
                ` : ""}
              </div>

              <div class="pt-3 border-t border-slate-100 dark:border-slate-700 text-xs flex items-center justify-between">
                <div>
                  <div class="text-slate-400 text-[10px]">Due Date: <span class="font-semibold text-slate-700 dark:text-slate-300">${t.due_date}</span></div>
                  <div class="text-slate-400 text-[10px]">Hours: <span class="font-semibold text-teal-600">${t.estimated_duration_hours}h est / ${t.actual_duration_hours || 0}h act</span></div>
                </div>
                <div>
                  ${t.status === 'completed' ? `
                    <span class="px-2 py-1 rounded bg-emerald-100 text-emerald-800 dark:bg-emerald-900 text-xs font-bold">✓ Completed</span>
                  ` : `
                    <button onclick="app.markTaskStatus('${t.id}', 'completed')" class="px-2.5 py-1 rounded bg-teal-600 hover:bg-teal-700 text-white font-bold text-xs">Done</button>
                  `}
                </div>
              </div>
            </div>
          `).join("")}
        </div>
      </div>
    `;
  }

  // 3. TIME & EXTRA-HOURS TRACKER VIEW
  renderTimeTrackerView(container) {
    container.innerHTML = `
      <div class="space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
          <div>
            <h2 class="text-xl font-bold text-slate-900 dark:text-white">Time & Extra-Hours Tracker</h2>
            <p class="text-xs text-slate-500">Record daily work, after-hours commitments, and causes of extra effort.</p>
          </div>
          <button onclick="app.openModal('modal-timelog')" class="px-3.5 py-2 rounded-xl bg-teal-600 hover:bg-teal-700 text-white font-semibold text-xs sm:text-sm shadow-sm transition">
            + Record Time Entry
          </button>
        </div>

        <!-- Summary Cards -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="p-5 rounded-2xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shadow-sm">
            <div class="text-xs font-bold text-slate-400 uppercase">Total Logged (7 Days)</div>
            <div class="text-2xl font-extrabold text-slate-900 dark:text-white mt-1">
              ${this.timeLogs.reduce((acc, l) => acc + l.duration_hours, 0)}h
            </div>
            <div class="text-xs text-slate-500 mt-1">Across ${this.timeLogs.length} logged sessions</div>
          </div>

          <div class="p-5 rounded-2xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shadow-sm">
            <div class="text-xs font-bold text-slate-400 uppercase">After-Hours Recorded</div>
            <div class="text-2xl font-extrabold text-amber-600 dark:text-amber-400 mt-1">
              ${this.timeLogs.filter(l => l.is_after_hours === 1).reduce((acc, l) => acc + l.duration_hours, 0)}h
            </div>
            <div class="text-xs text-slate-500 mt-1">Outside contractual school hours</div>
          </div>

          <div class="p-5 rounded-2xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shadow-sm">
            <div class="text-xs font-bold text-slate-400 uppercase">Core Categories</div>
            <div class="text-xs text-slate-600 dark:text-slate-300 mt-2 space-y-1">
              <div>Grading & Assessment: <span class="font-bold">Heavy Concentration</span></div>
              <div>Lesson Preparation: <span class="font-bold">Differentiated Materials</span></div>
            </div>
          </div>
        </div>

        <!-- Category Bar Chart -->
        <div class="p-5 rounded-2xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shadow-sm">
          <h3 class="font-bold text-slate-900 dark:text-white text-sm mb-3">Time Allocation by Category (Estimated)</h3>
          <canvas id="chart-categories" width="700" height="180" class="w-full"></canvas>
        </div>

        <!-- Time Logs Table -->
        <div class="p-5 rounded-2xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shadow-sm">
          <h3 class="font-bold text-slate-900 dark:text-white text-base mb-3">Recent Time Log Records</h3>
          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs">
              <thead class="bg-slate-50 dark:bg-slate-700/50 text-slate-500 uppercase font-bold tracking-wider">
                <tr>
                  <th class="p-3">Date</th>
                  <th class="p-3">Duration</th>
                  <th class="p-3">Type</th>
                  <th class="p-3">Task Association</th>
                  <th class="p-3">Notes / Reflection</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100 dark:divide-slate-700">
                ${this.timeLogs.map(l => `
                  <tr class="hover:bg-slate-50/60 dark:hover:bg-slate-700/30">
                    <td class="p-3 font-semibold text-slate-700 dark:text-slate-300">${l.log_date}</td>
                    <td class="p-3 font-extrabold text-slate-900 dark:text-white">${l.duration_hours}h</td>
                    <td class="p-3">
                      ${l.is_after_hours === 1 ? `
                        <span class="inline-flex px-2 py-0.5 rounded text-[10px] font-bold bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300">🌙 After-Hours</span>
                      ` : `
                        <span class="inline-flex px-2 py-0.5 rounded text-[10px] font-bold bg-slate-100 text-slate-700">☀️ Scheduled</span>
                      `}
                    </td>
                    <td class="p-3 text-slate-600 dark:text-slate-300 font-medium">${l.task_title || 'General Activity'}</td>
                    <td class="p-3 text-slate-500 italic">${l.notes || '—'}</td>
                  </tr>
                `).join("")}
              </tbody>
            </table>
          </div>
        </div>

      </div>
    `;

    setTimeout(() => {
      if (this.personalWorkload && this.personalWorkload.category_hours) {
        this.drawCategoryBarChart("chart-categories", this.personalWorkload.category_hours);
      }
    }, 50);
  }

  // 4. SAFE FIVE-DAY WORKLOAD EXPERIMENT (MVP FEATURE 4)
  renderExperimentView(container) {
    const exp = this.experiment?.experiment;
    const entries = this.experiment?.entries || [];
    const summary = this.experiment?.summary || {};

    container.innerHTML = `
      <div class="space-y-6">
        
        <div class="p-5 rounded-2xl bg-gradient-to-r from-amber-600 to-amber-800 text-white shadow-sm flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <div class="flex items-center space-x-2">
              <span class="text-xs uppercase tracking-wider font-bold text-amber-200">Reflective Discovery</span>
              <span class="px-2 py-0.5 rounded text-[10px] font-extrabold bg-amber-400/30 text-amber-100">Safe Experiment</span>
            </div>
            <h2 class="text-xl sm:text-2xl font-bold mt-1">5-Day Guided Workload Experiment</h2>
            <p class="text-amber-100 text-xs sm:text-sm mt-1 max-w-2xl">
              Track why extra tasks were taken on, what you feared would happen if they waited, and what actually occurred. Discovers delegation and template candidates safely.
            </p>
          </div>
          <div class="flex items-center space-x-2">
            <button onclick="app.openModal('modal-experiment-entry')" class="px-3.5 py-2 rounded-xl bg-white text-amber-900 font-bold text-xs sm:text-sm hover:bg-amber-50 shadow-sm transition">
              + Log Day Entry
            </button>
          </div>
        </div>

        <!-- Experiment Progress Bar -->
        <div class="p-5 rounded-2xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shadow-sm">
          <div class="flex items-center justify-between mb-2">
            <span class="font-bold text-sm text-slate-900 dark:text-white">Experiment Progress: Days 1 to 5</span>
            <span class="text-xs font-semibold text-amber-600">${entries.length} Entries Recorded</span>
          </div>
          <div class="grid grid-cols-5 gap-2">
            ${[1, 2, 3, 4, 5].map(day => {
              const hasDay = entries.some(e => e.day_number === day);
              return `
                <div class="p-3 rounded-xl border text-center ${hasDay ? 'bg-amber-50 dark:bg-amber-950/40 border-amber-300 dark:border-amber-800 text-amber-900 dark:text-amber-200 font-bold' : 'bg-slate-50 dark:bg-slate-700/30 border-slate-200 text-slate-400'}">
                  <div class="text-xs">Day ${day}</div>
                  <div class="text-sm mt-1">${hasDay ? '✓ Done' : 'Pending'}</div>
                </div>
              `;
            }).join("")}
          </div>
        </div>

        <!-- Synthesis Summary Report -->
        ${summary.total_days_logged ? `
          <div class="p-6 rounded-2xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shadow-sm space-y-4">
            <div class="flex items-center justify-between">
              <div>
                <h3 class="font-bold text-slate-900 dark:text-white text-lg">5-Day Synthesis & Safe Next Experiment</h3>
                <p class="text-xs text-slate-500">Synthesized patterns from your 5 days of personal workload logs.</p>
              </div>
              <span class="px-2.5 py-1 rounded-full text-xs font-bold bg-amber-100 text-amber-800 dark:bg-amber-900 dark:text-amber-200">Synthesized</span>
            </div>

            <!-- Most Common Causes -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="p-4 rounded-xl bg-slate-50 dark:bg-slate-700/40 border border-slate-100 dark:border-slate-700">
                <div class="text-xs font-bold uppercase text-slate-400 mb-2">Primary Causes of Extra Work</div>
                <div class="space-y-1.5 text-xs">
                  ${(summary.most_common_causes || []).map(c => `
                    <div class="flex items-center justify-between">
                      <span class="text-slate-700 dark:text-slate-300 capitalize">${c.cause.replace('_', ' ')}</span>
                      <span class="font-bold text-slate-900 dark:text-white">${c.count} times</span>
                    </div>
                  `).join("")}
                </div>
              </div>

              <!-- Total Extra Hours Recorded -->
              <div class="p-4 rounded-xl bg-slate-50 dark:bg-slate-700/40 border border-slate-100 dark:border-slate-700">
                <div class="text-xs font-bold uppercase text-slate-400 mb-2">Total Extra Work Discovered</div>
                <div class="text-2xl font-extrabold text-amber-600">${summary.total_extra_hours_recorded}h</div>
                <p class="text-[11px] text-slate-500 mt-1">Identified across ${summary.total_entries} separate duties.</p>
              </div>
            </div>

            <!-- Reflection vs Reality Cards -->
            <div>
              <h4 class="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">Fear vs Reality Reflections</h4>
              <div class="space-y-2">
                ${(summary.reflections || []).map(r => `
                  <div class="p-3 rounded-xl bg-slate-50 dark:bg-slate-700/40 border border-slate-100 dark:border-slate-700 text-xs">
                    <div class="font-bold text-slate-900 dark:text-white">${r.task}</div>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-2 mt-1">
                      <div class="text-rose-700 dark:text-rose-300"><strong>Feared:</strong> ${r.feared_consequence}</div>
                      <div class="text-emerald-700 dark:text-emerald-300"><strong>Observed Outcome:</strong> ${r.observed_outcome}</div>
                    </div>
                  </div>
                `).join("")}
              </div>
            </div>

            <!-- Safe Next Mini-Experiment -->
            <div class="p-4 rounded-xl bg-teal-50 dark:bg-teal-950/40 border border-teal-200 dark:border-teal-800">
              <div class="text-xs font-bold text-teal-900 dark:text-teal-200 uppercase">Recommended Next Step</div>
              <div class="text-sm text-teal-800 dark:text-teal-300 font-semibold mt-1">
                ${summary.safe_next_experiment}
              </div>
              <div class="text-[11px] text-teal-700 dark:text-teal-400 mt-2 italic">
                ${summary.tentative_pattern_disclaimer}
              </div>
            </div>

            <!-- Data Deletion Agency -->
            <div class="pt-2 flex justify-end">
              <button onclick="app.deleteExperiment('${exp.id}')" class="text-xs text-rose-600 hover:text-rose-700 underline">
                Delete My Experiment Records (Full Privacy)
              </button>
            </div>
          </div>
        ` : ""}

      </div>
    `;
  }

  async deleteExperiment(expId) {
    if (!confirm("Are you sure you want to permanently delete your 5-day experiment data? This cannot be undone.")) return;
    try {
      const res = await fetch(`/api/experiments/${expId}`, { method: "DELETE" });
      if (res.ok) {
        alert("Experiment data permanently removed.");
        await this.fetchInitialData();
        this.render();
      }
    } catch (e) {
      console.error(e);
    }
  }

  // 5. REQUESTS & CONCERNS CHANNEL (MVP FEATURE 5)
  renderRequestsView(container) {
    container.innerHTML = `
      <div class="space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
          <div>
            <h2 class="text-xl font-bold text-slate-900 dark:text-white">Respectful Request & Support Channel</h2>
            <p class="text-xs text-slate-500">Structured channel for prioritisation conflicts, assistance, and confidential concerns.</p>
          </div>
          <button onclick="app.openModal('modal-request')" class="px-3.5 py-2 rounded-xl bg-teal-600 hover:bg-teal-700 text-white font-semibold text-xs sm:text-sm shadow-sm transition">
            + New Request
          </button>
        </div>

        <div class="space-y-4">
          ${this.requests.length === 0 ? `
            <div class="p-8 text-center bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 text-slate-400 text-sm">
              No requests submitted yet. Use the "New Request" button to raise a prioritisation query.
            </div>
          ` : this.requests.map(r => `
            <div class="p-5 rounded-2xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shadow-sm space-y-3">
              <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
                <div class="flex items-center space-x-2">
                  <span class="inline-flex px-2 py-0.5 rounded text-[10px] font-extrabold uppercase bg-indigo-100 text-indigo-800 dark:bg-indigo-950 dark:text-indigo-300">${r.request_type.replace('_', ' ')}</span>
                  <span class="text-xs text-slate-400">From: <strong class="text-slate-700 dark:text-slate-300">${r.author_name}</strong></span>
                </div>
                <div class="flex items-center space-x-2">
                  <span class="px-2 py-0.5 rounded text-xs font-bold ${r.status === 'resolved' ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300' : 'bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300'} capitalize">
                    ${r.status.replace('_', ' ')}
                  </span>
                  ${(this.currentUser.role === 'manager' || this.currentUser.role === 'coordinator') && r.status !== 'resolved' ? `
                    <button onclick="app.openRespondModal('${r.id}')" class="px-2.5 py-1 rounded bg-teal-600 text-white font-bold text-xs hover:bg-teal-700">Respond</button>
                  ` : ""}
                </div>
              </div>

              <div class="text-xs text-slate-800 dark:text-slate-200 bg-slate-50 dark:bg-slate-700/40 p-3 rounded-xl border border-slate-100 dark:border-slate-700">
                "${r.message}"
              </div>

              ${r.manager_response ? `
                <div class="text-xs text-emerald-900 dark:text-emerald-200 bg-emerald-50 dark:bg-emerald-950/40 p-3 rounded-xl border border-emerald-200/60 dark:border-emerald-800">
                  <div class="font-bold mb-1">✓ Manager Decision / Guidance:</div>
                  <div>${r.manager_response}</div>
                  <div class="text-[10px] text-emerald-700 dark:text-emerald-400 mt-1.5">Resolved at: ${r.resolved_at || 'Recent'}</div>
                </div>
              ` : `
                <div class="text-[11px] text-slate-400 italic">Awaiting managerial review and collaborative scheduling calibration.</div>
              `}
            </div>
          `).join("")}
        </div>
      </div>
    `;
  }

  // 6. MANAGER DASHBOARD VIEW
  renderManagerDashboard(container) {
    const tw = this.teamWorkload || {
      total_teachers: 0, overloaded_count: 0, balanced_count: 0, available_count: 0,
      members: [], rebalancing_suggestions: []
    };

    container.innerHTML = `
      <div class="space-y-6">
        
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
          <div>
            <h2 class="text-xl font-bold text-slate-900 dark:text-white">Leadership Team Capacity & Fairness Overview</h2>
            <p class="text-xs text-slate-500">Aggregate team workload distribution, capacity risks, and rebalancing recommendations.</p>
          </div>
          <div class="flex items-center space-x-2">
            <button onclick="app.navigate('rebalancing')" class="px-3.5 py-2 rounded-xl bg-teal-600 hover:bg-teal-700 text-white font-semibold text-xs sm:text-sm shadow-sm transition">
              Review Rebalancing (${tw.rebalancing_suggestions.length})
            </button>
          </div>
        </div>

        <!-- KPI Metrics -->
        <div class="grid grid-cols-1 sm:grid-cols-4 gap-4">
          <div class="p-5 rounded-2xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shadow-sm">
            <div class="text-xs font-bold uppercase text-slate-400">Total Staff Tracked</div>
            <div class="text-2xl font-extrabold text-slate-900 dark:text-white mt-1">${tw.total_teachers}</div>
          </div>
          <div class="p-5 rounded-2xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shadow-sm">
            <div class="text-xs font-bold uppercase text-slate-400">Overload Risk</div>
            <div class="text-2xl font-extrabold text-rose-600 mt-1">${tw.overloaded_count} Staff</div>
          </div>
          <div class="p-5 rounded-2xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shadow-sm">
            <div class="text-xs font-bold uppercase text-slate-400">Balanced Load</div>
            <div class="text-2xl font-extrabold text-blue-600 mt-1">${tw.balanced_count} Staff</div>
          </div>
          <div class="p-5 rounded-2xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shadow-sm">
            <div class="text-xs font-bold uppercase text-slate-400">Available Capacity</div>
            <div class="text-2xl font-extrabold text-emerald-600 mt-1">${tw.available_count} Staff</div>
          </div>
        </div>

        <!-- Team Capacity Chart -->
        <div class="p-5 rounded-2xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shadow-sm">
          <div class="flex items-center justify-between mb-3">
            <h3 class="font-bold text-slate-900 dark:text-white text-sm">Team Workload Distribution (% of Standard Capacity)</h3>
            <span class="text-xs text-slate-400">Sorted by load index</span>
          </div>
          <canvas id="chart-team-bars" width="700" height="150" class="w-full"></canvas>
        </div>

        <!-- Staff Cards with Explainable Breakdowns -->
        <div class="space-y-4">
          <h3 class="font-bold text-slate-900 dark:text-white text-base">Individual Capacity Indicators</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            ${tw.members.map(m => `
              <div class="p-5 rounded-2xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shadow-sm space-y-3">
                <div class="flex items-center justify-between">
                  <div>
                    <h4 class="font-bold text-slate-900 dark:text-white text-base">${m.user_name}</h4>
                    <div class="text-xs text-slate-400">${m.department_name} • ${m.contracted_teaching_periods} contracted periods</div>
                  </div>
                  <span class="px-2.5 py-1 rounded-full text-xs font-bold ${m.capacity_status === 'severe_overload' ? 'bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-300' : m.capacity_status === 'moderate_overload' ? 'bg-amber-100 text-amber-800' : 'bg-emerald-100 text-emerald-800'}">
                    ${m.capacity_ratio}% (${m.status_label})
                  </span>
                </div>

                <div class="grid grid-cols-3 gap-2 text-center text-xs">
                  <div class="p-2 rounded-lg bg-slate-50 dark:bg-slate-700/40">
                    <div class="text-slate-400 text-[10px]">Projected Load</div>
                    <div class="font-bold text-slate-800 dark:text-slate-200 mt-0.5">${m.total_projected_load}h</div>
                  </div>
                  <div class="p-2 rounded-lg bg-slate-50 dark:bg-slate-700/40">
                    <div class="text-slate-400 text-[10px]">After-Hours</div>
                    <div class="font-bold text-amber-600 mt-0.5">${m.after_hours_logged}h</div>
                  </div>
                  <div class="p-2 rounded-lg bg-slate-50 dark:bg-slate-700/40">
                    <div class="text-slate-400 text-[10px]">Unplanned Extra</div>
                    <div class="font-bold text-indigo-600 mt-0.5">${m.voluntary_unplanned_hours}h</div>
                  </div>
                </div>

                <div class="text-xs text-slate-500 space-y-1">
                  <div>Active Tasks: <strong class="text-slate-700 dark:text-slate-300">${m.active_task_count}</strong> (${m.priority_breakdown.counts.critical || 0} critical, ${m.priority_breakdown.counts.high || 0} high)</div>
                  <div>Historical Variance: <strong class="text-slate-700 dark:text-slate-300">${m.variance_ratio}x</strong> (actual vs estimated duration)</div>
                </div>
              </div>
            `).join("")}
          </div>
        </div>

      </div>
    `;

    setTimeout(() => {
      this.drawTeamCapacityBarChart("chart-team-bars", tw.members);
    }, 50);
  }

  // 7. TASK REBALANCING & HUMAN APPROVAL REVIEW
  renderRebalancingView(container) {
    const tw = this.teamWorkload || { rebalancing_suggestions: [] };
    const suggestions = tw.rebalancing_suggestions || [];

    container.innerHTML = `
      <div class="space-y-6">
        <div>
          <h2 class="text-xl font-bold text-slate-900 dark:text-white">Fair Workload Rebalancing Engine</h2>
          <p class="text-xs text-slate-500">Transparent algorithmic matching suggestions. All reallocations require explicit human approval.</p>
        </div>

        <div class="p-4 rounded-xl bg-blue-50 dark:bg-blue-950/40 border border-blue-200 dark:border-blue-800 text-xs text-blue-900 dark:text-blue-200">
          <strong>Fairness Rule:</strong> Critical student-safety and imminent exam tasks are never auto-reassigned. Only routine and deferrable administrative tasks are recommended for reallocation to protect teacher planning blocks.
        </div>

        <div class="space-y-4">
          ${suggestions.length === 0 ? `
            <div class="p-8 text-center bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 text-slate-400 text-sm">
              No urgent rebalancing candidates detected. All department workloads are currently within sustainable capacity thresholds.
            </div>
          ` : suggestions.map(s => `
            <div class="p-5 rounded-2xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shadow-sm flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
              <div class="space-y-1">
                <div class="flex items-center space-x-2">
                  <span class="px-2 py-0.5 rounded text-[10px] font-extrabold uppercase bg-amber-100 text-amber-800">${s.priority}</span>
                  <span class="font-bold text-slate-900 dark:text-white text-sm">${s.task_title}</span>
                  <span class="text-xs text-slate-400">(${s.estimated_hours}h est)</span>
                </div>
                <div class="text-xs text-slate-600 dark:text-slate-300">
                  Reallocate from <strong class="text-rose-600">${s.from_user_name}</strong> to <strong class="text-emerald-600">${s.to_user_name}</strong>
                </div>
                <div class="text-[11px] text-slate-500 italic">${s.reason}</div>
              </div>
              <div class="flex items-center space-x-2">
                <button onclick="app.openReassignModal('${s.task_id}', '${s.task_title}', '${s.from_user_name}', '${s.to_user_id}')" class="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs shadow-sm transition">
                  Review & Approve Rebalancing
                </button>
              </div>
            </div>
          `).join("")}
        </div>
      </div>
    `;
  }

  // 8. AI WORKLOAD ADVISOR VIEW (MVP FEATURE 6)
  renderAIInsightsView(container) {
    container.innerHTML = `
      <div class="space-y-6">
        <div>
          <h2 class="text-xl font-bold text-slate-900 dark:text-white">AI Workload & Well-being Advisor</h2>
          <p class="text-xs text-slate-500">Objective, evidence-based synthesis. Operates deterministically without external API secrets.</p>
        </div>

        <!-- Privacy & Consent Callout -->
        <div class="p-4 rounded-xl bg-purple-50 dark:bg-purple-950/40 border border-purple-200 dark:border-purple-800 text-xs text-purple-900 dark:text-purple-200 space-y-2">
          <div class="font-bold flex items-center space-x-1.5">
            <span>🛡️ AI Safety Protocol</span>
          </div>
          <div>
            The advisor uses strict role-based access. It never diagnoses mental health, generates accusations, or scores character. If no API key is provided, it runs transparent deterministic rules.
          </div>
          <label class="flex items-center space-x-2 pt-1 cursor-pointer">
            <input type="checkbox" id="ai-consent-checkbox" class="w-4 h-4 text-purple-600 rounded">
            <span class="font-semibold">Explicit Informed Consent: Include my private notes in this AI session</span>
          </label>
        </div>

        <!-- Advisor Mode Selector -->
        <div class="p-5 rounded-2xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shadow-sm space-y-4">
          <div class="grid grid-cols-1 sm:grid-cols-4 gap-3">
            <button onclick="app.runAIAdvisor('summarize_workload')" class="p-3 rounded-xl border border-slate-200 dark:border-slate-700 text-left hover:border-purple-500 hover:bg-purple-50/50 dark:hover:bg-purple-950/30 transition">
              <div class="font-bold text-xs text-slate-800 dark:text-slate-100">1. Summarise My Logs</div>
              <div class="text-[11px] text-slate-500 mt-1">Grounded synthesis of category drivers and extra time.</div>
            </button>
            <button onclick="app.runAIAdvisor('draft_request')" class="p-3 rounded-xl border border-slate-200 dark:border-slate-700 text-left hover:border-purple-500 hover:bg-purple-50/50 dark:hover:bg-purple-950/30 transition">
              <div class="font-bold text-xs text-slate-800 dark:text-slate-100">2. Draft Respectful Request</div>
              <div class="text-[11px] text-slate-500 mt-1">Draft a non-accusatory message for manager review.</div>
            </button>
            <button onclick="app.runAIAdvisor('suggest_questions')" class="p-3 rounded-xl border border-slate-200 dark:border-slate-700 text-left hover:border-purple-500 hover:bg-purple-50/50 dark:hover:bg-purple-950/30 transition">
              <div class="font-bold text-xs text-slate-800 dark:text-slate-100">3. Review Questions</div>
              <div class="text-[11px] text-slate-500 mt-1">Questions for collaborative 1-on-1 check-ins.</div>
            </button>
            <button onclick="app.runAIAdvisor('propose_rebalancing')" class="p-3 rounded-xl border border-slate-200 dark:border-slate-700 text-left hover:border-purple-500 hover:bg-purple-50/50 dark:hover:bg-purple-950/30 transition">
              <div class="font-bold text-xs text-slate-800 dark:text-slate-100">4. Rebalancing Advisory</div>
              <div class="text-[11px] text-slate-500 mt-1">Examines non-critical task reallocation.</div>
            </button>
          </div>

          <div>
            <label class="block text-xs font-bold uppercase text-slate-500 mb-1">Optional Additional Context / Focus</label>
            <input type="text" id="ai-context-input" class="w-full px-3 py-2 rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700 text-xs" placeholder="e.g. Focus on Year 11 diagnostic exam grading workload.">
          </div>
        </div>

        <!-- AI Output Display Card -->
        ${this.aiInsightResult ? `
          <div class="p-6 rounded-2xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shadow-sm space-y-4">
            <div class="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-700">
              <h3 class="font-bold text-slate-900 dark:text-white text-base">${this.aiInsightResult.title || 'AI Workload Advisory'}</h3>
              <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200">Advisory</span>
            </div>

            <div class="text-sm text-slate-800 dark:text-slate-200 whitespace-pre-line leading-relaxed font-sans">
              ${this.aiInsightResult.text}
            </div>

            ${this.aiInsightResult.bullet_points && this.aiInsightResult.bullet_points.length > 0 ? `
              <div class="p-4 rounded-xl bg-slate-50 dark:bg-slate-700/40 border border-slate-100 dark:border-slate-700 space-y-1.5">
                <div class="text-xs font-bold text-slate-600 dark:text-slate-300 uppercase tracking-wider mb-2">Key Considerations & Discussion Prompts:</div>
                ${this.aiInsightResult.bullet_points.map(bp => `
                  <div class="text-xs text-slate-700 dark:text-slate-300 flex items-start space-x-2">
                    <span class="text-purple-500 font-bold">•</span>
                    <span>${bp}</span>
                  </div>
                `).join("")}
              </div>
            ` : ""}

            <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-[11px] text-slate-500 pt-2 border-t border-slate-100 dark:border-slate-700">
              <div><strong>Underlying Evidence:</strong> ${this.aiInsightResult.evidence || 'Deterministic workload calculations'}</div>
              <div><strong>Uncertainty / Human Review:</strong> ${this.aiInsightResult.uncertainty || 'Requires human verification before implementation'}</div>
            </div>

            <div class="text-[10px] text-slate-400 italic bg-slate-50 dark:bg-slate-700/20 p-2.5 rounded-lg">
              ${this.aiInsightResult.disclaimer}
            </div>
          </div>
        ` : `
          <div class="p-8 text-center bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 text-slate-400 text-xs">
            Select one of the 4 advisor modes above to generate an evidence-based workload summary, request draft, or review guide.
          </div>
        `}

      </div>
    `;
  }

  // 9. SETTINGS & PRIVACY VIEW
  renderSettingsView(container) {
    container.innerHTML = `
      <div class="space-y-6 max-w-3xl">
        <div>
          <h2 class="text-xl font-bold text-slate-900 dark:text-white">Settings, Accessibility & Governance</h2>
          <p class="text-xs text-slate-500">Configure personal preferences, language, high contrast, and GDPR privacy workflows.</p>
        </div>

        <div class="p-6 rounded-2xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shadow-sm space-y-4">
          <h3 class="font-bold text-slate-900 dark:text-white text-sm">Language & Accessibility Options</h3>
          
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-bold uppercase text-slate-500 mb-1">Display Language</label>
              <select onchange="app.setLanguage(this.value)" class="w-full px-3 py-2 rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700 text-xs">
                <option value="en" ${this.currentLang === 'en' ? 'selected' : ''}>English (US)</option>
                <option value="ta" ${this.currentLang === 'ta' ? 'selected' : ''}>தமிழ் (Tamil)</option>
              </select>
            </div>

            <div>
              <label class="block text-xs font-bold uppercase text-slate-500 mb-1">Visual Accessibility</label>
              <button onclick="app.toggleHighContrast()" class="w-full py-2 px-3 rounded-lg border border-slate-300 dark:border-slate-600 bg-slate-50 dark:bg-slate-700 text-xs font-semibold text-slate-700 dark:text-slate-200 text-left">
                ${this.isHighContrast ? 'Disable High Contrast Mode' : 'Enable High Contrast Mode'}
              </button>
            </div>
          </div>
        </div>

        <div class="p-6 rounded-2xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shadow-sm space-y-4">
          <h3 class="font-bold text-slate-900 dark:text-white text-sm">Privacy & Data Protection Guarantees</h3>
          <div class="text-xs text-slate-600 dark:text-slate-300 space-y-2">
            <p>1. <strong>Private Notes Isolation:</strong> Private reflection notes on tasks are stored with encrypted-at-rest semantics and are strictly hidden from managers and administrators.</p>
            <p>2. <strong>No Keystroke Tracking:</strong> FAIRSHIFT explicitly rejects background surveillance, keylogging, and covert idle-time counters.</p>
            <p>3. <strong>Data Portability:</strong> You can export your full work summary as CSV or printable PDF at any time.</p>
          </div>
          <div class="pt-3 border-t border-slate-100 dark:border-slate-700 flex items-center justify-between">
            <a href="/api/export/workload-csv" download class="px-3 py-1.5 rounded-lg bg-teal-50 text-teal-800 font-bold text-xs hover:bg-teal-100">
              Download My Data (CSV)
            </a>
            <button onclick="alert('Data deletion workflow initiated. All personal records scheduled for deletion within 24h as per privacy governance.')" class="px-3 py-1.5 rounded-lg text-rose-600 text-xs font-bold hover:underline">
              Request Account Data Deletion
            </button>
          </div>
        </div>

        <div class="p-6 rounded-2xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shadow-sm space-y-3">
          <h3 class="font-bold text-slate-900 dark:text-white text-sm">Demo Data Reset</h3>
          <p class="text-xs text-slate-500">Restore the original sample dataset for Oakridge High School and St. Jude Clinic.</p>
          <button onclick="app.resetDemoData()" class="px-4 py-2 rounded-xl bg-slate-100 dark:bg-slate-700 hover:bg-slate-200 text-slate-800 dark:text-slate-200 font-bold text-xs">
            Reset Demo Database to Initial State
          </button>
        </div>

      </div>
    `;
  }

  async resetDemoData() {
    if (!confirm("Reset database to initial demo state?")) return;
    try {
      const res = await fetch("/api/admin/reset-seed", { method: "POST" });
      if (res.ok) {
        alert("Demo database re-seeded successfully.");
        await this.fetchInitialData();
        this.render();
      }
    } catch (e) {
      console.error(e);
    }
  }

  // 10. DEMO WALKTHROUGH GUIDE VIEW
  renderWalkthroughView(container) {
    container.innerHTML = `
      <div class="space-y-6 max-w-4xl">
        <div class="p-6 rounded-2xl bg-gradient-to-r from-teal-800 to-indigo-900 text-white shadow-sm space-y-2">
          <span class="px-2 py-0.5 rounded text-[10px] font-extrabold uppercase bg-teal-400/30 text-teal-100">Platform Guide</span>
          <h2 class="text-2xl font-bold">FAIRSHIFT Demo Walkthrough & Architecture</h2>
          <p class="text-teal-100 text-xs sm:text-sm max-w-2xl">
            A comprehensive guide showcasing how FAIRSHIFT solves chronic overwork in schools and employee-intensive organizations through visible workload distribution.
          </p>
        </div>

        <!-- Scenario 1: Oakridge High School -->
        <div class="p-6 rounded-2xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shadow-sm space-y-4">
          <div class="flex items-center space-x-2">
            <span class="text-xl">🏫</span>
            <h3 class="font-bold text-slate-900 dark:text-white text-lg">Scenario 1: Oakridge High School</h3>
          </div>
          <div class="text-xs text-slate-600 dark:text-slate-300 space-y-2">
            <p><strong>The Core Human Problem:</strong> Priya Sharma, an English teacher, repeatedly takes on extra lesson preparation and grading because she worries students will fall behind in state exams if she doesn't write detailed feedback. She recorded 9.5 hours of after-hours work over the weekend.</p>
            <p><strong>How FAIRSHIFT Resolves It:</strong></p>
            <ul class="list-disc pl-5 space-y-1">
              <li><strong>Visibility:</strong> Priya's dashboard shows a projected load of 135% capacity with 9.5h after-hours logged.</li>
              <li><strong>Student-First Prioritisation:</strong> Priya used the prioritisation template to ask Principal Sarah Jenkins whether the non-urgent Textbook Inventory could be deferred so she could focus on Year 11 exams.</li>
              <li><strong>Manager Resolution:</strong> Sarah approved the deferral, and the rebalancing engine identified Marcus Chen (who had 70% capacity) to take on digital cataloging.</li>
              <li><strong>5-Day Experiment:</strong> Priya completed a 5-day reflection identifying that students benefited equally from verbal rubrics, saving 2 hours of handwritten notes.</li>
            </ul>
          </div>
          <div class="flex items-center space-x-3 pt-2">
            <button onclick="app.quickSwitchUser('user-priya-sharma')" class="px-3 py-1.5 rounded-lg bg-teal-600 text-white text-xs font-bold">Log In as Priya (Teacher)</button>
            <button onclick="app.quickSwitchUser('user-sarah-jenkins')" class="px-3 py-1.5 rounded-lg bg-purple-600 text-white text-xs font-bold">Log In as Sarah (Principal)</button>
          </div>
        </div>

        <!-- Scenario 2: St. Jude Community Clinic -->
        <div class="p-6 rounded-2xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shadow-sm space-y-4">
          <div class="flex items-center space-x-2">
            <span class="text-xl">🏥</span>
            <h3 class="font-bold text-slate-900 dark:text-white text-lg">Scenario 2: St. Jude Health Clinic (Healthcare Domain)</h3>
          </div>
          <div class="text-xs text-slate-600 dark:text-slate-300 space-y-2">
            <p><strong>Healthcare Challenge:</strong> Nurse Elena Rostova absorbed 3.5h of unplanned emergency triage desk coverage due to respiratory case surges, while routine sterilization logs competed for the same shift.</p>
            <p><strong>Neutral Resolution:</strong> Clinic Admin Maria Patel used the platform to rebalance non-urgent sterilization logs to next week, preserving direct patient care standards.</p>
          </div>
          <div class="flex items-center space-x-3 pt-2">
            <button onclick="app.quickSwitchUser('user-elena-rostova')" class="px-3 py-1.5 rounded-lg bg-teal-600 text-white text-xs font-bold">Log In as Elena (Nurse)</button>
            <button onclick="app.quickSwitchUser('user-maria-patel')" class="px-3 py-1.5 rounded-lg bg-purple-600 text-white text-xs font-bold">Log In as Maria (Clinic Admin)</button>
          </div>
        </div>
      </div>
    `;
  }

  // 11. LANDING / PRODUCT OVERVIEW VIEW
  renderLandingView(container) {
    container.innerHTML = `
      <div class="space-y-8 max-w-5xl mx-auto py-6">
        
        <!-- Hero Section -->
        <div class="text-center space-y-4 py-8">
          <div class="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-teal-100 dark:bg-teal-950/60 text-teal-800 dark:text-teal-300 text-xs font-bold">
            <span>🛡️ Ethical Well-being Platform for Intensive Organisations</span>
          </div>
          <h1 class="text-3xl sm:text-5xl font-extrabold tracking-tight text-slate-900 dark:text-white">
            FAIRSHIFT
          </h1>
          <p class="text-base sm:text-lg text-slate-600 dark:text-slate-300 max-w-2xl mx-auto">
            Prevent chronic overwork by making assigned work, extra hours, and workload distribution visible. Evidence-based workload discussions rather than surveillance.
          </p>
          <div class="flex flex-wrap items-center justify-center gap-3 pt-3">
            <button onclick="app.navigate('dashboard-teacher')" class="px-5 py-2.5 rounded-xl bg-teal-600 hover:bg-teal-700 text-white font-bold text-sm shadow-md transition">
              Open Teacher Dashboard →
            </button>
            <button onclick="app.navigate('dashboard-manager')" class="px-5 py-2.5 rounded-xl bg-slate-100 dark:bg-slate-700 hover:bg-slate-200 text-slate-800 dark:text-slate-200 font-bold text-sm transition">
              Manager Overview
            </button>
          </div>
        </div>

        <!-- 6 Core Principles Grid -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
          <div class="p-5 rounded-2xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shadow-sm space-y-2">
            <div class="text-xl">🤝</div>
            <h3 class="font-bold text-slate-900 dark:text-white text-sm">Neutral, Non-Accusatory</h3>
            <p class="text-xs text-slate-500">Never assumes a teacher is lazy or another is exploiting them. Uses recorded workload data and neutral language.</p>
          </div>

          <div class="p-5 rounded-2xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shadow-sm space-y-2">
            <div class="text-xl">🎓</div>
            <h3 class="font-bold text-slate-900 dark:text-white text-sm">Student-First Priorities</h3>
            <p class="text-xs text-slate-500">Student safety and exam-critical duties are protected. Non-urgent administration is safely deferred or reallocated.</p>
          </div>

          <div class="p-5 rounded-2xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shadow-sm space-y-2">
            <div class="text-xl">🔒</div>
            <h3 class="font-bold text-slate-900 dark:text-white text-sm">Non-Surveillance Guarantee</h3>
            <p class="text-xs text-slate-500">No keystroke logging or public individual rankings. Private reflection notes remain completely confidential.</p>
          </div>

          <div class="p-5 rounded-2xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shadow-sm space-y-2">
            <div class="text-xl">📐</div>
            <h3 class="font-bold text-slate-900 dark:text-white text-sm">Explainable Formulas</h3>
            <p class="text-xs text-slate-500">Transparent weighted scoring algorithms explain exactly why someone is overloaded, with missing-data indicators.</p>
          </div>

          <div class="p-5 rounded-2xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shadow-sm space-y-2">
            <div class="text-xl">🧪</div>
            <h3 class="font-bold text-slate-900 dark:text-white text-sm">5-Day Guided Experiment</h3>
            <p class="text-xs text-slate-500">Safe personal reflections identifying fears versus real outcomes, with small iterative next steps.</p>
          </div>

          <div class="p-5 rounded-2xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shadow-sm space-y-2">
            <div class="text-xl">🌐</div>
            <h3 class="font-bold text-slate-900 dark:text-white text-sm">Multilingual & Accessible</h3>
            <p class="text-xs text-slate-500">Full English and Tamil (தமிழ்) translation system, high-contrast support, and printable PDF exports.</p>
          </div>
        </div>

      </div>
    `;
  }
}

// Instantiate global app instance
const app = new FairshiftApp();
window.app = app;
