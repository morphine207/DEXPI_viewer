"""
DEXPI P&ID Visualizer — Streamlit app
Takes a DEXPI Proteus XML file, runs the GraphicBuilder JAR to render a PNG,
and displays the result.
"""

import subprocess
import tempfile
from pathlib import Path

import streamlit as st

JAVA = Path("/home/rumi/.local/opt/jdk8/bin/java")
JAR = Path("/home/rumi/dexpi/GraphicBuilder/org.dexpi.pid.imaging/target/GraphicBuilder-1.0-jar-with-dependencies.jar")
MAIN_CLASS = "org.dexpi.pid.test.old.CommandLineTester"


def render_xml_to_png(xml_bytes: bytes, filename: str) -> tuple[bytes, str]:
    """
    Write xml_bytes to a temp file, call the GraphicBuilder JAR, and return
    the PNG bytes plus any log output.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        xml_path = Path(tmpdir) / filename
        xml_path.write_bytes(xml_bytes)

        result = subprocess.run(
            [str(JAVA), "-cp", str(JAR), MAIN_CLASS, str(xml_path)],
            capture_output=True,
            text=True,
            timeout=120,
        )

        logs = result.stdout + result.stderr
        png_path = xml_path.with_suffix(".png")
        if not png_path.exists():
            raise RuntimeError(
                f"GraphicBuilder did not produce a PNG.\n\nOutput:\n{logs}"
            )
        return png_path.read_bytes(), logs


def main():
    st.set_page_config(
        page_title="DEXPI P&ID Visualizer",
        page_icon="🏭",
        layout="wide",
    )

    with st.sidebar:
        st.title("🏭 DEXPI Visualizer")
        st.markdown("Upload a **DEXPI Proteus XML** file to render it as a PNG diagram.")

        uploaded_xml = st.file_uploader("Upload XML file", type=["xml"])

        st.divider()
        st.markdown(
            "Rendered by the "
            "[DEXPI GraphicBuilder](https://github.com/DEXPI/GraphicBuilder) JAR."
        )

    # ── Resolve XML source ────────────────────────────────────────────────────
    xml_bytes, xml_name = None, None

    if uploaded_xml:
        xml_bytes = uploaded_xml.read()
        xml_name = uploaded_xml.name

    if xml_bytes is None:
        st.info("Upload a DEXPI Proteus XML file to render the P&ID diagram.")
        return

    st.title(f"DEXPI P&ID — {xml_name}")

    # ── Render ────────────────────────────────────────────────────────────────
    cache_key = f"png_{hash(xml_bytes)}"
    if cache_key not in st.session_state:
        with st.spinner("Rendering diagram…"):
            try:
                png_bytes, logs = render_xml_to_png(xml_bytes, xml_name)
                st.session_state[cache_key] = png_bytes
                st.session_state[cache_key + "_logs"] = logs
            except Exception as exc:
                st.error(str(exc))
                return

    png_bytes = st.session_state[cache_key]
    logs = st.session_state.get(cache_key + "_logs", "")

    # ── Display ───────────────────────────────────────────────────────────────
    st.image(png_bytes, use_container_width=True)

    png_name = Path(xml_name).stem + ".png"
    st.download_button(
        "⬇️ Download PNG",
        data=png_bytes,
        file_name=png_name,
        mime="image/png",
    )

    with st.expander("Build log"):
        st.code(logs)


if __name__ == "__main__":
    main()
