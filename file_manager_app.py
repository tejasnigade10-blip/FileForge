import streamlit as st
from pathlib import Path

st.set_page_config(page_title="FileForge — File Manager", page_icon="🗂️", layout="centered")

# ---------------- STYLING ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@700;800&display=swap');

:root {
    --accent: #c8f060;
    --bg: #0d0d0d;
    --card: #161616;
    --muted: #9a9a9a;
    --border: #2a2a2a;
}

.stApp {
    background: radial-gradient(circle at top left, #141414, #0a0a0a 60%);
    color: #eaeaea;
}

/* Hero */
.hero {
    padding: 2.2rem 1.5rem;
    border-radius: 16px;
    margin-bottom: 1.5rem;
    background: linear-gradient(120deg, #101010, #1a1f0d 60%, #101010);
    border: 1px solid var(--border);
    text-align: center;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2.4rem;
    margin: 0;
    background: linear-gradient(90deg, #ffffff, var(--accent));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero p {
    font-family: 'Space Mono', monospace;
    color: var(--muted);
    letter-spacing: .04em;
    margin-top: .4rem;
}

/* Cards */
.card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.4rem;
    margin-top: 1rem;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
}
.stTabs [data-baseweb="tab"] {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    font-family: 'Space Mono', monospace !important;
    text-transform: uppercase;
    letter-spacing: .06em;
    font-size: .78rem !important;
    color: var(--muted) !important;
    padding: .5rem 1rem !important;
}
.stTabs [aria-selected="true"] {
    color: #0d0d0d !important;
    background: var(--accent) !important;
    border-color: var(--accent) !important;
    font-weight: 700 !important;
}

/* Inputs */
[data-testid="stTextInput"] > div > div > input,
[data-testid="stTextArea"] textarea {
    background: #0d0d0d !important;
    border: 1px solid var(--border) !important;
    color: #eaeaea !important;
    border-radius: 8px !important;
    font-family: 'Space Mono', monospace !important;
}
[data-testid="stTextInput"] > div > div > input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(200,240,96,.12) !important;
}

label[data-testid="stWidgetLabel"] p {
    font-family: 'Space Mono', monospace !important;
    font-size: .78rem !important;
    letter-spacing: .06em;
    text-transform: uppercase;
    color: var(--muted) !important;
}

/* Buttons */
.stButton > button {
    background: var(--accent) !important;
    color: #0d0d0d !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: .9rem !important;
    letter-spacing: .04em;
    padding: .6rem 1.8rem !important;
    transition: transform .15s ease;
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 14px rgba(200,240,96,.25);
}

/* Radio (update operation choice) */
[data-testid="stRadio"] label {
    font-family: 'Space Mono', monospace !important;
}

footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ---------------- HERO ----------------
st.markdown("""
<div class="hero">
    <h1>🗂️ FileForge</h1>
    <p>// a minimal file management console built with python + streamlit</p>
</div>
""", unsafe_allow_html=True)

# ---------------- LOGIC (adapted from original CLI functions) ----------------

def create_file(name, content):
    path = Path(name)
    if not path.exists():
        with open(path, "w") as f:
            f.write(content)
        return "success", f"File '{name}' created successfully."
    return "error", f"A file named '{name}' already exists."

def read_file(name):
    path = Path(name)
    if path.exists():
        with open(path, "r") as f:
            return "success", f.read()
    return "error", f"File '{name}' does not exist."

def rename_file(name, new_name):
    path = Path(name)
    new_path = Path(new_name)
    if not path.exists():
        return "error", f"File '{name}' does not exist."
    if new_path.exists():
        return "error", f"A file named '{new_name}' already exists."
    path.rename(new_name)
    return "success", f"Renamed '{name}' to '{new_name}'."

def append_file(name, content):
    path = Path(name)
    if not path.exists():
        return "error", f"File '{name}' does not exist."
    with open(path, "a") as f:
        f.write("\n" + content)
    return "success", f"Content appended to '{name}'."

def overwrite_file(name, content):
    path = Path(name)
    if not path.exists():
        return "error", f"File '{name}' does not exist."
    with open(path, "w") as f:
        f.write(content)
    return "success", f"'{name}' overwritten successfully."

def delete_file(name):
    path = Path(name)
    try:
        if path.exists():
            path.unlink()
            return "success", f"File '{name}' deleted successfully."
        return "error", f"File '{name}' does not exist."
    except Exception as err:
        return "error", f"An error occurred: {err}"

def show_result(kind, msg):
    if kind == "success":
        st.success(msg)
    else:
        st.error(msg)

# ---------------- TABS ----------------
tab_create, tab_read, tab_update, tab_delete = st.tabs(
    ["📝 Create", "📖 Read", "✏️ Update", "🗑️ Delete"]
)

with tab_create:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Create a new file")
    c_name = st.text_input("File name", key="create_name", placeholder="notes.txt")
    c_content = st.text_area("Content", key="create_content", placeholder="Write something...", height=150)
    if st.button("Create File", key="create_btn"):
        if c_name.strip():
            show_result(*create_file(c_name.strip(), c_content))
        else:
            st.warning("Please enter a file name.")
    st.markdown('</div>', unsafe_allow_html=True)

with tab_read:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Read a file")
    r_name = st.text_input("File name", key="read_name", placeholder="notes.txt")
    if st.button("Read File", key="read_btn"):
        if r_name.strip():
            kind, msg = read_file(r_name.strip())
            if kind == "success":
                st.success(f"Contents of '{r_name}':")
                st.code(msg if msg else "(file is empty)")
            else:
                st.error(msg)
        else:
            st.warning("Please enter a file name.")
    st.markdown('</div>', unsafe_allow_html=True)

with tab_update:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Update a file")
    u_name = st.text_input("File name", key="update_name", placeholder="notes.txt")
    operation = st.radio(
        "Operation",
        ["Rename the file", "Append content", "Overwrite content"],
        key="update_op",
    )

    if operation == "Rename the file":
        new_name = st.text_input("New file name", key="rename_new")
        if st.button("Rename", key="rename_btn"):
            if u_name.strip() and new_name.strip():
                show_result(*rename_file(u_name.strip(), new_name.strip()))
            else:
                st.warning("Please fill in both file names.")

    elif operation == "Append content":
        append_content = st.text_area("Content to append", key="append_content", height=120)
        if st.button("Append", key="append_btn"):
            if u_name.strip():
                show_result(*append_file(u_name.strip(), append_content))
            else:
                st.warning("Please enter a file name.")

    elif operation == "Overwrite content":
        overwrite_content = st.text_area("New content", key="overwrite_content", height=120)
        if st.button("Overwrite", key="overwrite_btn"):
            if u_name.strip():
                show_result(*overwrite_file(u_name.strip(), overwrite_content))
            else:
                st.warning("Please enter a file name.")
    st.markdown('</div>', unsafe_allow_html=True)

with tab_delete:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Delete a file")
    d_name = st.text_input("File name", key="delete_name", placeholder="notes.txt")
    confirm = st.checkbox("I understand this cannot be undone", key="delete_confirm")
    if st.button("Delete File", key="delete_btn"):
        if not d_name.strip():
            st.warning("Please enter a file name.")
        elif not confirm:
            st.warning("Please confirm before deleting.")
        else:
            show_result(*delete_file(d_name.strip()))
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown(
    "<p style='text-align:center; color:#555; font-family:\"Space Mono\",monospace; "
    "font-size:.75rem; margin-top:2rem;'>built with python & streamlit</p>",
    unsafe_allow_html=True,
)