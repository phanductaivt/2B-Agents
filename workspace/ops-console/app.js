const state = {
  projects: [],
  currentProject: "",
  confirmationsProject: "",
  docsProject: "",
  actionsProject: "",
  confirmationRows: [],
  selectedConfirmationId: "",
  docsRows: [],
  selectedDocPath: "",
  selectedDocEditable: false,
  selectedDocOriginal: "",
};

function byId(id) {
  return document.getElementById(id);
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

async function fetchJson(path, options = undefined) {
  const response = await fetch(path, options);
  let data = {};
  try {
    data = await response.json();
  } catch (_error) {
    data = {};
  }
  if (!response.ok) {
    throw new Error(data.error || `Request failed: ${path}`);
  }
  return data;
}

function setMessage(id, text) {
  byId(id).textContent = text;
}

function setSelectOptions(id, optionsHtml, selectedValue) {
  const select = byId(id);
  select.innerHTML = optionsHtml;
  if (selectedValue !== undefined) {
    select.value = selectedValue;
  }
}

function renderMetrics(overview) {
  const container = byId("overview-metrics");
  const metrics = [
    ["Total Projects", overview.total_projects ?? 0],
    ["Active Projects", overview.active_projects ?? 0],
    ["Blocked Projects", overview.blocked_projects ?? 0],
    ["Done Projects", overview.done_projects ?? 0],
    ["Last Updated", overview.last_updated ?? "-"],
  ];
  container.innerHTML = metrics
    .map(
      ([label, value]) =>
        `<div class="metric-card"><div class="metric-label">${escapeHtml(label)}</div><div class="metric-value">${escapeHtml(value)}</div></div>`
    )
    .join("");
}

function renderOverviewProjects(projects) {
  const tbody = byId("overview-project-table").querySelector("tbody");
  tbody.innerHTML = projects
    .map((item) => {
      const summary = item.project_summary || {};
      const execution = item.execution_snapshot || {};
      return `<tr>
        <td>${escapeHtml(summary.project_name || item.project_name || "-")}</td>
        <td>${escapeHtml(summary.project_phase || "-")}</td>
        <td>${escapeHtml(summary.project_status || "-")}</td>
        <td>${escapeHtml(summary.project_readiness ?? 0)}%</td>
        <td>${escapeHtml(execution.current_execution_stage || "-")}</td>
        <td>${escapeHtml(execution.current_execution_owner || "-")}</td>
        <td>${escapeHtml(summary.stale_items_count ?? 0)}</td>
        <td>${escapeHtml(summary.needs_rerun_items_count ?? 0)}</td>
      </tr>`;
    })
    .join("");
}

function renderProjectSelects(projects) {
  const options = projects
    .map((item) => {
      const name = item.project_name || "";
      return `<option value="${escapeHtml(name)}">${escapeHtml(name)}</option>`;
    })
    .join("");

  if (!state.currentProject && projects.length > 0) {
    const first = projects[0].project_name;
    state.currentProject = first;
    state.confirmationsProject = first;
    state.docsProject = first;
    state.actionsProject = first;
  }

  setSelectOptions("project-select", options, state.currentProject);
  setSelectOptions("confirmation-project-select", options, state.confirmationsProject || state.currentProject);
  setSelectOptions("docs-project-select", options, state.docsProject || state.currentProject);
}

function renderProjectCards(bundle) {
  const summary = bundle.project_summary || {};
  const execution = bundle.execution_snapshot || {};
  byId("project-summary").innerHTML = `
    <div class="card">
      <h3>Project Summary</h3>
      <p><strong>Name:</strong> ${escapeHtml(summary.project_name || "-")}</p>
      <p><strong>Project Phase:</strong> ${escapeHtml(summary.project_phase || "-")}</p>
      <p><strong>Project Owner:</strong> ${escapeHtml(summary.project_owner || "-")}</p>
      <p><strong>Project Status:</strong> ${escapeHtml(summary.project_status || "-")}</p>
      <p><strong>Project Readiness:</strong> ${escapeHtml(summary.project_readiness ?? 0)}%</p>
      <p><strong>Last Update:</strong> ${escapeHtml(summary.last_update || "-")}</p>
      <p><strong>Stale Docs:</strong> ${escapeHtml(summary.stale_items_count ?? 0)}</p>
      <p><strong>Needs Rerun:</strong> ${escapeHtml(summary.needs_rerun_items_count ?? 0)}</p>
    </div>
    <div class="card">
      <h3>Execution Snapshot</h3>
      <p><strong>Current Execution Stage:</strong> ${escapeHtml(execution.current_execution_stage || "-")}</p>
      <p><strong>Current Execution Owner:</strong> ${escapeHtml(execution.current_execution_owner || "-")}</p>
      <p><strong>Artifact Completion Rate:</strong> ${escapeHtml(execution.artifact_completion_rate ?? 0)}%</p>
      <p><strong>Execution Health:</strong> ${escapeHtml(execution.execution_health || "-")}</p>
      <p><strong>Gate Summary:</strong> ${escapeHtml(execution.gate_summary || "-")}</p>
      <p><strong>Blocked Reason:</strong> ${escapeHtml(execution.blocked_reason || "-")}</p>
    </div>
  `;
}

function renderRequirements(rows) {
  const tbody = byId("requirements-table").querySelector("tbody");
  tbody.innerHTML = rows
    .map(
      (item) => `<tr>
        <td>${escapeHtml(item.requirement_name || "-")}</td>
        <td>${escapeHtml(item.processing_status || "-")}</td>
        <td>${escapeHtml(item.input_change_state || "-")}</td>
        <td>${escapeHtml(item.last_processed_at || "-")}</td>
        <td>${item.rerun_needed ? "Yes" : "No"}</td>
      </tr>`
    )
    .join("");
}

function renderTasks(rows) {
  const tbody = byId("tasks-table").querySelector("tbody");
  tbody.innerHTML = rows
    .map(
      (item) => `<tr>
        <td>${escapeHtml(item.task_id || "-")}</td>
        <td>${escapeHtml(item.artifact || "-")}</td>
        <td>${escapeHtml(item.stage || "-")}</td>
        <td>${escapeHtml(item.agent_owner || "-")}</td>
        <td>${escapeHtml(item.status || "-")}</td>
        <td>${escapeHtml(item.priority || "-")}</td>
      </tr>`
    )
    .join("");
}

function renderConfirmationFilterOptions(filters) {
  const typeFilter = byId("confirmation-type-filter");
  const ownerFilter = byId("confirmation-owner-filter");
  const currentType = typeFilter.value || "all";
  const currentOwner = ownerFilter.value || "all";
  const typeOptions = ["<option value=\"all\">All</option>"]
    .concat((filters.type_options || []).map((x) => `<option value="${escapeHtml(x)}">${escapeHtml(x)}</option>`))
    .join("");
  const ownerOptions = ["<option value=\"all\">All</option>"]
    .concat((filters.owner_options || []).map((x) => `<option value="${escapeHtml(x)}">${escapeHtml(x)}</option>`))
    .join("");
  typeFilter.innerHTML = typeOptions;
  ownerFilter.innerHTML = ownerOptions;
  typeFilter.value = currentType;
  ownerFilter.value = currentOwner;
}

function renderConfirmationsRows(rows) {
  state.confirmationRows = rows;
  const tbody = byId("confirmations-table").querySelector("tbody");
  tbody.innerHTML = rows
    .map(
      (item) => `<tr data-confirmation-id="${escapeHtml(item.confirmation_id || "")}">
        <td>${escapeHtml(item.confirmation_id || "-")}</td>
        <td>${escapeHtml(item.status || "-")}</td>
        <td>${escapeHtml(item.type || "-")}</td>
        <td>${escapeHtml(item.owner || "-")}</td>
        <td>${escapeHtml(item.title || "-")}</td>
      </tr>`
    )
    .join("");
  Array.from(tbody.querySelectorAll("tr")).forEach((row) => {
    row.addEventListener("click", () => {
      const id = row.getAttribute("data-confirmation-id") || "";
      openConfirmationDetail(id);
    });
  });
}

function openConfirmationDetail(itemId) {
  const item = state.confirmationRows.find((entry) => String(entry.confirmation_id) === String(itemId));
  if (!item) {
    byId("confirmation-detail").textContent = "Select a confirmation item.";
    byId("confirmation-editor").classList.add("hidden");
    state.selectedConfirmationId = "";
    return;
  }
  state.selectedConfirmationId = itemId;
  byId("confirmation-detail").innerHTML = `
    <p><strong>ID:</strong> ${escapeHtml(item.confirmation_id || "-")}</p>
    <p><strong>Requirement:</strong> ${escapeHtml(item.requirement || "-")}</p>
    <p><strong>Artifact:</strong> ${escapeHtml(item.artifact || "-")}</p>
    <p><strong>Type:</strong> ${escapeHtml(item.type || "-")}</p>
    <p><strong>Title:</strong> ${escapeHtml(item.title || "-")}</p>
    <p><strong>Description:</strong> ${escapeHtml(item.description || "-")}</p>
    <p><strong>Blocked Reason:</strong> ${escapeHtml(item.blocked_reason || "-")}</p>
    <p><strong>Impact:</strong> ${escapeHtml((item.impact || []).join(", ") || "-")}</p>
    <p><strong>Suggested Action:</strong> ${escapeHtml(item.suggested_action || "-")}</p>
    <p><strong>Recommendation Source:</strong> ${escapeHtml(item.recommendation_source || "-")}</p>
    <p><strong>Recommendation Label:</strong> ${escapeHtml(item.recommendation_label || "-")}</p>
    <p><strong>Decision Authority:</strong> ${escapeHtml(item.decision_authority || "-")}</p>
    <p><strong>Data State:</strong> ${escapeHtml(item.data_state || "-")}</p>
    <p><strong>Linked Files:</strong> ${escapeHtml((item.linked_files || []).join(", ") || "-")}</p>
    <p><strong>Current Decision:</strong> ${escapeHtml(item.decision || "-")}</p>
    <p><strong>Decision Note:</strong> ${escapeHtml(item.decision_note || "-")}</p>
    <p><strong>Confirmed By:</strong> ${escapeHtml(item.confirmed_by || "-")}</p>
    <p><strong>Confirmed At:</strong> ${escapeHtml(item.confirmed_at || "-")}</p>
    <p><strong>Final Decision By:</strong> ${escapeHtml(item.final_decision_by || "-")}</p>
  `;
  byId("confirmation-detail-status").value = item.status || "pending";
  byId("confirmation-detail-decision").value = item.decision || "";
  byId("confirmation-detail-note").value = item.decision_note || "";
  byId("confirmation-detail-by").value = item.confirmed_by || "";
  byId("confirmation-detail-at").value = item.confirmed_at || "";
  byId("confirmation-editor").classList.remove("hidden");
}

function confirmationPayload(action = "save") {
  return {
    project: state.confirmationsProject,
    item_id: state.selectedConfirmationId,
    action,
    status: byId("confirmation-detail-status").value,
    decision: byId("confirmation-detail-decision").value,
    decision_note: byId("confirmation-detail-note").value,
    confirmed_by: byId("confirmation-detail-by").value,
    confirmed_at: byId("confirmation-detail-at").value,
  };
}

async function updateConfirmation(action = "save") {
  if (!state.selectedConfirmationId) {
    throw new Error("Select a confirmation item first.");
  }
  await fetchJson("/api/confirmations/update", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(confirmationPayload(action)),
  });
}

