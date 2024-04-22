import streamlit as st
from user_agents import parse

# Ambil user agent dari sesi
user_agent = st.session_state.get("user_agent", "")

if not user_agent:
    # Jika user agent belum ada di sesi, ambil dari query_params
    user_agent = st.query_params.get("user_agent", "")
    st.session_state["user_agent"] = user_agent

# Parsing user agent
print("Query Params:", st.query_params)

print("User Agent:", user_agent)
parser = parse(user_agent)
print("Parser:", parser)

# Cek apakah perangkat adalah handphone
if parser.is_mobile:
    st.write("This is a mobile device")
else:
    st.write("This is not a mobile device")

# Tambahkan kode JavaScript untuk mengirim ulang permintaan dengan parameter user_agent
st.markdown(
    """
    <script>
        const userAgent = navigator.userAgent;
        window.location.href = window.location.href + "?user_agent=" + encodeURIComponent(userAgent);
    </script>
    """,
    unsafe_allow_html=True
)
