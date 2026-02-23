import streamlit as st
from agent import agent

st.title("🌍 Country Finance Agent")

country = st.text_input(
    "Enter Country (India, Japan, US, UK, China, South Korea)"
)

if st.button("Get Info"):
    if country:
        result = agent.run(
            f"""
            Give:
            - Official currency
            - Exchange rate to USD INR GBP EUR
            - Major stock indices with values
            - Stock exchange HQ map link
            for {country}
            """
        )
        st.write(result)
    else:
        st.warning("Enter a country.")