async function loadConfirmations() {
  const project = state.confirmationsProject || state.currentProject;
  if (!project) {
    return;
  }
  const status = byId("confirmation-status-filter").value || "all";
  const type = byId("confirmation-type-filter").value || "all";
  const owner = byId("confirmation-owner-filter").value || "all";
  const search = encodeURIComponent(byId("confirmation-search").value || "");
  const payload = await fetchJson(
    `/api/confirmations?project=${encodeURIComponent(project)}&status=${encodeURIComponent(status)}&type=${encodeURIComponent(type)}&owner=${encodeURIComponent(owner)}&search=${search}`
  );
  renderConfirmationFilterOptions(payload.filters || {});
  renderConfirmationsRows(payload.confirmations || []);
  if (state.selectedConfirmationId) {
    openConfirmationDetail(state.selectedConfirmationId);
  }
}

async function refreshConfirmationsFromStatus() {
  await fetchJson("/api/confirmations/refresh", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ project: state.confirmationsProject }),
  });
}

function renderDocsGroupOptions(groups) {
  const select = byId("docs-group-filter");
  const current = select.value || "all";
  select.innerHTML = ["<option value=\"all\">All</option>"]
    .concat((groups || []).map((group) => `<option value="${escapeHtml(group)}">${escapeHtml(group)}</option>`))
    .join("");
  if ((groups || []).includes(current) || current === "all") {
    select.value = current;
  } else {
    select.value = "all";
  }
}

