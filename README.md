# 🚀 EPIC Lab · Mentor Match Engine
### MAD Fellows Challenge 2026 — Track 01: Community Multiplier

> "El matching manual de mentores es lento, sesgado y no escala. Esta herramienta lo automatiza usando Machine Learning."

---

## ¿Qué problema resuelve?

En el EPIC Lab, conectar founders con los mentores correctos depende hoy de la memoria y red personal del equipo organizador. El proceso es:

- **Lento** — toma días o semanas
- **Sesgado** — favorece a quienes ya conocen a alguien
- **No escala** — cada nuevo mentor o founder aumenta la complejidad manualmente

Esta plataforma automatiza el matching usando ciencia de datos, reduciendo el tiempo de decisión de días a segundos.

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
         └──▶  Distancia Euclidiana  →  mentor más cercano = mejor match
```

### Los 5 arquetipos de mentor

| Arquetipo    | Fortaleza principal         | Ideal para founders que necesitan...        |
|-------------|----------------------------|---------------------------------------------|
| 🔵 Builders   | Tech + Producto             | Escalar su arquitectura o equipo técnico    |
| 🟠 Connectors | Marketing + Comunidad       | Distribución, marca y crecimiento orgánico  |
| 🔴 Operators  | Finanzas + Legal            | Fundraising, compliance y estructura legal  |
| 🩵 Visionaries| Estrategia general          | Visión de largo plazo y decisiones de board |
| 🟣 Specialists| Expertise vertical profundo | Validación en industrias específicas        |

---

## Stack tecnológico

| Capa       | Tecnología                          |
|------------|-------------------------------------|
| Backend    | FastAPI + scikit-learn              |
| ML         | PCA, K-Means, StandardScaler        |
| Frontend   | Streamlit + Plotly (Scatter, Radar) |
| Datos      | Dataset sintético de 60 mentores    |

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

## Evidencia de uso de IA

Esta solución usó IA en cada etapa del proceso (criterio de evaluación del reto):

| Etapa            | Herramienta        | Cómo se usó                                                          |
|------------------|--------------------|----------------------------------------------------------------------|
| Ideación         | Claude (Sonnet 4)  | Generación y evaluación de propuestas para los 3 tracks              |
| Arquitectura     | Claude (Sonnet 4)  | Diseño del sistema FastAPI + Streamlit + sklearn                     |
| Código           | Claude (Sonnet 4)  | Generación de `main.py` y `app.py` completos                        |
| Dataset          | Claude (Sonnet 4)  | Diseño de los arquetipos de mentores y sus sesgos de habilidades     |
| UX / Copy        | Claude (Sonnet 4)  | Nombres de clusters, descripciones y textos de la interfaz           |
| Este README      | Claude (Sonnet 4)  | Estructura, tabla de arquetipos y sección de evidencia de IA         |

---

## Guía para el video (3 minutos en inglés)

### Estructura sugerida

**0:00 – 0:30 · El problema**
> "At EPIC Lab, mentor-founder matching is done manually. It takes days, it's biased toward who you already know, and it doesn't scale. I built a tool to fix that."

**0:30 – 1:00 · La solución**
> "This is a real machine learning pipeline. I take a founder's skill profile across 5 dimensions, run it through PCA to reduce the space, use K-Means to find mentor archetypes, and then calculate Euclidean distance to find the closest match."

**1:00 – 2:30 · Demo en vivo**
- Mueve los sliders (ej. sube Tech, baja Marketing)
- Señala cómo el punto rojo se mueve en el mapa PCA
- Muestra el match principal con su arquetipo (Builders, Connectors, etc.)
- Señala el radar chart: "this is where he complements me"
- Cambia el número de clusters y muestra cómo el mapa se reorganiza

**2:30 – 3:00 · Impacto y próximos pasos**
> "With real LinkedIn or EPIC Lab profile data, this tool could run live at every EPIC event — matching any new founder to the right mentor in under 10 seconds, at scale."

### Tips para el video
- Graba con Loom (pantalla + cámara en esquina)
- Habla mientras mueves los sliders — el movimiento en tiempo real es tu diferenciador visual
- Muestra el terminal del backend corriendo en paralelo: evidencia de que es código real, no un prototipo de no-code
