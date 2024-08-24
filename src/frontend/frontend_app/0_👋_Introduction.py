import streamlit as st
from pathlib import Path

st.set_page_config(layout="wide")


def read_markdown_file(file_path: Path) -> str:
    return file_path.read_text()


st.title("Financial Engineering App")


intro_md = read_markdown_file(file_path=Path("./frontend_app/README.md"))
st.markdown(intro_md)
