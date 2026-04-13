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

# ── Mentor database (150 mentors, 30 per archetype) ──────────────────────────
MENTOR_NAMES = [
    # Builders (0–29) — Tech + Product
    "Alejandro Ríos","Carolina Fuentes","Diego Salinas","Elena Vargas",
    "Fernanda Ibáñez","Gerardo Ochoa","Héctor Palma","Irene Castañeda",
    "Jorge Montes","Karen Zúñiga","Luis Espinoza","Mónica Prado",
    "Nicolás Herrera","Olivia Castillo","Pedro Aguilar","Renata Solis",
    "Samuel Lara","Tamara Ibarra","Uriel Pedraza","Verónica Ángel",
    "Axel Romero","Brenda Quiroga","Cristóbal Peña","Dafne Lozano",
    "Esteban Varela","Flor Aguirre","Gonzalo Reyes","Ingrid Mora",
    "Julio Pacheco","Katia Estrada",
    # Connectors (30–59) — Marketing + Growth
    "Natalia Serrano","Omar Delgado","Patricia Leal","Quentin Bravo",
    "Raquel Soto","Santiago Ramos","Teresa Aguilar","Ulises Mora",
    "Valentina Reyes","Wendy Cabrera","Xavier Flores","Yolanda Peña",
    "Adriana Vega","Bruno Salazar","Claudia Nava","Daniel Esqueda",
    "Estefanía Ruiz","Felipe Montoya","Gisela Paredes","Hugo Téllez",
    "Ilse Fuentes","Javier Cordero","Karla Bustamante","León Prieto",
    "Marisol Tapia","Noel Barrios","Ofelia Cano","Patricio Leal",
    "Querida Sosa","Rodrigo Mena",
    # Operators (60–89) — Finance + Legal
    "Zoe Guerrero","Arturo Medina","Beatriz Ortega","César Navarro",
    "Daniela Rojas","Emilio Guzmán","Fabiola Torres","Gilberto Ángel",
    "Hana Cervantes","Iván Paredes","Julia Herrera","Kevin Blanco",
    "Lorena Fuentes","Mauricio Rivas","Norma Espinoza","Octavio Leiva",
    "Pilar Contreras","Quintín Aranda","Rosa Villanueva","Sergio Ponce",
    "Talia Bravo","Ulises Campos","Valeria Nieto","Wilfrido Salinas",
    "Xochitl Pedraza","Yésica Montiel","Zenón Aguirre","Amalia Cruz",
    "Benjamín Olvera","Carmen Duarte",
    # Visionaries (90–119) — Strategy + Leadership
    "Laura Mendoza","Marco Ruiz","Nora Vega","Pablo Jiménez",
    "Quintina Luna","Rodrigo Díaz","Sofía Romero","Tomás Acosta",
    "Ursula Ramírez","Víctor Cortés","Wendy Morales","Ximena López",
    "Andrés Peñaloza","Blanca Treviño","Carlos Alarcón","Diana Buendía",
    "Eduardo Saavedra","Francisca Olea","Gustavo Naranjo","Helena Quiroz",
    "Itzel Cabrera","Joaquín Espino","Kenji Watanabe","Lorenza Palma",
    "Mateo Ibarra","Nicolette Vidal","Osvaldo Ferrán","Pamela Ugarte",
    "Renato Solano","Sabrina Meza",
    # Specialists (120–149) — Deep Domain Experts
    "Yael Sandoval","Zaira Contreras","Abel Hidalgo","Bárbara Esquivel",
    "Claudio Treviño","Dora Alvarado","Ernesto Bautista","Fanny Campos",
    "Gonzalo Ponce","Hortensia Meza","Ignacio Solís","Jimena Barrera",
    "Karina Velasco","Leonardo Ibáñez","Margarita Flores","Néstor Gutiérrez",
    "Olga Serrano","Rafael Zamora","Silvia Acosta","Tania Mendívil",
    "Ulises Parra","Verónica Salcedo","Walther Núñez","Ximena Bernal",
    "Yosef Mizrahi","Zulema Arce","Armando Cisneros","Belén Orozco",
    "Ciro Valdés","Deborah Esparza",
]

