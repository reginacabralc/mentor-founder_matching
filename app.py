import streamlit as st
import requests
import plotly.graph_objects as go

st.set_page_config(
    page_title="EPIC Lab · Mentor Matcher",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Design system ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,300&family=DM+Serif+Display:ital@0;1&display=swap');

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"],
[data-testid="stApp"], .main { background: #FAFAF8 !important; }

[data-testid="stAppViewContainer"] {
    font-family: 'DM Sans', sans-serif;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #FFFFFF !important;
    border-right: 1px solid #E8E6E1 !important;
    padding-top: 0 !important;
}
[data-testid="stSidebar"] > div:first-child { padding-top: 0; }

/* ── Headings ── */
h1, h2, h3, h4 {
    font-family: 'DM Serif Display', Georgia, serif !important;
    color: #1A1A18 !important;
    font-weight: 400 !important;
    letter-spacing: -0.02em;
}
h1 { font-size: 2.6rem !important; line-height: 1.1 !important; }
h2 { font-size: 1.5rem !important; }
h3 { font-size: 1.15rem !important; }

/* ── Body text ── */
p, label, .stMarkdown p, span {
    font-family: 'DM Sans', sans-serif !important;
    color: #4A4A44 !important;
    font-size: 0.9rem;
    line-height: 1.6;
}

/* ── Metric cards ── */
[data-testid="metric-container"] {
    background: #FFFFFF !important;
    border: 1px solid #E8E6E1 !important;
    border-radius: 14px !important;
    padding: 16px 20px !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
}
[data-testid="stMetricValue"] {
    font-family: 'DM Serif Display', serif !important;
    color: #1A1A18 !important;
    font-size: 1.8rem !important;
    font-weight: 400 !important;
}
[data-testid="stMetricLabel"] {
    font-family: 'DM Sans', sans-serif !important;
    color: #9B9B8F !important;
    font-size: 0.75rem !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
[data-testid="stMetricDelta"] { display: none; }

/* ── Slider accent ── */
[data-testid="stSlider"] > div > div > div > div {
    background: #2D6A4F !important;
}

/* ── Button ── */
.stButton > button {
    background: #1A1A18 !important;
    color: #FAFAF8 !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    padding: 12px 20px !important;
    letter-spacing: 0.01em;
    transition: all 0.2s ease;
}
.stButton > button:hover {
    background: #2D6A4F !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(45,106,79,0.3) !important;
}

/* ── Divider ── */
hr { border: none; border-top: 1px solid #E8E6E1 !important; margin: 1.2rem 0 !important; }

/* ── Custom cards ── */
.match-card {
    background: #FFFFFF;
    border: 1px solid #D4E8DC;
    border-left: 4px solid #2D6A4F;
    border-radius: 14px;
    padding: 22px 24px;
    margin-bottom: 16px;
    box-shadow: 0 2px 12px rgba(45,106,79,0.08);
}
.match-card .match-name {
    font-family: 'DM Serif Display', serif;
    font-size: 1.25rem;
    color: #1A1A18;
    margin: 0 0 4px 0;
    font-weight: 400;
}
.match-card .match-meta {
    font-size: 0.83rem;
    color: #9B9B8F;
    margin: 2px 0;
}

.runner-card {
    background: #FFFFFF;
    border: 1px solid #E8E6E1;
    border-radius: 12px;
    padding: 14px 18px;
    margin-bottom: 8px;
    transition: box-shadow 0.15s;
}
.runner-card:hover { box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
.runner-card .runner-name {
    font-family: 'DM Sans', sans-serif;
    font-weight: 600;
    font-size: 0.9rem;
    color: #1A1A18;
    margin: 0 0 3px 0;
}
.runner-card .runner-meta { font-size: 0.78rem; color: #9B9B8F; margin: 0; }

.cluster-pill {
    display: inline-block;
    border-radius: 20px;
    padding: 3px 11px;
    font-size: 0.72rem;
    font-weight: 600;
    font-family: 'DM Sans', sans-serif;
    letter-spacing: 0.03em;
    margin-right: 5px;
    margin-bottom: 4px;
}

.stat-chip {
    display: inline-block;
    background: #F0F0EC;
    color: #4A4A44;
    border-radius: 8px;
    padding: 3px 10px;
    font-size: 0.75rem;
    font-family: 'DM Sans', sans-serif;
    margin-right: 6px;
    margin-bottom: 4px;
}

.section-eyebrow {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: #B0AFA8 !important;
    margin-bottom: 10px !important;
    font-weight: 500 !important;
}

.gap-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 8px 0;
    border-bottom: 1px solid #F0F0EC;
    font-size: 0.83rem;
}
.gap-label { color: #4A4A44; font-family: 'DM Sans', sans-serif; }
.gap-value { font-weight: 600; font-family: 'DM Sans', sans-serif; }

.algo-step {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 10px 0;
    border-bottom: 1px solid #F0F0EC;
}
.algo-num {
    min-width: 24px; height: 24px;
    background: #1A1A18;
    color: #FAFAF8;
    border-radius: 50%;
    font-size: 0.72rem;
    font-weight: 600;
    display: flex; align-items: center; justify-content: center;
    font-family: 'DM Sans', sans-serif;
    margin-top: 1px;
}
.algo-text { font-size: 0.82rem; color: #4A4A44; font-family: 'DM Sans', sans-serif; line-height: 1.5; }
.algo-text b { color: #1A1A18; }

/* ── Sidebar logo zone ── */
.sidebar-logo {
    background: #F0EDE8;
    border-bottom: 1px solid #E0DDD8;
    margin: -1rem -1rem 1.5rem -1rem;
    padding: 24px 24px 20px 24px;
}
.sidebar-logo .logo-text {
    font-family: 'DM Serif Display', serif;
    font-size: 1.4rem;
    color: #1A1A18;
    margin: 0;
    font-weight: 400;
}
.sidebar-logo .logo-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.75rem;
    color: #9B9B8F;
    margin: 4px 0 0 0;
    letter-spacing: 0.04em;
}

/* ── Page title zone ── */
.page-header {
    padding: 2rem 0 1.5rem 0;
    border-bottom: 1px solid #E8E6E1;
    margin-bottom: 2rem;
}
.page-eyebrow {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.72rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #2D6A4F;
    font-weight: 600;
    margin-bottom: 8px;
}
.page-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.8rem;
    color: #1A1A18;
    line-height: 1.05;
    margin: 0 0 8px 0;
    font-weight: 400;
}
.page-title em { color: #2D6A4F; font-style: italic; }
.page-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.88rem;
    color: #9B9B8F;
    margin: 0;
}

/* ── Legend bar ── */
.legend-bar {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    align-items: center;
    padding: 14px 20px;
    background: #FFFFFF;
    border: 1px solid #E8E6E1;
    border-radius: 12px;
    margin-bottom: 20px;
}
.legend-label {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.72rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #B0AFA8;
    margin-right: 4px;
    font-weight: 500;
}

/* ── Section titles ── */
.section-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.1rem;
    color: #1A1A18;
    margin: 0 0 14px 0;
    font-weight: 400;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0 !important; padding-bottom: 3rem; max-width: 1400px; }
</style>
""", unsafe_allow_html=True)

# ── Constants ─────────────────────────────────────────────────────────────────
API_URL = "http://localhost:8000"
FEATURES = ["Tech", "Marketing", "Legal", "Finance", "Strategy"]
FEATURE_ICONS = {"Tech": "💻", "Marketing": "📣", "Legal": "⚖️", "Finance": "💰", "Strategy": "♟️"}

CLUSTER_PALETTE = {
    "Builders":    "#2563EB",
    "Connectors":  "#D97706",
    "Operators":   "#DC2626",
    "Visionaries": "#059669",
    "Specialists": "#7C3AED",
}
DEFAULT_COLORS = ["#2563EB", "#D97706", "#DC2626", "#059669", "#7C3AED"]

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class='sidebar-logo'>
        <p class='logo-text'>EPIC Lab</p>
        <p class='logo-sub'>Mentor Match Engine · MAD Fellows 2026</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<p class='section-eyebrow'>Tu perfil de Founder</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.8rem;color:#9B9B8F;margin-bottom:12px;'>Arrastra cada slider para reflejar tu nivel de expertise actual (1 = básico · 10 = experto)</p>", unsafe_allow_html=True)

    tech      = st.slider("💻 Tech & Producto",  1, 10, 5)
    marketing = st.slider("📣 Marketing & Growth",1, 10, 5)
    legal     = st.slider("⚖️ Legal",             1, 10, 3)
    finance   = st.slider("💰 Finanzas",          1, 10, 4)
    strategy  = st.slider("♟️ Estrategia",        1, 10, 6)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<p class='section-eyebrow'>Configuración del modelo</p>", unsafe_allow_html=True)
    n_clusters = st.select_slider("Número de clusters K-Means", options=[2, 3, 4, 5], value=5)

    st.markdown("<hr>", unsafe_allow_html=True)
    run = st.button("Encontrar mi mentor →", use_container_width=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class='page-header'>
    <p class='page-eyebrow'>EPIC Lab · ITAM · MAD Fellows 2026</p>
    <h1 class='page-title'>Mentor <em>Match</em> Engine</h1>
    <p class='page-sub'>PCA + K-Means sobre 100 mentores · Encuentra al mentor que más te complementa</p>
</div>
""", unsafe_allow_html=True)

# ── Fetch data ────────────────────────────────────────────────────────────────
if "result" not in st.session_state:
    run = True

if run:
    with st.spinner("Corriendo PCA + K-Means..."):
        try:
            resp = requests.post(f"{API_URL}/match", json={
                "tech": tech, "marketing": marketing,
                "legal": legal, "finance": finance,
                "strategy": strategy, "n_clusters": n_clusters,
            }, timeout=10)
            resp.raise_for_status()
            st.session_state["result"] = resp.json()
        except Exception as e:
            st.error(f"⚠️ Backend no disponible. Corre: `uvicorn main:app --reload`\n\n`{e}`")
            st.stop()

data = st.session_state.get("result")
if not data:
    st.stop()

mentors       = data["mentors"]
founder       = data["founder"]
best_idx      = data["best_match_idx"]
top3          = data["top3_idx"]
explained     = data["explained_variance"]
best          = mentors[best_idx]
cluster_names = data.get("cluster_names", {})
cluster_descs = data.get("cluster_descriptions", {})

# ── Metrics row ───────────────────────────────────────────────────────────────
m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Mentores en base", str(data.get("n_mentors", len(mentors))))
m2.metric("Arquetipos (k)", str(n_clusters))
m3.metric("Varianza PC1", f"{explained[0]}%")
m4.metric("Varianza PC2", f"{explained[1]}%")
m5.metric("Match score", f"{max(0, round(100 - best['distance'] * 6.5))}%")

st.markdown("<div style='margin:28px 0 0 0;'></div>", unsafe_allow_html=True)

# ── Cluster legend ─────────────────────────────────────────────────────────────
unique_names = list(dict.fromkeys(
    [cluster_names.get(str(m["cluster"]), cluster_names.get(m["cluster"], f"Cluster {m['cluster']+1}")) for m in mentors]
))
pills_html = "<span class='legend-label'>Arquetipos</span>"
for name in unique_names:
    color = CLUSTER_PALETTE.get(name, "#888")
    pills_html += (
        f"<span class='cluster-pill' "
        f"style='background:{color}15;color:{color};border:1.5px solid {color}40;'>"
        f"{name}</span>"
    )
st.markdown(f"<div class='legend-bar'>{pills_html}</div>", unsafe_allow_html=True)

# ── Main layout ───────────────────────────────────────────────────────────────
col_chart, col_match = st.columns([13, 7], gap="large")

# ── PCA scatter ───────────────────────────────────────────────────────────────
with col_chart:
    st.markdown("<p class='section-title'>Espacio de similitud — 100 mentores</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.8rem;color:#9B9B8F;margin:-8px 0 14px;'>Cada punto es un mentor proyectado en 2D mediante PCA. El diamante rojo eres tú. La línea conecta con tu mejor match.</p>", unsafe_allow_html=True)

    fig = go.Figure()

    # ── 1. Confidence ellipses (drawn first, behind points) ───────────────────
    ellipses = data.get("ellipses", [])

    def hex_to_rgba(hex_color, alpha):
        """Convert #RRGGBB to rgba(r,g,b,alpha) for Plotly."""
        h = hex_color.lstrip("#")
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        return f"rgba({r},{g},{b},{alpha})"

    for ell in ellipses:
        c_name = ell["cluster_name"]
        color  = CLUSTER_PALETTE.get(c_name, DEFAULT_COLORS[ell["cluster"] % len(DEFAULT_COLORS)])
        fig.add_trace(go.Scatter(
            x=ell["x"] + [ell["x"][0]],
            y=ell["y"] + [ell["y"][0]],
            mode="lines",
            fill="toself",
            fillcolor=hex_to_rgba(color, 0.08),
            line=dict(color=hex_to_rgba(color, 0.55), width=1.5, dash="dot"),
            hoverinfo="skip",
            showlegend=False,
        ))
        fig.add_trace(go.Scatter(
            x=[ell["cx"]], y=[ell["cy"]],
            mode="text",
            text=[f"<b>{c_name}</b>"],
            textfont=dict(size=10, color=color, family="DM Sans"),
            hoverinfo="skip",
            showlegend=False,
        ))

    # ── 2. Color by cluster (K-Means) — ellipses make grouping clear ──────────
    clusters_drawn = {}
    for m in mentors:
        c_id   = m["cluster"]
        c_name = cluster_names.get(str(c_id), cluster_names.get(c_id, f"Cluster {c_id+1}"))
        color  = CLUSTER_PALETTE.get(c_name, DEFAULT_COLORS[c_id % len(DEFAULT_COLORS)])

        if c_name not in clusters_drawn:
            clusters_drawn[c_name] = {"x":[], "y":[], "hover":[], "sizes":[], "symbols":[], "opacities":[], "color": color}

        is_best = m["id"] == best_idx
        is_top3 = m["id"] in top3

        clusters_drawn[c_name]["x"].append(m["x"])
        clusters_drawn[c_name]["y"].append(m["y"])
        clusters_drawn[c_name]["hover"].append(
            f"<b style='font-size:14px'>{m['name']}</b><br>"
            f"<span style='color:#666'>{c_name} · {m['sector']} · {m['stage']}</span><br><br>"
            f"Tech {m['scores']['Tech']:.0f}  ·  Mktg {m['scores']['Marketing']:.0f}  ·  "
            f"Fin {m['scores']['Finance']:.0f}  ·  Strat {m['scores']['Strategy']:.0f}<br>"
            f"<b>Match score: {max(0, round(100 - m['distance'] * 6.5))}%</b>"
        )
        clusters_drawn[c_name]["sizes"].append(18 if is_best else (14 if is_top3 else 9))
        clusters_drawn[c_name]["symbols"].append("star" if is_best else "circle")
        clusters_drawn[c_name]["opacities"].append(1.0 if is_best or is_top3 else 0.65)

    for c_name, d in clusters_drawn.items():
        fig.add_trace(go.Scatter(
            x=d["x"], y=d["y"],
            mode="markers",
            marker=dict(
                size=d["sizes"],
                color=d["color"],
                opacity=d["opacities"],
                line=dict(width=1.5, color="white"),
                symbol=d["symbols"],
            ),
            hovertext=d["hover"],
            hoverinfo="text",
            name=c_name,
        ))

    # Connection line
    fig.add_trace(go.Scatter(
        x=[founder["x"], best["x"]], y=[founder["y"], best["y"]],
        mode="lines",
        line=dict(color="#059669", width=1.5, dash="dash"),
        showlegend=False, hoverinfo="skip",
    ))

    # Founder
    fig.add_trace(go.Scatter(
        x=[founder["x"]], y=[founder["y"]],
        mode="markers+text",
        marker=dict(
            size=22, color="#EF4444", symbol="diamond",
            line=dict(width=2.5, color="white"),
        ),
        text=["Tú"], textposition="top center",
        textfont=dict(size=12, color="#EF4444", family="DM Sans"),
        hovertext=["<b>Tu perfil de Founder</b>"],
        hoverinfo="text",
        name="Founder (Tú)",
    ))

    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FAFAF8",
        font=dict(family="DM Sans, sans-serif", color="#4A4A44", size=12),
        xaxis=dict(
            title=f"Componente Principal 1  ({explained[0]}% varianza)",
            gridcolor="#F0F0EC", zeroline=False,
            title_font=dict(color="#9B9B8F", size=11),
            tickfont=dict(color="#B0AFA8", size=10),
        ),
        yaxis=dict(
            title=f"Componente Principal 2  ({explained[1]}% varianza)",
            gridcolor="#F0F0EC", zeroline=False,
            title_font=dict(color="#9B9B8F", size=11),
            tickfont=dict(color="#B0AFA8", size=10),
        ),
        legend=dict(
            bgcolor="rgba(255,255,255,0.95)",
            bordercolor="#E8E6E1", borderwidth=1,
            font=dict(size=11, family="DM Sans"),
            title=dict(text="Arquetipos", font=dict(size=10, color="#9B9B8F")),
        ),
        margin=dict(l=50, r=20, t=20, b=60),
        height=480,
        hovermode="closest",
        hoverlabel=dict(
            bgcolor="white", bordercolor="#E8E6E1",
            font=dict(family="DM Sans", size=12),
        ),
    )

    st.plotly_chart(fig, use_container_width=True)

    # ── Radar ────────────────────────────────────────────────────────────────
    st.markdown("<p class='section-title'>Comparativa de habilidades</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:0.8rem;color:#9B9B8F;margin:-8px 0 14px;'>Tu perfil (rojo) vs. <b style='color:#1A1A18;'>{best['name']}</b> (verde)</p>", unsafe_allow_html=True)

    fig_r = go.Figure()
    theta = FEATURES + [FEATURES[0]]

    fig_r.add_trace(go.Scatterpolar(
        r=[founder["scores"][f] for f in FEATURES] + [founder["scores"][FEATURES[0]]],
        theta=theta, fill="toself", name="Tú",
        line=dict(color="#EF4444", width=2),
        fillcolor="rgba(239,68,68,0.08)",
    ))
    fig_r.add_trace(go.Scatterpolar(
        r=[best["scores"][f] for f in FEATURES] + [best["scores"][FEATURES[0]]],
        theta=theta, fill="toself", name=best["name"].split()[0],
        line=dict(color="#059669", width=2),
        fillcolor="rgba(5,150,105,0.08)",
    ))

    fig_r.update_layout(
        polar=dict(
            bgcolor="#FAFAF8",
            radialaxis=dict(
                visible=True, range=[0, 10],
                gridcolor="#E8E6E1",
                tickfont=dict(color="#B0AFA8", size=9),
                tickvals=[2,4,6,8,10],
            ),
            angularaxis=dict(
                gridcolor="#E8E6E1",
                tickfont=dict(color="#4A4A44", size=11, family="DM Sans"),
            ),
        ),
        paper_bgcolor="#FFFFFF",
        template="plotly_white",
        legend=dict(
            bgcolor="rgba(255,255,255,0.95)",
            bordercolor="#E8E6E1", borderwidth=1,
            font=dict(size=11, family="DM Sans"),
        ),
        margin=dict(l=40, r=40, t=30, b=30),
        height=320,
        hoverlabel=dict(bgcolor="white", bordercolor="#E8E6E1", font=dict(family="DM Sans")),
    )
    st.plotly_chart(fig_r, use_container_width=True)

# ── Match panel ───────────────────────────────────────────────────────────────
with col_match:
    best_cluster_name = cluster_names.get(str(best["cluster"]), cluster_names.get(best["cluster"], "—"))


    cluster_color = CLUSTER_PALETTE.get(best_cluster_name, "#059669")
    cluster_desc  = cluster_descs.get(str(best["cluster"]),
                    cluster_descs.get(best["cluster"], ""))

    st.markdown("<p class='section-eyebrow'>Tu mejor match</p>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='match-card'>
        <p class='match-name'>⭐ {best['name']}</p>
        <span class='cluster-pill'
          style='background:{cluster_color}18;color:{cluster_color};border:1.5px solid {cluster_color}50;'>
          {best_cluster_name}
        </span>
        <p class='match-meta' style='margin-top:10px;'>
            📍 {best['sector']}&nbsp;&nbsp;·&nbsp;&nbsp;{best['stage']}
        </p>
        <p class='match-meta' style='margin-top:6px;font-style:italic;color:#9B9B8F;'>
            {cluster_desc}
        </p>
        <div style='margin-top:14px;padding-top:12px;border-top:1px solid #E8E6E1;display:flex;gap:8px;flex-wrap:wrap;'>
            <span class='stat-chip'>Tech {best['scores']['Tech']:.0f}/10</span>
            <span class='stat-chip'>Mktg {best['scores']['Marketing']:.0f}/10</span>
            <span class='stat-chip'>Fin {best['scores']['Finance']:.0f}/10</span>
        </div>
        <p style='margin-top:12px;font-size:0.75rem;color:#B0AFA8;'>
            Match score <b style='color:{cluster_color};font-size:1rem;'>{max(0, round(100 - best['distance'] * 6.5))}%</b>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Gap analysis ──────────────────────────────────────────────────────────
    st.markdown("<p class='section-eyebrow' style='margin-top:20px;'>Análisis de brecha</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.78rem;color:#9B9B8F;margin-bottom:10px;'>Dónde el mentor te complementa (▲) o coincide (▼)</p>", unsafe_allow_html=True)

    gap_html = ""
    for feat, icon in FEATURE_ICONS.items():
        gap   = best["scores"][feat] - founder["scores"][feat]
        arrow = "▲" if gap > 0 else ("▼" if gap < 0 else "—")
        color = "#059669" if gap > 0 else ("#EF4444" if gap < 0 else "#9B9B8F")
        bar_w = min(abs(gap) * 10, 100)
        bar_c = color + "30"
        gap_html += f"""
        <div class='gap-row'>
            <span class='gap-label'>{icon} {feat}</span>
            <span class='gap-value' style='color:{color};'>{arrow} {abs(gap):.0f}</span>
        </div>
        """
    st.markdown(gap_html, unsafe_allow_html=True)

    # ── Runners up ────────────────────────────────────────────────────────────
    st.markdown("<p class='section-eyebrow' style='margin-top:24px;'>Otros candidatos</p>", unsafe_allow_html=True)
    for rank, idx in enumerate(top3):
        if idx == best_idx:
            continue
        m = mentors[idx]
        m_cname = cluster_names.get(str(m["cluster"]), cluster_names.get(m["cluster"], "—"))
        m_color = CLUSTER_PALETTE.get(m_cname, "#2563EB")
        st.markdown(f"""
        <div class='runner-card'>
            <p class='runner-name'>{m['name']}</p>
            <p class='runner-meta'>
                <span class='cluster-pill'
                  style='background:{m_color}15;color:{m_color};border:1px solid {m_color}40;font-size:0.68rem;'>
                  {m_cname}
                </span>
                {m['sector']} · {m['stage']}
            </p>
            <p class='runner-meta' style='margin-top:5px;'>
                Match <b style='color:{m_color};'>{max(0, round(100 - m['distance'] * 6.5))}%</b>
            </p>
        </div>
        """, unsafe_allow_html=True)

    # ── How it works ──────────────────────────────────────────────────────────
    st.markdown("<p class='section-eyebrow' style='margin-top:24px;'>Cómo funciona el algoritmo</p>", unsafe_allow_html=True)
    steps = [
        ("StandardScaler", "Normaliza las 5 dimensiones a media 0 y std 1 para evitar sesgos de escala."),
        ("PCA", "Reduce el espacio a 2 componentes principales para visualización e interpretación."),
        ("K-Means", "Agrupa los 100 mentores en arquetipos por similitud de habilidades."),
        ("Distancia euclidiana", "Mide la cercanía entre tu perfil y cada mentor en el espacio 2D."),
    ]
    for i, (title, desc) in enumerate(steps, 1):
        st.markdown(f"""
        <div class='algo-step'>
            <div class='algo-num'>{i}</div>
            <div class='algo-text'><b>{title}</b> — {desc}</div>
        </div>
        """, unsafe_allow_html=True)
