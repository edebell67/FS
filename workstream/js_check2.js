
        let isEditMode = false;
        let editOriginalFolder = null;
        let editOriginalFilename = null;

        function openCreateModal() { 
            isEditMode = false;
            document.getElementById('createModalTitle').innerHTML = '<i class="fas fa-plus"></i> <span>Create New Entry</span>';
            document.getElementById('createTitle').value = '';
            document.getElementById('createContent').value = '';
            document.getElementById('createModal').style.display = 'flex'; 
        }
        function closeCreateModal(e) {
            if (e && e.target.id === 'createModal') document.getElementById('createModal').style.display = 'none';
            else if (!e) document.getElementById('createModal').style.display = 'none';
        }
        
        async function openEditModal() {
            if (!currentFileContext) return;
            isEditMode = true;
            editOriginalFolder = currentFileContext.folder;
            editOriginalFilename = currentFileContext.filename;
            
            const task = lastTasksData.find(t => t.folder === currentFileContext.folder && t.filename === currentFileContext.filename);
            if (!task) return;
            
            closeModal();
            
            document.getElementById('createTitle').value = task.title;
            document.getElementById('createProject').value = task.project;
            let typeVal = currentFileContext.folder.includes("backlog") ? "backlog" : "task";
            document.getElementById('createType').value = typeVal;
            document.getElementById('createPriority').value = task.priority || "2";
            
            let agentStr = ""; 
            if (currentFileContext.folder.includes("codex")) agentStr = "codex";
            else if (currentFileContext.folder.includes("gemini")) agentStr = "gemini";
            else if (currentFileContext.folder.includes("claude")) agentStr = "claude";
            else if (currentFileContext.folder.includes("general")) agentStr = "general";
            document.getElementById('createAgent').value = agentStr;
            
            let rawContent = document.getElementById('modalContentText').innerText;
            // Best effort cleanup of backend injected lines
            rawContent = rawContent.replace(/Priority:\s*\d+
+/, '');
            const compMatches = rawContent.match(/
+- `Completion Status`:.*$/i);
            if (compMatches) {
                rawContent = rawContent.replace(compMatches[0], '');
            }
            document.getElementById('createContent').value = rawContent.trim();
            
            document.getElementById('createModalTitle').innerHTML = '<i class="fas fa-edit"></i> <span>Edit Entry</span>';
            document.getElementById('createModal').style.display = 'flex';
        }

        async function submitCreate() {
            const payload = {
                type: document.getElementById('createType').value,
                agent: document.getElementById('createAgent').value,
                priority: document.getElementById('createPriority').value,
                completionAction: document.getElementById('createCompletionAction').value,
                project: document.getElementById('createProject').value.toLowerCase().replace(/[^a-z0-9_-]/g, ''),
                title: document.getElementById('createTitle').value.toLowerCase().replace(/[^a-z0-9_-]/g, '_'),
                content: document.getElementById('createContent').value,
                is_edit: isEditMode,
                original_folder: editOriginalFolder,
                original_filename: editOriginalFilename
            };
            if(!payload.project || !payload.title) { alert("Project and Title are required"); return; }
            try {
                const res = await fetch('/api/create-entry', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(payload)
                });
                if(res.ok) {
                    closeCreateModal();
                    document.getElementById('createTitle').value = '';
                    document.getElementById('createContent').value = '';
                    fetchTasks();
                } else {
                    alert("Failed to create file");
                }
            } catch(err) { console.error(err); }
        }

        let currentVerifyTask = null;

        function closeVerifyModal(e) {
            if (e && e.target.id === 'verifyModal') {
                document.getElementById('verifyModal').style.display = 'none';
            } else if (!e) {
                document.getElementById('verifyModal').style.display = 'none';
            }
        }

        function escapeHtml(unsafe) {
            if (!unsafe) return "";
            return unsafe
                 .replace(/&/g, "&amp;")
                 .replace(/</g, "&lt;")
                 .replace(/>/g, "&gt;")
                 .replace(/"/g, "&quot;")
                 .replace(/'/g, "&#039;");
        }

        function openVerifyModal(e, folder, filename) {
            e.stopPropagation();
            const task = lastTasksData.find(t => t.folder === folder && t.filename === filename);
            if (!task) return;
            currentVerifyTask = task;
            
            document.getElementById('vModalTitle').innerText = `Verify: ${task.title}`;
            let html = `
                <div style="margin-bottom: 20px;">
                    <h3 style="color:#6366f1; margin-bottom:8px;"><i class="fas fa-bullseye"></i> Task Summary</h3>
                    <div style="background:rgba(255,255,255,0.05); padding:12px; border-radius:8px;">${escapeHtml(task.summary)}</div>
                </div>
                <div style="margin-bottom: 20px;">
                    <h3 style="color:#10b981; margin-bottom:8px;"><i class="fas fa-code-branch"></i> Changes Made</h3>
                    <div style="background:rgba(255,255,255,0.05); padding:12px; border-radius:8px;"><pre style="background:transparent; padding:0; margin:0;">${escapeHtml(task.changes_made)}</pre></div>
                </div>
                <div style="margin-bottom: 20px;">
                    <h3 style="color:#f59e0b; margin-bottom:8px;"><i class="fas fa-flask"></i> Validation Steps</h3>
                    <div style="background:rgba(255,255,255,0.05); padding:12px; border-radius:8px;"><pre style="background:transparent; padding:0; margin:0;">${escapeHtml(task.validation)}</pre></div>
                </div>
                
                <div style="display:flex; gap:10px; margin-top:20px;">
                    <button class="search-btn" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%);" onclick="handleVerifyPass()"><i class="fas fa-check"></i> Pass & Complete</button>
                    <button class="search-btn" style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);" onclick="openVerifyFail()"><i class="fas fa-times"></i> Fail & Request Fix</button>
                </div>
                <div id="verifyFailBox" style="display:none; margin-top:20px;">
                    <textarea id="verifyFeedbackText" style="width:100%; height:100px; background:rgba(0,0,0,0.3); border:1px solid #ef4444; color:white; padding:10px; border-radius:8px;" placeholder="Describe exactly why validation failed so the agent can fix it..."></textarea>
                    <button class="search-btn" style="background:#ef4444; margin-top:10px;" onclick="handleVerifyFailSubmit()">Submit Failure</button>
                </div>
            `;
            document.getElementById('vModalBody').innerHTML = html;
            document.getElementById('verifyModal').style.display = 'flex';
        }

        function openVerifyFail() {
            document.getElementById('verifyFailBox').style.display = 'block';
        }

        async function handleVerifyPass() {
            if(!currentVerifyTask) return;
            try {
                const res = await fetch('/api/verify-task', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ folder: currentVerifyTask.folder, filename: currentVerifyTask.filename, action: 'pass' })
                });
                if(res.ok) { closeVerifyModal(); fetchTasks(); }
            } catch(e) {}
        }

        async function handleVerifyFailSubmit() {
            if(!currentVerifyTask) return;
            const fb = document.getElementById('verifyFeedbackText').value;
            try {
                const res = await fetch('/api/verify-task', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ folder: currentVerifyTask.folder, filename: currentVerifyTask.filename, action: 'fail', feedback: fb })
                });
                if(res.ok) { closeVerifyModal(); fetchTasks(); }
            } catch(e) {}
        }
        function getProjectColor(project) {
            let hash = 0;
            for (let i = 0; i < project.length; i++) {
                hash = project.charCodeAt(i) + ((hash << 5) - hash);
            }
            const h = Math.abs(hash) % 360;
            // Generate distinct vibrant colors
            return `hsl(${h}, 70%, 65%)`; 
        }

        function createCardHtml(task) {
            const color = getProjectColor(task.project);
            let timeStr = task.timestamp;
            if(timeStr.length === 15) { // format yyyymmdd_hhmmss
                timeStr = `${timeStr.slice(0,4)}-${timeStr.slice(4,6)}-${timeStr.slice(6,8)} ${timeStr.slice(9,11)}:${timeStr.slice(11,13)}`;
            }

            let progressHtml = '';
            if (task.progress !== null && task.progress !== undefined) {
                let p = Math.max(0, Math.min(100, task.progress));
                progressHtml = `
                    <div style="margin-top: 12px; margin-bottom: 4px; display: flex; align-items: center; justify-content: space-between; font-size: 0.75em; color: var(--text-dim); font-weight: 600;">
                        <span>PROGRESS</span>
                        <span>${p}%</span>
                    </div>
                    <div style="margin-bottom: 12px; height: 6px; background: rgba(0,0,0,0.3); border-radius: 4px; overflow: hidden; position: relative;">
                        <div style="width: ${p}%; height: 100%; background: linear-gradient(90deg, #6366f1, #a855f7); border-radius: 4px; transition: width 0.3s ease; box-shadow: 0 0 10px rgba(99, 102, 241, 0.4);"></div>
                    </div>
                `;
            }

            let verifyBadge = '';
            if (task.needs_verification && task.folder.includes("200_inprogress")) {
                verifyBadge = `<button onclick="openVerifyModal(event, '${task.folder}', '${task.filename}')" style="background:#f59e0b; color:#111; border:none; padding:4px 8px; border-radius:4px; font-weight:800; cursor:pointer; font-size:0.8em; z-index:10; float:right;">🔍 VERIFY</button>`;
            }
            
            let priorityBadge = '';
            if (task.priority) {
                if (task.priority === 1) priorityBadge = `<span style="background:rgba(239, 68, 68, 0.2); color:#ef4444; border:1px solid #ef4444; padding:2px 6px; border-radius:4px; font-size:0.7em; margin-right:5px; font-weight:800;">⚡ P1</span>`;
                else if (task.priority === 2) priorityBadge = `<span style="background:rgba(99, 102, 241, 0.2); color:#a855f7; border:1px solid #8b5cf6; padding:2px 6px; border-radius:4px; font-size:0.7em; margin-right:5px; font-weight:800;">⚙️ P2</span>`;
                else if (task.priority === 3) priorityBadge = `<span style="background:rgba(255, 255, 255, 0.1); color:#94a3b8; border:1px solid #475569; padding:2px 6px; border-radius:4px; font-size:0.7em; margin-right:5px; font-weight:600;">💤 P3</span>`;
            }

            return `
                <div class="task-card" draggable="true" ondragstart="handleDragStart(event, '${task.folder}', '${task.filename}')" style="border-left-color: ${color}" onclick="openFile('${task.folder}', '${task.filename}')">
                    ${verifyBadge}
                    <div class="project-badge" style="background: ${color}20; color: ${color}; border: 1px solid ${color}40;">
                        ${task.project}
                    </div>
                    <div class="task-title">${priorityBadge}${task.title}</div>
                    <div class="task-summary">${task.summary}</div>
                    ${progressHtml}
                    <div class="task-footer">
                        <span><i class="far fa-folder" style="color:#6366f1"></i> ${task.folder.replace('_', ' ')}</span>
                        <span class="task-date"><i class="far fa-clock"></i> ${timeStr}</span>
                    </div>
                </div>
            `;
        }

        let currentFileContext = null;

        function closeModal(e) {
            if (e && e.target.id === 'contentModal') {
                document.getElementById('contentModal').style.display = 'none';
            } else if (!e) {
                document.getElementById('contentModal').style.display = 'none';
            }
        }

        async function openAndCloseLocal() {
            if (!currentFileContext) return;
            try {
                await fetch('/api/open-file', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(currentFileContext)
                });
            } catch(err) {}
        }

        async function openFile(folder, filename) {
            currentFileContext = { folder, filename };
            document.getElementById('modalTitle').innerText = filename;
            document.getElementById('modalContentText').innerText = "Loading document contents...";
            document.getElementById('contentModal').style.display = 'flex';
            
            const delBtn = document.getElementById('deleteBtnModal');
            const editBtn = document.getElementById('editBtnModal');
            if (folder === '000_backlog/general' || folder === '000_backlog' || folder.includes('100_todo') || folder.includes('200_inprogress')) {
                delBtn.style.display = (folder === '000_backlog/general' || folder === '000_backlog') ? 'flex' : 'none';
                editBtn.style.display = (folder.includes('100_todo') || folder.includes('200_inprogress') || folder.includes('backlog')) ? 'flex' : 'none';
            } else {
                delBtn.style.display = 'none';
                editBtn.style.display = 'none';
            }
            
            try {
                const res = await fetch(`/api/file-content?folder=${encodeURIComponent(folder)}&filename=${encodeURIComponent(filename)}`);
                const data = await res.json();
                if (data.success) {
                    document.getElementById('modalContentText').innerText = data.content;
                } else {
                    document.getElementById('modalContentText').innerText = "❌ Error: " + data.error;
                }
            } catch (err) {
                console.error("Failed to fetch file content", err);
                document.getElementById('modalContentText').innerText = "❌ Failed to load content completely. See console for details.";
            }
        }

        async function deleteCurrentFile() {
            if (!currentFileContext) return;
            const sf = currentFileContext.folder;
            if (sf !== '000_backlog/general' && sf !== '000_backlog') {
                alert("Only items in general backlog can be directly deleted.");
                return;
            }
            if (!confirm(`Are you sure you want to permanently delete:\n\n${currentFileContext.filename}\n\nThis action cannot be undone.`)) {
                return;
            }
            
            try {
                const res = await fetch('/api/delete-task', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(currentFileContext)
                });
                const data = await res.json();
                if (data.success) {
                    closeModal();
                    fetchTasks();
                } else {
                    alert("Error deleting:\n" + data.error);
                }
            } catch(err) {
                console.error("Delete failed", err);
                alert("Network error processing deletion.");
            }
        }

        let lastTasksData = [];
        let expandedGroups = {};
        let expandAllForce = false;
        let expandedGroupsBacklog = {};
        let expandAllForceBacklog = false;
        let expandedGroupsTodo = {};
        let expandAllForceTodo = false;
        let expandedGroupsInprogress = {};
        let expandAllForceInprogress = false;
        let expandedGroupsFailed = {};
        let expandAllForceFailed = false;
        
        // Drag and Drop State
        let dragSrcFolder = null;
        let dragFilename = null;

        function handleDragStart(e, folder, filename) {
            dragSrcFolder = folder;
            dragFilename = filename;
            e.dataTransfer.effectAllowed = 'move';
            e.dataTransfer.setData('text/plain', filename);
            e.stopPropagation();
        }

        function handleDragOver(e) {
            e.preventDefault();
            e.dataTransfer.dropEffect = 'move';
        }

        async function handleDrop(e, targetFolder) {
            e.preventDefault();
            e.stopPropagation();
            if(!dragFilename || !dragSrcFolder) return;
            
            // Allow drop to different column conceptually
            if(dragSrcFolder === targetFolder) return;
            
            try {
                await fetch('/api/move-task', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        source_folder: dragSrcFolder,
                        target_folder: targetFolder,
                        filename: dragFilename
                    })
                });
                fetchTasks(); // Force immediate re-render
            } catch(err) {
                 console.error("Failed to execute move-task", err);
            }
            dragFilename = null;
            dragSrcFolder = null;
        }

        function toggleGroup(proj, e) {
            if(e) e.stopPropagation();
            expandedGroups[proj] = !expandedGroups[proj];
            renderBoard(lastTasksData);
        }

        function toggleGroupBacklog(proj, e) {
            if(e) e.stopPropagation();
            expandedGroupsBacklog[proj] = !expandedGroupsBacklog[proj];
            renderBoard(lastTasksData);
        }

        function toggleAllComplete() {
            expandAllForce = !expandAllForce;
            const btn = document.getElementById('toggleAllBtn');
            if(expandAllForce) {
                btn.innerText = "Collapse All";
            } else {
                btn.innerText = "Expand All";
                expandedGroups = {};
            }
            renderBoard(lastTasksData);
        }

        function toggleAllBacklog() {
            expandAllForceBacklog = !expandAllForceBacklog;
            const btn = document.getElementById('toggleAllBacklogBtn');
            if(expandAllForceBacklog) {
                btn.innerText = "Collapse All";
            } else {
                btn.innerText = "Expand All";
                expandedGroupsBacklog = {};
            }
            renderBoard(lastTasksData);
        }

        function toggleGroupTodo(proj, e) {
            if(e) e.stopPropagation();
            expandedGroupsTodo[proj] = !expandedGroupsTodo[proj];
            renderBoard(lastTasksData);
        }

        function toggleAllTodo() {
            expandAllForceTodo = !expandAllForceTodo;
            const btn = document.getElementById('toggleAllTodoBtn');
            if(expandAllForceTodo) {
                btn.innerText = "Collapse All";
            } else {
                btn.innerText = "Expand All";
                expandedGroupsTodo = {};
            }
            renderBoard(lastTasksData);
        }

        function toggleGroupInprogress(proj, e) {
            if(e) e.stopPropagation();
            expandedGroupsInprogress[proj] = !expandedGroupsInprogress[proj];
            renderBoard(lastTasksData);
        }

        function toggleAllInprogress() {
            expandAllForceInprogress = !expandAllForceInprogress;
            const btn = document.getElementById('toggleAllInprogressBtn');
            if(expandAllForceInprogress) {
                btn.innerText = "Collapse All";
            } else {
                btn.innerText = "Expand All";
                expandedGroupsInprogress = {};
            }
            renderBoard(lastTasksData);
        }

        function toggleGroupFailed(proj, e) {
            if(e) e.stopPropagation();
            expandedGroupsFailed[proj] = !expandedGroupsFailed[proj];
            renderBoard(lastTasksData);
        }

        function toggleAllFailed() {
            expandAllForceFailed = !expandAllForceFailed;
            const btn = document.getElementById('toggleAllFailedBtn');
            if(expandAllForceFailed) {
                btn.innerText = "Collapse All";
            } else {
                btn.innerText = "Expand All";
                expandedGroupsFailed = {};
            }
            renderBoard(lastTasksData);
        }

        let currentlyReviewing = null;
        async function checkReviewTasks() {
            const reviews = lastTasksData.filter(t => t.folder.startsWith('050_review'));
            if (reviews.length > 0 && !currentlyReviewing) {
                // Group by agent/backlog core
                const agent = reviews[0].folder.split('/')[1] || 'general';
                // Extract core name
                let coreName = "Unknown Backlog";
                const match = reviews[0].filename.match(/from_(.+)\.md$/);
                if(match) coreName = match[1];

                currentlyReviewing = { agent, coreName, tasks: reviews };
                
                document.getElementById('modalTitle').innerHTML = `Awaiting Approval: <span>${coreName}</span>`;
                let taskListStr = reviews.map(t => `<div style="background:rgba(255,255,255,0.05); padding:10px; margin-bottom:8px; border-radius:8px; border-left:3px solid #6366f1;">${t.filename}</div>`).join('');
                document.getElementById('modalContentText').innerHTML = `
                    <div style="margin-bottom:15px; font-size:1.1em; color:#cbd5e1;">The <b>${agent.toUpperCase()}</b> agent has generated the following draft tasks:</div>
                    ${taskListStr}
                    <div style="margin-top:20px; display:flex; gap:10px;">
                        <button class="search-btn" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%);" onclick="handleReviewApprove()"><i class="fas fa-check"></i> Approve & Proceed</button>
                        <button class="search-btn" style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);" onclick="handleReviewModify()"><i class="fas fa-edit"></i> Request Changes</button>
                        <button class="search-btn" style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);" onclick="handleReviewReject()"><i class="fas fa-ban"></i> Reject & Suspend</button>
                    </div>
                    <div id="reviewFeedbackBox" style="display:none; margin-top:15px;">
                        <textarea id="reviewFeedbackText" style="width:100%; height:80px; background:rgba(0,0,0,0.3); border:1px solid #6366f1; color:white; padding:10px; border-radius:8px;" placeholder="Describe what changes or additions are needed..."></textarea>
                        <button class="search-btn" style="margin-top:10px; padding:8px 16px; font-size:0.9em;" onclick="submitReviewModify()">Submit Feedback</button>
                    </div>
                `;
                
                document.getElementById('contentModal').style.display = 'flex';
                document.getElementById('deleteBtnModal').style.display = 'none';
            } else if (reviews.length === 0 && currentlyReviewing) {
                currentlyReviewing = null;
                closeModal();
            }
        }

        async function handleReviewApprove() {
            if(!currentlyReviewing) return;
            const res = await fetch('/api/review-approve', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(currentlyReviewing) });
            if(res.ok) fetchTasks();
        }
        function handleReviewModify() {
            document.getElementById('reviewFeedbackBox').style.display = 'block';
        }
        async function submitReviewModify() {
            if(!currentlyReviewing) return;
            const fb = document.getElementById('reviewFeedbackText').value;
            const res = await fetch('/api/review-modify', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({ ...currentlyReviewing, feedback: fb }) });
            if(res.ok) { currentlyReviewing = null; closeModal(); fetchTasks(); }
        }
        async function handleReviewReject() {
            if(!currentlyReviewing) return;
            if(!confirm("Are you sure you want to discard these drafts and suspend the backlog?")) return;
            const res = await fetch('/api/review-reject', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(currentlyReviewing) });
            if(res.ok) fetchTasks();
        }

        function renderBoard(tasks) {
            const groups = {
                "000_backlog": [], "100_todo": [], "200_inprogress": [], "300_complete": [], "400_failed": []
            };
            
            const agentList = [
                { name: "🤖 Codex", handle: "codex" },
                { name: "✨ Gemini", handle: "gemini" },
                { name: "🧠 Claude", handle: "claude" },
                { name: "📋 General", handle: "general" },
                { name: "📁 Root", handle: "" }
            ];

            ["000_backlog", "100_todo", "200_inprogress", "300_complete", "400_failed"].forEach(col => {
                const agents = agentList.map(a => ({
                    kanbanGroup: a.name,
                    dropFolder: a.handle ? `${col}/${a.handle}` : col,
                    timestamp: "99999999_999999",
                    isDummy: true,
                    folder: a.handle ? `${col}/${a.handle}` : col
                }));
                groups[col].push(...agents);
            });

            tasks.forEach(t => {
                let col = t.folder;
                if (col.includes("backlog")) col = "000_backlog";
                else if (col.includes("todo")) col = "100_todo";
                else if (col.includes("inprogress")) col = "200_inprogress";
                else if (col.includes("complete")) col = "300_complete";
                else if (col.includes("failed")) col = "400_failed";
                
                if (groups[col]) {
                    if (["000_backlog", "100_todo", "200_inprogress", "300_complete", "400_failed"].includes(col)) {
                        if (t.folder.endsWith("codex")) { t.kanbanGroup = "🤖 Codex"; t.dropFolder = `${col}/codex`; }
                        else if (t.folder.endsWith("gemini")) { t.kanbanGroup = "✨ Gemini"; t.dropFolder = `${col}/gemini`; }
                        else if (t.folder.endsWith("claude")) { t.kanbanGroup = "🧠 Claude"; t.dropFolder = `${col}/claude`; }
                        else if (t.folder.endsWith("general")) { t.kanbanGroup = "📋 General"; t.dropFolder = `${col}/general`; }
                        else { t.kanbanGroup = "📁 Root"; t.dropFolder = col; }
                    } else {
                        t.kanbanGroup = t.project;
                        t.dropFolder = col;
                    }
                    groups[col].push(t);
                }
            });

            for (const folder in groups) {
                // Filter out the dummy tasks when taking real column counts
                const realTasks = groups[folder].filter(t => !t.isDummy);
                const sortedTasks = realTasks.sort((a,b) => b.timestamp.localeCompare(a.timestamp));
                document.getElementById(`count-${folder}`).innerText = realTasks.length;
                
                if (["300_complete", "000_backlog", "100_todo", "200_inprogress", "400_failed"].includes(folder)) {
                     const groupedByProject = {};
                     groups[folder].forEach(t => {
                         if(!groupedByProject[t.kanbanGroup]) groupedByProject[t.kanbanGroup] = [];
                         groupedByProject[t.kanbanGroup].push(t);
                     });
                     
                     // Ensure the projects themselves are ordered by the newest timestamp in their group
                     const sortedProjects = Object.keys(groupedByProject).sort((a,b) => {
                         const timeA = groupedByProject[a][0] ? groupedByProject[a][0].timestamp : "";
                         const timeB = groupedByProject[b][0] ? groupedByProject[b][0].timestamp : "";
                         return timeB.localeCompare(timeA);
                     });
                     
                     let groupHtml = '';
                     for (const proj of sortedProjects) {
                         const projColor = getProjectColor(proj);
                         
                         // Explicitly sort the tasks inside the group descending by timestamp
                         groupedByProject[proj].sort((a,b) => b.timestamp.localeCompare(a.timestamp));
                         // Filter out the dummy task during loop rendering
                         const realCards = groupedByProject[proj].filter(t => !t.isDummy);
                         const projCount = realCards.length;
                         
                         let isExpanded = false;
                         let toggleFunc = '';
                         
                         if (folder === "300_complete") {
                             isExpanded = expandAllForce ? true : !!expandedGroups[proj];
                             toggleFunc = `toggleGroup('${proj}', event)`;
                         } else if (folder === "000_backlog") {
                             isExpanded = expandAllForceBacklog ? true : !!expandedGroupsBacklog[proj];
                             toggleFunc = `toggleGroupBacklog('${proj}', event)`;
                         } else if (folder === "100_todo") {
                             isExpanded = expandAllForceTodo ? true : !!expandedGroupsTodo[proj];
                             toggleFunc = `toggleGroupTodo('${proj}', event)`;
                         } else if (folder === "200_inprogress") {
                             isExpanded = expandAllForceInprogress ? true : !!expandedGroupsInprogress[proj];
                             toggleFunc = `toggleGroupInprogress('${proj}', event)`;
                         } else if (folder === "400_failed") {
                             isExpanded = expandAllForceFailed ? true : !!expandedGroupsFailed[proj];
                             toggleFunc = `toggleGroupFailed('${proj}', event)`;
                         }
                         
                         const icon = isExpanded ? 'fa-minus' : 'fa-plus';
                         
                         const dropTarget = groupedByProject[proj][0].dropFolder || folder;
                         
                         groupHtml += `
                            <div class="project-group" ondragover="handleDragOver(event)" ondrop="handleDrop(event, '${dropTarget}')" style="margin-bottom: 12px; border: 1px solid var(--glass-border); border-radius: 12px; overflow: hidden; background: var(--bg-accent);">
                                <div class="group-header" onclick="${toggleFunc}" style="padding: 12px 16px; background: rgba(255,255,255,0.02); cursor: pointer; display: flex; justify-content: space-between; align-items: center; border-left: 4px solid ${projColor};">
                                    <div style="font-weight: 600; color: #cbd5e1; display:flex; align-items:center;"><i class="fas ${icon}" style="margin-right: 8px; color: ${projColor}; width: 14px;"></i> ${proj} <span style="font-size: 0.8em; opacity: 0.6; margin-left: 8px;">(${projCount})</span></div>
                                </div>
                                <div class="group-content" style="display: ${isExpanded ? 'flex' : 'none'}; flex-direction: column; gap: 12px; padding: 12px; background: rgba(0,0,0,0.2);">
                                    ${realCards.map(createCardHtml).join('')}
                                </div>
                            </div>
                         `;
                     }
                     document.getElementById(`list-${folder}`).innerHTML = groupHtml;
                } else {
                    document.getElementById(`list-${folder}`).innerHTML = sortedTasks.map(createCardHtml).join('');
                }
            }
            document.getElementById('last-updated').innerText = "Last update: " + new Date().toLocaleTimeString();
        }

        let isSearching = false;

        async function performSearch() {
            const q = document.getElementById('searchInput').value.trim();
            if (!q) {
                clearSearch();
                return;
            }
            
            isSearching = true;
            document.getElementById('mainBoard').style.display = 'none';
            document.getElementById('searchResults').style.display = 'block';
            document.getElementById('clearSearchBtn').style.display = 'inline-block';
            document.getElementById('searchResultsList').innerHTML = '<div style="text-align:center; padding:30px;"><i class="fas fa-spinner fa-spin fa-2x"></i><p style="margin-top:10px;">Searching...</p></div>';
            
            try {
                const res = await fetch(`/api/search?q=${encodeURIComponent(q)}`);
                const data = await res.json();
                
                if (data.success) {
                    document.getElementById('searchCount').innerText = data.results.length;
                    if (data.results.length === 0) {
                        document.getElementById('searchResultsList').innerHTML = '<div style="text-align:center; padding:30px; color: var(--text-dim);"><i class="fas fa-box-open fa-2x"></i><p style="margin-top:10px;">No matching tasks found.</p></div>';
                    } else {
                        let html = '';
                        data.results.forEach(r => {
                            let stateColor = '#6366f1';
                            if (r.state === 'Complete') stateColor = '#22c55e';
                            else if (r.state === 'Todo') stateColor = '#eab308';
                            else if (r.state === 'In Progress') stateColor = '#f59e0b';
                            
                            html += `
                                <div class="task-card" style="border-left-color: ${stateColor}; max-width: 800px; margin: 0 auto 12px auto;" onclick="openFile('${r.folder}', '${r.filename}')">
                                    <div style="display:flex; justify-content:space-between; align-items:center;">
                                        <div class="project-badge" style="background: ${stateColor}20; color: ${stateColor}; border: 1px solid ${stateColor}40; margin-bottom: 0;">
                                            ${r.state}
                                        </div>
                                        <div class="task-date"><i class="far fa-clock"></i> ${r.date}</div>
                                    </div>
                                    <div class="task-title" style="margin-top: 12px;">${r.filename}</div>
                                    <div class="search-snippet">${r.snippet.replace(/</g, "&lt;").replace(/>/g, "&gt;")}</div>
                                </div>
                            `;
                        });
                        document.getElementById('searchResultsList').innerHTML = html;
                    }
                }
            } catch (err) {
                document.getElementById('searchResultsList').innerHTML = '<p style="color:#f43f5e; text-align:center;">Error searching.</p>';
            }
        }
        
        function clearSearch() {
            document.getElementById('searchInput').value = '';
            isSearching = false;
            document.getElementById('mainBoard').style.display = 'grid';
            document.getElementById('searchResults').style.display = 'none';
            document.getElementById('clearSearchBtn').style.display = 'none';
            fetchTasks();
        }

        async function fetchTasks() {
            if (isSearching) return;
            try {
                const res = await fetch('/api/tasks');
                lastTasksData = await res.json();
                renderBoard(lastTasksData);
                checkReviewTasks();
            } catch (err) {
                console.error("Failed to fetch tasks", err);
            }
        }

        // Initial fetch and poll every 2 seconds
        fetchTasks();
        setInterval(fetchTasks, 2000);
    