MENTOR_SECTORS = [
    # Builders (30)
    "DeepTech","SaaS B2B","Fintech","HealthTech","DeepTech","SaaS B2B",
    "EdTech","IoT","DeepTech","SaaS B2B","CyberSec","Fintech",
    "AI/ML","Robotics","SaaS B2B","DeepTech","HealthTech","EdTech","CyberSec","IoT",
    "AI/ML","SaaS B2B","DeepTech","HealthTech","Robotics","CyberSec",
    "IoT","Fintech","EdTech","DeepTech",
    # Connectors (30)
    "E-commerce","Consumer App","Marketplace","D2C","E-commerce","Consumer App",
    "Creator Economy","Marketplace","Social Media","D2C","Consumer App","Marketplace",
    "Influencer Mktg","Brand Strategy","D2C","Consumer App","E-commerce","Social Media",
    "Community","Growth Hacking",
    "Affiliate Mktg","Retention","Performance Mktg","D2C","Marketplace","Creator Economy",
    "Social Media","Brand Strategy","E-commerce","Consumer App",
    # Operators (30)
    "Fintech","Legal Tech","Fintech","Accounting","Legal Tech","Fintech",
    "Real Estate","Fintech","Legal Tech","Private Equity","Fintech","Legal Tech",
    "CFO Advisory","Compliance","Tax & Audit","Fintech","Legal Tech","Private Equity",
    "Accounting","Real Estate",
    "M&A Advisory","Venture Debt","Legal Tech","Fintech","Compliance",
    "Real Estate","Accounting","Private Equity","CFO Advisory","Legal Tech",
    # Visionaries (30)
    "ClimaTech","AgriTech","ClimaTech","VC / Investing","Sustainability","VC / Investing",
    "AgriTech","ClimaTech","VC / Investing","Sustainability","AgriTech","ClimaTech",
    "Future of Work","Smart Cities","VC / Investing","Sustainability","ClimaTech",
    "AgriTech","Blue Economy","GovTech",
    "Impact Investing","Circular Economy","VC / Investing","ClimaTech","Smart Cities",
    "Sustainability","Future of Work","AgriTech","GovTech","Blue Economy",
    # Specialists (30)
    "BioTech","BioTech","NanoTech","SpaceTech","BioTech","NanoTech",
    "SpaceTech","BioTech","NanoTech","SpaceTech","BioTech","NanoTech",
    "Quantum Computing","Genomics","Materials Science","BioTech","SpaceTech",
    "NanoTech","Synthetic Biology","Photonics",
    "Neuroscience","Proteomics","SpaceTech","Quantum Computing","BioTech",
    "NanoTech","Materials Science","Genomics","Photonics","Synthetic Biology",
]

MENTOR_STAGES = [
    # Builders (30)
    "Series A","Series B","Seed","Series A","Series B","Series A",
    "Seed","Series B","Series A","Series B","Seed","Series A",
    "Growth","Series B","Seed","Series A","Series B","Growth","Seed","Series A",
    "Series A","Seed","Series B","Growth","Series A","Seed",
    "Series B","Series A","Growth","Seed",
    # Connectors (30)
    "Growth","Series A","Growth","Seed","Series A","Growth",
    "Seed","Series A","Growth","Seed","Series A","Growth",
    "Series B","Growth","Seed","Series A","Growth","Series B","Seed","Series A",
    "Growth","Seed","Series A","Series B","Growth","Seed",
    "Series A","Growth","Series B","Seed",
    # Operators (30)
    "Series B","Series A","Series B","Series A","Series B","Series A",
    "Growth","Series B","Series A","Series B","Series A","Series B",
    "Growth","Series A","Series B","Growth","Series A","Series B","Growth","Series A",
    "Series B","Growth","Series A","Series B","Growth",
    "Series A","Series B","Growth","Series A","Series B",
    # Visionaries (30)
    "Series B","Growth","Series B","Growth","Series B","Growth",
    "Series B","Growth","Series B","Growth","Series B","Growth",
    "Series A","Series B","Growth","Series B","Growth","Series A","Series B","Growth",
    "Series B","Growth","Series A","Growth","Series B",
    "Growth","Series A","Series B","Growth","Series B",
    # Specialists (30)
    "Pre-seed","Seed","Pre-seed","Seed","Pre-seed","Seed",
    "Pre-seed","Seed","Pre-seed","Seed","Pre-seed","Seed",
    "Series A","Pre-seed","Seed","Pre-seed","Seed","Series A","Pre-seed","Seed",
    "Pre-seed","Seed","Series A","Pre-seed","Seed",
    "Pre-seed","Seed","Series A","Pre-seed","Seed",
]

# ── Skill matrix — strong archetype separation so PCA/KMeans cluster cleanly ──
rng = np.random.default_rng(42)
N = 150

ARCHETYPE_CENTERS = {
    0: [8, 3, 3, 3, 6],   # Builders   — high Tech, moderate Strategy
    1: [3, 8, 3, 3, 6],   # Connectors — high Marketing, moderate Strategy
    2: [3, 3, 8, 8, 3],   # Operators  — high Legal & Finance
    3: [5, 5, 5, 5, 8],   # Visionaries— high Strategy, balanced rest
    4: [7, 3, 3, 3, 3],   # Specialists— high Tech, lower everything else
}
archetype_ranges = {0: range(0,30), 1: range(30,60), 2: range(60,90),
                    3: range(90,120), 4: range(120,150)}

