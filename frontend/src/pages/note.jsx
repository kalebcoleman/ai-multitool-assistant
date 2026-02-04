import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";
import Note from "../components/Note";
import "../styles/Note.css";

function Notes() {
    const [notes, setNotes] = useState([]);
    const [content, setContent] = useState("");
    const [title, setTitle] = useState("");
    const [loading, setLoading] = useState(true);
    const [creating, setCreating] = useState(false);
    const navigate = useNavigate();
    const titleRef = useRef(null);

    useEffect(() => {
        getNotes();
    }, []);

    const getNotes = async () => {
        try {
            const res = await api.get("/api/notes/");
            setNotes(res.data);
        } catch (err) {
            console.error("Error fetching notes:", err);
        } finally {
            setLoading(false);
        }
    };

    const deleteNote = async (id) => {
        if (!window.confirm("Delete this note?")) return;

        try {
            const res = await api.delete(`/api/notes/delete/${id}/`);
            if (res.status === 204) {
                setNotes(notes.filter(note => note.id !== id));
            }
        } catch (error) {
            console.error("Error deleting note:", error);
        }
    };

    const createNote = async (e) => {
        e.preventDefault();
        if (!title.trim() || !content.trim()) return;

        setCreating(true);
        try {
            const res = await api.post("/api/notes/", { content, title });
            if (res.status === 201) {
                setNotes([res.data, ...notes]);
                setTitle("");
                setContent("");
                titleRef.current?.focus();
            }
        } catch (err) {
            console.error("Error creating note:", err);
        } finally {
            setCreating(false);
        }
    };

    return (
        <div className="notes-page">
            {/* Header */}
            <header className="notes-header">
                <button className="btn-icon" onClick={() => navigate('/')} title="Go Home">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
                        <polyline points="9,22 9,12 15,12 15,22" />
                    </svg>
                </button>
                <h1 className="notes-title">
                    <span className="title-icon">📝</span>
                    My Notes
                </h1>
                <div className="notes-count">
                    {notes.length} note{notes.length !== 1 ? 's' : ''}
                </div>
            </header>

            <div className="notes-content">
                {/* Create Note Section */}
                <section className="create-section">
                    <h2>Create a Note</h2>
                    <form onSubmit={createNote} className="create-form">
                        <div className="form-group">
                            <input
                                ref={titleRef}
                                type="text"
                                id="title"
                                placeholder="Note title..."
                                value={title}
                                onChange={(e) => setTitle(e.target.value)}
                                required
                            />
                        </div>
                        <div className="form-group">
                            <textarea
                                id="content"
                                placeholder="Write your note here..."
                                value={content}
                                onChange={(e) => setContent(e.target.value)}
                                rows="4"
                                required
                            />
                        </div>
                        <button
                            type="submit"
                            className="btn btn-primary create-btn"
                            disabled={creating || !title.trim() || !content.trim()}
                        >
                            {creating ? (
                                <>
                                    <div className="spinner"></div>
                                    Creating...
                                </>
                            ) : (
                                <>
                                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                        <line x1="12" y1="5" x2="12" y2="19" />
                                        <line x1="5" y1="12" x2="19" y2="12" />
                                    </svg>
                                    Create Note
                                </>
                            )}
                        </button>
                    </form>
                </section>

                {/* Notes List */}
                <section className="notes-list-section">
                    <h2>Your Notes</h2>
                    {loading ? (
                        <div className="loading-state">
                            <div className="spinner"></div>
                            <p>Loading notes...</p>
                        </div>
                    ) : notes.length === 0 ? (
                        <div className="empty-state">
                            <div className="empty-icon">📋</div>
                            <h3>No notes yet</h3>
                            <p>Create your first note above to get started!</p>
                        </div>
                    ) : (
                        <div className="notes-grid">
                            {notes.map((note) => (
                                <Note key={note.id} note={note} onDelete={deleteNote} />
                            ))}
                        </div>
                    )}
                </section>
            </div>
        </div>
    );
}

export default Notes;