function renderDocsList(rows) {
  state.docsRows = rows;
  const list = byId("docs-list");
  list.innerHTML = "";
  rows.forEach((doc) => {
    const li = document.createElement("li");
    const tag = doc.editable ? "Editable" : "View-only";
    const stale = doc.stale_state || "fresh";
    const recommendation = doc.rerun_recommendation || "none";
    li.textContent = `${doc.file_path} (${doc.group}, ${tag}, ${stale}, ${recommendation})`;
    li.addEventListener("click", async () => {
      await openDoc(doc.file_path);
    });
    list.appendChild(li);
  });
}

function renderDocsSummary(payload) {
  const stale = payload.stale_items_count ?? 0;
  const rerun = payload.needs_rerun_items_count ?? 0;
  byId("docs-staleness-summary").textContent =
    `Stale docs: ${stale} | Needs rerun: ${rerun} (recommendation only, no auto-rerun).`;
}

function setDocEditorMode(editable) {
  state.selectedDocEditable = editable;
  byId("doc-editor").readOnly = !editable;
  byId("doc-save").disabled = !editable;
}

async function openDoc(path) {
  const payload = await fetchJson(
    `/api/doc-preview?project=${encodeURIComponent(state.docsProject)}&path=${encodeURIComponent(path)}`
  );
  const preview = payload.preview || {};
  state.selectedDocPath = preview.file_path || path;
  state.selectedDocOriginal = preview.content || "";
  byId("docs-meta").innerHTML = `
    <p><strong>Path:</strong> ${escapeHtml(preview.file_path || "-")}</p>
    <p><strong>Group:</strong> ${escapeHtml(preview.group || "-")}</p>
    <p><strong>Doc Type:</strong> ${escapeHtml(preview.doc_type || "-")}</p>
    <p><strong>Editable:</strong> ${preview.editable ? "true" : "false"}</p>
    <p><strong>Source Layer:</strong> ${escapeHtml(preview.source_layer || "-")}</p>
    <p><strong>Last Modified:</strong> ${escapeHtml(preview.last_modified || "-")}</p>
    <p><strong>Stale State:</strong> ${escapeHtml(preview.stale_state || "fresh")}</p>
    <p><strong>Rerun Recommendation:</strong> ${escapeHtml(preview.rerun_recommendation || "none")}</p>
    <p><strong>Impacted Requirements:</strong> ${escapeHtml((preview.impacted_requirements || []).join(", ") || "-")}</p>
    <p><strong>Impacted Artifacts:</strong> ${escapeHtml((preview.impacted_artifacts || []).join(", ") || "-")}</p>
    <p><strong>Impacted Stages:</strong> ${escapeHtml((preview.impacted_stages || []).join(", ") || "-")}</p>
    <p><strong>Impact Reason:</strong> ${escapeHtml((preview.impact_reason || []).join(" | ") || "-")}</p>
    <p><strong>Reason:</strong> ${escapeHtml(preview.protected_reason || "-")}</p>
  `;
  byId("doc-editor").value = preview.content || "";
  setDocEditorMode(Boolean(preview.editable));
  setMessage("docs-message", "");
}

