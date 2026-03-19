const state = {
    epics: [],
    tasks: [],
    selectedPaths: new Set(),
    acceptedPaths: new Set(),
    assignedModels: new Map(),
    activeTaskPath: null,
    epicFolderPath: "workstream/000_epic",
};

const epicSelect = document.getElementById("epicSelect");
const epicMeta = document.getElementById("epicMeta");
const workstreamFilter = document.getElementById("workstreamFilter");
const statusFilter = document.getElementById("statusFilter");
const priorityFilter = document.getElementById("priorityFilter");
const sortBy = document.getElementById("sortBy");
const taskGroups = document.getElementById("taskGroups");
const taskSummary = document.getElementById("taskSummary");
const detailMeta = document.getElementById("detailMeta");
const detailBody = document.getElementById("detailBody");
const selectionCount = document.getElementById("selectionCount");
const defaultModel = document.getElementById("defaultModel");
const modelStatus = document.getElementById("modelStatus");
const extendDecompositionButton = document.getElementById("extendDecompositionButton");
const deleteSelectedButton = document.getElementById("deleteSelectedButton");
const themeStorageKey = "taskReviewTheme";
const folderPathInput = document.getElementById("folderPath");
const folderBrowserModal = document.getElementById("folderBrowserModal");
const folderBrowserList = document.getElementById("folderBrowserList");
const folderBrowserPath = document.getElementById("folderBrowserPath");

function isAllocatableTask(task) {
    return task.status_folder === "100_backlog";
}

function isMoveToGeneralCandidate(task) {
    if (!state.folderPath) return false;
    const normalized = String(task.path || "").replace(/\\/g, "/").toLowerCase();
    return !normalized.includes("/workstream/100_backlog/general/");
}

function isSelectableTask(task) {
    return isAllocatableTask(task) || isMoveToGeneralCandidate(task);
}

function allocationStateLabel(task) {
    if (isMoveToGeneralCandidate(task)) {
        return {
            text: "Browsable task: can be moved into 100_backlog/general for automatic pickup",
            className: "ready",
        };
    }
    if (!isAllocatableTask(task)) {
        return {
            text: `Locked: ${task.status_folder}${task.agent ? `/${task.agent}` : ""} tasks cannot be allocated from Epic Review`,
            className: "locked",
        };
    }
    if (task.agent) {
        return {
            text: `Allocatable: currently assigned to ${task.agent}; reallocation will move it to the selected model lane`,
            className: "ready",
        };
    }
    return {
        text: "Allocatable: unassigned todo task ready for model allocation",
        className: "ready",
    };
}

function applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    const icon = document.getElementById("themeIcon");
    const toggle = document.getElementById("themeToggle");
    if (icon) {
        icon.className = theme === "dark" ? "fas fa-sun" : "fas fa-moon";
    }
    if (toggle) {
        toggle.setAttribute("aria-label", theme === "dark" ? "Switch to light mode" : "Switch to dark mode");
        toggle.title = theme === "dark" ? "Switch to Light Mode" : "Switch to Dark Mode";
    }
}

function initTheme() {
    const themeParam = new URL(window.location.href).searchParams.get("theme");
    const savedTheme = window.localStorage.getItem(themeStorageKey);
    const prefersDark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
    const initialTheme = themeParam === "dark" || themeParam === "light"
        ? themeParam
        : (savedTheme || (prefersDark ? "dark" : "light"));
    applyTheme(initialTheme);
    if (themeParam !== "dark" && themeParam !== "light") {
        window.localStorage.setItem(themeStorageKey, initialTheme);
    }
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute("data-theme") === "dark" ? "dark" : "light";
    const nextTheme = currentTheme === "dark" ? "light" : "dark";
    applyTheme(nextTheme);
    window.localStorage.setItem(themeStorageKey, nextTheme);
}

window.toggleTheme = toggleTheme;

async function api(path, options = {}) {
    const response = await fetch(path, {
        headers: { "Content-Type": "application/json" },
        ...options,
    });
    if (!response.ok) {
        const text = await response.text();
        throw new Error(text || `Request failed: ${response.status}`);
    }
    return response.json();
}

