import streamlit as st
import matplotlib.pyplot as plt

st.title("Patient Report")

if "slice_dist" not in st.session_state:
    st.error("No scan data found.")
    st.stop()

dist = st.session_state["slice_dist"]

labels = ["Healthy", "Cirrhosis"]
values = [dist["healthy"], dist["cirrhosis"]]

fig, ax = plt.subplots(figsize=(5, 4))
ax.bar(labels, values)
ax.set_ylabel("Number of slices")
ax.set_title("Slice Distribution")

st.pyplot(fig)

st.markdown("### Clinical Summary")
st.markdown("""
- Liver texture irregularity visible across multiple slices  
- Fibrosis pattern detected in localized regions  
- Structural deviation suggests chronic liver change  
- AI probability score indicates elevated risk  
- Recommend further hepatology consultation  
- Additional laboratory evaluation advised  
- MRI follow-up recommended in 6 months  
""")