async function loadDocs() {
  if (!state.docsProject) {
    return;
  }
  const group = byId("docs-group-filter").value || "all";
  const payload = await fetchJson(
    `/api/docs?project=${encodeURIComponent(state.docsProject)}&group=${encodeURIComponent(group)}`
  );
  renderDocsSummary(payload);
  renderDocsGroupOptions(payload.groups || []);
  renderDocsList(payload.documents || []);
}

async function saveDoc() {
  if (!state.selectedDocPath) {
    throw new Error("Select a document first.");
  }
  if (!state.selectedDocEditable) {
    throw new Error("This document is view-only.");
  }
  const content = byId("doc-editor").value;
  return fetchJson("/api/doc-save", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      project: state.docsProject,
      path: state.selectedDocPath,
      content,
    }),
  });
}

function renderActions(capabilities, context) {
  const card = byId("actions-card");
  const items = capabilities.capabilities || [];
  const projects = state.projects.map((item) => item.project_name).filter(Boolean);
  if (!state.actionsProject && projects.length > 0) {
    state.actionsProject = projects[0];
  }
  const actionProject = state.actionsProject || "";
  const reqOptions = (context.requirement_options || [])
    .map((name) => `<option value="${escapeHtml(name)}">${escapeHtml(name)}</option>`)
    .join("");
  const stageOptions = (context.stage_options || [])
    .map((name) => `<option value="${escapeHtml(name)}">${escapeHtml(name)}</option>`)
    .join("");
  const staleRows = (context.stale_documents || [])
    .map(
      (row) =>
        `<tr>
          <td>${escapeHtml(row.file_path || "-")}</td>
          <td>${escapeHtml(row.stale_state || "-")}</td>
          <td>${escapeHtml(row.rerun_recommendation || "-")}</td>
          <td>${escapeHtml((row.impacted_requirements || []).join(", ") || "-")}</td>
          <td>${escapeHtml((row.impacted_stages || []).join(", ") || "-")}</td>
        </tr>`
    )
    .join("");

  card.innerHTML = `
    <p><strong>Mode:</strong> ${escapeHtml(capabilities.mode || "-")}</p>
    <p><strong>Actions Enabled:</strong> ${capabilities.actions_enabled ? "Yes" : "No"}</p>
    <ul>
      ${items
        .map(
          (item) =>
            `<li><strong>${escapeHtml(item.name)}</strong> - ${item.enabled ? "Enabled" : "Disabled"} (${escapeHtml(item.reason || item.note || "")})</li>`
        )
        .join("")}
    </ul>
    <hr />
    <h3>Controlled Rerun (Phase 3B)</h3>
    <div class="controls-grid">
      <label for="actions-project-select">Project:</label>
      <select id="actions-project-select">
        ${projects
          .map(
            (name) =>
              `<option value="${escapeHtml(name)}" ${name === actionProject ? "selected" : ""}>${escapeHtml(name)}</option>`
          )
          .join("")}
      </select>
      <label for="rerun-action-select">Rerun Level:</label>
      <select id="rerun-action-select">
        <option value="rerun_project">Rerun Project</option>
        <option value="rerun_requirement">Rerun Requirement</option>
        <option value="rerun_from_stage">Rerun From Stage</option>
      </select>
      <label for="rerun-requirement-select">Requirement:</label>
      <select id="rerun-requirement-select">
        <option value="">(optional)</option>
        ${reqOptions}
      </select>
      <label for="rerun-stage-select">Stage:</label>
      <select id="rerun-stage-select">
        <option value="">(optional)</option>
        ${stageOptions}
      </select>
      <button id="actions-check-btn">Check Eligibility</button>
      <button id="actions-run-btn">Run Action</button>
    </div>
    <p><strong>Stale docs:</strong> ${escapeHtml(context.stale_items_count ?? 0)} |
    <strong>Needs rerun:</strong> ${escapeHtml(context.needs_rerun_items_count ?? 0)}</p>
    <p><strong>Recommended requirements:</strong> ${escapeHtml((context.recommended_requirements || []).join(", ") || "-")}</p>
    <p><strong>Recommended stages:</strong> ${escapeHtml((context.recommended_stages || []).join(", ") || "-")}</p>
    <div id="actions-message" class="muted-text"></div>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Document</th>
            <th>Stale State</th>
            <th>Recommendation</th>
            <th>Impacted Requirements</th>
            <th>Impacted Stages</th>
          </tr>
        </thead>
        <tbody>${staleRows || `<tr><td colspan="5">No stale items.</td></tr>`}</tbody>
      </table>
    </div>
    <div id="actions-output" class="meta-box"></div>
  `;
}

