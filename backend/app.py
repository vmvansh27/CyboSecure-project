from flask import Flask, render_template, request, make_response
from fpdf import FPDF
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import io
import os
from waitress import serve

app = Flask(__name__)

# Updated score map with only "Yes" and "No"
score_map = {"Yes": 2, "No": 0}

@app.route('/')
def home():
    return render_template('assessment.html')

@app.route('/generate_report', methods=['POST'])
def generate_report():
    form = request.form

    total_score = 0
    score = 0

    for field in form:
        if field == 'client_name':
            continue
        value = form.get(field)
        if value in score_map:
            total_score += 2  # since only "Yes" = 2, "No" = 0
            score += score_map[value]

    incorrect_score = total_score - score

    posture = "Strong" if score >= 0.8 * total_score else "Moderate" if score >= 0.5 * total_score else "Weak"
    percentage = round((score / total_score) * 100) if total_score > 0 else 0

    # Pie chart
    labels = ['Score Received', 'Score Missed']
    sizes = [score, incorrect_score]
    colors = ['#00d15f', '#ff4c4c']
    explode = (0.1, 0)

    plt.figure(figsize=(5, 5))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140, explode=explode)
    plt.title("Overall Assessment Result", color='#00d15f')
    plt.tight_layout()

    chart_stream = io.BytesIO()
    plt.savefig(chart_stream, format='png', bbox_inches="tight", dpi=100)
    chart_stream.seek(0)
    plt.close()

    pdf = FPDF()
    pdf.add_page()

    try:
        logo_path = os.path.abspath('logo1.png')
        pdf.image(logo_path, x=10, y=8, w=40)
    except Exception as e:
        print(f"Error adding logo: {e}")

    pdf.set_font("Arial", "B", 16)
    pdf.set_text_color(0, 209, 95)
    pdf.cell(190, 10, "Cybosecure Networks Pvt Ltd", ln=True, align="C")

    pdf.ln(5)
    pdf.set_font("Arial", "", 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(200, 10, f"Client: {form.get('client_name', 'N/A')}", ln=True)
    pdf.cell(200, 10, f"Total Score: {score}/{total_score} - {percentage}%", ln=True)
    pdf.cell(200, 10, f"Security Posture: {posture}", ln=True)

    pdf.ln(10)
    pdf.multi_cell(0, 10, "This report includes a comprehensive assessment of technical and governance-level controls. "
                          "Please review the recommendations provided to enhance your security posture.")

    pdf.ln(10)
    chart_path = 'chart.png'
    with open(chart_path, 'wb') as f:
        f.write(chart_stream.read())
    pdf.image(chart_path, x=50, y=None, w=110)
    os.remove(chart_path)

    pdf.ln(10)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "Further Enhancement of Security Posture", ln=True, align="L")

    pdf.ln(5)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
                          "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit "
                          "in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident.")

    response = make_response(pdf.output(dest="S").encode("latin1"))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=cyber_risk_report.pdf'
    return response

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
