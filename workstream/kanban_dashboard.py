import os
import json
import re
import shlex
import sys
import datetime
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn

WORKSTREAM_DIR = r"C:\Users\edebe\eds\workstream"
FOLDERS = [
    "000_backlog", "000_backlog/codex", "000_backlog/gemini", "000_backlog/claude", "000_backlog/general",
    "050_review", "050_review/codex", "050_review/gemini", "050_review/claude", "050_review/general",
    "100_todo", "100_todo/codex", "100_todo/gemini", "100_todo/claude", "100_todo/general",
    "200_inprogress", "200_inprogress/codex", "200_inprogress/gemini", "200_inprogress/claude", "200_inprogress/general",
    "300_complete", "300_complete/codex", "300_complete/gemini", "300_complete/claude", "300_complete/general",
    "400_failed", "400_failed/codex", "400_failed/gemini", "400_failed/claude", "400_failed/general"
]

# The duration in seconds for the news ticker to complete one full scroll across the screen
TICKER_SCROLL_SPEED_SECONDS = 240

# HTML Template exactly matching beautiful dark mode UI guidelines
HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Workstream Kanban Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --bg-deep: #080a18;
            --bg-accent: #0f1225;
            --glass-bg: rgba(255, 255, 255, 0.03);
            --glass-border: rgba(255, 255, 255, 0.08);
            --text-main: #f1f5f9;
            --text-dim: #94a3b8;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Outfit', sans-serif;
            background: radial-gradient(circle at 50% 0%, #1e1b4b 0%, var(--bg-deep) 100%);
            color: var(--text-main);
            min-height: 100vh;
            padding: 30px;
        }
        .header {
            text-align: center; margin-bottom: 40px; padding: 30px;
            background: var(--glass-bg); backdrop-filter: blur(20px);
            border-radius: 24px; border: 1px solid var(--glass-border);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        }
        .header h1 { font-size: 2.5em; font-weight: 800; margin-bottom: 10px; background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .kanban-board {
            display: grid; grid-template-columns: repeat(6, 1fr); gap: 24px;
            align-items: start;
        }
        .kanban-column {
            background: rgba(15, 18, 37, 0.6);
            border-radius: 20px; border: 1px solid var(--glass-border);
            padding: 20px; min-height: 500px;
            display: flex; flex-direction: column; gap: 16px;
        }
        .column-header {
            display: flex; justify-content: space-between; align-items: center;
            padding-bottom: 15px; border-bottom: 1px solid var(--glass-border);
            margin-bottom: 10px; font-weight: 700; font-size: 1.1em;
            color: #cbd5e1;
            text-transform: uppercase; letter-spacing: 1px;
        }
        .task-count {
            background: rgba(255, 255, 255, 0.1); padding: 2px 8px;
            border-radius: 12px; font-size: 0.8em; font-family: monospace;
        }
        .task-card {
            background: var(--glass-bg); border: 1px solid var(--glass-border);
            border-radius: 16px; padding: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            transition: transform 0.2s, box-shadow 0.2s;
            cursor: pointer;
            border-left: 4px solid #6366f1; /* Default project color */
        }
        .task-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.4);
            background: rgba(255, 255, 255, 0.06);
        }
        .project-badge {
            display: inline-block; padding: 4px 10px; font-size: 0.7em;
            font-weight: 700; text-transform: uppercase; border-radius: 8px;
            margin-bottom: 12px; letter-spacing: 1px;
        }
        .task-title {
            font-size: 1.1em; font-weight: 600; margin-bottom: 8px; line-height: 1.4;
        }
        .task-summary {
            font-size: 0.85em; color: var(--text-dim); margin-bottom: 15px;
            line-height: 1.5;
        }
        .task-footer {
            display: flex; justify-content: space-between; align-items: center;
            font-size: 0.75em; color: var(--text-dim); border-top: 1px solid var(--glass-border);
            padding-top: 10px;
        }
        .task-date { font-family: monospace; opacity: 0.8; }
        
        /* Modal Styles */
        .modal-overlay {
            display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.7); backdrop-filter: blur(8px);
            z-index: 1000; justify-content: center; align-items: center;
        }
        .modal-content {
            background: var(--bg-accent); border: 1px solid var(--glass-border);
            border-radius: 16px; width: 90%; max-width: 1000px; max-height: 85vh;
            display: flex; flex-direction: column; overflow: hidden;
            box-shadow: 0 15px 50px rgba(0,0,0,0.5);
            animation: fadeIn 0.2s ease-out forwards;
        }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        .modal-header {
            padding: 20px; border-bottom: 1px solid var(--glass-border);
            display: flex; justify-content: space-between; align-items: center;
            background: rgba(15, 18, 37, 0.8);
        }
        .modal-header h2 { font-size: 1.2em; color: #a855f7; display: flex; align-items: center; gap: 10px; }
        .modal-header h2 i { color: #6366f1; }
        .close-btn {
            background: rgba(255, 255, 255, 0.05); border: 1px solid var(--glass-border); color: var(--text-dim);
            font-size: 1.2em; cursor: pointer; transition: all 0.2s; border-radius: 8px; width: 36px; height: 36px;
            display: flex; align-items: center; justify-content: center;
        }
        .close-btn:hover { background: rgba(244, 63, 94, 0.2); color: var(--rose, #f43f5e); border-color: rgba(244, 63, 94, 0.4); }
        .btn-action {
            background: rgba(99, 102, 241, 0.15); border: 1px solid rgba(99, 102, 241, 0.3); color: #818cf8;
            padding: 8px 16px; border-radius: 8px; font-size: 0.9em; font-weight: 600; cursor: pointer; transition: all 0.2s;
            display: flex; align-items: center; gap: 8px;
        }
        .btn-action:hover { background: rgba(99, 102, 241, 0.3); color: #fff; }
        .modal-body {
            padding: 25px; overflow-y: auto; flex-grow: 1;
        }
        .modal-body pre {
            white-space: pre-wrap; word-wrap: break-word; font-family: 'JetBrains Mono', Consolas, monospace;
            font-size: 0.95em; line-height: 1.6; color: #cbd5e1;
        }
        .search-container {
            margin-top: 20px;
            display: flex;
            justify-content: center;
            gap: 10px;
        }
        .search-input {
            padding: 12px 20px;
            border-radius: 20px;
            border: 1px solid var(--glass-border);
            background: rgba(0,0,0,0.2);
            color: var(--text-main);
            width: 400px;
            font-family: 'Outfit', sans-serif;
            font-size: 1rem;
        }
        .search-input:focus { outline: none; border-color: #a855f7; }
        .search-btn {
            background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
            border: none;
            padding: 12px 24px;
            border-radius: 20px;
            color: white;
            cursor: pointer;
            font-weight: 600;
        }
        #searchResults {
            display: none;
            background: rgba(15, 18, 37, 0.6);
            border-radius: 20px; border: 1px solid var(--glass-border);
            padding: 20px;
            margin-top: 20px;
        }
        .search-snippet {
            font-family: 'JetBrains Mono', Consolas, monospace;
            font-size: 0.85em; color: #a855f7; background: rgba(0,0,0,0.3);
            padding: 8px; border-radius: 6px; margin-top: 8px;
        }
        
        /* News Ticker Components */
        .ticker-wrap {
            width: 100%;
            overflow: hidden;
            background: rgba(15, 18, 37, 0.9);
            border-bottom: 1px solid var(--glass-border);
            padding: 8px 0;
            box-sizing: content-box;
            position: relative;
        }
        .ticker {
            display: inline-block;
            white-space: nowrap;
            padding-right: 100%;
            box-sizing: content-box;
            transform: translateX(0);
            animation: ticker ##TICKER_SCROLL_SPEED##s linear infinite;
        }
        .ticker:hover {
            animation-play-state: paused;
        }
        @keyframes ticker {
            0% { transform: translateX(100vw); }
            100% { transform: translateX(-100%); }
        }
        .ticker-item {
            display: inline-block;
            padding: 0 30px;
            font-family: 'Outfit', sans-serif;
            font-size: 0.95em;
            font-weight: 500;
        }
        .ticker-agent { color: #a855f7; font-weight: 800; text-transform: uppercase; }
        .ticker-state { color: #6366f1; font-weight: 600; text-transform: uppercase; margin: 0 5px; }
        .ticker-task { color: var(--text-main); }
        .ticker-separator { color: #f43f5e; margin: 0 15px; font-weight: 800; display: inline-block; }

    </style>
</head>
<body>
    <div class="ticker-wrap">
        <div class="ticker" id="newsTicker">
            <span class="ticker-item"><span class="ticker-agent">SYSTEM</span> <span class="ticker-state">INITIALIZING</span> <span class="ticker-task">Fetching latest kanban pipeline statuses...</span></span>
        </div>
    </div>
    
    <div class="header">
        <h1>🚀 Workstream Kanban</h1>
        <p style="color: var(--text-dim);">Real-time workflow monitoring (Refreshes every 2s) <br> <span id="last-updated" style="font-family: monospace; font-size: 0.9em; color: #a855f7;"></span></p>
        <div class="search-container">
            <input type="text" id="searchInput" class="search-input" placeholder="Search task contents, titles..." onkeyup="if(event.key === 'Enter') performSearch()">
            <button class="search-btn" onclick="performSearch()"><i class="fas fa-search"></i> Search</button>
            <button class="search-btn" id="clearSearchBtn" style="display:none; background: rgba(244, 63, 94, 0.2); color: #f43f5e;" onclick="clearSearch()"><i class="fas fa-times"></i> Clear</button>
            <button class="search-btn" style="margin-left:20px; background: linear-gradient(135deg, #10b981 0%, #059669 100%);" onclick="openCreateModal()"><i class="fas fa-plus"></i> Create Entry</button>
        </div>
    </div>

    <div class="kanban-board" id="mainBoard">
        <div class="kanban-column" id="col-000_backlog" ondragover="handleDragOver(event)" ondrop="handleDrop(event, '000_backlog')">
            <div class="column-header">
                <div>📋 Backlog <span class="task-count" id="count-000_backlog">0</span></div>
                <button id="toggleAllBacklogBtn" onclick="toggleAllBacklog()" style="background:transparent; border:1px solid #6366f1; color:#6366f1; border-radius:4px; cursor:pointer; font-size:0.6em; padding:4px 8px; text-transform: uppercase;">Expand All</button>
            </div>
            <div class="column-content" id="list-000_backlog"></div>
        </div>
        <div class="kanban-column" id="col-050_review" ondragover="handleDragOver(event)" ondrop="handleDrop(event, '050_review')">
            <div class="column-header">
                <div>📝 Review <span class="task-count" id="count-050_review">0</span></div>
            </div>
            <div class="column-content" id="list-050_review"></div>
        </div>
        <div class="kanban-column" id="col-100_todo" ondragover="handleDragOver(event)" ondrop="handleDrop(event, '100_todo')">
            <div class="column-header">
                <div>🎯 To Do <span class="task-count" id="count-100_todo">0</span></div>
                <button id="toggleAllTodoBtn" onclick="toggleAllTodo()" style="background:transparent; border:1px solid #6366f1; color:#6366f1; border-radius:4px; cursor:pointer; font-size:0.6em; padding:4px 8px; text-transform: uppercase;">Expand All</button>
            </div>
            <div class="column-content" id="list-100_todo"></div>
        </div>
        <div class="kanban-column" id="col-200_inprogress" ondragover="handleDragOver(event)" ondrop="handleDrop(event, '200_inprogress')">
            <div class="column-header">
                <div>⚡ In Progress <span class="task-count" id="count-200_inprogress">0</span></div>
                <button id="toggleAllInprogressBtn" onclick="toggleAllInprogress()" style="background:transparent; border:1px solid #6366f1; color:#6366f1; border-radius:4px; cursor:pointer; font-size:0.6em; padding:4px 8px; text-transform: uppercase;">Expand All</button>
            </div>
            <div class="column-content" id="list-200_inprogress"></div>
        </div>
        <div class="kanban-column" id="col-300_complete" ondragover="handleDragOver(event)" ondrop="handleDrop(event, '300_complete')">
            <div class="column-header">
                <div>✅ Complete <span class="task-count" id="count-300_complete">0</span></div>
                <button id="toggleAllBtn" onclick="toggleAllComplete()" style="background:transparent; border:1px solid #6366f1; color:#6366f1; border-radius:4px; cursor:pointer; font-size:0.6em; padding:4px 8px; text-transform: uppercase;">Expand All</button>
            </div>
            <div class="column-content" id="list-300_complete"></div>
        </div>
        <div class="kanban-column" id="col-400_failed" ondragover="handleDragOver(event)" ondrop="handleDrop(event, '400_failed')">
            <div class="column-header">
                <div>💥 Failed & Blocked <span class="task-count" id="count-400_failed">0</span></div>
                <button id="toggleAllFailedBtn" onclick="toggleAllFailed()" style="background:transparent; border:1px solid #ef4444; color:#ef4444; border-radius:4px; cursor:pointer; font-size:0.6em; padding:4px 8px; text-transform: uppercase;">Expand All</button>
            </div>
            <div class="column-content" id="list-400_failed"></div>
        </div>
    </div>
    
    <div id="searchResults">
        <h2 style="margin-bottom: 20px;"><i class="fas fa-search"></i> Search Results (<span id="searchCount">0</span>)</h2>
        <div id="searchResultsList"></div>
    </div>

    <!-- Modal Overlay -->
    <div id="contentModal" class="modal-overlay" onclick="closeModal(event)">
        <div class="modal-content" onclick="event.stopPropagation()">
            <div class="modal-header">
                <h2><i class="far fa-file-alt"></i> <span id="modalTitle">Loading Document...</span></h2>
                <div style="display:flex; gap:10px;">
                    <button class="btn-action" id="editBtnModal" onclick="openEditModal()" style="display:none; background: rgba(16, 185, 129, 0.2); color: #10b981; border-color: rgba(16, 185, 129, 0.4);" title="Edit Task">
                        <i class="fas fa-edit"></i> Edit
                    </button>
                    <button class="btn-action" onclick="openAndCloseLocal()" title="Open externally in VSCode/Editor">
                        <i class="fas fa-external-link-alt"></i> Open Externally
                    </button>
                    <button class="btn-action" id="deleteBtnModal" onclick="deleteCurrentFile()" style="display:none; background: rgba(244, 63, 94, 0.2); color: #f43f5e; border-color: rgba(244, 63, 94, 0.4);" title="Delete Task">
                        <i class="fas fa-trash"></i> Delete
                    </button>
                    <button class="close-btn" onclick="closeModal()"><i class="fas fa-times"></i></button>
                </div>
            </div>
            <div class="modal-body">
                <pre id="modalContentText"></pre>
            </div>
        </div>
    </div>

    <!-- Verify Modal Overlay -->
    <div id="verifyModal" class="modal-overlay" onclick="closeVerifyModal(event)">
        <div class="modal-content" onclick="event.stopPropagation()">
            <div class="modal-header">
                <h2><i class="fas fa-search"></i> <span id="vModalTitle">Verification Required</span></h2>
                <button class="close-btn" onclick="closeVerifyModal()"><i class="fas fa-times"></i></button>
            </div>
            <div class="modal-body" id="vModalBody">
                <!-- Javascript injects content here -->
            </div>
        </div>
    </div>

    <!-- Feedback Modal Overlay -->
    <div id="feedbackModal" class="modal-overlay" onclick="closeFeedbackModal(event)">
        <div class="modal-content" onclick="event.stopPropagation()">
            <div class="modal-header">
                <h2><i class="fas fa-comment-dots"></i> <span id="fbModalTitle">User Feedback Required</span></h2>
                <button class="close-btn" onclick="closeFeedbackModal()"><i class="fas fa-times"></i></button>
            </div>
            <div class="modal-body" id="fbModalBody">
                <!-- Javascript injects content here -->
            </div>
        </div>
    </div>

    <!-- Create Entry Modal Overlay -->
    <div id="createModal" class="modal-overlay" onclick="closeCreateModal(event)">
        <div class="modal-content" onclick="event.stopPropagation()">
            <div class="modal-header">
                <h2 id="createModalTitle"><i class="fas fa-plus"></i> <span>Create New Entry</span></h2>
                <button class="close-btn" onclick="closeCreateModal()"><i class="fas fa-times"></i></button>
            </div>
            <div class="modal-body">
                <div style="display:grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap:15px; margin-bottom:15px;">
                    <div>
                        <label style="color:#a855f7; font-size:0.85em; font-weight:700; display:block; margin-bottom:5px;">Type</label>
                        <select id="createType" style="width:100%; padding:10px; background:rgba(0,0,0,0.3); border:1px solid #6366f1; color:white; border-radius:8px;">
                            <option value="task">Atomic Task (To Do)</option>
                            <option value="backlog">Backlog Specification</option>
                        </select>
                    </div>
                    <div>
                        <label style="color:#a855f7; font-size:0.85em; font-weight:700; display:block; margin-bottom:5px;">Agent Lane</label>
                        <select id="createAgent" style="width:100%; padding:10px; background:rgba(0,0,0,0.3); border:1px solid #6366f1; color:white; border-radius:8px;">
                            <option value="codex">Codex</option>
                            <option value="gemini">Gemini</option>
                            <option value="claude">Claude</option>
                            <option value="general">General</option>
                            <option value="">📁 ROOT (Hold)</option>
                        </select>
                    </div>
                    <div>
                        <label style="color:#a855f7; font-size:0.85em; font-weight:700; display:block; margin-bottom:5px;">Priority</label>
                        <select id="createPriority" style="width:100%; padding:10px; background:rgba(0,0,0,0.3); border:1px solid #6366f1; color:white; border-radius:8px;">
                            <option value="1">P1 (Immediate/High)</option>
                            <option value="2" selected>P2 (Normal)</option>
                            <option value="3">P3 (Low/Backlog)</option>
                        </select>
                    </div>
                    <div>
                        <label style="color:#a855f7; font-size:0.85em; font-weight:700; display:block; margin-bottom:5px;">Completion Action</label>
                        <select id="createCompletionAction" style="width:100%; padding:10px; background:rgba(0,0,0,0.3); border:1px solid #6366f1; color:white; border-radius:8px;">
                            <option value="Awaiting user verification" selected>Awaiting user verification</option>
                            <option value="Evidence of completion">Evidence of completion</option>
                            <option value="Proceed without permission">Proceed without permission</option>
                            <option value="Proceed with Permission">Proceed with Permission</option>
                            <option value="Provide user feedback">Provide user feedback</option>
                        </select>
                    </div>
                </div>
                <div style="display:grid; grid-template-columns: 1fr 2fr; gap:15px; margin-bottom:15px;">
                    <div>
                        <label style="color:#a855f7; font-size:0.85em; font-weight:700; display:block; margin-bottom:5px;">Project Token (e.g. general, dbx)</label>
                        <input type="text" id="createProject" placeholder="general" value="general" style="width:100%; padding:10px; background:rgba(0,0,0,0.3); border:1px solid #6366f1; color:white; border-radius:8px;">
                    </div>
                    <div>
                        <label style="color:#a855f7; font-size:0.85em; font-weight:700; display:block; margin-bottom:5px;">Title</label>
                        <input type="text" id="createTitle" placeholder="e.g. update configuration parser" style="width:100%; padding:10px; background:rgba(0,0,0,0.3); border:1px solid #6366f1; color:white; border-radius:8px;">
                    </div>
                </div>
                <div style="margin-bottom:20px;">
                    <label style="color:#a855f7; font-size:0.85em; font-weight:700; display:block; margin-bottom:5px;">Requirements / Markdown Content</label>
                    <textarea id="createContent" style="width:100%; height:200px; padding:15px; background:rgba(0,0,0,0.3); border:1px solid #6366f1; color:#e2e8f0; font-family:monospace; border-radius:8px;" placeholder="# Task Summary\n...\n# Implementation Plan\n..."></textarea>
                </div>
                <div style="display:flex; justify-content:flex-end;">
                    <button class="search-btn" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%);" onclick="submitCreate()"><i class="fas fa-save"></i> Save File explicitly to lane</button>
                </div>
            </div>
        </div>
    </div>

    <script>
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
            rawContent = rawContent.replace(/Priority:\\s*\\d+\\n+/, '');
            const compMatches = rawContent.match(/\\n+- `Completion Status`:.*$/i);
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
        
        let currentFeedbackTask = null;
        function closeFeedbackModal(e) {
            if (e && e.target.id === 'feedbackModal') document.getElementById('feedbackModal').style.display = 'none';
            else if (!e) document.getElementById('feedbackModal').style.display = 'none';
        }

        function openFeedbackModal(e, folder, filename) {
            e.stopPropagation();
            const task = lastTasksData.find(t => t.folder === folder && t.filename === filename);
            if (!task) return;
            currentFeedbackTask = task;
            
            document.getElementById('fbModalTitle').innerText = `Feedback: ${task.title}`;
            let html = `
                <div style="margin-bottom: 20px;">
                    <h3 style="color:#6366f1; margin-bottom:8px;"><i class="fas fa-bullseye"></i> Task Summary</h3>
                    <div style="background:rgba(255,255,255,0.05); padding:12px; border-radius:8px;">${escapeHtml(task.summary)}</div>
                </div>
                <div style="margin-bottom: 20px;">
                    <h3 style="color:#10b981; margin-bottom:8px;"><i class="fas fa-code-branch"></i> Changes Made</h3>
                    <div style="background:rgba(255,255,255,0.05); padding:12px; border-radius:8px;"><pre style="background:transparent; padding:0; margin:0;">${escapeHtml(task.changes_made)}</pre></div>
                </div>
                
                <div style="margin-top:20px;">
                    <label style="color:#a855f7; font-size:0.85em; font-weight:700; display:block; margin-bottom:5px;">Specific Feedback On Outcomes / Findings:</label>
                    <textarea id="userFeedbackText" style="width:100%; height:120px; background:rgba(0,0,0,0.3); border:1px solid #0ea5e9; color:white; padding:10px; border-radius:8px;" placeholder="Provide explicit feedback or findings to append to this task..."></textarea>
                </div>
                
                <div style="display:flex; gap:10px; margin-top:20px;">
                    <button class="search-btn" style="background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);" onclick="handleFeedbackSubmit()"><i class="fas fa-paper-plane"></i> Submit & Complete Task</button>
                    <button class="search-btn" style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);" onclick="handleFeedbackReturn()"><i class="fas fa-undo"></i> Submit & Return to ToDo</button>
                </div>
            `;
            document.getElementById('fbModalBody').innerHTML = html;
            document.getElementById('feedbackModal').style.display = 'flex';
        }

        async function postFeedback(action) {
            if(!currentFeedbackTask) return;
            const fb = document.getElementById('userFeedbackText').value;
            if(!fb) { alert('Please provide specific feedback before submitting.'); return; }
            try {
                const res = await fetch('/api/submit-feedback', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ folder: currentFeedbackTask.folder, filename: currentFeedbackTask.filename, action: action, feedback: fb })
                });
                if(res.ok) { closeFeedbackModal(); fetchTasks(); }
            } catch(e) {}
        }
        function handleFeedbackSubmit() { postFeedback('complete'); }
        function handleFeedbackReturn() { postFeedback('todo'); }

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
            if (task.needs_feedback && task.folder.includes("200_inprogress")) {
                verifyBadge += `<button onclick="openFeedbackModal(event, '${task.folder}', '${task.filename}')" style="background:#0ea5e9; color:#fff; border:none; padding:4px 8px; border-radius:4px; font-weight:800; cursor:pointer; font-size:0.8em; z-index:10; float:right; margin-right:5px;">💬 FEEDBACK</button>`;
            }
            if (task.needs_verification && task.folder.includes("200_inprogress")) {
                verifyBadge += `<button onclick="openVerifyModal(event, '${task.folder}', '${task.filename}')" style="background:#f59e0b; color:#111; border:none; padding:4px 8px; border-radius:4px; font-weight:800; cursor:pointer; font-size:0.8em; z-index:10; float:right;">🔍 VERIFY</button>`;
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

        async function openAndCloseLocalReview(folder, filename) {
            try {
                await fetch('/api/open-file', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ folder, filename })
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
            if (!confirm(`Are you sure you want to permanently delete:\\n\\n${currentFileContext.filename}\\n\\nThis action cannot be undone.`)) {
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
                    alert("Error deleting:\\n" + data.error);
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
                const match = reviews[0].filename.match(/from_(.+)\\.md$/);
                if(match) coreName = match[1];

                currentlyReviewing = { agent, coreName, tasks: reviews };
                
                document.getElementById('modalTitle').innerHTML = `Awaiting Approval: <span>${coreName}</span>`;
                let taskListStr = reviews.map(t => `
                    <div style="background:rgba(255,255,255,0.05); padding:10px; margin-bottom:8px; border-radius:8px; border-left:3px solid #6366f1;">
                        <div style="display:flex; align-items:center; justify-content:space-between; gap:10px;">
                            <div style="word-break:break-word; color:#e2e8f0;">${t.filename}</div>
                            <div style="display:flex; gap:8px; flex-shrink:0;">
                                <button class="search-btn" style="padding:6px 10px; font-size:0.8em;" onclick="openFile('${t.folder}', '${t.filename}')" title="Preview file contents in-app"><i class="fas fa-eye"></i> Preview</button>
                                <button class="search-btn" style="padding:6px 10px; font-size:0.8em; background: rgba(99,102,241,0.2);" onclick="openAndCloseLocalReview('${t.folder}', '${t.filename}')" title="Open file externally"><i class="fas fa-external-link-alt"></i> External</button>
                            </div>
                        </div>
                    </div>
                `).join('');
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
                "000_backlog": [], "050_review": [], "100_todo": [], "200_inprogress": [], "300_complete": [], "400_failed": []
            };
            
            const agentList = [
                { name: "🤖 Codex", handle: "codex" },
                { name: "✨ Gemini", handle: "gemini" },
                { name: "🧠 Claude", handle: "claude" },
                { name: "📋 General", handle: "general" },
                { name: "📁 Root", handle: "" }
            ];

            ["000_backlog", "050_review", "100_todo", "200_inprogress", "300_complete", "400_failed"].forEach(col => {
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
                else if (col.includes("review")) col = "050_review";
                else if (col.includes("todo")) col = "100_todo";
                else if (col.includes("inprogress")) col = "200_inprogress";
                else if (col.includes("complete")) col = "300_complete";
                else if (col.includes("failed")) col = "400_failed";
                
                if (groups[col]) {
                    if (["000_backlog", "050_review", "100_todo", "200_inprogress", "300_complete", "400_failed"].includes(col)) {
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
                
                if (["300_complete", "000_backlog", "050_review", "100_todo", "200_inprogress", "400_failed"].includes(folder)) {
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
                         } else if (folder === "050_review") {
                             isExpanded = true;
                             toggleFunc = '';
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
            updateTicker(tasks);
            document.getElementById('last-updated').innerText = "Last update: " + new Date().toLocaleTimeString();
        }

        function updateTicker(tasks) {
             const tickerDiv = document.getElementById('newsTicker');
             if (!tasks || tasks.length === 0) {
                 tickerDiv.innerHTML = '<span class="ticker-item"><span class="ticker-agent">SYSTEM</span> <span class="ticker-state" style="color:#6366f1; margin:0 5px; font-weight:600;">IDLE</span> <span class="ticker-task">No active tasks found in the pipeline.</span></span>';
                 return;
             }

             // Sort all tasks by latest timestamp first for ticker relevance
             const sortedAll = [...tasks].filter(t => !["000_backlog", "050_review", "100_todo", "200_inprogress", "300_complete", "400_failed"].includes(t.folder)).sort((a,b) => b.timestamp.localeCompare(a.timestamp));
             
             let tickerItems = [];
             for (const t of sortedAll) {
                 let agent = (t.folder.split('/')[1] || "general").toLowerCase();
                 let state = "Unknown";
                 if (t.folder.includes("backlog")) state = "Decomposition";
                 else if (t.folder.includes("review")) state = "Review";
                 else if (t.folder.includes("todo")) state = "To Do";
                 else if (t.folder.includes("inprogress")) state = "In Progress";
                 else if (t.folder.includes("complete")) state = "Complete";
                 else if (t.folder.includes("failed")) state = "Failed/Blocked";
                 
                 let itemStr = `<span class="ticker-item"><span class="ticker-agent" style="color:#a855f7; font-weight:800; text-transform:uppercase;">${agent}</span> - <span class="ticker-state" style="color:#6366f1; font-weight:600; text-transform:uppercase; margin:0 5px;">${state}</span> <span class="ticker-task">${t.title}</span></span>`;
                 tickerItems.push(itemStr);
                 
                 // Limit ticker to latest ~30 tasks across the board so the loop completes reasonably quickly
                 if(tickerItems.length >= 30) break;
             }
             
             if(tickerItems.length > 0) {
                 tickerDiv.innerHTML = tickerItems.join('<span class="ticker-separator" style="color:#f43f5e; margin:0 15px; font-weight:800; display:inline-block;">|</span>');
             }
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
    </script>
</body>
</html>
"""

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

class KanbanHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass # Suppress logging to keep console clean

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            rendered_html = HTML_PAGE.replace('##TICKER_SCROLL_SPEED##', str(TICKER_SCROLL_SPEED_SECONDS))
            self.wfile.write(rendered_html.encode('utf-8'))
        
        elif self.path.startswith('/api/file-content'):
            from urllib.parse import urlparse, parse_qs
            query_components = parse_qs(urlparse(self.path).query)
            folder = query_components.get('folder', [''])[0]
            filename = query_components.get('filename', [''])[0]
            
            if folder and filename:
                filepath = os.path.join(WORKSTREAM_DIR, folder, filename)
                if os.path.exists(filepath):
                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                            content = f.read()
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps({"success": True, "content": content}).encode('utf-8'))
                        return
                    except Exception as e:
                        pass
            
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": "File not found"}).encode('utf-8'))

        elif self.path.startswith('/api/search'):
            from urllib.parse import urlparse, parse_qs
            query_components = parse_qs(urlparse(self.path).query)
            q = query_components.get('q', [''])[0].lower()
            
            results = []
            if q:
                for folder in FOLDERS:
                    folder_path = os.path.join(WORKSTREAM_DIR, folder)
                    if not os.path.exists(folder_path):
                        continue
                        
                    for filename in os.listdir(folder_path):
                        if not filename.endswith(".md"):
                            continue
                        
                        filepath = os.path.join(folder_path, filename)
                        state = folder.split('_', 1)[1].title() if '_' in folder else folder.title()
                        if state.lower() == 'inprogress':
                            state = 'In Progress'
                        elif state.lower() == 'todo':
                            state = 'Todo'
                        
                        pattern = re.compile(r"^(\d{8}_\d{6})_")
                        match = pattern.match(filename)
                        date_str = "Unknown"
                        if match:
                            ts = match.group(1)
                            if len(ts) == 15:
                                date_str = f"{ts[0:4]}-{ts[4:6]}-{ts[6:8]} {ts[9:11]}:{ts[11:13]}"
                        
                        try:
                            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                                content = f.read()
                                
                            snippet = ""
                            if q in filename.lower():
                                snippet = "Match in filename."
                            else:
                                match_index = content.lower().find(q)
                                if match_index != -1:
                                    start = max(0, match_index - 40)
                                    end = min(len(content), match_index + len(q) + 40)
                                    snippet = "... " + content[start:end].replace('\\n', ' ') + " ..."
                            
                            if snippet:
                                results.append({
                                    "filename": filename,
                                    "folder": folder,
                                    "state": state,
                                    "date": date_str,
                                    "snippet": snippet
                                })
                        except Exception as e:
                            pass
                            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "results": results}).encode('utf-8'))

        elif self.path == '/api/tasks':
            tasks = []
            pattern = re.compile(r"^(\d{8}_\d{6})_([^_]+)_(.+)\.md$")
            
            for folder in FOLDERS:
                folder_path = os.path.join(WORKSTREAM_DIR, folder)
                if not os.path.exists(folder_path):
                    continue
                
                for filename in os.listdir(folder_path):
                    if not filename.endswith(".md"):
                        continue
                        
                    match = pattern.match(filename)
                    filepath = os.path.join(folder_path, filename)
                    if match:
                        timestamp, part1, rest = match.groups()
                        if part1.lower() in ['codex', 'gemini', 'claude', 'general']:
                            if '_' in rest:
                                project, unique_task = rest.split('_', 1)
                            else:
                                project = "Unassigned"
                                unique_task = rest
                        else:
                            project = part1
                            unique_task = rest
                        title = unique_task.replace('_', ' ').title()
                    else:
                        # Auto-rename if format doesn't match
                        try:
                            ctime = os.path.getctime(filepath)
                            dt = datetime.datetime.fromtimestamp(ctime)
                            timestamp_str = dt.strftime("%Y%m%d_%H%M%S")
                            
                            # Ensure the file respects the schema: {timestamp}_{project}_{task}.md
                            parts = filename[:-3].split('_')
                            if len(parts) >= 2:
                                # Has at least two sections, maybe {project}_{task}
                                new_filename = f"{timestamp_str}_{filename}"
                            else:
                                new_filename = f"{timestamp_str}_unassigned_{filename}"
                            
                            new_filepath = os.path.join(folder_path, new_filename)
                            # Avoid trying to rename open files by catching any exception
                            os.rename(filepath, new_filepath)
                            
                            # Update references for continued processing
                            filename = new_filename
                            filepath = new_filepath
                            
                            # Recalculate match
                            match = pattern.match(filename)
                            if match:
                                timestamp, project, unique_task = match.groups()
                                title = unique_task.replace('_', ' ').title()
                            else:
                                timestamp = timestamp_str
                                project = "Unassigned"
                                title = filename[:-3].replace('_', ' ').title()
                        except Exception as e:
                            print(f"[Kanban API] Info: Could not rename file {filename}: {e}")
                            timestamp = ""
                            project = "Unassigned"
                            title = filename.replace('.md', '').replace('_', ' ').title()
                    
                    # Extract robust summary
                    summary = "No summary provided."
                    changes_made = "No specific changes listed."
                    validation = "No validation steps provided."
                    progress = None
                    needs_verification = False
                    needs_feedback = False
                    priority = 2
                    
                    try:
                        filepath = os.path.join(folder_path, filename)
                        with open(filepath, "r", encoding="utf-8") as f:
                            content = f.read()
                            
                            prio_match = re.search(r"Priority:\s*(\d)", content, re.IGNORECASE)
                            if prio_match:
                                priority = int(prio_match.group(1))
                            
                            # Extract Progress Marker if it exists
                            p_match = re.search(r"Progress:\s*(\d+)%?", content, re.IGNORECASE)
                            if not p_match:
                                p_match = re.search(r"\[(\d+)/100\]", content)
                            if p_match:
                                progress = int(p_match.group(1))
                                
                            # Find Task Summary section
                            s_match = re.search(r"#\s*Task Summary\s*\n(.*?)(?=\n#|$)", content, re.DOTALL | re.IGNORECASE)
                            if s_match:
                                summary = s_match.group(1).strip()
                                # Clean up formatting for display
                                summary = re.sub(r'[\r\n]+', ' ', summary)
                                if len(summary) > 120:
                                    summary = summary[:120] + "..."
                                    
                            c_match = re.search(r"#\s*Changes Made\s*\n(.*?)(?=\n#|$)", content, re.DOTALL | re.IGNORECASE)
                            if c_match:
                                changes_made = c_match.group(1).strip()
                                
                            v_match = re.search(r"#\s*Validation\s*\n(.*?)(?=\n#|$)", content, re.DOTALL | re.IGNORECASE)
                            if v_match:
                                validation = v_match.group(1).strip()
                                
                            if "awaiting user verification" in content.lower():
                                needs_verification = True
                                
                            if "provide user feedback" in content.lower():
                                needs_feedback = True
                                
                    except Exception as e:
                        print(f"Error reading {filename}: {e}")
                        pass
                    
                    tasks.append({
                        "filename": filename,
                        "folder": folder,
                        "timestamp": timestamp,
                        "project": project,
                        "title": title,
                        "summary": summary,
                        "progress": progress,
                        "needs_verification": needs_verification,
                        "needs_feedback": needs_feedback,
                        "changes_made": changes_made,
                        "validation": validation,
                        "priority": priority
                    })
            
            try:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(tasks).encode('utf-8'))
            except Exception as e:
                # Silently catch ConnectionAbortedError (WinError 10053) when browser refreshes during poll
                pass
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == '/api/open-file':
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                try:
                    data = json.loads(post_data.decode('utf-8'))
                    folder = data.get('folder')
                    filename = data.get('filename')
                    if folder and filename:
                        filepath = os.path.join(WORKSTREAM_DIR, folder, filename)
                        if os.path.exists(filepath):
                            os.startfile(filepath)
                            self.send_response(200)
                            self.send_header('Content-type', 'application/json')
                            self.end_headers()
                            self.wfile.write(json.dumps({"success": True}).encode('utf-8'))
                            return
                except Exception as e:
                    print(f"Error opening file: {e}")
            self.send_error(400)

        elif self.path == '/api/move-task':
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                try:
                    data = json.loads(post_data.decode('utf-8'))
                    source_folder = data.get('source_folder')
                    target_folder = data.get('target_folder')
                    filename = data.get('filename')
                    
                    if source_folder and target_folder and filename:
                        target_agent = target_folder.split('/')[-1] if '/' in target_folder else None
                        
                        source_path = os.path.join(WORKSTREAM_DIR, source_folder, filename)
                        
                        new_filename = filename
                        
                        if target_agent in ['codex', 'gemini', 'claude', 'general']:
                            pattern = re.compile(r"^(\d{8}_\d{6})_([^_]+)_(.+)\.md$")
                            match = pattern.match(filename)
                            if match:
                                timestamp, part1, rest = match.groups()
                                if part1.lower() in ['codex', 'gemini', 'claude', 'general']:
                                    new_filename = f"{timestamp}_{target_agent}_{rest}.md"
                                else:
                                    new_filename = f"{timestamp}_{target_agent}_{part1}_{rest}.md"
                        else:
                            # Moving out of an agent folder, strip the agent tag if present
                            pattern = re.compile(r"^(\d{8}_\d{6})_([^_]+)_(.+)\.md$")
                            match = pattern.match(filename)
                            if match:
                                timestamp, part1, rest = match.groups()
                                if part1.lower() in ['codex', 'gemini', 'claude', 'general']:
                                    new_filename = f"{timestamp}_{rest}.md"

                        target_path = os.path.join(WORKSTREAM_DIR, target_folder, new_filename)
                        
                        if os.path.exists(source_path):
                            os.rename(source_path, target_path)
                            self.send_response(200)
                            self.send_header('Content-type', 'application/json')
                            self.end_headers()
                            self.wfile.write(json.dumps({"success": True}).encode('utf-8'))
                            return
                except Exception as e:
                    print(f"Error moving file: {e}")
            self.send_error(400)

        elif self.path == '/api/delete-task':
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                try:
                    data = json.loads(post_data.decode('utf-8'))
                    folder = data.get('folder')
                    filename = data.get('filename')
                    
                    if folder in ['000_backlog/general', '000_backlog'] and filename:
                        # Safety Check: Does the file have derived tasks?
                        core_name = filename.replace('.md', '').replace('_processed', '')
                        has_children = False
                        
                        # Just grab all files in the system and see if they contain 'from_{core_name}'
                        search_dirs = [os.path.join(WORKSTREAM_DIR, f) for f in FOLDERS]
                        for sd in search_dirs:
                            if not os.path.exists(sd): continue
                            for ch in os.listdir(sd):
                                if ch.endswith(".md") and f"from_{core_name}" in ch:
                                    has_children = True
                                    break
                            if has_children: break
                        
                        if has_children:
                            self.send_response(200)
                            self.send_header('Content-type', 'application/json')
                            self.end_headers()
                            self.wfile.write(json.dumps({"success": False, "error": "Cannot delete: Child tasks derived from this backlog item currently exist in the system."}).encode('utf-8'))
                            return
                        else:
                            f_path = os.path.join(WORKSTREAM_DIR, folder, filename)
                            if os.path.exists(f_path):
                                os.remove(f_path)
                                self.send_response(200)
                                self.send_header('Content-type', 'application/json')
                                self.end_headers()
                                self.wfile.write(json.dumps({"success": True}).encode('utf-8'))
                                return
                except Exception as e:
                    print(f"Error deleting file: {e}")
            self.send_error(400)

        elif self.path == '/api/verify-task':
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                try:
                    data = json.loads(post_data.decode('utf-8'))
                    folder = data.get('folder')
                    filename = data.get('filename')
                    action = data.get('action')
                    
                    filepath = os.path.join(WORKSTREAM_DIR, folder, filename)
                    if not os.path.exists(filepath):
                        self.send_error(404)
                        return
                    
                    agent = folder.split('/')[-1] if '/' in folder else 'general'
                    
                    if action == 'pass':
                        # Append feedback
                        with open(filepath, 'a', encoding='utf-8') as f:
                            f.write("\n\n# User Feedback\nUser Verified: PASS\n")
                        # Move to 300_complete
                        target_dir = os.path.join(WORKSTREAM_DIR, f"300_complete/{agent}")
                        os.makedirs(target_dir, exist_ok=True)
                        os.rename(filepath, os.path.join(target_dir, filename))
                        
                    elif action == 'fail':
                        feedback = data.get('feedback', '')
                        with open(filepath, 'a', encoding='utf-8') as f:
                            f.write(f"\n\n# User Feedback\nUser Verified: FAIL\nDetails: {feedback}\n")
                        # Move back to 100_todo
                        target_dir = os.path.join(WORKSTREAM_DIR, f"100_todo/{agent}")
                        os.makedirs(target_dir, exist_ok=True)
                        os.rename(filepath, os.path.join(target_dir, filename))
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": True}).encode('utf-8'))
                    return
                except Exception as e:
                    print(f"Error handling verify: {e}")
            self.send_error(400)

        elif self.path == '/api/submit-feedback':
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                try:
                    data = json.loads(post_data.decode('utf-8'))
                    folder = data.get('folder')
                    filename = data.get('filename')
                    action = data.get('action')
                    feedback = data.get('feedback', '')
                    
                    filepath = os.path.join(WORKSTREAM_DIR, folder, filename)
                    if not os.path.exists(filepath):
                        self.send_error(404)
                        return
                    
                    agent = folder.split('/')[-1] if '/' in folder else 'general'
                    
                    with open(filepath, 'r+', encoding='utf-8') as f:
                        content = f.read()
                        f.seek(0)
                        f.truncate()
                        content = re.sub(r"- `Completion Status`:.*", "- `Completion Status`: Feedback provided", content, count=1, flags=re.IGNORECASE)
                        content += f"\n\n# User Formulated Feedback\n{feedback}\n"
                        f.write(content)

                    if action == 'complete':
                        target_dir = os.path.join(WORKSTREAM_DIR, f"300_complete/{agent}")
                    else:
                        target_dir = os.path.join(WORKSTREAM_DIR, f"100_todo/{agent}")
                        
                    os.makedirs(target_dir, exist_ok=True)
                    os.rename(filepath, os.path.join(target_dir, filename))
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": True}).encode('utf-8'))
                    return
                except Exception as e:
                    print(f"Error handling feedback: {e}")
            self.send_error(400)

        elif self.path == '/api/create-entry':
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                try:
                    data = json.loads(post_data.decode('utf-8'))
                    entry_type = data.get('type')  # task vs backlog
                    agent = data.get('agent')
                    priority = data.get('priority', '2')
                    completion_action = data.get('completionAction', 'Awaiting user verification')
                    project = data.get('project', 'general')
                    title = data.get('title', 'new_task')
                    content = data.get('content', '')
                    
                    is_edit = data.get('is_edit', False)
                    original_folder = data.get('original_folder')
                    original_filename = data.get('original_filename')
                    
                    if entry_type == 'backlog':
                        target_dir = os.path.join(WORKSTREAM_DIR, f"000_backlog/{agent}" if agent else "000_backlog")
                    else:
                        target_dir = os.path.join(WORKSTREAM_DIR, f"100_todo/{agent}" if agent else "100_todo")
                    
                    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    
                    if is_edit and original_folder and original_filename:
                        # Keep it in original state category
                        target_dir = os.path.join(WORKSTREAM_DIR, original_folder)
                        if agent and '/' not in original_folder:
                             target_dir = os.path.join(WORKSTREAM_DIR, f"{original_folder}/{agent}")
                        elif agent and '/' in original_folder:
                             base_folder = original_folder.split('/')[0]
                             target_dir = os.path.join(WORKSTREAM_DIR, f"{base_folder}/{agent}")
                             
                        match = re.search(r"^(\d{8}_\d{6})", original_filename)
                        if match:
                            ts = match.group(1)
                            
                        # Delete original to cleanly rename
                        orig_path = os.path.join(WORKSTREAM_DIR, original_folder, original_filename)
                        if os.path.exists(orig_path):
                            os.remove(orig_path)
                            
                    os.makedirs(target_dir, exist_ok=True)
                    
                    if agent:
                        filename = f"{ts}_{agent}_{project}_{title}.md"
                    else:
                        filename = f"{ts}_{project}_{title}.md"
                        
                    filepath = os.path.join(target_dir, filename)
                    
                    full_content = f"Priority: {priority}\n\n" + content + f"\n\n- `Completion Status`: {completion_action}\n"
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(full_content)
                        
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": True}).encode('utf-8'))
                    return
                except Exception as e:
                    print(f"Error creating entry: {e}")
            self.send_error(400)

        elif self.path in ['/api/review-approve', '/api/review-modify', '/api/review-reject']:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                try:
                    data = json.loads(post_data.decode('utf-8'))
                    agent = data.get('agent')
                    core_name = data.get('coreName')
                    
                    review_dir = os.path.join(WORKSTREAM_DIR, f"050_review/{agent}")
                    todo_dir = os.path.join(WORKSTREAM_DIR, f"100_todo/{agent}")
                    backlog_dir = os.path.join(WORKSTREAM_DIR, f"000_backlog/{agent}")
                    
                    backlog_review_file = os.path.join(backlog_dir, f"{core_name}_review.md")
                    
                    if self.path == '/api/review-approve':
                        # Move drafts to todo
                        for f in os.listdir(review_dir):
                            if f.endswith('.md') and core_name in f:
                                os.rename(os.path.join(review_dir, f), os.path.join(todo_dir, f))
                        # Rename backlog to processed
                        if os.path.exists(backlog_review_file):
                            os.rename(backlog_review_file, os.path.join(backlog_dir, f"{core_name}_processed.md"))
                            
                    elif self.path == '/api/review-modify':
                        feedback = data.get('feedback', '')
                        # Delete drafts
                        for f in os.listdir(review_dir):
                            if f.endswith('.md') and core_name in f:
                                os.remove(os.path.join(review_dir, f))
                        # Revert backlog to raw .md, append feedback
                        if os.path.exists(backlog_review_file):
                            with open(backlog_review_file, 'a', encoding='utf-8') as blf:
                                blf.write(f"\\n\\n# User Feedback (Task Generation)\\n{feedback}\\n")
                            os.rename(backlog_review_file, os.path.join(backlog_dir, f"{core_name}.md"))
                            
                    elif self.path == '/api/review-reject':
                        # Delete drafts
                        for f in os.listdir(review_dir):
                            if f.endswith('.md') and core_name in f:
                                os.remove(os.path.join(review_dir, f))
                        # Mark backlog suspended
                        if os.path.exists(backlog_review_file):
                            os.rename(backlog_review_file, os.path.join(backlog_dir, f"{core_name}_suspended.md"))
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": True}).encode('utf-8'))
                    return
                except Exception as e:
                    print(f"Error handling review gate: {e}")
            self.send_error(400)
            
        else:
            self.send_error(404)

import threading
import time
import subprocess

def _extract_project_from_core_name(core_name):
    project = "unassigned"
    pattern = re.compile(r"^(\d{8}_\d{6})_([^_]+)_(.+)$")
    match = pattern.match(core_name)
    if not match:
        return project
    _, part1, rest = match.groups()
    if part1.lower() in ['codex', 'gemini', 'claude', 'general']:
        if '_' in rest:
            project, _ = rest.split('_', 1)
        else:
            project = rest
    else:
        project = part1
    return (project or "unassigned").lower()

def _build_decompose_command(agent, backlog_path):
    """
    Returns command list for real decomposition call.
    Supports env override:
      KANBAN_LLM_DECOMP_CMD='python path\\to\\script.py --agent {agent} --input "{backlog_path}"'
    """
    cmd_tpl = os.environ.get("KANBAN_LLM_DECOMP_CMD", "").strip()
    if cmd_tpl:
        formatted = cmd_tpl.format(
            agent=agent,
            backlog_path=backlog_path,
            backlog_file=os.path.basename(backlog_path),
        )
        return shlex.split(formatted, posix=False)

    # Default integration path. If script is not present, worker logs and retries later.
    default_script = os.path.join(WORKSTREAM_DIR, "llm_decompose_cli.py")
    return [sys.executable, default_script, "--agent", agent, "--input", backlog_path]

def _validate_decomposition_payload(payload):
    """
    Accept either:
      - list[task]
      - { "tasks": list[task] }
    where task minimally includes:
      title, summary (or description), and optional tests/acceptance_criteria/steps.
    """
    tasks = payload.get("tasks") if isinstance(payload, dict) else payload
    if not isinstance(tasks, list) or not tasks:
        raise ValueError("Decomposition payload missing non-empty task list.")

    normalized = []
    for idx, item in enumerate(tasks, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Task {idx} is not an object.")
        title = str(item.get("title") or "").strip()
        summary = str(item.get("summary") or item.get("description") or "").strip()
        if not title or not summary:
            raise ValueError(f"Task {idx} missing required title/summary.")
        tests = item.get("tests") or item.get("acceptance_criteria") or item.get("validation") or []
        if isinstance(tests, str):
            tests = [tests]
        if not isinstance(tests, list):
            tests = []
        steps = item.get("steps") or []
        if isinstance(steps, str):
            steps = [steps]
        if not isinstance(steps, list):
            steps = []
        normalized.append({
            "title": title,
            "summary": summary,
            "tests": [str(t).strip() for t in tests if str(t).strip()],
            "steps": [str(s).strip() for s in steps if str(s).strip()],
            "priority": item.get("priority", 2),
            "source_backlog": str(item.get("source_backlog") or "").strip(),
        })
    return normalized

def _render_generated_task_md(item, core_name, idx, agent, backlog_review_relpath):
    tests = item.get("tests") or []
    steps = item.get("steps") or []
    lines = []
    lines.append(f"Priority: {item.get('priority', 2)}")
    lines.append("")
    lines.append(f"# {item['title']}")
    lines.append("")
    lines.append(f"- Source backlog: `{core_name}.md`")
    lines.append(f"- Source backlog path: `{backlog_review_relpath}`")
    lines.append(f"- Parent backlog id: `{core_name}`")
    lines.append(f"- Generated by: real_llm_decomposition")
    lines.append(f"- Required skill: `C:\\Users\\edebe\\eds\\skills\\workstream-task-lifecycle\\SKILL.md`")
    lines.append("")
    lines.append("## Prerequisite")
    lines.append("- [ ] Read `C:\\Users\\edebe\\eds\\skills\\workstream-task-lifecycle\\SKILL.md` before starting implementation.")
    lines.append("")
    lines.append("## Task Summary")
    lines.append(item["summary"])
    lines.append("")
    lines.append("## Plan")
    if steps:
        for step_idx, step in enumerate(steps, start=1):
            lines.append(f"- [ ] {step_idx}. {step}")
    else:
        lines.append(f"- [ ] 1. Implement `{item['title']}` according to summary.")
    lines.append("")
    lines.append("## Validation")
    if tests:
        for t in tests:
            lines.append(f"- [ ] {t}")
    else:
        lines.append("- [ ] Add and run implementation-specific validation.")
    lines.append("")
    lines.append(f"## Notes")
    lines.append(f"- Generated item index: {idx}")
    lines.append(f"- Generated for lane: {agent}")
    return "\n".join(lines).strip() + "\n"

def _append_generated_tasks_to_backlog(backlog_review_path, review_rel_dir, generated_files):
    if not generated_files:
        return
    try:
        existing = ""
        if os.path.exists(backlog_review_path):
            with open(backlog_review_path, "r", encoding="utf-8") as f:
                existing = f.read()
        lines = []
        lines.append("")
        lines.append("## Generated Tasks")
        lines.append("| Task | File |")
        lines.append("|------|------|")
        for fname in generated_files:
            title = fname.replace(".md", "")
            rel = f"{review_rel_dir}/{fname}".replace("\\", "/")
            lines.append(f"| {title} | `{rel}` |")
        lines.append("")
        block = "\n".join(lines)
        if "## Generated Tasks" in existing:
            existing = re.sub(r"## Generated Tasks[\s\S]*?$", block.strip() + "\n", existing.strip(), flags=re.MULTILINE)
            content = existing
        else:
            content = existing.rstrip() + "\n" + block
        with open(backlog_review_path, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as exc:
        print(f"[DECOMP] Failed to append generated task links to backlog review: {exc}")

def _extract_section(raw, section_name):
    pattern = re.compile(
        rf"^\s*##\s*{re.escape(section_name)}\s*$([\s\S]*?)(?=^\s*##\s+|\Z)",
        flags=re.MULTILINE | re.IGNORECASE
    )
    m = pattern.search(raw or "")
    return (m.group(1) if m else "").strip()

def _checkbox_stats(raw):
    lines = (raw or "").splitlines()
    boxes = [ln for ln in lines if re.search(r"^\s*[-*]\s+\[[ xX]\]\s+", ln)]
    checked = [ln for ln in boxes if re.search(r"\[[xX]\]", ln)]
    return len(boxes), len(checked)

def _task_quality_gate(task_path):
    """
    Require required structure before auto-execution starts:
    - Plan section: at least one checkbox
    - Validation section: at least one checkbox
    """
    try:
        raw = Path(task_path).read_text(encoding="utf-8", errors="ignore")
    except Exception as exc:
        return False, f"read_error: {exc}"

    plan = _extract_section(raw, "Plan")
    val = _extract_section(raw, "Validation")
    plan_total, plan_checked = _checkbox_stats(plan)
    val_total, val_checked = _checkbox_stats(val)

    if plan_total <= 0:
        return False, "missing_plan_checklist"
    if val_total <= 0:
        return False, "missing_validation_checklist"
    return True, "ok"

def _mark_all_checkboxes_complete(task_path):
    try:
        raw = Path(task_path).read_text(encoding="utf-8", errors="ignore")
        updated = re.sub(r"^(\s*[-*]\s+\[)\s(\]\s+)", r"\1x\2", raw, flags=re.MULTILINE)
        if updated != raw:
            Path(task_path).write_text(updated, encoding="utf-8")
    except Exception as exc:
        print(f"[Worker] failed to mark checklist complete for {task_path}: {exc}")

def _decompose_backlog_real(agent, backlog_path, timeout_sec=120):
    started = time.time()
    cmd = _build_decompose_command(agent, backlog_path)
    print(f"[Lane Worker: {agent.upper()}] [DECOMP] invoking command: {' '.join(cmd)}")
    if len(cmd) >= 2 and cmd[1].endswith("llm_decompose_cli.py") and not os.path.exists(cmd[1]):
        raise RuntimeError(f"LLM decomposition script not found: {cmd[1]}")
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_sec)
    duration = round(time.time() - started, 2)
    if proc.returncode != 0:
        err = (proc.stderr or proc.stdout or "").strip()
        raise RuntimeError(f"Decomposition command failed (rc={proc.returncode}, {duration}s): {err[-600:]}")
    raw = (proc.stdout or "").strip()
    if not raw:
        raise ValueError("Decomposition command returned empty stdout.")
    payload = json.loads(raw)
    tasks = _validate_decomposition_payload(payload)
    print(f"[Lane Worker: {agent.upper()}] [DECOMP] success: {len(tasks)} tasks in {duration}s")
    return tasks, duration

def _build_agent_execution_command(agent, task_path):
    """
    Real execution command resolver.
    Supported env vars:
    - KANBAN_AGENT_EXEC_CMD_<AGENT> (e.g., ..._CODEX)
    - KANBAN_AGENT_EXEC_CMD (fallback)
    Placeholders: {agent}, {task_path}, {task_file}
    """
    key_specific = f"KANBAN_AGENT_EXEC_CMD_{agent.upper()}"
    tpl = os.environ.get(key_specific, "").strip() or os.environ.get("KANBAN_AGENT_EXEC_CMD", "").strip()
    if not tpl:
        if agent.lower() == "codex":
            prompt = (
                "Execute this task file end-to-end. "
                "Read and follow C:\\Users\\edebe\\eds\\skills\\workstream-task-lifecycle\\SKILL.md first. "
                f"Task file: {task_path}. "
                "Implement required changes in the workspace, run validations, and update checklist items."
            )
            return ["codex", "exec", "-C", r"C:\Users\edebe\eds", prompt]
        return None
    formatted = tpl.format(
        agent=agent,
        task_path=task_path,
        task_file=os.path.basename(task_path),
    )
    return shlex.split(formatted, posix=False)

def multi_model_lane_worker(agent):
    print(f"[Agent Worker: {agent.upper()}] Lane daemon started...")
    while True:
        try:
            todo_dir = os.path.join(WORKSTREAM_DIR, f"100_todo/{agent}")
            inprog_dir = os.path.join(WORKSTREAM_DIR, f"200_inprogress/{agent}")
            failed_dir = os.path.join(WORKSTREAM_DIR, f"400_failed/{agent}")
            complete_dir = os.path.join(WORKSTREAM_DIR, f"300_complete/{agent}")
            backlog_dir = os.path.join(WORKSTREAM_DIR, f"000_backlog/{agent}")
            review_dir = os.path.join(WORKSTREAM_DIR, f"050_review/{agent}")

            # Check capacity constraints
            active_tasks = []
            if os.path.exists(todo_dir):
                active_tasks.extend([f for f in os.listdir(todo_dir) if f.endswith(".md") and not f.startswith(".")])
            if os.path.exists(inprog_dir):
                active_tasks.extend([f for f in os.listdir(inprog_dir) if f.endswith(".md") and not f.startswith(".")])
            if os.path.exists(review_dir):
                active_tasks.extend([f for f in os.listdir(review_dir) if f.endswith(".md") and not f.startswith(".")])

            # Poll Backlog Decomposition if capacity is zero
            if len(active_tasks) == 0 and os.path.exists(backlog_dir):
                backlogs = [f for f in os.listdir(backlog_dir) if f.endswith(".md") and not f.endswith("_processed.md") and not f.endswith("_review.md") and not f.endswith("_suspended.md") and not f.startswith(".")]
                if backlogs:
                    backlogs.sort()
                    bl_file = backlogs[0]
                    bl_src = os.path.join(backlog_dir, bl_file)
                    
                    print(f"[Lane Worker: {agent.upper()}] Decomposing Backlog Item: {bl_file} ...")
                    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    core_name = bl_file.replace(".md", "")
                    project = _extract_project_from_core_name(core_name)
                    try:
                        tasks, duration = _decompose_backlog_real(agent, bl_src, timeout_sec=120)
                    except subprocess.TimeoutExpired:
                        print(f"[Lane Worker: {agent.upper()}] [DECOMP] timeout for {bl_file}; will retry.")
                        time.sleep(2)
                        continue
                    except Exception as decomp_err:
                        print(f"[Lane Worker: {agent.upper()}] [DECOMP] failed for {bl_file}: {decomp_err}")
                        time.sleep(2)
                        continue

                    generated = 0
                    generated_files = []
                    bl_new_name = f"{core_name}_review.md"
                    bl_review_path = os.path.join(backlog_dir, bl_new_name)
                    if os.path.exists(bl_review_path):
                        suffix = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                        bl_new_name = f"{core_name}_review_{suffix}.md"
                        bl_review_path = os.path.join(backlog_dir, bl_new_name)
                    backlog_review_relpath = f"000_backlog/{agent}/{bl_new_name}"
                    for idx, item in enumerate(tasks, start=1):
                        new_task = f"{ts}_{agent}_{project}_task_{idx:02d}_from_{core_name}.md"
                        task_path = os.path.join(review_dir, new_task)
                        with open(task_path, "w", encoding="utf-8") as tf:
                            tf.write(_render_generated_task_md(item, core_name, idx, agent, backlog_review_relpath))
                        generated += 1
                        generated_files.append(new_task)

                    if generated <= 0:
                        print(f"[Lane Worker: {agent.upper()}] [DECOMP] no tasks produced for {bl_file}; keeping backlog for retry.")
                        time.sleep(2)
                        continue

                    # Mark Backlog as pending review only after successful generation
                    os.rename(bl_src, bl_review_path)
                    _append_generated_tasks_to_backlog(bl_review_path, f"050_review/{agent}", generated_files)
                    print(f"[Lane Worker: {agent.upper()}] [DECOMP] pending review: {bl_new_name} (generated={generated}, duration={duration}s)")
                    time.sleep(2)
                    continue # Skip directly to next iteration to let UI update

            # Poll To-Do tasks
            if os.path.exists(todo_dir):
                tasks = [f for f in os.listdir(todo_dir) if f.endswith(".md") and not f.startswith(".")]
                
                # Prevent worker picking up newly generated BLOCKER tickets
                valid_tasks = [t for t in tasks if "BLOCKER_" not in t]
                
                if valid_tasks:
                    # Advanced Priority Sorter
                    parsed_tasks = []
                    for t_file in valid_tasks:
                        priority = 2
                        try:
                            with open(os.path.join(todo_dir, t_file), 'r', encoding='utf-8') as f:
                                # Intentionally read only first 2KB for speed
                                raw = f.read(2048) 
                                p_match = re.search(r"Priority:\s*(\d)", raw, re.IGNORECASE)
                                if p_match:
                                    priority = int(p_match.group(1))
                        except Exception:
                            pass
                        parsed_tasks.append({'filename': t_file, 'p': priority})
                    
                    # Sort primarily by Priority (1 is high, 3 is low), secondarily alphabetically by timestamp
                    parsed_tasks.sort(key=lambda x: (x['p'], x['filename']))
                    
                    task_file = parsed_tasks[0]['filename']
                    source_path = os.path.join(todo_dir, task_file)
                    inprog_path = os.path.join(inprog_dir, task_file)

                    # Enforce checklist/test quality gate before any auto execution.
                    gate_ok, gate_reason = _task_quality_gate(source_path)
                    if not gate_ok:
                        print(f"[Lane Worker: {agent.upper()}] QUALITY_GATE blocked {task_file}: {gate_reason}")
                        time.sleep(2)
                        continue
                    
                    # Phase B: Sequential Locking
                    try:
                        os.rename(source_path, inprog_path)
                        print(f"[Lane Worker: {agent.upper()}] Claimed task: {task_file}")
                    except OSError:
                        continue # File might be locked by another process or user moving it
                    
                    # Phase C: Real execution only (no simulation).
                    cli_command = _build_agent_execution_command(agent, inprog_path)
                    if not cli_command:
                        print(f"[Lane Worker: {agent.upper()}] EXECUTION_CONFIG missing for {task_file}; set KANBAN_AGENT_EXEC_CMD_{agent.upper()} or KANBAN_AGENT_EXEC_CMD.")
                        # Return task to todo and skip.
                        if os.path.exists(inprog_path):
                            os.rename(inprog_path, source_path)
                        time.sleep(2)
                        continue
                    
                    try:
                        print(f"[Lane Worker: {agent.upper()}] Launching headless agent execution...")
                        
                        result = subprocess.run(cli_command, capture_output=True, text=True, timeout=120)

                        # Persist execution evidence into the task file.
                        try:
                            with open(inprog_path, 'a', encoding='utf-8') as f:
                                f.write("\n\n## Execution Evidence\n")
                                f.write(f"- Agent lane: {agent}\n")
                                f.write(f"- Command: {' '.join(cli_command)}\n")
                                f.write(f"- Return code: {result.returncode}\n")
                                out = (result.stdout or "").strip()
                                err = (result.stderr or "").strip()
                                if out:
                                    f.write("- Stdout:\n```text\n" + out[-4000:] + "\n```\n")
                                if err:
                                    f.write("- Stderr:\n```text\n" + err[-4000:] + "\n```\n")
                        except Exception as ev_err:
                            print(f"[Lane Worker: {agent.upper()}] Failed to append execution evidence: {ev_err}")
                        
                        if result.returncode == 0:
                            # Phase D: Completion
                            print(f"[Lane Worker: {agent.upper()}] Success! Completed: {task_file}")
                            
                            # Clean up final progress marker before moving to complete
                            try:
                                with open(inprog_path, 'r', encoding='utf-8') as f:
                                    cont = f.read()
                                cont = re.sub(r'\n\nProgress:\s*\d+%', '', cont)
                                with open(inprog_path, 'w', encoding='utf-8') as f:
                                    f.write(cont.strip())
                            except:
                                pass

                            _mark_all_checkboxes_complete(inprog_path)
                                
                            complete_path = os.path.join(complete_dir, task_file)
                            os.rename(inprog_path, complete_path)
                            
                            # Future update: trigger sync logic here to verify if parent Backlog item is also complete.
                        else:
                            print(f"[Lane Worker: {agent.upper()}] Failed or Blocked: {task_file}")
                            failed_path = os.path.join(failed_dir, task_file)
                            os.rename(inprog_path, failed_path)
                            
                            # Spawn New Blocker Task
                            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                            blocker_filename = f"{timestamp}_{agent}_BLOCKER_{task_file}"
                            blocker_path = os.path.join(todo_dir, blocker_filename)
                            with open(blocker_path, "w", encoding="utf-8") as bf:
                                bf.write(f"# Task Summary\nBlocker encountered while executing `{task_file}` via `{agent}` agent.\n\n")
                                bf.write(f"# Error Log Details\n```bash\n{result.stderr[-2000:]}\n```\n")
                    except Exception as e:
                        print(f"[Lane Worker: {agent.upper()}] Exception executing {task_file}: {str(e)}")
                        failed_path = os.path.join(failed_dir, task_file)
                        if os.path.exists(inprog_path):
                            os.rename(inprog_path, failed_path)

        except Exception as e:
            print(f"[Agent Worker: {agent.upper()}] Master Loop error: {e}")
        time.sleep(10)

if __name__ == '__main__':
    # Start Multi-Model Lane Worker Daemon Threads (Parallel Execution)
    agents = ['codex', 'gemini', 'claude']
    for agent in agents:
        worker_t = threading.Thread(target=multi_model_lane_worker, args=(agent,), daemon=True)
        worker_t.start()
    
    PORT = 8080
    server = ThreadedHTTPServer(('localhost', PORT), KanbanHandler)
    print(f"Real-Time Kanban Dashboard starting on http://localhost:{PORT}")
    print("Keep this terminal open, or run in background. Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nKanban Dashboard stopped.")