function rerunPayloadFromForm() {
  return {
    project: byId("actions-project-select").value || state.actionsProject || "",
    action: byId("rerun-action-select").value || "rerun_project",
    requirement: byId("rerun-requirement-select").value || "",
    stage: byId("rerun-stage-select").value || "",
  };
}

function setActionsMessage(text) {
  const node = byId("actions-message");
  if (node) {
    node.textContent = text;
  }
}

function setActionsOutput(text) {
  const node = byId("actions-output");
  if (node) {
    node.textContent = text;
  }
}

async function loadActionsContext(project) {
  return fetchJson(`/api/actions/context?project=${encodeURIComponent(project)}`);
}

async function refreshActionsWorkspace() {
  const project = state.actionsProject || state.currentProject;
  if (!project) {
    return;
  }
  const [capabilities, context] = await Promise.all([
    fetchJson(`/api/actions?project=${encodeURIComponent(project)}`),
    loadActionsContext(project),
  ]);
  renderActions(capabilities, context);
  bindActionsControls();
}

async function refreshAfterAction() {
  await refreshOverviewData();
  if (state.currentProject) {
    await loadProject(state.currentProject);
  }
  if (state.confirmationsProject) {
    await loadConfirmations();
  }
  if (state.docsProject) {
    await loadDocs();
  }
  await refreshActionsWorkspace();
}

