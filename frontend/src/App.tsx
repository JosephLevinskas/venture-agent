import { useEffect, useState } from "react";
import "./App.css";

const API_BASE = "http://127.0.0.1:8000";

type Project = {
  id: number;
  title: string;
  description: string | null;
  owner_id: number;
  created_at: string;
  updated_at: string;
};

type ProjectDocument = {
  id: number;
  project_id: number;
  title: string;
  content: string;
  created_at: string;
  updated_at: string;
};

type NoticeType = "success" | "error" | "info";

type Notice = {
  type: NoticeType;
  text: string;
};

function App() {
  const [email, setEmail] = useState("test@example.com");
  const [password, setPassword] = useState("password123");

  const [token, setToken] = useState<string>(() => {
    return localStorage.getItem("access_token") ?? "";
  });

  const [projects, setProjects] = useState<Project[]>([]);
  const [selectedProjectId, setSelectedProjectId] = useState<number | null>(null);

  const [documents, setDocuments] = useState<ProjectDocument[]>([]);
  const [selectedDocumentId, setSelectedDocumentId] = useState<number | null>(null);

  const [projectTitle, setProjectTitle] = useState("Frontend Test Project");
  const [projectDescription, setProjectDescription] = useState("Created from React");

  const [documentTitle, setDocumentTitle] = useState("Research Note");
  const [documentContent, setDocumentContent] = useState(
    "These are notes for this project."
  );

  const [notice, setNotice] = useState<Notice | null>(null);
  const [isBusy, setIsBusy] = useState(false);

  const selectedProject = projects.find((project) => project.id === selectedProjectId);
  const selectedDocument = documents.find(
    (document) => document.id === selectedDocumentId
  );

  function showNotice(text: string, type: NoticeType = "info") {
    setNotice({ text, type });
  }

  async function registerUser() {
    setIsBusy(true);
    setNotice(null);

    try {
      const response = await fetch(`${API_BASE}/auth/register`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        const error = await response.json();
        showNotice(`Register failed: ${error.detail}`, "error");
        return;
      }

      showNotice("Account created. Now log in.", "success");
    } finally {
      setIsBusy(false);
    }
  }

  async function loginUser() {
    setIsBusy(true);
    setNotice(null);

    try {
      const response = await fetch(`${API_BASE}/auth/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        const error = await response.json();
        showNotice(`Login failed: ${error.detail}`, "error");
        return;
      }

      const data = await response.json();

      localStorage.setItem("access_token", data.access_token);
      setToken(data.access_token);

      showNotice(`Logged in as ${email}.`, "success");
    } finally {
      setIsBusy(false);
    }
  }

  function logoutUser() {
    localStorage.removeItem("access_token");
    setToken("");
    setProjects([]);
    setDocuments([]);
    setSelectedProjectId(null);
    setSelectedDocumentId(null);
    showNotice("Logged out.", "info");
  }

  async function loadProjects() {
    if (!token) {
      showNotice("Log in first.", "error");
      return;
    }

    const response = await fetch(`${API_BASE}/projects`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      showNotice("Failed to load projects.", "error");
      return;
    }

    const data = await response.json();
    setProjects(data);

    showNotice(`Loaded ${data.length} project(s).`, "success");
  }

  async function createProject() {
    if (!token) {
      showNotice("Log in first.", "error");
      return;
    }

    setIsBusy(true);

    try {
      const response = await fetch(`${API_BASE}/projects`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          title: projectTitle,
          description: projectDescription,
        }),
      });

      if (!response.ok) {
        showNotice("Failed to create project.", "error");
        return;
      }

      const createdProject = await response.json();

      await loadProjects();
      setSelectedProjectId(createdProject.id);
      setSelectedDocumentId(null);
      setDocuments([]);

      showNotice(`Project created and selected: ${createdProject.title}`, "success");
    } finally {
      setIsBusy(false);
    }
  }

  async function selectProject(projectId: number) {
    const project = projects.find((item) => item.id === projectId);

    setSelectedProjectId(projectId);
    setSelectedDocumentId(null);

    showNotice(`Selected project: ${project?.title ?? projectId}`, "info");

    await loadDocuments(projectId);
  }

  async function loadDocuments(projectId: number) {
    if (!token) {
      showNotice("Log in first.", "error");
      return;
    }

    const response = await fetch(`${API_BASE}/projects/${projectId}/documents`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      showNotice("Failed to load documents.", "error");
      return;
    }

    const data = await response.json();
    setDocuments(data);

    if (data.length === 0) {
      showNotice("No documents found for this project yet.", "info");
    } else {
      showNotice(`Loaded ${data.length} document(s).`, "success");
    }
  }

  async function createDocument() {
    if (!token) {
      showNotice("Log in first.", "error");
      return;
    }

    if (selectedProjectId === null) {
      showNotice("Select a project first.", "error");
      return;
    }

    setIsBusy(true);

    try {
      const response = await fetch(
        `${API_BASE}/projects/${selectedProjectId}/documents`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            title: documentTitle,
            content: documentContent,
          }),
        }
      );

      if (!response.ok) {
        showNotice("Failed to create document.", "error");
        return;
      }

      const createdDocument = await response.json();

      await loadDocuments(selectedProjectId);
      setSelectedDocumentId(createdDocument.id);

      showNotice(`Document created and selected: ${createdDocument.title}`, "success");
    } finally {
      setIsBusy(false);
    }
  }

  function selectDocument(documentId: number) {
    const document = documents.find((item) => item.id === documentId);

    setSelectedDocumentId(documentId);
    showNotice(`Selected document: ${document?.title ?? documentId}`, "info");
  }

  useEffect(() => {
    if (token) {
      loadProjects();
    }
  }, [token]);

  return (
    <main className="page">
      <section className="hero">
        <div>
          <h1>VentureAgent</h1>
          <p>Frontend MVP: auth, projects, and project documents.</p>
        </div>

        <div className={token ? "status-pill success" : "status-pill muted"}>
          {token ? "Logged in" : "Not logged in"}
        </div>
      </section>

      {notice && (
        <section className={`notice ${notice.type}`}>
          <strong>{notice.type.toUpperCase()}</strong>
          <span>{notice.text}</span>
        </section>
      )}

      <section className="card">
        <div className="card-header">
          <h2>Auth</h2>
          <span className={token ? "mini-badge success" : "mini-badge"}>
            {token ? `Signed in as ${email}` : "No active session"}
          </span>
        </div>

        <label>
          Email
          <input
            value={email}
            onChange={(event) => setEmail(event.target.value)}
          />
        </label>

        <label>
          Password
          <input
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
          />
        </label>

        <div className="button-row">
          <button disabled={isBusy} onClick={registerUser}>
            Register
          </button>
          <button disabled={isBusy} onClick={loginUser}>
            Login
          </button>
          <button disabled={isBusy} onClick={logoutUser}>
            Logout
          </button>
        </div>
      </section>

      <section className="card">
        <div className="card-header">
          <h2>Create Project</h2>
          {selectedProject && (
            <span className="mini-badge success">
              Selected: {selectedProject.title}
            </span>
          )}
        </div>

        <label>
          Title
          <input
            value={projectTitle}
            onChange={(event) => setProjectTitle(event.target.value)}
          />
        </label>

        <label>
          Description
          <textarea
            value={projectDescription}
            onChange={(event) => setProjectDescription(event.target.value)}
          />
        </label>

        <button disabled={isBusy} onClick={createProject}>
          Create Project
        </button>
      </section>

      <section className="card">
        <div className="card-header">
          <h2>Your Projects</h2>
          <span className="mini-badge">{projects.length} project(s)</span>
        </div>

        <button disabled={isBusy} onClick={loadProjects}>
          Refresh Projects
        </button>

        {projects.length === 0 ? (
          <p className="empty-state">No projects loaded yet.</p>
        ) : (
          <ul className="project-list">
            {projects.map((project) => (
              <li
                key={project.id}
                className={
                  project.id === selectedProjectId
                    ? "project-item selected"
                    : "project-item"
                }
              >
                <div className="item-top">
                  <h3>{project.title}</h3>
                  {project.id === selectedProjectId && (
                    <span className="selected-label">Selected</span>
                  )}
                </div>

                <p>{project.description}</p>

                <small>
                  project id: {project.id} | owner id: {project.owner_id}
                </small>

                <br />

                <button disabled={isBusy} onClick={() => selectProject(project.id)}>
                  {project.id === selectedProjectId ? "Selected" : "Select Project"}
                </button>
              </li>
            ))}
          </ul>
        )}
      </section>

      <section className="card">
        <div className="card-header">
          <h2>Create Document / Note</h2>
          {selectedProject ? (
            <span className="mini-badge success">
              Adding to: {selectedProject.title}
            </span>
          ) : (
            <span className="mini-badge warning">Select project first</span>
          )}
        </div>

        <label>
          Title
          <input
            value={documentTitle}
            onChange={(event) => setDocumentTitle(event.target.value)}
          />
        </label>

        <label>
          Content
          <textarea
            value={documentContent}
            onChange={(event) => setDocumentContent(event.target.value)}
          />
        </label>

        <button disabled={isBusy} onClick={createDocument}>
          Create Document
        </button>
      </section>

      <section className="card">
        <div className="card-header">
          <h2>Documents for Selected Project</h2>
          <span className="mini-badge">{documents.length} document(s)</span>
        </div>

        {selectedProjectId !== null ? (
          <button disabled={isBusy} onClick={() => loadDocuments(selectedProjectId)}>
            Refresh Documents
          </button>
        ) : (
          <p className="empty-state">Select a project to view its documents.</p>
        )}

        {documents.length > 0 && (
          <ul className="document-list">
            {documents.map((document) => (
              <li
                key={document.id}
                className={
                  document.id === selectedDocumentId
                    ? "document-item selected"
                    : "document-item"
                }
              >
                <div className="item-top">
                  <h3>{document.title}</h3>
                  {document.id === selectedDocumentId && (
                    <span className="selected-label">Viewing</span>
                  )}
                </div>

                <p>{document.content.slice(0, 120)}</p>

                <small>
                  document id: {document.id} | project id: {document.project_id}
                </small>

                <br />

                <button disabled={isBusy} onClick={() => selectDocument(document.id)}>
                  {document.id === selectedDocumentId
                    ? "Viewing Document"
                    : "View Document"}
                </button>
              </li>
            ))}
          </ul>
        )}
      </section>

      <section className="card viewer-card">
        <div className="card-header">
          <h2>Document Viewer</h2>
          {selectedDocument && (
            <span className="mini-badge success">Open document</span>
          )}
        </div>

        {selectedDocument ? (
          <article>
            <h3>{selectedDocument.title}</h3>
            <p className="document-content">{selectedDocument.content}</p>
            <small>
              document id: {selectedDocument.id} | project id:{" "}
              {selectedDocument.project_id}
            </small>
          </article>
        ) : (
          <p className="empty-state">
            Click “View Document” on a document to read its full content here.
          </p>
        )}
      </section>
    </main>
  );
}

export default App;