import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

df = pd.read_excel("students.xlsx")

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

styles = getSampleStyleSheet()

# 🔥 LOOP for all students
for i, student in df.iterrows():

    pdf = SimpleDocTemplate(f"{student['Name']}_report.pdf")

    content = []

    title = Paragraph("📊 Student Report Card", styles["Title"])
    content.append(title)
    content.append(Spacer(1, 20))

    details = f"""
Name: {student['Name']}<br/>
Total Marks: {student['Total']}<br/>
Percentage: {student['Percentage']:.2f}%<br/>
Grade: {student['Grade']}<br/>
"""

    content.append(Paragraph(details, styles["BodyText"]))

    pdf.build(content)

print("All PDFs generated successfully 🚀")