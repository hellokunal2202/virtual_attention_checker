import streamlit as st
import streamlit.components.v1 as components
import time
if st.button("Show JavaScript Alert"):
    time.sleep(3)
    components.html(
        """
        <script>
        alert("This is a JavaScript alert!");
        </script>
        """,
        height=0,
    )
    