
import streamlit as st
import pandas as pd
import pydeck as pdk
from assigner import load_reps, assign_leads
import base64
import io

st.set_page_config(page_title="LeafGuard Lead Assignment Tool", layout="wide")
st.title("🛠️ LeafGuard Lead Assignment Tool")
st.markdown("Upload your Excel file with daily leads and assign them to reps smartly.")

# === FILE UPLOAD ===
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    try:
        leads_df = pd.read_excel(uploaded_file)
        st.success("File uploaded successfully!")

        # === LEAD ASSIGNMENT ===
        reps = load_reps("reps.json")
        result_df = assign_leads(leads_df, reps)

        # === SHOW RESULTS ===
        st.subheader("📋 Assigned Leads")
        st.dataframe(result_df)

        # === MAP DISPLAY ===
        st.subheader("🗺️ Map View")
        st.pydeck_chart(pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state=pdk.ViewState(
                latitude=result_df["lat"].mean(),
                longitude=result_df["lng"].mean(),
                zoom=9,
                pitch=0,
            ),
            layers=[
                pdk.Layer(
                    "ScatterplotLayer",
                    data=result_df,
                    get_position='[lng, lat]',
                    get_fill_color='[180, 0, 200, 140]',
                    get_radius=100,
                ),
            ],
        ))

        # === DOWNLOAD RESULTS ===
        st.subheader("⬇️ Download")
        towrite = io.BytesIO()
        result_df.to_excel(towrite, index=False, engine='openpyxl')
        towrite.seek(0)
        st.download_button("Download Excel", data=towrite, file_name="assigned_leads.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