function bindActionsControls() {
  const projectSelect = byId("actions-project-select");
  const checkButton = byId("actions-check-btn");
  const runButton = byId("actions-run-btn");
  if (!projectSelect || !checkButton || !runButton) {
    return;
  }

  projectSelect.addEventListener("change", async (event) => {
    state.actionsProject = event.target.value;
    await refreshActionsWorkspace();
  });

  checkButton.addEventListener("click", async () => {
    try {
      const payload = rerunPayloadFromForm();
      setActionsMessage("Checking eligibility...");
      const result = await fetchJson("/api/actions/check", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      setActionsMessage(result.eligible ? "Eligible." : `Blocked: ${result.reason}`);
      setActionsOutput(JSON.stringify(result, null, 2));
    } catch (error) {
      setActionsMessage(`Eligibility check failed: ${error.message}`);
    }
  });

  runButton.addEventListener("click", async () => {
    try {
      const payload = rerunPayloadFromForm();
      setActionsMessage("Executing action...");
      const result = await fetchJson("/api/actions/execute", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (result.executed) {
        setActionsMessage("Action completed successfully.");
        setActionsOutput(JSON.stringify(result, null, 2));
        await refreshAfterAction();
      } else {
        setActionsMessage(
          result.blocked_reason ? `Blocked: ${result.blocked_reason}` : (result.message || "Action failed.")
        );
        setActionsOutput(JSON.stringify(result, null, 2));
      }
    } catch (error) {
      setActionsMessage(`Action failed: ${error.message}`);
    }
  });
}

async function loadProject(projectName) {
  const detailPayload = await fetchJson(`/api/project?name=${encodeURIComponent(projectName)}`);
  const reqPayload = await fetchJson(`/api/requirements?project=${encodeURIComponent(projectName)}`);
  const taskPayload = await fetchJson(`/api/tasks?project=${encodeURIComponent(projectName)}`);
  renderProjectCards(detailPayload.project || {});
  renderRequirements(reqPayload.requirements || []);
  renderTasks(taskPayload.tasks || []);
}

function bindTabs() {
  const tabs = document.querySelectorAll(".tab");
  const panels = document.querySelectorAll(".panel");
  tabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      tabs.forEach((item) => item.classList.remove("active"));
      panels.forEach((item) => item.classList.remove("active"));
      tab.classList.add("active");
      byId(tab.dataset.tab).classList.add("active");
    });
  });
}

async function refreshOverviewData() {
  const overviewPayload = await fetchJson("/api/overview");
  renderMetrics(overviewPayload.overview || {});
  renderOverviewProjects(overviewPayload.projects || []);
  state.projects = overviewPayload.projects || [];
  renderProjectSelects(state.projects);
}