function markdownToHtml(markdown) {
    let html = markdown.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    html = html.replace(/```([\s\S]*?)```/g, (_, code) => `<pre><code>${code.trim()}</code></pre>`);
    html = html.replace(/^###\s+(.+)$/gm, "<h3>$1</h3>");
    html = html.replace(/^##\s+(.+)$/gm, "<h2>$1</h2>");
    html = html.replace(/^#\s+(.+)$/gm, "<h1>$1</h1>");
    html = html.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
    html = html.replace(/`([^`]+)`/g, "<code>$1</code>");
    html = html.replace(/^- (.+)$/gm, "<li>$1</li>");
    html = html.replace(/(<li>[\s\S]*?<\/li>)/g, "<ul>$1</ul>");
    html = html.replace(/\n{2,}/g, "</p><p>");
    html = `<p>${html}</p>`;
    return html.replace(/<p>\s*<\/p>/g, "");
}

function updateSelectionCount() {
    const selected = selectedTasks();
    const allocatable = selected.filter(isAllocatableTask).length;
    const movable = selected.filter(isMoveToGeneralCandidate).length;
    const deletable = selected.filter(isDeletableTask).length;
    const decomposable = selected.filter(isDecomposableTask).length;
    selectionCount.textContent = `${selected.length} selected (${allocatable} allocatable, ${movable} movable)`;
    if (deleteSelectedButton) {
        deleteSelectedButton.style.display = deletable ? "" : "none";
        deleteSelectedButton.disabled = deletable === 0;
    }
    if (extendDecompositionButton) {
        extendDecompositionButton.style.display = decomposable ? "" : "none";
        extendDecompositionButton.disabled = decomposable === 0;
    }
}

function setActiveTask(task) {
    state.activeTaskPath = task.path;
    detailMeta.textContent = `${task.task_id} | ${task.workstream} | ${task.status_folder}${task.agent ? `/${task.agent}` : ""}`;
    detailBody.classList.remove("empty");
    detailBody.innerHTML = `
        <div class="markdown">
            <h2>${task.title}</h2>
            <p><strong>Purpose:</strong> ${task.purpose || "Not specified"}</p>
            <p><strong>Input:</strong> ${task.input || "Not specified"}</p>
            <p><strong>Output:</strong> ${task.output || "Not specified"}</p>
            <p><strong>Verification:</strong> ${task.verification || "Not specified"}</p>
            <hr>
            ${markdownToHtml(task.content)}
        </div>
    `;
    document.querySelectorAll(".task-card").forEach((node) => node.classList.remove("active"));
    const active = document.querySelector(`[data-task-path="${CSS.escape(task.path)}"]`);
    if (active) active.classList.add("active");
}

function groupedTasks() {
    const groups = new Map();
    state.tasks.forEach((task) => {
        if (!groups.has(task.workstream_group)) groups.set(task.workstream_group, []);
        groups.get(task.workstream_group).push(task);
    });
    return [...groups.entries()];
}

function renderTasks() {
    taskGroups.innerHTML = "";
    taskSummary.textContent = `${state.tasks.length} tasks loaded`;
    const template = document.getElementById("taskCardTemplate");
    groupedTasks().forEach(([group, tasks]) => {
        const wrapper = document.createElement("section");
        wrapper.className = "task-group";
        wrapper.innerHTML = `<div class="task-group-title"><h3>Workstream ${group}</h3><p>${tasks.length} task(s)</p></div>`;
        tasks.forEach((task) => {
            const clone = template.content.firstElementChild.cloneNode(true);
            clone.dataset.taskPath = task.path;
            if (state.acceptedPaths.has(task.path)) clone.classList.add("accepted");
            clone.querySelector(".task-check").checked = state.selectedPaths.has(task.path);
            clone.querySelector(".ws-badge").textContent = `[${task.workstream_group}]`;
            clone.querySelector(".task-id").textContent = task.task_id;
            clone.querySelector(".task-priority").textContent = `P${task.priority}`;
            clone.querySelector(".task-title").textContent = task.title;
            clone.querySelector(".task-meta").textContent = `${task.status_folder}${task.agent ? `/${task.agent}` : ""} | ${task.timestamp || "no timestamp"}`;
            const allocatable = isAllocatableTask(task);
            const selectable = isSelectableTask(task);
            const allocationState = allocationStateLabel(task);
            clone.classList.toggle("locked", !selectable);
            const allocationStateNode = clone.querySelector(".task-allocation-state");
            allocationStateNode.textContent = allocationState.text;
            allocationStateNode.className = `task-allocation-state ${allocationState.className}`;
            const taskCheck = clone.querySelector(".task-check");
            const modelSelect = clone.querySelector(".task-model");
            modelSelect.value = state.assignedModels.get(task.path) || defaultModel.value;
            modelSelect.addEventListener("change", (event) => state.assignedModels.set(task.path, event.target.value));
            taskCheck.disabled = !selectable;
            modelSelect.disabled = !allocatable;
            clone.querySelector(".accept-button").disabled = !allocatable;
            clone.querySelector(".task-check").addEventListener("change", (event) => {
                if (event.target.checked) state.selectedPaths.add(task.path);
                else state.selectedPaths.delete(task.path);
                updateSelectionCount();
            });
            clone.querySelector(".accept-button").addEventListener("click", (event) => {
                event.stopPropagation();
                if (!allocatable) return;
                state.acceptedPaths.add(task.path);
                state.assignedModels.set(task.path, modelSelect.value);
                renderTasks();
            });
            clone.querySelector(".reject-button").addEventListener("click", async (event) => {
                event.stopPropagation();
                state.selectedPaths.add(task.path);
                updateSelectionCount();
                await rejectSelected();
            });
            clone.addEventListener("click", () => setActiveTask(task));
            wrapper.appendChild(clone);
        });
        taskGroups.appendChild(wrapper);
    });
    updateSelectionCount();
    if (!state.activeTaskPath && state.tasks[0]) setActiveTask(state.tasks[0]);
}

async function loadModelStatus() {
    const payload = await api("/api/models/status");
    modelStatus.innerHTML = "";
    payload.models.forEach((entry) => {
        const div = document.createElement("div");
        div.className = "model-pill";
        div.innerHTML = `<strong>${entry.model}</strong><span>${entry.count} task(s)</span>`;
        modelStatus.appendChild(div);
    });
}

function syncWorkstreamOptions() {
    const groups = [...new Set(state.tasks.map((task) => task.workstream_group))].sort();
    const previous = workstreamFilter.value;
    workstreamFilter.innerHTML = '<option value="">All</option>';
    groups.forEach((group) => {
        const option = document.createElement("option");
        option.value = group;
        option.textContent = group;
        workstreamFilter.appendChild(option);
    });
    workstreamFilter.value = groups.includes(previous) ? previous : "";
}

async function loadTasks() {
    const epicSlug = epicSelect.value;
    if (!epicSlug) {
        state.tasks = [];
        renderTasks();
        return;
    }
    const params = new URLSearchParams();
    if (workstreamFilter.value) params.set("workstream", workstreamFilter.value);
    if (statusFilter.value) params.set("status", statusFilter.value);
    if (priorityFilter.value) params.set("priority", priorityFilter.value);
    if (state.folderPath) params.set("folder", state.folderPath);
    params.set("sort_by", sortBy.value);
    const payload = await api(`/api/epics/${epicSlug}/tasks?${params.toString()}`);
    state.tasks = payload.tasks;
    const visiblePaths = new Set(state.tasks.map((task) => task.path));
    state.selectedPaths = new Set([...state.selectedPaths].filter((path) => visiblePaths.has(path)));
    state.acceptedPaths = new Set([...state.acceptedPaths].filter((path) => visiblePaths.has(path)));
    state.assignedModels = new Map([...state.assignedModels.entries()].filter(([path]) => visiblePaths.has(path)));
    syncWorkstreamOptions();
    const epic = state.epics.find((entry) => entry.slug === epicSlug);
    epicMeta.textContent = epic
        ? `${payload.tasks.length} task(s) in ${state.folderPath || "all task folders"} | ${epic.path || "workstream/000_epic"}`
        : "";
    renderTasks();
}

async function loadEpics() {
    const params = new URLSearchParams();
    params.set("folder", state.epicFolderPath || "workstream/000_epic");
    const payload = await api(`/api/epics?${params.toString()}`);
    state.epics = payload.epics;
    epicSelect.innerHTML = "";
    if (!payload.epics.length) {
        const option = document.createElement("option");
        option.value = "";
        option.textContent = "No epics found";
        epicSelect.appendChild(option);
        epicMeta.textContent = "No markdown epics were found under workstream/000_epic.";
        state.tasks = [];
        renderTasks();
        await loadModelStatus();
        return;
    }
    payload.epics.forEach((epic) => {
        const option = document.createElement("option");
        option.value = epic.slug;
        option.textContent = epic.name;
        epicSelect.appendChild(option);
    });
    const urlEpic = new URL(window.location.href).searchParams.get("epic");
    if (urlEpic && payload.epics.some((epic) => epic.slug === urlEpic)) epicSelect.value = urlEpic;
    await loadTasks();
    await loadModelStatus();
}

function selectedTasks() {
    return state.tasks.filter((task) => state.selectedPaths.has(task.path));
}

async function allocate(taskPaths, targetModel) {
    if (!taskPaths.length) return;
    return api("/api/tasks/allocate", {
        method: "POST",
        body: JSON.stringify({ task_paths: taskPaths, target_model: targetModel }),
    });
}

async function moveToGeneral(taskPaths) {
    if (!taskPaths.length) return;
    return api("/api/tasks/move-to-general", {
        method: "POST",
        body: JSON.stringify({ task_paths: taskPaths }),
    });
}

async function openFolderBrowser(startPath = null) {
    const path = startPath || state.browsePath || state.folderPath || "workstream";
    state.browsePath = path;
    folderBrowserModal.style.display = "flex";
    folderBrowserPath.textContent = path;
    folderBrowserList.innerHTML = '<div class="empty-state" style="padding:20px;"><i class="fas fa-spinner fa-spin"></i><p>Loading folders...</p></div>';
    try {
        const payload = await api(`/api/browse-files?path=${encodeURIComponent(path)}`);
        const items = (payload.items || []).filter((item) => item.is_dir).sort((a, b) => a.name.localeCompare(b.name));
        const parent = path.split("/").slice(0, -1).join("/");
        const rows = [];
        if (path) {
            rows.push(`<button class="ghost" type="button" data-path="${parent}" style="text-align:left;">..</button>`);
        }
        items.forEach((item) => {
            rows.push(`<button class="ghost" type="button" data-path="${item.path}" style="text-align:left;">${item.name}</button>`);
        });
        folderBrowserList.innerHTML = rows.join("") || '<div class="empty-state" style="padding:20px;"><i class="fas fa-folder-open"></i><p>No subfolders found</p></div>';
        folderBrowserList.querySelectorAll("[data-path]").forEach((node) => {
            node.addEventListener("click", () => openFolderBrowser(node.dataset.path || ""));
        });
    } catch (error) {
        folderBrowserList.innerHTML = `<div class="empty-state" style="padding:20px;"><i class="fas fa-exclamation-triangle"></i><p>${error.message}</p></div>`;
    }
}

function closeFolderBrowser() {
    if (folderBrowserModal) folderBrowserModal.style.display = "none";
}

async function applyFolderPath(path) {
    state.folderPath = path || "workstream/100_backlog";
    if (folderPathInput) folderPathInput.value = state.folderPath;
    state.selectedPaths.clear();
    state.acceptedPaths.clear();
    state.assignedModels.clear();
    await loadEpics();
    closeFolderBrowser();
}

function summarizeAllocationFailures(results) {
    if (!results || !results.failed || !results.failed.length) return "";
    return results.failed.map((entry) => `${entry.path}: ${entry.error}`).join("\n");
}

async function rejectSelected() {
    const tasks = selectedTasks();
    if (!tasks.length) return;
    const reason = window.prompt("Rejection reason");
    if (!reason) return;
    await api("/api/tasks/reject", {
        method: "POST",
        body: JSON.stringify({ task_paths: tasks.map((task) => task.path), reason }),
    });
    state.selectedPaths.clear();
    state.acceptedPaths = new Set([...state.acceptedPaths].filter((path) => !tasks.some((task) => task.path === path)));
    await loadTasks();
    await loadModelStatus();
}

document.getElementById("selectAllButton").addEventListener("click", () => {
    const visiblePaths = state.tasks.filter(isSelectableTask).map((task) => task.path);
    const allSelected = visiblePaths.every((path) => state.selectedPaths.has(path));
    if (allSelected) visiblePaths.forEach((path) => state.selectedPaths.delete(path));
    else visiblePaths.forEach((path) => state.selectedPaths.add(path));
    renderTasks();
});

document.getElementById("acceptSelectedButton").addEventListener("click", () => {
    selectedTasks().filter(isAllocatableTask).forEach((task) => {
        state.acceptedPaths.add(task.path);
        state.assignedModels.set(task.path, state.assignedModels.get(task.path) || defaultModel.value);
    });
    renderTasks();
});

document.getElementById("allocateSelectedButton").addEventListener("click", async () => {
    const tasks = selectedTasks().filter(isAllocatableTask);
    if (!tasks.length) {
        window.alert("No allocatable 100_backlog tasks selected.");
        return;
    }
    const buckets = new Map();
    tasks.forEach((task) => {
        const model = state.assignedModels.get(task.path) || defaultModel.value;
        if (!buckets.has(model)) buckets.set(model, []);
        buckets.get(model).push(task.path);
    });
    const failures = [];
    for (const [model, taskPaths] of buckets.entries()) {
        const results = await allocate(taskPaths, model);
        const failed = summarizeAllocationFailures(results);
        if (failed) failures.push(failed);
    }
    state.selectedPaths.clear();
    state.acceptedPaths = new Set([...state.acceptedPaths].filter((path) => !tasks.some((task) => task.path === path)));
    await loadTasks();
    await loadModelStatus();
    if (failures.length) window.alert(`Some allocations failed:\n\n${failures.join("\n")}`);
});

document.getElementById("allocateAcceptedButton").addEventListener("click", async () => {
    const accepted = state.tasks.filter((task) => state.acceptedPaths.has(task.path) && isAllocatableTask(task));
    if (!accepted.length) {
        window.alert("No accepted allocatable 100_backlog tasks to allocate.");
        return;
    }
    const buckets = new Map();
    accepted.forEach((task) => {
        const model = state.assignedModels.get(task.path) || defaultModel.value;
        if (!buckets.has(model)) buckets.set(model, []);
        buckets.get(model).push(task.path);
    });
    const failures = [];
    for (const [model, taskPaths] of buckets.entries()) {
        const results = await allocate(taskPaths, model);
        const failed = summarizeAllocationFailures(results);
        if (failed) failures.push(failed);
    }
    state.selectedPaths.clear();
    state.acceptedPaths.clear();
    await loadTasks();
    await loadModelStatus();
    if (failures.length) window.alert(`Some allocations failed:\n\n${failures.join("\n")}`);
});

document.getElementById("moveToGeneralButton").addEventListener("click", async () => {
    const tasks = selectedTasks().filter(isMoveToGeneralCandidate);
    if (!tasks.length) {
        window.alert("No selected browsed tasks available to move into 100_backlog/general.");
        return;
    }
    const results = await moveToGeneral(tasks.map((task) => task.path));
    const failed = summarizeAllocationFailures(results);
    state.selectedPaths.clear();
    state.acceptedPaths.clear();
    await loadEpics();
    await loadModelStatus();
    if (failed) window.alert(`Some moves failed:\n\n${failed}`);
});

document.getElementById("rejectSelectedButton").addEventListener("click", rejectSelected);

// Delete Selected functionality
const deleteConfirmModal = document.getElementById("deleteConfirmModal");
const deleteTaskList = document.getElementById("deleteTaskList");

function isDeletableTask(task) {
    // Only allow deletion of tasks in 100_backlog or 050_review
    return task.status_folder === "100_backlog" || task.status_folder === "050_review";
}

function openDeleteModal() {
    const tasks = selectedTasks().filter(isDeletableTask);
    if (!tasks.length) {
        window.alert("No deletable tasks selected. Only tasks in 100_backlog or 050_review can be deleted.");
        return;
    }
    deleteTaskList.innerHTML = tasks.map((task) => `
        <div style="padding:8px; background:rgba(244,63,94,0.1); border-radius:8px; border-left:3px solid #f43f5e;">
            <strong>${task.task_id}</strong>: ${task.title}
            <div style="font-size:0.75rem; color:#94a3b8; margin-top:4px;">${task.path}</div>
        </div>
    `).join("");
    deleteConfirmModal.style.display = "flex";
}

function closeDeleteModal() {
    deleteConfirmModal.style.display = "none";
}

async function deleteSelectedTasks() {
    const tasks = selectedTasks().filter(isDeletableTask);
    if (!tasks.length) return;
    try {
        const response = await api("/api/tasks/delete-bulk", {
            method: "POST",
            body: JSON.stringify({ task_paths: tasks.map((task) => task.path) }),
        });
        if (response.failed && response.failed.length > 0) {
            window.alert(`Some deletions failed:\n\n${response.failed.map((f) => `${f.path}: ${f.error}`).join("\n")}`);
        }
        state.selectedPaths.clear();
        state.acceptedPaths = new Set([...state.acceptedPaths].filter((path) => !tasks.some((task) => task.path === path)));
        closeDeleteModal();
        await loadTasks();
        await loadModelStatus();
    } catch (error) {
        window.alert(`Error deleting tasks: ${error.message}`);
    }
}

extendDecompositionButton?.style && (extendDecompositionButton.style.display = "none");
deleteSelectedButton?.style && (deleteSelectedButton.style.display = "none");

deleteSelectedButton?.addEventListener("click", openDeleteModal);
document.getElementById("closeDeleteModalButton").addEventListener("click", closeDeleteModal);
document.getElementById("cancelDeleteButton").addEventListener("click", closeDeleteModal);
document.getElementById("confirmDeleteButton").addEventListener("click", deleteSelectedTasks);
if (deleteConfirmModal) {
    deleteConfirmModal.addEventListener("click", (event) => {
        if (event.target === deleteConfirmModal) closeDeleteModal();
    });
}

// Extended Decomposition functionality
const extendDecompModal = document.getElementById("extendDecompModal");
const extendTaskList = document.getElementById("extendTaskList");
const extendDecompProgress = document.getElementById("extendDecompProgress");
const extendDecompResult = document.getElementById("extendDecompResult");

function isDecomposableTask(task) {
    // Only allow decomposition of tasks in 100_backlog or 050_review
    return task.status_folder === "100_backlog" || task.status_folder === "050_review";
}

function openExtendModal() {
    const tasks = selectedTasks().filter(isDecomposableTask);
    if (!tasks.length) {
        window.alert("No decomposable tasks selected. Only tasks in 100_backlog or 050_review can be further decomposed.");
        return;
    }
    extendTaskList.innerHTML = tasks.map((task) => `
        <div style="padding:8px; background:rgba(139,92,246,0.1); border-radius:8px; border-left:3px solid #8b5cf6;">
            <strong>${task.task_id}</strong>: ${task.title}
            <div style="font-size:0.75rem; color:#94a3b8; margin-top:4px;">${task.workstream} | Priority ${task.priority}</div>
        </div>
    `).join("");
    extendDecompProgress.style.display = "none";
    extendDecompResult.style.display = "none";
    document.getElementById("confirmExtendButton").disabled = false;
    extendDecompModal.style.display = "flex";
}

function closeExtendModal() {
    extendDecompModal.style.display = "none";
}

async function runExtendedDecomposition() {
    const tasks = selectedTasks().filter(isDecomposableTask);
    if (!tasks.length) return;

    extendDecompProgress.style.display = "block";
    extendDecompResult.style.display = "none";
    document.getElementById("confirmExtendButton").disabled = true;

    try {
        const response = await api("/api/tasks/extend-decomposition", {
            method: "POST",
            body: JSON.stringify({ task_paths: tasks.map((task) => task.path) }),
        });

        extendDecompProgress.style.display = "none";
        extendDecompResult.style.display = "block";

        if (response.success) {
            const subtasksCreated = response.subtasks_created || [];
            extendDecompResult.innerHTML = `
                <p style="margin:0 0 8px; color:#10b981; font-weight:600;"><i class="fas fa-check-circle"></i> Decomposition Complete</p>
                <p style="margin:0; color:#94a3b8; font-size:0.85rem;">Created ${subtasksCreated.length} new sub-task(s)</p>
                ${subtasksCreated.length > 0 ? `<ul style="margin:8px 0 0; padding-left:20px; color:#e2e8f0; font-size:0.8rem;">${subtasksCreated.slice(0, 10).map((t) => `<li>${t.task_id}: ${t.title}</li>`).join("")}${subtasksCreated.length > 10 ? `<li>...and ${subtasksCreated.length - 10} more</li>` : ""}</ul>` : ""}
            `;
            state.selectedPaths.clear();
            await loadTasks();
            await loadModelStatus();
        } else {
            extendDecompResult.style.background = "rgba(244,63,94,0.1)";
            extendDecompResult.style.borderColor = "rgba(244,63,94,0.3)";
            extendDecompResult.innerHTML = `
                <p style="margin:0; color:#f43f5e; font-weight:600;"><i class="fas fa-exclamation-circle"></i> Decomposition Failed</p>
                <p style="margin:8px 0 0; color:#94a3b8; font-size:0.85rem;">${response.error || "Unknown error"}</p>
            `;
        }
    } catch (error) {
        extendDecompProgress.style.display = "none";
        extendDecompResult.style.display = "block";
        extendDecompResult.style.background = "rgba(244,63,94,0.1)";
        extendDecompResult.style.borderColor = "rgba(244,63,94,0.3)";
        extendDecompResult.innerHTML = `
            <p style="margin:0; color:#f43f5e; font-weight:600;"><i class="fas fa-exclamation-circle"></i> Request Failed</p>
            <p style="margin:8px 0 0; color:#94a3b8; font-size:0.85rem;">${error.message}</p>
        `;
    }
    document.getElementById("confirmExtendButton").disabled = false;
}

extendDecompositionButton?.addEventListener("click", openExtendModal);
document.getElementById("closeExtendModalButton").addEventListener("click", closeExtendModal);
document.getElementById("cancelExtendButton").addEventListener("click", closeExtendModal);
document.getElementById("confirmExtendButton").addEventListener("click", runExtendedDecomposition);
if (extendDecompModal) {
    extendDecompModal.addEventListener("click", (event) => {
        if (event.target === extendDecompModal) closeExtendModal();
    });
}

[epicSelect, workstreamFilter, statusFilter, priorityFilter, sortBy].forEach((node) => node.addEventListener("change", loadTasks));
document.getElementById("browseFolderButton").addEventListener("click", () => openFolderBrowser("workstream"));
document.getElementById("clearFolderButton").addEventListener("click", () => applyFolderPath("workstream/100_backlog"));
document.getElementById("closeFolderBrowserButton").addEventListener("click", closeFolderBrowser);
document.getElementById("chooseCurrentFolderButton").addEventListener("click", () => applyFolderPath(state.browsePath || state.folderPath || "workstream/100_backlog"));
if (folderBrowserModal) {
    folderBrowserModal.addEventListener("click", (event) => {
        if (event.target === folderBrowserModal) closeFolderBrowser();
    });
}

// Augment Epic functionality
const augmentEpicModal = document.getElementById("augmentEpicModal");
const augmentEpicSelect = document.getElementById("augmentEpicSelect");
const augmentSolutionPath = document.getElementById("augmentSolutionPath");
const augmentSolutionAnalysis = document.getElementById("augmentSolutionAnalysis");
const augmentFeatureSection = document.getElementById("augmentFeatureSection");
const augmentFeatureDescription = document.getElementById("augmentFeatureDescription");
const augmentProgress = document.getElementById("augmentProgress");
const augmentProgressText = document.getElementById("augmentProgressText");
const augmentResult = document.getElementById("augmentResult");

async function openAugmentModal() {
    augmentEpicModal.style.display = "flex";
    augmentProgress.style.display = "none";
    augmentResult.style.display = "none";
    augmentSolutionAnalysis.innerHTML = '<p style="margin:0; color:#64748b; font-size:0.85rem; text-align:center;"><i class="fas fa-spinner fa-spin"></i> Loading epics with solutions...</p>';

    // Reset checkboxes
    document.querySelectorAll("#augmentEpicModal input[type='checkbox']").forEach((cb) => cb.checked = false);
    augmentFeatureSection.style.display = "none";
    augmentFeatureDescription.value = "";

    try {
        // Load epics that have solution folders
        const response = await api("/api/epics/with-solutions");
        const epics = response.epics || [];

        augmentEpicSelect.innerHTML = '<option value="">Select an epic...</option>';
        epics.forEach((epic) => {
            const option = document.createElement("option");
            option.value = epic.slug;
            option.textContent = `${epic.name} (${epic.solution_path})`;
            option.dataset.solutionPath = epic.solution_path;
            augmentEpicSelect.appendChild(option);
        });

        if (epics.length === 0) {
            augmentSolutionAnalysis.innerHTML = '<p style="margin:0; color:#f97316; font-size:0.85rem; text-align:center;"><i class="fas fa-exclamation-triangle"></i> No epics with solution folders found. Decompose an epic first.</p>';
        } else {
            augmentSolutionAnalysis.innerHTML = '<p style="margin:0; color:#64748b; font-size:0.85rem; text-align:center;"><i class="fas fa-info-circle"></i> Select an epic to analyze existing solution</p>';
        }
    } catch (error) {
        augmentSolutionAnalysis.innerHTML = `<p style="margin:0; color:#f43f5e; font-size:0.85rem; text-align:center;"><i class="fas fa-exclamation-circle"></i> Error: ${error.message}</p>`;
    }
}

async function analyzeSolution(epicSlug, solutionPath) {
    if (!epicSlug || !solutionPath) {
        augmentSolutionAnalysis.innerHTML = '<p style="margin:0; color:#64748b; font-size:0.85rem; text-align:center;"><i class="fas fa-info-circle"></i> Select an epic to analyze existing solution</p>';
        augmentSolutionPath.value = "";
        return;
    }

    augmentSolutionPath.value = solutionPath;
    augmentSolutionAnalysis.innerHTML = '<p style="margin:0; color:#64748b; font-size:0.85rem; text-align:center;"><i class="fas fa-spinner fa-spin"></i> Analyzing solution structure...</p>';

    try {
        const response = await api(`/api/analyze-solution?path=${encodeURIComponent(solutionPath)}`);
        const analysis = response.analysis || {};

        let html = '<div style="display:flex; flex-direction:column; gap:10px;">';

        // Summary row
        html += `<div style="display:flex; gap:12px; flex-wrap:wrap;">`;
        html += `<span style="padding:6px 12px; background:rgba(16,185,129,0.15); border-radius:8px; font-size:0.8rem; color:#10b981;"><i class="fas fa-file-code"></i> ${analysis.total_files || 0} files</span>`;
        html += `<span style="padding:6px 12px; background:rgba(59,130,246,0.15); border-radius:8px; font-size:0.8rem; color:#3b82f6;"><i class="fas fa-folder"></i> ${analysis.total_dirs || 0} directories</span>`;
        html += `</div>`;

        // Existing components
        if (analysis.has_backend) {
            html += `<div style="padding:8px 12px; background:rgba(139,92,246,0.1); border-radius:8px; border-left:3px solid #8b5cf6;">
                <strong style="color:#a78bfa; font-size:0.85rem;"><i class="fas fa-server"></i> Backend</strong>
                <p style="margin:4px 0 0; color:#94a3b8; font-size:0.75rem;">${analysis.backend_details || 'Express/Node.js API'}</p>
            </div>`;
        }
        if (analysis.has_frontend) {
            html += `<div style="padding:8px 12px; background:rgba(16,185,129,0.1); border-radius:8px; border-left:3px solid #10b981;">
                <strong style="color:#34d399; font-size:0.85rem;"><i class="fas fa-desktop"></i> Frontend</strong>
                <p style="margin:4px 0 0; color:#94a3b8; font-size:0.75rem;">${analysis.frontend_details || 'Web UI'}</p>
            </div>`;
        }
        if (analysis.has_tests) {
            html += `<div style="padding:8px 12px; background:rgba(59,130,246,0.1); border-radius:8px; border-left:3px solid #3b82f6;">
                <strong style="color:#60a5fa; font-size:0.85rem;"><i class="fas fa-vial"></i> Tests</strong>
                <p style="margin:4px 0 0; color:#94a3b8; font-size:0.75rem;">${analysis.test_details || 'Test suite'}</p>
            </div>`;
        }
        if (analysis.has_infra) {
            html += `<div style="padding:8px 12px; background:rgba(249,115,22,0.1); border-radius:8px; border-left:3px solid #f97316;">
                <strong style="color:#fb923c; font-size:0.85rem;"><i class="fas fa-cogs"></i> Infrastructure</strong>
                <p style="margin:4px 0 0; color:#94a3b8; font-size:0.75rem;">${analysis.infra_details || 'Docker/setup scripts'}</p>
            </div>`;
        }

        // Missing components
        const missing = [];
        if (!analysis.has_frontend) missing.push("Frontend/UI");
        if (!analysis.has_tests) missing.push("Tests");
        if (!analysis.has_infra) missing.push("Infrastructure");
        if (!analysis.has_docs) missing.push("Documentation");

        if (missing.length > 0) {
            html += `<div style="padding:8px 12px; background:rgba(244,63,94,0.1); border-radius:8px; border-left:3px solid #f43f5e;">
                <strong style="color:#fb7185; font-size:0.85rem;"><i class="fas fa-exclamation-triangle"></i> Missing Components</strong>
                <p style="margin:4px 0 0; color:#94a3b8; font-size:0.75rem;">${missing.join(", ")}</p>
            </div>`;
        }

        // Key files
        if (analysis.key_files && analysis.key_files.length > 0) {
            html += `<div style="padding:8px 12px; background:rgba(0,0,0,0.2); border-radius:8px;">
                <strong style="color:#94a3b8; font-size:0.8rem;"><i class="fas fa-file-alt"></i> Key Files</strong>
                <div style="margin-top:6px; font-family:'JetBrains Mono', monospace; font-size:0.7rem; color:#64748b; max-height:80px; overflow:auto;">
                    ${analysis.key_files.slice(0, 10).map((f) => `<div>${f}</div>`).join("")}
                    ${analysis.key_files.length > 10 ? `<div>...and ${analysis.key_files.length - 10} more</div>` : ""}
                </div>
            </div>`;
        }

        html += '</div>';
        augmentSolutionAnalysis.innerHTML = html;

        // Auto-check missing components
        if (!analysis.has_frontend) document.getElementById("augmentAddUI").checked = true;
        if (!analysis.has_tests) document.getElementById("augmentAddTests").checked = true;
        if (!analysis.has_infra) document.getElementById("augmentAddInfra").checked = true;
        if (!analysis.has_docs) document.getElementById("augmentAddDocs").checked = true;

    } catch (error) {
        augmentSolutionAnalysis.innerHTML = `<p style="margin:0; color:#f43f5e; font-size:0.85rem;"><i class="fas fa-exclamation-circle"></i> Error analyzing solution: ${error.message}</p>`;
    }
}

function closeAugmentModal() {
    augmentEpicModal.style.display = "none";
}

async function runAugmentation() {
    const epicSlug = augmentEpicSelect.value;
    const solutionPath = augmentSolutionPath.value;

    if (!epicSlug || !solutionPath) {
        window.alert("Please select an epic with an existing solution.");
        return;
    }

    // Gather selected augmentation types
    const augmentTypes = [];
    if (document.getElementById("augmentAddUI").checked) augmentTypes.push("ui");
    if (document.getElementById("augmentAddTests").checked) augmentTypes.push("tests");
    if (document.getElementById("augmentAddDocs").checked) augmentTypes.push("docs");
    if (document.getElementById("augmentAddInfra").checked) augmentTypes.push("infra");
    if (document.getElementById("augmentAddFeature").checked) augmentTypes.push("feature");

    if (augmentTypes.length === 0) {
        window.alert("Please select at least one type of augmentation.");
        return;
    }

    const featureDescription = augmentTypes.includes("feature") ? augmentFeatureDescription.value.trim() : "";
    if (augmentTypes.includes("feature") && !featureDescription) {
        window.alert("Please provide a description for the new feature.");
        return;
    }

    augmentProgress.style.display = "block";
    augmentProgressText.textContent = "Analyzing existing solution and generating augmentation tasks...";
    augmentResult.style.display = "none";
    document.getElementById("runAugmentButton").disabled = true;

    try {
        const response = await api("/api/augment-epic", {
            method: "POST",
            body: JSON.stringify({
                epic_slug: epicSlug,
                solution_path: solutionPath,
                augment_types: augmentTypes,
                feature_description: featureDescription
            }),
        });

        augmentProgress.style.display = "none";
        augmentResult.style.display = "block";

        if (response.success) {
            const tasksCreated = response.tasks_created || [];
            augmentResult.style.background = "rgba(16,185,129,0.1)";
            augmentResult.style.borderColor = "rgba(16,185,129,0.3)";
            augmentResult.innerHTML = `
                <p style="margin:0 0 8px; color:#10b981; font-weight:600;"><i class="fas fa-check-circle"></i> Augmentation Complete</p>
                <p style="margin:0; color:#94a3b8; font-size:0.85rem;">Created ${tasksCreated.length} new task(s) in workstream/100_backlog</p>
                ${tasksCreated.length > 0 ? `<ul style="margin:8px 0 0; padding-left:20px; color:#e2e8f0; font-size:0.8rem;">${tasksCreated.slice(0, 8).map((t) => `<li>${t.task_id}: ${t.title}</li>`).join("")}${tasksCreated.length > 8 ? `<li>...and ${tasksCreated.length - 8} more</li>` : ""}</ul>` : ""}
            `;
            // Reload tasks to show new ones
            await loadTasks();
            await loadModelStatus();
        } else {
            augmentResult.style.background = "rgba(244,63,94,0.1)";
            augmentResult.style.borderColor = "rgba(244,63,94,0.3)";
            augmentResult.innerHTML = `
                <p style="margin:0; color:#f43f5e; font-weight:600;"><i class="fas fa-exclamation-circle"></i> Augmentation Failed</p>
                <p style="margin:8px 0 0; color:#94a3b8; font-size:0.85rem;">${response.error || "Unknown error"}</p>
            `;
        }
    } catch (error) {
        augmentProgress.style.display = "none";
        augmentResult.style.display = "block";
        augmentResult.style.background = "rgba(244,63,94,0.1)";
        augmentResult.style.borderColor = "rgba(244,63,94,0.3)";
        augmentResult.innerHTML = `
            <p style="margin:0; color:#f43f5e; font-weight:600;"><i class="fas fa-exclamation-circle"></i> Request Failed</p>
            <p style="margin:8px 0 0; color:#94a3b8; font-size:0.85rem;">${error.message}</p>
        `;
    }
    document.getElementById("runAugmentButton").disabled = false;
}

// Augment Epic event listeners
if (document.getElementById("augmentEpicBtn")) {
    document.getElementById("augmentEpicBtn").addEventListener("click", openAugmentModal);
}
if (document.getElementById("closeAugmentModalButton")) {
    document.getElementById("closeAugmentModalButton").addEventListener("click", closeAugmentModal);
}
if (document.getElementById("cancelAugmentButton")) {
    document.getElementById("cancelAugmentButton").addEventListener("click", closeAugmentModal);
}
if (document.getElementById("runAugmentButton")) {
    document.getElementById("runAugmentButton").addEventListener("click", runAugmentation);
}
if (augmentEpicSelect) {
    augmentEpicSelect.addEventListener("change", () => {
        const selectedOption = augmentEpicSelect.options[augmentEpicSelect.selectedIndex];
        const solutionPath = selectedOption?.dataset?.solutionPath || "";
        analyzeSolution(augmentEpicSelect.value, solutionPath);
    });
}
if (document.getElementById("augmentAddFeature")) {
    document.getElementById("augmentAddFeature").addEventListener("change", (e) => {
        augmentFeatureSection.style.display = e.target.checked ? "block" : "none";
    });
}
if (augmentEpicModal) {
    augmentEpicModal.addEventListener("click", (event) => {
        if (event.target === augmentEpicModal) closeAugmentModal();
    });
}

document.addEventListener("DOMContentLoaded", () => {
    initTheme();
    state.folderPath = "workstream/100_backlog";
    state.browsePath = "workstream";
    if (folderPathInput) folderPathInput.value = state.folderPath;
    loadEpics().catch((error) => {
        detailBody.classList.remove("empty");
        detailBody.innerHTML = `<pre>${error.message}</pre>`;
    });
});
