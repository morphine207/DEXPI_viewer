# DEXPI P&ID Visualizer

A Streamlit web app that renders [DEXPI](https://dexpi.org/) Proteus XML files as P&ID diagrams.

## Overview

Upload a DEXPI-compliant XML file and the app will invoke the GraphicBuilder JAR to produce a PNG rendering of the P&ID, displayed directly in the browser.

## Requirements

- Python 3.11+
- Java 8 (JDK8) — expected at `/home/rumi/.local/opt/jdk8/bin/java`
- The GraphicBuilder JAR (built from `GraphicBuilder/org.dexpi.pid.imaging`)
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

## Installation

```bash
# Install Python dependencies
uv sync
```

## Running the App

```bash
uv run streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

## Usage

1. Upload a DEXPI Proteus XML file via the sidebar.
2. Click **Render** to generate the P&ID diagram.
3. View the PNG output and optionally download it.

## Project Structure

```
app.py              # Streamlit application
main.py             # CLI entry point
pyproject.toml      # Python project config & dependencies
GraphicBuilder/     # Java-based SVG/PNG rendering engine (git submodule)
```
