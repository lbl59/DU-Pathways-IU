FROM python:3.11-slim

WORKDIR /app

# requirements.txt only needs pure-Python / manylinux wheels (streamlit,
# plotly, pillow) - no system packages required.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Only copy what the app reads at runtime. results/, scripts/, and src/ are
# reproducibility artifacts for the paper, not used by streamlit_app.py.
COPY streamlit_app.py hotspot_explorer.py method_step_explorer.py ./
COPY pages/ ./pages/
COPY figures/ ./figures/

EXPOSE 8080

# Cloud Run sets $PORT (defaults to 8080); server.address must be 0.0.0.0
# so the container accepts connections from outside localhost.
CMD ["sh", "-c", "streamlit run streamlit_app.py --server.port=${PORT:-8080} --server.address=0.0.0.0 --server.headless=true"]
