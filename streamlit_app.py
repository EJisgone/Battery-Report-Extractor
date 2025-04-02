import os
import subprocess
import pandas as pd
import streamlit as st
from bs4 import BeautifulSoup

# Set page config with custom background
st.set_page_config(page_title="Battery Report Extractor", layout="wide")

# Custom CSS for background image
st.markdown(
    """
    <style>
    .stApp {
        background: url("assets/battery_background.png") no-repeat center fixed;
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to generate the battery report
def generate_battery_report():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(dir_path, "battery-report", "battery-report.html")

    os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Ensure directory exists

    command = f'powercfg /batteryreport /output "{file_path}"'
    subprocess.run(command, shell=True)

    return file_path

# Function to parse the battery report HTML
def parse_battery_report(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    def find_table_value(label):
        cell = soup.find("td", string=lambda text: text and label.lower() in text.lower())
        return cell.find_next_sibling("td").text.strip() if cell else "N/A"

    system_info = {
        "Computer Name": find_table_value("COMPUTER NAME"),
        "System Product Name": find_table_value("SYSTEM PRODUCT NAME"),
        "OS Build": find_table_value("OS BUILD"),
        "BIOS": find_table_value("BIOS"),
        "Report Time": find_table_value("REPORT TIME"),
    }

    return system_info

# UI Layout
st.title("🔋 Laptop Battery Report Extractor")
st.write("Generate and analyze your Windows battery report with an elegant UI.")

if st.button("Generate Battery Report"):
    with st.spinner("Generating battery report..."):
        report_path = generate_battery_report()
        system_data = parse_battery_report(report_path)
        st.success("Battery report generated successfully!")

        # Display System Info
        st.subheader("📋 System Information")
        st.json(system_data)

        # Provide Download Option
        with open(report_path, "rb") as f:
            st.download_button(label="📥 Download Battery Report (HTML)", data=f, file_name="battery-report.html", mime="text/html")
