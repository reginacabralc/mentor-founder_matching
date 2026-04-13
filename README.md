# 🚀 EPIC Lab · Mentor Match Engine
### MAD Fellows Challenge 2026 — Track 01: Community Multiplier

> "El matching manual de mentores es lento, sesgado y no escala. Esta herramienta lo automatiza usando machine learning."

---

## ¿Qué problema resuelve?

En el EPIC Lab, conectar founders con los mentores correctos depende hoy de la memoria y red personal del equipo organizador. El proceso es:

- **Lento** — toma días 
- **Sesgado** 
- **No escala** — cada nuevo mentor o founder aumenta la complejidad manualmente

Esta plataforma automatiza el matching usando ciencia de datos, reduciendo el tiempo de decisión de días a segundos.

---

## Instalación y uso (2 minutos)

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Terminal A — backend
uvicorn main:app --reload --port 8000

# 3. Terminal B — frontend
streamlit run app.py
```

La app abre en **http://localhost:8501**

Verifica que el backend responde en: `http://localhost:8000/health`

---

## Cómo funciona (el algoritmo)

```
Perfil del Founder (5 dimensiones)
         │
         ▼
  StandardScaler  →  normaliza a media 0, desviación 1
         │
         ▼
  PCA (2 componentes)  →  reduce dimensiones para visualización
         │
         ├──▶  K-Means (k clusters)  →  agrupa mentores en arquetipos
         │
         └──▶  Hybrid scoring system  → 60% complementarity and 40% proximity 

```

### Los 5 arquetipos de mentor

| Arquetipo    | Fortaleza principal       | Ideal para founders que necesitan...        |
|-------------|----------------------------|---------------------------------------------|
| Builders   | Tech + Producto             | Escalar su arquitectura o equipo técnico    |
| Connectors | Marketing + Comunidad       | Distribución, marca y crecimiento orgánico  |
| Operators  | Finanzas + Legal            | Fundraising, compliance y estructura legal  |
| Visionaries| Estrategia general          | Visión de largo plazo y decisiones de board |
| Specialists| Expertise vertical profundo | Validación en industrias específicas        |

---

## Stack tecnológico

| Capa       | Tecnología                          |
|------------|-------------------------------------|
| Backend    | FastAPI + scikit-learn              |
| ML         | PCA, K-Means, StandardScaler        |
| Frontend   | Streamlit + Plotly (Scatter, Radar) |
| Datos      | Dataset sintético de 60 mentores    |

---

## Evidencia de uso de IA

Esta solución usó IA en cada etapa del proceso (criterio de evaluación del reto):

| Etapa            | Herramienta        | Cómo se usó                                                          |
|------------------|--------------------|----------------------------------------------------------------------|
| Ideación         | Claude (Sonnet 4)  | Generación y evaluación de propuestas para los 3 tracks              |
| Arquitectura     | Claude (Sonnet 4)  | Diseño del sistema FastAPI + Streamlit + sklearn                     |
| Código           | Claude (Sonnet 4)  | Generación de `main.py` y `app.py`                                   |
| Dataset          | Claude (Sonnet 4)  | Diseño de los arquetipos de mentores y sus sesgos de habilidades     |
| UX / Copy        | Claude (Sonnet 4)  | Nombres de clusters, descripciones y textos de la interfaz           |

---
