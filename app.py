
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="SafeLabel & Allergen Shield - Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.0rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F3F4F6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1E3A8A;
    }
    .status-pass { color: #16A34A; font-weight: bold; }
    .status-caution { color: #D97706; font-weight: bold; }
    .status-fail { color: #DC2626; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# DATA LOADING
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    df_cleaning = pd.read_csv("nightly_3m_cleaning_logs.csv")
    df_schedule = pd.read_csv("production_sequencing_schedule.csv")
    df_ocr = pd.read_csv("ocr_label_inspections.csv")
    return df_cleaning, df_schedule, df_ocr

try:
    df_cleaning, df_schedule, df_ocr = load_data()
except Exception as e:
    st.error(f"Error cargando los archivos CSV: {e}")
    st.stop()

# -----------------------------------------------------------------------------
# SIDEBAR FILTERS
# -----------------------------------------------------------------------------
st.sidebar.image("https://img.icons8.com/color/96/shield-with-cross.png", width=64)
st.sidebar.title("Filtros de Planta")

available_dates = sorted(df_cleaning['date'].unique())
selected_date = st.sidebar.selectbox("📅 Seleccionar Fecha", available_dates, index=len(available_dates)-1)

available_rooms = sorted(df_cleaning['room_id'].unique())
selected_room = st.sidebar.selectbox("🏭 Seleccionar Sala / Línea", ["Todas"] + available_rooms)

# Filter datasets based on selection
if selected_room != "Todas":
    filtered_cleaning = df_cleaning[(df_cleaning['date'] == selected_date) & (df_cleaning['room_id'] == selected_room)]
    filtered_schedule = df_schedule[(df_schedule['date'] == selected_date) & (df_schedule['room_id'] == selected_room)]
else:
    filtered_cleaning = df_cleaning[df_cleaning['date'] == selected_date]
    filtered_schedule = df_schedule[df_schedule['date'] == selected_date]

filtered_ocr = df_ocr[df_ocr['batch_id'].isin(filtered_schedule['batch_id'])]

# -----------------------------------------------------------------------------
# MAIN HEADER
# -----------------------------------------------------------------------------
st.markdown('<div class="main-header">🛡️ SafeLabel & Allergen Shield</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Sistema Digital de Control de Alérgenos, Liberación Pre-operativa (3M Clean-Trace) e Inspección OCR</div>', unsafe_allow_html=True)

# Top Metrics Row
col1, col2, col3, col4 = st.columns(4)

total_batches = len(filtered_schedule)
atp_fails = len(filtered_cleaning[filtered_cleaning['atp_status_3m'] == 'FAIL'])
seq_warnings = len(filtered_schedule[filtered_schedule['requires_intermediate_cleaning'] == True])
ocr_fails = len(filtered_ocr[filtered_ocr['inspection_status'].str.startswith('FAIL')])

col1.metric("📦 Lotes Programados", total_batches)
col2.metric("🧪 Fallos ATP 3M (>300 RLU)", atp_fails, delta_color="inverse")
col3.metric("⚠️ Riesgos de Secuencia", seq_warnings, delta_color="inverse")
col4.metric("❌ Alertas OCR Etiquetado", ocr_fails, delta_color="inverse")

st.divider()

# -----------------------------------------------------------------------------
# NAVIGATION TABS
# -----------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "🌙 1. Liberación Pre-operativa (ATP 3M)", 
    "🔄 2. Secuenciación y Arrastre de Alérgenos", 
    "🔍 3. Auditoría OCR de Etiquetado"
])

# -----------------------------------------------------------------------------
# TAB 1: LIBERACIÓN PRE-OPERATIVA (ATP 3M CLEAN-TRACE)
# -----------------------------------------------------------------------------
with tab1:
    st.subheader("Control Higiénico Nocturno - Estándar 3M Clean-Trace")
    st.markdown("Auditoría de luminometría ATP realizada en el turno de noche previa al arranque de producción.")
    
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        # Distribution of ATP Status
        status_counts = filtered_cleaning['atp_status_3m'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']
        color_map = {'PASS': '#10B981', 'CAUTION': '#F59E0B', 'FAIL': '#EF4444'}
        
        fig_atp = px.pie(
            status_counts, 
            values='Count', 
            names='Status', 
            title="Distribución de Resultados 3M Clean-Trace",
            color='Status',
            color_discrete_map=color_map,
            hole=0.4
        )
        st.plotly_chart(fig_atp, use_container_width=True)
        
    with col_right:
        # RLU values by room
        fig_bar = px.bar(
            filtered_cleaning,
            x='room_id',
            y='atp_result_rlu',
            color='atp_status_3m',
            color_discrete_map=color_map,
            title="Lecturas RLU por Sala / Línea",
            labels={'atp_result_rlu': 'RLU (Relative Light Units)', 'room_id': 'Sala'},
            hover_data=['swab_point', 'chemical_agent', 'operator_id']
        )
        # Add 3M Threshold lines
        fig_bar.add_hline(y=150, line_dash="dash", line_color="orange", annotation_text="Límite Precaución (150 RLU)")
        fig_bar.add_hline(y=300, line_dash="dash", line_color="red", annotation_text="Límite Fallo (300 RLU)")
        st.plotly_chart(fig_bar, use_container_width=True)

    st.subheader("📋 Registro Detallado de Limpiezas Nocturnas")
    st.dataframe(
        filtered_cleaning[['cleaning_id', 'room_id', 'swab_point', 'chemical_agent', 'atp_result_rlu', 'atp_status_3m', 'operator_id']],
        use_container_width=True
    )

# -----------------------------------------------------------------------------
# TAB 2: SECUENCIACIÓN Y ARRASTRE DE ALÉRGENOS
# -----------------------------------------------------------------------------
with tab2:
    st.subheader("Matriz de Secuenciación Diaria y Arrastre de Alérgenos (*Carry-Over*)")
    st.markdown("""
    Regla operativa: La producción se programa de **menor a mayor número de alérgenos** sin limpiezas intermedias. 
    Si un lote requiere eliminar alérgenos activos de la máquina, se marca como **Riesgo de Secuencia**.
    """)
    
    if len(filtered_schedule) == 0:
        st.info("No hay lotes programados para la selección actual.")
    else:
        # Display schedule table with status highlights
        for room in filtered_schedule['room_id'].unique():
            st.markdown(f"#### 🏭 Línea: `{room}`")
            room_schedule = filtered_schedule[filtered_schedule['room_id'] == room].sort_values('sequence_order')
            
            for _, row in room_schedule.iterrows():
                card_border = "#EF4444" if row['requires_intermediate_cleaning'] else "#10B981"
                bg_color = "#FEF2F2" if row['requires_intermediate_cleaning'] else "#F0FDF4"
                
                status_badge = "🔴 REQUIERE LIMPIEZA INTERMEDIA (Secuencia Inválida)" if row['requires_intermediate_cleaning'] else "🟢 SECUENCIA VÁLIDA"
                
                st.markdown(f"""
                <div style="border: 2px solid {card_border}; background-color: {bg_color}; padding: 12px; border-radius: 8px; margin-bottom: 10px;">
                    <div style="display: flex; justify-content: space-between;">
                        <strong>Lote: {row['batch_id']} - {row['product_name']}</strong>
                        <span>{status_badge}</span>
                    </div>
                    <hr style="margin: 6px 0;">
                    <p style="margin: 0; font-size: 0.9em;">
                        <b>Horario:</b> {row['start_time']} ➔ {row['end_time']}<br>
                        <b>Alérgenos Declarados:</b> <code>{row['declared_allergens']}</code><br>
                        <b>Alérgenos Activos Acumulados en Línea:</b> <code style="color: #B91C1C;">{row['carryover_allergens_active']}</code>
                    </p>
                </div>
                """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# TAB 3: AUDITORÍA OCR DE ETIQUETADO
# -----------------------------------------------------------------------------
with tab3:
    st.subheader("Auditoría de Visión Artificial / OCR en Cinta de Envasado")
    st.markdown("Validación continua en tiempo real de las etiquetas impresas contra la ficha técnica del producto.")
    
    if len(filtered_ocr) == 0:
        st.info("No hay inspeciones OCR registradas para esta selección.")
    else:
        ocr_pass = len(filtered_ocr[filtered_ocr['inspection_status'] == 'PASS'])
        ocr_fail_missing = len(filtered_ocr[filtered_ocr['inspection_status'] == 'FAIL_MISSING_ALLERGEN'])
        ocr_fail_blur = len(filtered_ocr[filtered_ocr['inspection_status'] == 'FAIL_OCR_UNREADABLE'])
        
        c1, c2, c3 = st.columns(3)
        c1.metric("✅ Inspecciones Conformes", ocr_pass)
        c2.metric("⚠️ Alérgenos Faltantes", ocr_fail_missing, delta_color="inverse")
        c3.metric("🔍 Lectura Borrosa", ocr_fail_blur, delta_color="inverse")
        
        st.subheader("🔍 Buscador y Registro de Inspecciones OCR")
        status_filter = st.multiselect("Filtrar por Estado OCR", filtered_ocr['inspection_status'].unique(), default=filtered_ocr['inspection_status'].unique())
        
        display_ocr = filtered_ocr[filtered_ocr['inspection_status'].isin(status_filter)]
        
        st.dataframe(
            display_ocr[['inspection_id', 'timestamp', 'batch_id', 'expected_allergens', 'extracted_allergens_ocr', 'inspection_status', 'discrepancy_note']],
            use_container_width=True
        )
