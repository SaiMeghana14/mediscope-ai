import streamlit as st

if "result" in st.session_state:
    st.subheader("🔍 Named Entities")
    for ent in st.session_state.result["entities"]:
        st.write(f"{ent['word']} ({ent['entity_group']})")

    st.subheader("📄 Summary")
    st.write(st.session_state.result["summary"])

    st.subheader("🌐 Translation (EN→FR)")
    st.write(st.session_state.result["translation"])
