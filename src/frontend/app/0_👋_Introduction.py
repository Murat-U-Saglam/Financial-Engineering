import streamlit as st
from pathlib import Path


def read_markdown_file(file_path: Path) -> str:
    return file_path.read_text()


st.set_page_config(layout="wide")

st.title("Financial Engineering App")


intro_md = read_markdown_file(file_path=Path("./app/README.md"))
st.markdown(intro_md)