function bindProjectOpsControls() {
  byId("project-select").addEventListener("change", async (event) => {
    state.currentProject = event.target.value;
    await loadProject(state.currentProject);
  });
}

function bindConfirmationControls() {
  const load = async () => {
    try {
      await loadConfirmations();
    } catch (error) {
      setMessage("confirmations-message", `Failed to load confirmations: ${error.message}`);
    }
  };

  byId("confirmation-project-select").addEventListener("change", async (event) => {
    state.confirmationsProject = event.target.value;
    state.selectedConfirmationId = "";
    await load();
  });
  byId("confirmation-status-filter").addEventListener("change", load);
  byId("confirmation-type-filter").addEventListener("change", load);
  byId("confirmation-owner-filter").addEventListener("change", load);
  byId("confirmation-search").addEventListener("input", () => {
    clearTimeout(window._confirmationSearchDebounce);
    window._confirmationSearchDebounce = setTimeout(load, 250);
  });
  byId("confirmations-refresh").addEventListener("click", async () => {
    try {
      setMessage("confirmations-message", "Refreshing from _ops/status.md...");
      await refreshConfirmationsFromStatus();
      await load();
      setMessage("confirmations-message", "Refresh completed.");
    } catch (error) {
      setMessage("confirmations-message", `Refresh failed: ${error.message}`);
    }
  });

  const actionBindings = [
    ["btn-confirm", "confirm"],
    ["btn-reject", "reject"],
    ["btn-needs-info", "needs_more_info"],
    ["btn-resolve", "mark_resolved"],
    ["btn-note", "add_decision_note"],
    ["btn-by", "set_confirmed_by"],
    ["btn-at", "set_confirmed_at"],
    ["btn-save-confirmation", "save"],
  ];
  actionBindings.forEach(([buttonId, action]) => {
    byId(buttonId).addEventListener("click", async () => {
      try {
        setMessage("confirmations-message", `Saving ${action}...`);
        await updateConfirmation(action);
        await loadConfirmations();
        openConfirmationDetail(state.selectedConfirmationId);
        setMessage("confirmations-message", `Saved ${action}.`);
      } catch (error) {
        setMessage("confirmations-message", `Failed ${action}: ${error.message}`);
      }
    });
  });
}

function bindDocsControls() {
  byId("docs-project-select").addEventListener("change", async (event) => {
    state.docsProject = event.target.value;
    state.selectedDocPath = "";
    state.selectedDocOriginal = "";
    byId("doc-editor").value = "";
    byId("docs-meta").textContent = "Select a document.";
    setDocEditorMode(false);
    await loadDocs();
  });

  byId("docs-group-filter").addEventListener("change", async () => {
    await loadDocs();
  });

  byId("docs-refresh").addEventListener("click", async () => {
    try {
      setMessage("docs-message", "Refreshing document list...");
      await loadDocs();
      setMessage("docs-message", "Document list refreshed.");
    } catch (error) {
      setMessage("docs-message", `Refresh failed: ${error.message}`);
    }
  });

  byId("doc-cancel").addEventListener("click", () => {
    byId("doc-editor").value = state.selectedDocOriginal;
    setMessage("docs-message", "Changes reverted.");
  });

  byId("doc-save").addEventListener("click", async () => {
    try {
      setMessage("docs-message", "Saving document...");
      await saveDoc();
      setMessage("docs-message", "Save successful.");
      await openDoc(state.selectedDocPath);
      await loadDocs();
    } catch (error) {
      setMessage("docs-message", `Save failed: ${error.message}`);
    }
  });
}

async function init() {
  bindTabs();
  bindProjectOpsControls();
  bindConfirmationControls();
  bindDocsControls();

  await refreshOverviewData();

  if (state.currentProject) {
    await loadProject(state.currentProject);
  }
  if (state.confirmationsProject) {
    await loadConfirmations();
  }
  if (state.docsProject) {
    await loadDocs();
  }

  await refreshActionsWorkspace();
}

init().catch((error) => {
  byId("overview").insertAdjacentHTML(
    "afterbegin",
    `<div class="card"><strong>Failed to load console data:</strong> ${escapeHtml(error.message)}</div>`
  );
});
