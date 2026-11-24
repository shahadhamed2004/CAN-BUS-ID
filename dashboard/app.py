import streamlit as st
import pandas as pd
import joblib
import streamlit.components.v1 as components

from pathlib import Path

# ==================================================
# 1. PROJECT PATHS
# ==================================================

PROJECT_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = PROJECT_DIR / "results"
MODELS_DIR = PROJECT_DIR / "models"

FEATURE_COLUMNS = [
    "CAN_ID", "DLC", "Byte_0", "Byte_1", "Byte_2",
    "Byte_3", "Byte_4", "Byte_5", "Byte_6", "Byte_7"
]

DEVELOPER = "Shahad Hamed Majeed"

# ==================================================
# 2. PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="CAN-BUS IDS | Automotive Security",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# 3. AUTOMOTIVE DARK DESIGN
# ==================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
:root {
    --bg: #111B28; --panel: #1A293A; --panel2: #22364B;
    --blue: #38A7FF; --cyan: #45D9F2; --orange: #FF9B54;
    --green: #45D6A0; --text: #F4F8FC; --muted: #B2C2D2;
    --border: #344B63;
}
.stApp { background: radial-gradient(ellipse at 75% 0%, #20364B 0%, #111B28 55%); color:var(--text); font-family:'Inter',sans-serif; }
.main .block-container { padding-top:1.5rem; padding-bottom:3rem; max-width:1500px; }
[data-testid="stSidebar"] { background:linear-gradient(180deg,#1B2B3D,#142131); border-right:1px solid #3B536B; }
[data-testid="stSidebar"] * { color:var(--text); }
h1,h2,h3,h4 { color:#F7FAFF !important; font-family:'Inter',sans-serif !important; font-weight:800 !important; }
p,label,.stMarkdown { color:#C1CEDB; }
[data-testid="stMetric"] { background:linear-gradient(145deg,#263D53,#1A2A3B); border:1px solid #405B75; border-radius:16px; padding:20px; box-shadow:0 8px 24px rgba(0,0,0,.14); transition:.2s ease; }
[data-testid="stMetric"]:hover { border-color:var(--cyan); transform:translateY(-3px); }
[data-testid="stMetricLabel"] { color:#B9CAD9 !important; }
[data-testid="stMetricValue"] { color:#FFFFFF !important; font-weight:800 !important; }
.stButton>button { background:linear-gradient(90deg,#147FD1,#36AEFF); color:white !important; border:1px solid #54B9FF; border-radius:10px; padding:10px 22px; font-weight:700; box-shadow:0 5px 18px rgba(38,155,255,.18); }
.stButton>button:hover { background:linear-gradient(90deg,#269BFF,#55D6F0); border-color:#8AEAFF; }
.stDownloadButton>button { background:#20384F; color:#8AD7FF !important; border:1px solid #4A88B7; border-radius:10px; }
.stTextInput input,.stSelectbox div[data-baseweb="select"],.stFileUploader section { background:#1C2D40 !important; color:white !important; border-color:#49627B !important; border-radius:10px !important; }
[data-testid="stDataFrame"] { border:1px solid var(--border); border-radius:12px; overflow:hidden; }
[data-testid="stAlert"] { border-radius:12px; border:1px solid var(--border); }
hr { border-color:#3A5067 !important; }
[data-testid="stSidebar"] [role="radiogroup"] { gap:8px; }
[data-testid="stSidebar"] [role="radio"] { background:#203247; border:1px solid #354D65; border-radius:10px; padding:9px; }
.custom-card { background:linear-gradient(145deg,#263D53,#1A2A3B); border:1px solid #405B75; border-radius:16px; padding:22px; min-height:145px; box-shadow:0 8px 22px rgba(0,0,0,.12); }
.custom-card h3 { color:#FFFFFF !important; margin-bottom:8px; }
.custom-card p { color:#BDCCDA; font-size:14px; }
.eyebrow { color:#54DDF2; font-size:11px; font-weight:800; letter-spacing:2px; }
.hero-title { font-size:clamp(27px,4vw,43px); font-weight:900; color:#FFFFFF; line-height:1.12; text-shadow:0 4px 20px rgba(0,0,0,.2); }
.hero-subtitle { color:#C3D2E0; font-size:15px; margin-top:12px; }
.hero-credit { color:#65C8FF; font-size:12px; font-weight:700; margin-top:25px; }
.status-label { color:#75E6FF; background:rgba(38,155,255,.14); border:1px solid rgba(69,217,242,.4); padding:8px 13px; border-radius:20px; font-size:11px; font-weight:800; display:inline-block; }
.small-muted { color:#A8BACB; font-size:12px; }
</style>
""", unsafe_allow_html=True)

# ==================================================
# 4. ANIMATED 3D AUTOMOTIVE SCENE
# ==================================================

THREE_D_SCENE = r"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
html,body{margin:0;width:100%;height:100%;overflow:hidden;background:transparent}
#scene{width:100%;height:370px;border-radius:20px;overflow:hidden;position:relative;background:radial-gradient(ellipse at 50% 45%,#294966 0%,#172A3D 55%,#132131 100%);border:1px solid rgba(111,190,235,.28);box-shadow:0 18px 45px rgba(0,0,0,.22)}
#scene canvas{display:block;width:100%;height:100%}
.hud{position:absolute;z-index:2;left:18px;top:16px;color:#BCEEFF;font:700 10px Inter,Arial;letter-spacing:2px;text-shadow:0 0 12px #159bdc;pointer-events:none}
.hud span{display:block;color:#FFFFFF;font-size:16px;letter-spacing:1px;margin-top:6px}
.hud-right{position:absolute;right:17px;bottom:16px;color:#8FE8FF;font:600 10px Inter,Arial;letter-spacing:1.4px;text-align:right;pointer-events:none}
.pulse{display:inline-block;width:7px;height:7px;border-radius:50%;background:#4DE2B1;box-shadow:0 0 12px #4DE2B1;margin-right:6px}
</style>
</head>
<body>
<div id="scene">
 <div class="hud">AUTOMOTIVE CYBERSECURITY<span>3D VEHICLE SIMULATION</span></div>
 <div class="hud-right"><span class="pulse"></span>SYSTEM ONLINE<br>CAN NETWORK VISUALIZATION</div>
</div>
<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
<script>
(function(){
 const host=document.getElementById('scene');
 if(!window.THREE){host.innerHTML+='<div style="padding:130px 20px;text-align:center;color:#fff;font:600 14px Arial">3D preview needs an internet connection to load.</div>';return;}
 const scene=new THREE.Scene();
 scene.fog=new THREE.Fog(0x172a3d,12,42);
 const camera=new THREE.PerspectiveCamera(42,host.clientWidth/host.clientHeight,.1,100);
 camera.position.set(5.8,4.0,8.8); camera.lookAt(0,.6,-1.5);
 const renderer=new THREE.WebGLRenderer({antialias:true,alpha:true});
 renderer.setPixelRatio(Math.min(window.devicePixelRatio||1,2));
 renderer.setSize(host.clientWidth,host.clientHeight);
 renderer.shadowMap.enabled=true; renderer.shadowMap.type=THREE.PCFSoftShadowMap;
 renderer.outputColorSpace=THREE.SRGBColorSpace;
 host.appendChild(renderer.domElement);
 scene.add(new THREE.HemisphereLight(0xb9e8ff,0x172234,2.0));
 const key=new THREE.DirectionalLight(0xffffff,3.0); key.position.set(4,8,5); key.castShadow=true; scene.add(key);
 const blueLight=new THREE.PointLight(0x16aaff,24,13); blueLight.position.set(-3,2,1); scene.add(blueLight);
 const orangeLight=new THREE.PointLight(0xff8b45,12,10); orangeLight.position.set(3,1,-4); scene.add(orangeLight);
 // Road platform and luminous lane lines
 const road=new THREE.Mesh(new THREE.PlaneGeometry(12,60),new THREE.MeshStandardMaterial({color:0x172638,metalness:.55,roughness:.42}));
 road.rotation.x=-Math.PI/2; road.position.y=-.03; road.position.z=-12; road.receiveShadow=true; scene.add(road);
 const grid=new THREE.GridHelper(12,24,0x238ec4,0x29445b); grid.position.y=.015; grid.position.z=-10; scene.add(grid);
 const laneMat=new THREE.MeshBasicMaterial({color:0x42d9ff});
 const dashes=[];
 for(let z=-29;z<7;z+=4){const dash=new THREE.Mesh(new THREE.BoxGeometry(.055,.025,1.65),laneMat);dash.position.set(0,.025,z);scene.add(dash);dashes.push(dash);}
 // Build a sporty 3D coupe from meshes
 const car=new THREE.Group(); scene.add(car); car.position.set(0,.32,0);
 const paint=new THREE.MeshStandardMaterial({color:0x168fe0,metalness:.82,roughness:.22});
 const glass=new THREE.MeshStandardMaterial({color:0x142d43,metalness:.55,roughness:.12,transparent:true,opacity:.94});
 const dark=new THREE.MeshStandardMaterial({color:0x101923,metalness:.65,roughness:.35});
 const trim=new THREE.MeshStandardMaterial({color:0x5be6ff,emissive:0x087da8,emissiveIntensity:1.8,metalness:.5,roughness:.25});
 const body=new THREE.Mesh(new THREE.BoxGeometry(2.25,.55,4.25),paint); body.position.y=.62; body.castShadow=true; car.add(body);
 const hood=new THREE.Mesh(new THREE.BoxGeometry(2.12,.22,1.05),paint); hood.position.set(0,.94,-1.48); hood.castShadow=true; car.add(hood);
 const cabin=new THREE.Mesh(new THREE.BoxGeometry(1.72,.72,1.9),glass); cabin.position.set(0,1.18,.05); cabin.castShadow=true; car.add(cabin);
 const roof=new THREE.Mesh(new THREE.BoxGeometry(1.76,.12,1.55),paint); roof.position.set(0,1.58,.05); car.add(roof);
 // front and rear bumpers
 const bumper1=new THREE.Mesh(new THREE.BoxGeometry(2.3,.18,.22),dark); bumper1.position.set(0,.43,-2.13); car.add(bumper1);
 const bumper2=bumper1.clone(); bumper2.position.z=2.13; car.add(bumper2);
 // Headlights and tail lamps
 for(const x of [-.78,.78]){
  const head=new THREE.Mesh(new THREE.BoxGeometry(.48,.10,.07),trim); head.position.set(x,.78,-2.15); car.add(head);
  const tail=new THREE.Mesh(new THREE.BoxGeometry(.48,.10,.07),new THREE.MeshBasicMaterial({color:0xff554d})); tail.position.set(x,.78,2.15); car.add(tail);
 }
 // wheels
 const wheels=[];
 for(const x of [-1.13,1.13]) for(const z of [-1.35,1.35]){
  const wheel=new THREE.Mesh(new THREE.CylinderGeometry(.43,.43,.24,32),dark); wheel.rotation.z=Math.PI/2; wheel.position.set(x,.43,z); wheel.castShadow=true; car.add(wheel); wheels.push(wheel);
  const hub=new THREE.Mesh(new THREE.CylinderGeometry(.19,.19,.255,24),new THREE.MeshStandardMaterial({color:0x7b9db8,metalness:.9,roughness:.2})); hub.rotation.z=Math.PI/2; hub.position.copy(wheel.position); car.add(hub);
 }
 // Floating network nodes around the vehicle
 const nodes=[];
 for(let i=0;i<13;i++){const a=i/13*Math.PI*2;const r=3.1+(i%3)*.35;const node=new THREE.Mesh(new THREE.SphereGeometry(.055,12,12),new THREE.MeshBasicMaterial({color:i%3===0?0xffa05c:0x52dcff}));node.position.set(Math.cos(a)*r,.7+(i%4)*.42,-1+Math.sin(a)*r);scene.add(node);nodes.push({mesh:node,phase:i});}
 const ring=new THREE.Mesh(new THREE.TorusGeometry(3.0,.012,8,100),new THREE.MeshBasicMaterial({color:0x238ec4,transparent:true,opacity:.65}));ring.rotation.x=Math.PI/2;ring.position.y=.04;ring.position.z=-.2;scene.add(ring);
 let t=0;
 function animate(){requestAnimationFrame(animate);t+=.012;
  car.position.z=Math.sin(t*.7)*.22; car.position.y=.32+Math.sin(t*2.1)*.025; car.rotation.y=Math.sin(t*.55)*.045;
  wheels.forEach(w=>w.rotation.x+=.09);
  dashes.forEach(d=>{d.position.z+=.105;if(d.position.z>7)d.position.z=-29;});
  nodes.forEach(n=>{n.mesh.position.y=.7+(n.phase%4)*.42+Math.sin(t*1.8+n.phase)*.12;});
  camera.position.x=5.8+Math.sin(t*.22)*.35; camera.lookAt(0,.7,-1.3);
  renderer.render(scene,camera);
 }
 animate();
 const resize=new ResizeObserver(()=>{const w=host.clientWidth,h=host.clientHeight;camera.aspect=w/h;camera.updateProjectionMatrix();renderer.setSize(w,h);});resize.observe(host);
})();
</script>
</body>
</html>
"""

# ==================================================
# 5. SIDEBAR NAVIGATION
# ==================================================

with st.sidebar:

    st.markdown(
        """
        <div style="padding: 10px 0 20px 0;">
            <div style="font-size:25px; font-weight:800; color:#FFFFFF;">
                <span style="color:#269BFF;">◆</span> CAN-BUS IDS
            </div>
            <div style="color:#39C6E8; font-size:10px;
                        letter-spacing:2px; font-weight:700;">
                AUTOMOTIVE SECURITY
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown(
        '<p class="eyebrow">MAIN NAVIGATION</p>',
        unsafe_allow_html=True
    )

    page = st.radio(
        "MAIN MENU",
        ["Overview", "Detection", "Model Evaluation", "About Project"],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown(
        '<p class="eyebrow">PROJECT STATUS</p>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="custom-card" style="min-height:90px; padding:14px;">
            <span style="color:#39C995;">●</span>
            <b style="color:#FFFFFF;"> Dashboard Ready</b>
            <p style="margin:7px 0 0 0;">Offline analysis environment</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")
    st.caption("CAN-BUS-IDS | Research Prototype")
    st.caption("Designed & Developed by")
    st.markdown(
        f"<p style='color:#39A9FF; font-size:12px; font-weight:600;'>{DEVELOPER}</p>",
        unsafe_allow_html=True
    )

# ==================================================
# 6. MAIN HERO HEADER
# ==================================================

left, right = st.columns([0.95, 1.15], vertical_alignment="center")

with left:
    st.markdown(
        """
        <div style="padding:18px 0;">
            <div class="eyebrow">
                AUTOMOTIVE • ARTIFICIAL INTELLIGENCE • SECURITY
            </div>
            <div class="hero-title" style="margin-top:14px;">
                CAN-BUS<br>INTRUSION DETECTION
            </div>
            <div class="hero-subtitle">
                Machine Learning-Based Security for
                Automotive CAN Networks
            </div>
            <div style="margin-top:22px;">
                <span class="status-label">● OFFLINE ANALYSIS MODE</span>
            </div>
            <div class="hero-credit">
                Designed & Developed by Shahad Hamed Majeed
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with right:
    components.html(
        THREE_D_SCENE,
        height=390,
        scrolling=False
    )

st.divider()

# ==================================================
# 7. OVERVIEW PAGE
# ==================================================

if page == "Overview":

    st.header("Security Overview")
    st.write(
        "Explore dataset statistics, traffic distribution "
        "and machine learning components."
    )

    diversity_path = RESULTS_DIR / "feature_diversity.csv"

    if diversity_path.exists():

        diversity = pd.read_csv(diversity_path)

        required_diversity_columns = [
            "Total Records",
            "Label",
            "Unique Feature Combinations"
        ]

        missing_diversity_columns = [
            col for col in required_diversity_columns
            if col not in diversity.columns
        ]

        if missing_diversity_columns:
            st.error(
                "The feature_diversity.csv file is missing these columns: "
                + ", ".join(missing_diversity_columns)
            )
        else:
            total_records = int(diversity["Total Records"].sum())

            normal_records = int(
                diversity.loc[
                    diversity["Label"] == 0, "Total Records"
                ].sum()
            )

            attack_records = int(
                diversity.loc[
                    diversity["Label"] == 1, "Total Records"
                ].sum()
            )

            attack_rows = diversity.loc[diversity["Label"] == 1]
            attack_combinations = (
                int(attack_rows["Unique Feature Combinations"].sum())
                if not attack_rows.empty else 0
            )

            st.markdown(
                '<div class="eyebrow">DATASET INTELLIGENCE</div>',
                unsafe_allow_html=True
            )
            st.subheader("Dataset Statistics")

            col1, col2, col3 = st.columns(3)
            col1.metric("TOTAL RECORDS", f"{total_records:,}")
            col2.metric("NORMAL TRAFFIC", f"{normal_records:,}")
            col3.metric("ATTACK TRAFFIC", f"{attack_records:,}")

            st.divider()

            left_col, right_col = st.columns([1.2, 1])

            with left_col:
                st.subheader("Traffic Distribution")
                distribution = pd.DataFrame({
                    "Class": ["Normal", "Attack"],
                    "Records": [normal_records, attack_records]
                })
                st.bar_chart(
                    distribution.set_index("Class"),
                    color="#269BFF"
                )

            with right_col:
                st.subheader("Dataset Insights")
                attack_percentage = (
                    attack_records / total_records * 100
                    if total_records else 0
                )
                st.metric("Attack Traffic Share", f"{attack_percentage:.2f}%")
                st.metric(
                    "Unique Attack Combinations",
                    f"{attack_combinations:,}"
                )

    else:
        st.warning("Dataset information file was not found.")

    st.divider()
    st.markdown(
        '<div class="eyebrow">MACHINE LEARNING ENGINE</div>',
        unsafe_allow_html=True
    )
    st.subheader("Detection Models")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="custom-card">
                <div style="font-size:28px;color:#39A9FF;">◈</div>
                <h3>Decision Tree</h3>
                <p>
                    A tree-based classification model that learns
                    decision rules from data.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="custom-card">
                <div style="font-size:28px;color:#39C6E8;">◈</div>
                <h3>Random Forest</h3>
                <p>
                    An ensemble model combining multiple decision
                    trees for classification.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

# ==================================================
# 8. DETECTION PAGE
# ==================================================

elif page == "Detection":

    st.header("Intrusion Detection Center")
    st.write(
        "Upload CAN-BUS feature records and analyze them "
        "using a trained machine learning model."
    )

    st.markdown(
        '<div class="eyebrow">STEP 01 • MODEL CONFIGURATION</div>',
        unsafe_allow_html=True
    )

    model_choice = st.selectbox(
        "Select Machine Learning Model",
        ["Decision Tree", "Random Forest"]
    )

    st.divider()
    st.markdown(
        '<div class="eyebrow">STEP 02 • DATA INPUT</div>',
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Upload CAN-BUS CSV Dataset",
        type=["csv"]
    )

    if uploaded_file is not None:

        try:
            input_data = pd.read_csv(uploaded_file)

            missing_columns = [
                column for column in FEATURE_COLUMNS
                if column not in input_data.columns
            ]

            if missing_columns:
                st.error(
                    "Missing columns: " + ", ".join(missing_columns)
                )

            elif input_data.empty:
                st.error("The uploaded file is empty.")

            else:
                input_features = input_data[FEATURE_COLUMNS].copy()
                input_features = input_features.apply(
                    pd.to_numeric,
                    errors="coerce"
                )

                if input_features.isnull().any().any():
                    st.error(
                        "The file contains missing or invalid feature values."
                    )

                else:
                    st.success(
                        f"{len(input_features):,} records loaded successfully."
                    )

                    with st.expander("Preview uploaded records"):
                        st.dataframe(
                            input_features.head(10),
                            use_container_width=True
                        )

                    st.divider()
                    st.markdown(
                        '<div class="eyebrow">STEP 03 • RUN ANALYSIS</div>',
                        unsafe_allow_html=True
                    )

                    if st.button(
                        "▶  START INTRUSION DETECTION",
                        type="primary",
                        use_container_width=True
                    ):

                        model_filename = (
                            "decision_tree.pkl"
                            if model_choice == "Decision Tree"
                            else "random_forest.pkl"
                        )
                        model_path = MODELS_DIR / model_filename

                        if not model_path.exists():
                            st.error(f"Model file not found: {model_path}")
                        else:
                            model = joblib.load(model_path)
                            predictions = model.predict(input_features)

                            results = input_features.copy()
                            results["Prediction"] = [
                                "Attack" if value == 1 else "Normal"
                                for value in predictions
                            ]

                            attack_count = int((predictions == 1).sum())
                            normal_count = int((predictions == 0).sum())

                            st.divider()
                            st.subheader("Detection Results")

                            col1, col2 = st.columns(2)
                            col1.metric(
                                "NORMAL RECORDS",
                                f"{normal_count:,}"
                            )
                            col2.metric(
                                "ATTACK RECORDS",
                                f"{attack_count:,}"
                            )

                            if attack_count > 0:
                                st.warning(
                                    f"{attack_count:,} records were classified as Attack."
                                )
                            else:
                                st.success(
                                    "No records were classified as Attack."
                                )

                            st.subheader("Prediction Distribution")
                            chart_data = pd.DataFrame({
                                "Class": ["Normal", "Attack"],
                                "Records": [normal_count, attack_count]
                            })
                            st.bar_chart(
                                chart_data.set_index("Class"),
                                color="#269BFF"
                            )

                            st.subheader("Prediction Table")
                            st.dataframe(
                                results,
                                use_container_width=True
                            )

                            csv_data = results.to_csv(index=False).encode("utf-8")
                            st.download_button(
                                "Download Prediction Results",
                                data=csv_data,
                                file_name="detection_results.csv",
                                mime="text/csv"
                            )

        except Exception as error:
            st.error(f"An error occurred: {error}")

# ==================================================
# 9. MODEL EVALUATION PAGE
# ==================================================

elif page == "Model Evaluation":

    st.header("AI Model Performance")
    st.write(
        "Evaluation and comparison of the trained "
        "machine learning classifiers."
    )

    evaluation_path = RESULTS_DIR / "model_evaluation.csv"

    if evaluation_path.exists():

        evaluation = pd.read_csv(evaluation_path)
        st.subheader("Evaluation Metrics")
        st.dataframe(evaluation, use_container_width=True)

        metric_columns = [
            column for column in [
                "Accuracy", "Precision", "Recall", "F1-Score", "F1"
            ]
            if column in evaluation.columns
        ]

        if metric_columns and "Model" in evaluation.columns:
            st.subheader("Model Performance Comparison")
            st.bar_chart(
                evaluation.set_index("Model")[metric_columns],
                color="#269BFF"
            )

    else:
        st.warning("Model evaluation file was not found.")

    st.divider()
    st.markdown(
        '<div class="eyebrow">CLASSIFICATION PERFORMANCE</div>',
        unsafe_allow_html=True
    )
    st.subheader("Confusion Matrices")

    col1, col2 = st.columns(2)

    decision_tree_image = (
        RESULTS_DIR / "decision_tree_confusion_matrix.png"
    )
    random_forest_image = (
        RESULTS_DIR / "random_forest_confusion_matrix.png"
    )

    with col1:
        st.markdown("### Decision Tree")
        if decision_tree_image.exists():
            st.image(
                str(decision_tree_image),
                use_container_width=True
            )
        else:
            st.warning("Decision Tree image not found.")

    with col2:
        st.markdown("### Random Forest")
        if random_forest_image.exists():
            st.image(
                str(random_forest_image),
                use_container_width=True
            )
        else:
            st.warning("Random Forest image not found.")

# ==================================================
# 10. ABOUT PROJECT PAGE
# ==================================================

elif page == "About Project":

    st.header("About the Project")
    st.write(
        "The CAN-BUS Intrusion Detection System is a research "
        "prototype using machine learning to classify "
        "automotive CAN-BUS records."
    )

    st.divider()
    st.markdown(
        '<div class="eyebrow">PROJECT INFORMATION</div>',
        unsafe_allow_html=True
    )
    st.subheader("Technical Overview")

    st.markdown("""
    | Category | Information |
    |---|---|
    | Project Name | CAN-BUS-IDS |
    | Dataset | HCRL DoS Dataset |
    | Programming Language | Python |
    | Machine Learning Library | Scikit-learn |
    | Dashboard Framework | Streamlit |
    | Model 1 | Decision Tree |
    | Model 2 | Random Forest |
    """)

    st.divider()
    st.subheader("System Architecture")

    st.markdown(
        """
        <div class="custom-card">
            <div style="color:#39A9FF;font-weight:700;">CAN-BUS DATASET</div>
            <p>Input traffic records and features</p>
            <div style="color:#39A9FF;font-size:20px;">↓</div>
            <div style="color:#39A9FF;font-weight:700;">MACHINE LEARNING</div>
            <p>Decision Tree / Random Forest</p>
            <div style="color:#39A9FF;font-size:20px;">↓</div>
            <div style="color:#39C995;font-weight:700;">CLASSIFICATION</div>
            <p>Normal Traffic / Attack Traffic</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()
    st.subheader("Dataset Limitations")

    st.warning(
        "All 587,521 attack records in the current dataset have the same "
        "feature combination. Perfect evaluation results do not prove "
        "detection of previously unseen attack patterns."
    )

    st.info(
        "This dashboard performs offline CSV predictions. "
        "It does not provide live CAN-BUS monitoring."
    )

    st.divider()
    st.markdown(
        f"""
        <div class="custom-card">
            <div class="eyebrow">PROJECT DEVELOPER</div>
            <h2 style="color:#FFFFFF !important;">{DEVELOPER}</h2>
            <p>
                Designed &amp; Developed by
                <span style="color:#39A9FF;">{DEVELOPER}</span>
            </p>
            <p>
                Automotive Cybersecurity |
                Machine Learning |
                Intrusion Detection
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ==================================================
# 11. FOOTER
# ==================================================

st.divider()

st.markdown(
    f"""
    <div style="text-align:center;padding:12px 0;">
        <div style="color:#39A9FF;font-size:11px;
                    font-weight:700;letter-spacing:2px;">
            CAN-BUS IDS
        </div>
        <div style="color:#8798AA;font-size:11px;margin-top:7px;">
            Automotive Intrusion Detection Research Prototype
        </div>
        <div style="color:#AAB7C4;font-size:11px;margin-top:7px;">
            Designed &amp; Developed by {DEVELOPER}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)