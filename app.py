import streamlit as st
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os
import zipfile

st.title("📊 Advanced Student Automation System")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:

    df = pd.read_excel(uploaded_file)

    # Calculations
    df["Total"] = df["Math"] + df["English"] + df["Science"]
    df["Percentage"] = (df["Total"] / 300) * 100

    def grade(p):
        if p >= 80:
            return "A+"
        elif p >= 70:
            return "A"
        elif p >= 60:
            return "B"
        else:
            return "C"

    df["Grade"] = df["Percentage"].apply(grade)

    st.subheader("📋 Processed Data")
    st.dataframe(df)

    # Topper
    topper = df.loc[df["Total"].idxmax()]
    st.success(f"🏆 Topper: {topper['Name']} ({topper['Total']} marks)")

    # Metrics
    st.metric("Average Percentage", f"{df['Percentage'].mean():.2f}%")
    st.metric("Highest Marks", int(df["Total"].max()))

    # ---------------- PDF GENERATION ----------------
    if st.button("📄 Generate PDF Reports"):

        styles = getSampleStyleSheet()
        folder = "reports"

        if not os.path.exists(folder):
            os.makedirs(folder)

        for _, student in df.iterrows():

            pdf = SimpleDocTemplate(f"{folder}/{student['Name']}.pdf")

            content = []

            content.append(Paragraph("Student Report Card", styles["Title"]))
            content.append(Spacer(1, 20))

            details = f"""
Name: {student['Name']}<br/>
Total: {student['Total']}<br/>
Percentage: {student['Percentage']:.2f}%<br/>
Grade: {student['Grade']}<br/>
"""

            content.append(Paragraph(details, styles["BodyText"]))

            pdf.build(content)

        # ZIP FILE CREATE
        zip_path = "reports.zip"
        with zipfile.ZipFile(zip_path, "w") as zipf:
            for file in os.listdir(folder):
                zipf.write(os.path.join(folder, file), file)

        with open(zip_path, "rb") as f:
            st.download_button(
                "⬇️ Download All PDF Reports (ZIP)",
                f,
                file_name="student_reports.zip"
            )

        st.success("All PDF reports generated successfully 🚀")