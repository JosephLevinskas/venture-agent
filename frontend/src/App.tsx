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

type Document = {
  id: number;
  project_id: number;
  title: string;
  content: string;
  created_at: string;
  updated_at: string;
};

function App() {
  const [email, setEmail] = useState("test@example.com");
  const [password, setPassword] = useState("password123");

  const [token, setToken] = useState<string>(() => {
    return localStorage.getItem("access_token") ?? "";
  });

  const [projects, setProjects] = useState<Project[]>([]);
  const [selectedProjectId, setSelectedProjectId] = useState<number | null>(null);

  const [documents, setDocuments] = useState<Document[]>([]);

  const [projectTitle, setProjectTitle] = useState("Frontend Test Project");
  const [projectDescription, setProjectDescription] = useState("Created from React");

  const [documentTitle, setDocumentTitle] = useState("Research Note");
  const [documentContent, setDocumentContent] = useState("These are notes for this project.");

  const [message, setMessage] = useState("");

  async function registerUser() {
    setMessage("");

    const response = await fetch(`${API_BASE}/auth/register`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
      const error = await response.json();
      setMessage(`Register failed: ${error.detail}`);
      return;
    }

    setMessage("Registered successfully. Now log in.");
  }

  async function loginUser() {
    setMessage("");

    const response = await fetch(`${API_BASE}/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
      const error = await response.json();
      setMessage(`Login failed: ${error.detail}`);
      return;
    }

    const data = await response.json();

    localStorage.setItem("access_token", data.access_token);
    setToken(data.access_token);

    setMessage("Logged in successfully.");
  }

  function logoutUser() {
    localStorage.removeItem("access_token");
    setToken("");
    setProjects([]);
    setDocuments([]);
    setSelectedProjectId(null);
    setMessage("Logged out.");
  }

  async function loadProjects() {
    if (!token) {
      setMessage("Log in first.");
      return;
    }

    const response = await fetch(`${API_BASE}/projects`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      setMessage("Failed to load projects.");
      return;
    }

    const data = await response.json();
    setProjects(data);
  }

  async function createProject() {
    if (!token) {
      setMessage("Log in first.");
      return;
    }

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
      setMessage("Failed to create project.");
      return;
    }

    setMessage("Project created.");
    await loadProjects();
  }

  async function selectProject(projectId: number) {
    setSelectedProjectId(projectId);
    await loadDocuments(projectId);
  }

  async function loadDocuments(projectId: number) {
    if (!token) {
      setMessage("Log in first.");
      return;
    }

    const response = await fetch(`${API_BASE}/projects/${projectId}/documents`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      setMessage("Failed to load documents.");
      return;
    }

    const data = await response.json();
    setDocuments(data);
  }

  async function createDocument() {
    if (!token) {
      setMessage("Log in first.");
      return;
    }

    if (selectedProjectId === null) {
      setMessage("Select a project first.");
      return;
    }

    const response = await fetch(`${API_BASE}/projects/${selectedProjectId}/documents`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        title: documentTitle,
        content: documentContent,
      }),
    });

    if (!response.ok) {
      setMessage("Failed to create document.");
      return;
    }

    setMessage("Document created.");
    await loadDocuments(selectedProjectId);
  }

  const selectedProject = projects.find((project) => project.id === selectedProjectId);

  useEffect(() => {
    if (token) {
      loadProjects();
    }
  }, [token]);

  return (
    <main className="page">
      <section className="hero">
        <h1>VentureAgent</h1>
        <p>Frontend MVP: auth, projects, and project documents.</p>
      </section>

      <section className="card">
        <h2>Auth</h2>

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
          <button onClick={registerUser}>Register</button>
          <button onClick={loginUser}>Login</button>
          <button onClick={logoutUser}>Logout</button>
        </div>

        <p>
          Status: <strong>{token ? "Logged in" : "Not logged in"}</strong>
        </p>
      </section>

      <section className="card">
        <h2>Create Project</h2>

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

        <button onClick={createProject}>Create Project</button>
      </section>

      <section className="card">
        <h2>Your Projects</h2>

        <button onClick={loadProjects}>Refresh Projects</button>

        {projects.length === 0 ? (
          <p>No projects loaded yet.</p>
        ) : (
          <ul className="project-list">
            {projects.map((project) => (
              <li key={project.id} className="project-item">
                <h3>{project.title}</h3>
                <p>{project.description}</p>
                <small>
                  project id: {project.id} | owner id: {project.owner_id}
                </small>
                <br />
                <button onClick={() => selectProject(project.id)}>
                  Select Project
                </button>
              </li>
            ))}
          </ul>
        )}
      </section>

      <section className="card">
        <h2>Selected Project</h2>

        {selectedProject ? (
          <p>
            Selected: <strong>{selectedProject.title}</strong>
          </p>
        ) : (
          <p>No project selected.</p>
        )}
      </section>

      <section className="card">
        <h2>Create Document / Note</h2>

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

        <button onClick={createDocument}>Create Document</button>
      </section>

      <section className="card">
        <h2>Documents for Selected Project</h2>

        {selectedProjectId !== null && (
          <button onClick={() => loadDocuments(selectedProjectId)}>
            Refresh Documents
          </button>
        )}

        {documents.length === 0 ? (
          <p>No documents loaded yet.</p>
        ) : (
          <ul className="document-list">
            {documents.map((document) => (
              <li key={document.id} className="document-item">
                <h3>{document.title}</h3>
                <p>{document.content}</p>
                <small>
                  document id: {document.id} | project id: {document.project_id}
                </small>
              </li>
            ))}
          </ul>
        )}
      </section>

      {message && <p className="message">{message}</p>}
    </main>
  );
}

export default App;