MENTOR_MATRIX = np.zeros((N, 5))
for archetype, rows in archetype_ranges.items():
    center = np.array(ARCHETYPE_CENTERS[archetype], dtype=float)
    for i in list(rows):
        noise = rng.uniform(-2.0, 2.0, size=5)
        MENTOR_MATRIX[i] = np.clip(center + noise, 1, 10)

MENTOR_MATRIX = MENTOR_MATRIX.astype(float)
FEATURES = ["Tech", "Marketing", "Legal", "Finance", "Strategy"]


class FounderProfile(BaseModel):
    tech: float
    marketing: float
    legal: float
    finance: float
    strategy: float
    n_clusters: int = 5


# ── Helpers ───────────────────────────────────────────────────────────────────
ARCHETYPE_PER_MENTOR = [i // 30 for i in range(N)]


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

    # ── Matching: complementary within a PCA neighborhood ────────────────────
    # Step 1: compute PCA distances and keep top 40% closest mentors (neighborhood)
    # Step 2: within that pool, find who best fills the founder's skill gaps
    #
    # This guarantees the match is visually close on the scatter AND complementary.

    pca_dist = np.linalg.norm(mentor_coords - founder_coord, axis=1)

    # Neighborhood = closest 40 mentors by PCA distance (40% of 100)
    neighborhood_size = max(20, N // 3)
    neighborhood_idx  = np.argsort(pca_dist)[:neighborhood_size]

    # Complementarity target: where founder is weak, mentor should be strong
    complement_target = 10.0 - founder_vec

    # Among neighborhood, find most complementary
    comp_dist_all = np.linalg.norm(MENTOR_MATRIX - complement_target, axis=1)
    comp_dist_neighborhood = comp_dist_all[neighborhood_idx]
    best_local = int(np.argmin(comp_dist_neighborhood))
    best_idx   = int(neighborhood_idx[best_local])
    top3_idx   = [int(neighborhood_idx[i])
                  for i in np.argsort(comp_dist_neighborhood)[:3]]

    # ── Confidence ellipses per K-Means cluster (2-sigma) ────────────────────
    ellipses = []
    for c in range(k):
        pts = mentor_coords[np.array(cluster_labels) == c]
        if len(pts) < 3:
            continue
        mu  = pts.mean(axis=0)
        cov = np.cov(pts.T)
        # eigen decomposition → semi-axes and angle
        vals, vecs = np.linalg.eigh(cov)
        vals = np.abs(vals)
        order = np.argsort(vals)[::-1]
        vals, vecs = vals[order], vecs[:, order]
        # 2-sigma scale (≈95% of points)
        a, b  = 2 * np.sqrt(vals[0]), 2 * np.sqrt(vals[1])
        angle = float(np.degrees(np.arctan2(vecs[1, 0], vecs[0, 0])))
        # parametric ellipse path (100 pts)
        t   = np.linspace(0, 2 * np.pi, 100)
        ex  = a * np.cos(t)
        ey  = b * np.sin(t)
        ca, sa = np.cos(np.radians(angle)), np.sin(np.radians(angle))
        rx  = (ca * ex - sa * ey + mu[0]).tolist()
        ry  = (sa * ex + ca * ey + mu[1]).tolist()
        ellipses.append({
            "cluster": c,
            "cluster_name": cluster_name_map[c],
            "x": rx, "y": ry,
            "cx": float(mu[0]), "cy": float(mu[1]),
        })

    mentors_payload = []
    for i in range(N):
        c = cluster_labels[i]
        archetype_id = ARCHETYPE_PER_MENTOR[i]
        mentors_payload.append({
            "id": i,
            "name": MENTOR_NAMES[i],
            "sector": MENTOR_SECTORS[i],
            "stage": MENTOR_STAGES[i],
            "x": float(mentor_coords[i, 0]),
            "y": float(mentor_coords[i, 1]),
            "cluster": c,
            "cluster_name": cluster_name_map[c],
            "archetype": archetype_id,
            "archetype_name": CLUSTER_NAMES[archetype_id],
            "distance": float(comp_dist_all[i]),      # complementarity score
            "pca_distance": float(pca_dist[i]),       # PCA distance for scatter
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
        "ellipses": ellipses,
        "feature_names": FEATURES,
        "n_mentors": N,
    }


@app.get("/health")
def health():
    return {"status": "ok", "service": "EPIC Lab Mentor Matcher", "n_mentors": N}
