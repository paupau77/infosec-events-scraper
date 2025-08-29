# infosec-events-scraper

[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-Async-green)](https://playwright.dev/python/)
[![License](https://img.shields.io/badge/license-MIT-orange)](LICENSE)
[![Build Status](https://img.shields.io/badge/status-stable-success)]()

Scraper en **Python** usando `Playwright` y `asyncio` para recolectar información de conferencias de seguridad informática desde [infosec-conferences.com](https://infosec-conferences.com).  

El script extrae:
- Nombre, fecha, ubicación y detalles de cada evento.
- Descripción completa de cada conferencia.
- Exporta todo a un **CSV estructurado** (`infosec_with_descriptions.csv`).

---

## 🚀 Instalación

git clone https://github.com/tuusuario/infosec-events-scraper.git
cd infosec-events-scraper
pip install -r requirements.txt


---

▶️ Uso

python ScrappingDescription.py

Esto generará un archivo CSV con toda la información:

infosec_with_descriptions.csv


---

📂 Archivos principales

ScrappingDescription.py → Script principal del scraper.

infosec_local.csv → Ejemplo de salida.



---

📜 Licencia

Mi proyecto está bajo la licencia MIT.

---
