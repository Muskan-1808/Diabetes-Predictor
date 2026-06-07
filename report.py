from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import datetime

def generate_pdf(patient_df, prediction, proba):

    doc = SimpleDocTemplate("patient_report.pdf")
    styles = getSampleStyleSheet()
    content = []

    # Title
    content.append(Paragraph("Diabetes Prediction Report", styles['Title']))
    content.append(Spacer(1, 12))

    # Date
    content.append(Paragraph(f"Date: {datetime.datetime.now()}", styles['Normal']))
    content.append(Spacer(1, 12))

    # Patient Data
    content.append(Paragraph("Patient Details:", styles['Heading2']))
    content.append(Spacer(1, 10))

    for col in patient_df.columns:
        value = patient_df.iloc[0][col]
        content.append(Paragraph(f"{col}: {value}", styles['Normal']))

    content.append(Spacer(1, 12))

    # Result
    result_text = "High Risk of Diabetes" if prediction == 1 else "Low Risk of Diabetes"

    content.append(Paragraph("Prediction Result:", styles['Heading2']))
    content.append(Paragraph(result_text, styles['Normal']))
    content.append(Spacer(1, 12))

    # Probability
    content.append(Paragraph("Probability Analysis:", styles['Heading2']))
    content.append(Paragraph(f"Not Diabetic: {proba[0]*100:.2f}%", styles['Normal']))
    content.append(Paragraph(f"Diabetic: {proba[1]*100:.2f}%", styles['Normal']))

    doc.build(content)

    return "patient_report.pdf"