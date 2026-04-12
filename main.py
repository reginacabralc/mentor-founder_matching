from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

app = FastAPI(title="EPIC Lab Mentor Matcher API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Cluster archetypes ────────────────────────────────────────────────────────
CLUSTER_NAMES = {
    0: "Builders",
    1: "Connectors",
    2: "Operators",
    3: "Visionaries",
    4: "Specialists",
}
CLUSTER_DESCRIPTIONS = {
    0: "Engineers & product builders — turn ideas into scalable systems",
    1: "Growth experts & networkers — community, brand, and distribution",
    2: "Finance & legal experts — fundraising, compliance, and structure",
    3: "Strategic generalists — board-level thinking and market vision",
    4: "Domain specialists — deep expertise in one vertical",
}

# ── Mentor database (60 mentors) ──────────────────────────────────────────────
MENTOR_NAMES = [
    # Builders (0–11)
    "Alejandro Ríos","Carolina Fuentes","Diego Salinas","Elena Vargas",
    "Fernanda Ibáñez","Gerardo Ochoa","Héctor Palma","Irene Castañeda",
    "Jorge Montes","Karen Zúñiga","Luis Espinoza","Mónica Prado",
    # Connectors (12–23)
    "Natalia Serrano","Omar Delgado","Patricia Leal","Quentin Bravo",
    "Raquel Soto","Santiago Ramos","Teresa Aguilar","Ulises Mora",
    "Valentina Reyes","Wendy Cabrera","Xavier Flores","Yolanda Peña",
    # Operators (24–35)
    "Zoe Guerrero","Arturo Medina","Beatriz Ortega","César Navarro",
    "Daniela Rojas","Emilio Guzmán","Fabiola Torres","Gilberto Ángel",
    "Hana Cervantes","Iván Paredes","Julia Herrera","Kevin Blanco",
    # Visionaries (36–47)
    "Laura Mendoza","Marco Ruiz","Nora Vega","Pablo Jiménez",
    "Quintina Luna","Rodrigo Díaz","Sofía Romero","Tomás Acosta",
    "Ursula Ramírez","Víctor Cortés","Wendy Morales","Ximena López",
    # Specialists (48–59)
    "Yael Sandoval","Zaira Contreras","Abel Hidalgo","Bárbara Esquivel",
    "Claudio Treviño","Dora Alvarado","Ernesto Bautista","Fanny Campos",
    "Gonzalo Ponce","Hortensia Meza","Ignacio Solís","Jimena Barrera",
]

MENTOR_SECTORS = [
    "DeepTech","SaaS B2B","Fintech","HealthTech","DeepTech","SaaS B2B",
    "EdTech","IoT","DeepTech","SaaS B2B","CyberSec","Fintech",
    "E-commerce","Consumer App","Marketplace","D2C","E-commerce","Consumer App",
    "Creator Economy","Marketplace","Social Media","D2C","Consumer App","Marketplace",
    "Fintech","Legal Tech","Fintech","Accounting","Legal Tech","Fintech",
    "Real Estate","Fintech","Legal Tech","Private Equity","Fintech","Legal Tech",
    "ClimaTech","AgriTech","ClimaTech","VC / Investing","Sustainability","VC / Investing",
    "AgriTech","ClimaTech","VC / Investing","Sustainability","AgriTech","ClimaTech",
    "BioTech","BioTech","NanoTech","SpaceTech","BioTech","NanoTech",
    "SpaceTech","BioTech","NanoTech","SpaceTech","BioTech","NanoTech",
]

MENTOR_STAGES = [
    "Series A","Series B","Seed","Series A","Series B","Series A",
    "Seed","Series B","Series A","Series B","Seed","Series A",
    "Growth","Series A","Growth","Seed","Series A","Growth",
    "Seed","Series A","Growth","Seed","Series A","Growth",
    "Series B","Series A","Series B","Series A","Series B","Series A",
    "Growth","Series B","Series A","Series B","Series A","Series B",
    "Series B","Growth","Series B","Growth","Series B","Growth",
    "Series B","Growth","Series B","Growth","Series B","Growth",
    "Pre-seed","Seed","Pre-seed","Seed","Pre-seed","Seed",
    "Pre-seed","Seed","Pre-seed","Seed","Pre-seed","Seed",
]

# ── Skill matrix with archetype biases  [Tech, Mktg, Legal, Finance, Strategy]
rng = np.random.default_rng(42)
N = 60
MENTOR_MATRIX = rng.integers(3, 8, size=(N, 5)).astype(float)

boosts = {
    0: [3, 0, 0, 0, 2],
    1: [0, 3, 0, 0, 2],
    2: [0, 0, 3, 3, 0],
    3: [1, 1, 1, 1, 3],
    4: [2, 0, 0, 0, 0],
}
archetype_ranges = {0: range(0,12), 1: range(12,24), 2: range(24,36),
                    3: range(36,48), 4: range(48,60)}

for archetype, rows in archetype_ranges.items():
    for col, boost in enumerate(boosts[archetype]):
        if boost:
            MENTOR_MATRIX[list(rows), col] += rng.integers(1, boost + 1, size=12)

MENTOR_MATRIX = np.clip(MENTOR_MATRIX, 1, 10)
FEATURES = ["Tech", "Marketing", "Legal", "Finance", "Strategy"]


class FounderProfile(BaseModel):
    tech: float
    marketing: float
    legal: float
    finance: float
    strategy: float
    n_clusters: int = 5


# ── Helpers ───────────────────────────────────────────────────────────────────
ARCHETYPE_PER_MENTOR = [i // 12 for i in range(N)]


def resolve_cluster_names(cluster_labels, k):
    """Map KMeans cluster IDs to archetype names by majority vote."""
    name_map = {}
    desc_map = {}
    for c in range(k):
        members = [ARCHETYPE_PER_MENTOR[i]
                   for i, lbl in enumerate(cluster_labels) if lbl == c]
        dominant = max(set(members), key=members.count) if members else 0
        name_map[c] = CLUSTER_NAMES.get(dominant, f"Cluster {c+1}")
        desc_map[c] = CLUSTER_DESCRIPTIONS.get(dominant, "")
    return name_map, desc_map


# ── Endpoint ──────────────────────────────────────────────────────────────────
@app.post("/match")
def match_founder(founder: FounderProfile):
    founder_vec = np.array([
        founder.tech, founder.marketing,
        founder.legal, founder.finance, founder.strategy,
    ])

    all_data = np.vstack([MENTOR_MATRIX, founder_vec])
    scaler = StandardScaler()
    scaled = scaler.fit_transform(all_data)

    pca = PCA(n_components=2, random_state=42)
    coords_2d = pca.fit_transform(scaled)

    mentor_coords = coords_2d[:N]
    founder_coord = coords_2d[N]

    k = min(founder.n_clusters, N)
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(scaled[:N])
    cluster_labels = km.labels_.tolist()

    cluster_name_map, cluster_desc_map = resolve_cluster_names(cluster_labels, k)

    distances = np.linalg.norm(mentor_coords - founder_coord, axis=1)
    best_idx  = int(np.argmin(distances))
    top3_idx  = np.argsort(distances)[:3].tolist()

    mentors_payload = []
    for i in range(N):
        c = cluster_labels[i]
        archetype_id = ARCHETYPE_PER_MENTOR[i]          # fixed, based on dataset design
        mentors_payload.append({
            "id": i,
            "name": MENTOR_NAMES[i],
            "sector": MENTOR_SECTORS[i],
            "stage": MENTOR_STAGES[i],
            "x": float(mentor_coords[i, 0]),
            "y": float(mentor_coords[i, 1]),
            "cluster": c,
            "cluster_name": cluster_name_map[c],
            "archetype": archetype_id,                   # 0‒4, always stable
            "archetype_name": CLUSTER_NAMES[archetype_id],
            "distance": float(distances[i]),
            "scores": {f: float(MENTOR_MATRIX[i, j]) for j, f in enumerate(FEATURES)},
        })

    explained = [round(float(v) * 100, 1) for v in pca.explained_variance_ratio_]

    return {
        "mentors": mentors_payload,
        "founder": {
            "x": float(founder_coord[0]),
            "y": float(founder_coord[1]),
            "scores": {f: float(founder_vec[j]) for j, f in enumerate(FEATURES)},
        },
        "best_match_idx": best_idx,
        "top3_idx": top3_idx,
        "explained_variance": explained,
        "n_clusters": k,
        "cluster_names": cluster_name_map,
        "cluster_descriptions": cluster_desc_map,
        "feature_names": FEATURES,
        "n_mentors": N,
    }


@app.get("/health")
def health():
    return {"status": "ok", "service": "EPIC Lab Mentor Matcher", "n_mentors": N}
