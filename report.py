from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import datetime


def generate_pdf(patient_df, prediction, proba, gender):

    file_path = "patient_report.pdf"

    doc = SimpleDocTemplate(file_path)

    styles = getSampleStyleSheet()

    content = []

    # =====================================================
    # TITLE
    # =====================================================

    content.append(
        Paragraph(
            "Diabetes Prediction Report",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 12))

    # =====================================================
    # DATE
    # =====================================================

    date = datetime.datetime.now().strftime(
        "%d-%m-%Y %H:%M"
    )

    content.append(
        Paragraph(
            f"Date: {date}",
            styles["Normal"]
        )
    )

    content.append(Spacer(1, 15))

    # =====================================================
    # PATIENT DETAILS
    # =====================================================

    content.append(
        Paragraph(
            "Patient Details:",
            styles["Heading2"]
        )
    )

    content.append(Spacer(1, 10))

    # IMPORTANT:
    # Show readable gender instead of 0/1
    content.append(
        Paragraph(
            f"Gender: {gender}",
            styles["Normal"]
        )
    )

    # Other patient features
    for col in patient_df.columns:

        # Skip model's numerical gender value
        if col.lower() == "gender":
            continue

        value = patient_df.iloc[0][col]

        content.append(
            Paragraph(
                f"{col}: {value}",
                styles["Normal"]
            )
        )

    content.append(Spacer(1, 15))

    # =====================================================
    # PREDICTION
    # =====================================================

    content.append(
        Paragraph(
            "Prediction Result:",
            styles["Heading2"]
        )
    )

    if prediction == 1:
        result_text = "High Risk of Diabetes"
    else:
        result_text = "Low Risk of Diabetes"

    content.append(
        Paragraph(
            result_text,
            styles["Normal"]
        )
    )

    content.append(Spacer(1, 15))

    # =====================================================
    # PROBABILITY
    # =====================================================

    content.append(
        Paragraph(
            "Probability Analysis:",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            f"Not Diabetic: {float(proba[0]) * 100:.2f}%",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Diabetic: {float(proba[1]) * 100:.2f}%",
            styles["Normal"]
        )
    )

    # =====================================================
    # BUILD PDF
    # =====================================================

    doc.build(content)

    return file_path