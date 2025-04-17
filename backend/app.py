from flask import Flask, render_template, request, make_response
from fpdf import FPDF
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import io
import os
import json
from waitress import serve
import base64

app = Flask(__name__)

score_map = {"Yes": 1, "No": 0}

categories = {
    "Applications": {
        "fields": ["app_platforms", "waf", "siem", "apt_protection"],
        "weight": 20
    },
    "Data Protection": {
        "fields": ["big_data_analytics", "data_encryption", "email_security"],
        "weight": 20
    },
    "Access Management": {
        "fields": ["idm", "sso"],
        "weight": 10
    },
    "Endpoint Security": {
        "fields": [
            "antivirus_hips", "endpoint_patch", "config_mgmt", "endpoint_vuln",
            "aaa", "endpoint_2fa", "pim"
        ],
        "weight": 25
    },
    "Infrastructure": {
        "fields": [
            "infra_firewall", "ips", "vpn", "web_gateway", "network_antivirus",
            "wireless_security"
        ],
        "weight": 25
    }
}

def calculate_scores(form):
    total_weighted_score = 0
    category_results = {}

    for category, data in categories.items():
        fields = data["fields"]
        weight = data["weight"]

        implemented = sum(score_map.get(form.get(field, "No"), 0) for field in fields)
        total = len(fields)
        weighted_score = (implemented / total) * weight if total else 0

        category_results[category] = {
            "score": implemented,
            "total": total,
            "weight": weight,
            "weighted_score": weighted_score
        }

        total_weighted_score += weighted_score

    final_percentage = round(total_weighted_score, 2)
    posture = (
        "Strong" if final_percentage >= 80 else
        "Moderate" if final_percentage >= 50 else
        "Weak"
    )


    roadmap = (
        "Long-Term (12-24 Months):\n"
        "- Access & Endpoint Management:\n"
        "  - Implement advanced IAM solutions, including Single Sign-On (SSO) and Privileged Access Management (PAM).\n"
        "  - Deploy endpoint detection and response (EDR) solutions across all devices.\n"
        "- Industry-Specific Controls:\n"
        "  - Achieve relevant industry certifications (e.g., PCI DSS, HIPAA) based on sector requirements.\n"
        "  - Regularly assess and update controls to align with evolving industry standards. \n\n"

        "Mid-Term (6-12 Months):\n"
        "- Operations & Infrastructure:\n"
        "  - Establish comprehensive incident and change management processes.\n"
        "  - Deploy intrusion prevention systems (IPS) and secure VPNs for remote access.\n"
        "- Application & Data Security:\n"
        "  - Integrate Web Application Firewalls (WAF) and Security Information and Event Management (SIEM) tools.\n"
        "  - Ensure sensitive data is encrypted both at rest and in transit. \n\n"

        "Short-Term (0-6 Months):\n"
        "- Governance & Compliance:\n"
        "  - Appoint a Data Protection Officer (DPO) or Chief Information Security Officer (CISO).\n"
        "  - Develop and implement a Cyber Crisis Management Plan (CCMP).\n"
        "  - Ensure compliance with CERT-IN's 6-hour incident reporting requirement.\n"
        "- Technical Controls:\n"
        "  - Implement or enhance firewall configurations.\n"
        "  - Automate patch management processes.\n"
        "  - Enforce 2FA across all applications and endpoints."
    )

    return category_results, final_percentage, posture, roadmap

@app.route('/')
def home():
    return render_template('assessment.html')

@app.route('/generate_report', methods=['POST'])
def generate_report():
    form = request.form.to_dict()
    category_results, final_percentage, posture, roadmap = calculate_scores(form)

    # Generate Pie Chart
    labels = ['Score Received', 'Score Missed']
    sizes = [final_percentage, 100 - final_percentage]
    colors = ['#00d15f', '#ff4c4c']
    explode = (0.1, 0)

    plt.figure(figsize=(5, 5))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140, explode=explode)
    plt.title("Overall Assessment Result", color='#00d15f')
    plt.tight_layout()

    pie_stream = io.BytesIO()
    plt.savefig(pie_stream, format='png', bbox_inches="tight", dpi=100)
    pie_stream.seek(0)
    plt.close()

    chart_base64 = base64.b64encode(pie_stream.read()).decode('utf-8')

    # Generate Bar Graph for Category Scores
    categories_list = list(category_results.keys())
    scores_list = [v['score'] for v in category_results.values()]
    totals_list = [v['total'] for v in category_results.values()]

    plt.figure(figsize=(8, 5))
    bars = plt.bar(categories_list, scores_list, color='#00d15f')
    plt.ylim(0, max(totals_list) + 1)
    plt.title("Category-wise Scores", color='#00d15f')
    plt.xlabel("Categories")
    plt.ylabel("Score")
    plt.xticks(rotation=30, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    bar_stream = io.BytesIO()
    plt.savefig(bar_stream, format='png', bbox_inches="tight", dpi=100)
    bar_stream.seek(0)
    plt.close()

    bar_chart_base64 = base64.b64encode(bar_stream.read()).decode('utf-8')

    return render_template('report.html',
                           form=form,
                           category_results=category_results,
                           final_percentage=final_percentage,
                           posture=posture,
                           roadmap=roadmap,
                           scores=category_results,
                           chart_base64=chart_base64,
                           bar_chart_base64=bar_chart_base64)

@app.route('/download', methods=['POST'])
def download():
    form = json.loads(request.form['form_data'])
    category_results, final_percentage, posture, roadmap = calculate_scores(form)

    # Pie Chart
    labels = ['Score Received', 'Score Missed']
    sizes = [final_percentage, 100 - final_percentage]
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

    # Bar Graph
    categories_list = list(category_results.keys())
    scores_list = [v['score'] for v in category_results.values()]
    totals_list = [v['total'] for v in category_results.values()]

    plt.figure(figsize=(8, 5))
    bars = plt.bar(categories_list, scores_list, color='#00d15f')
    plt.ylim(0, max(totals_list) + 1)
    plt.title("Category-wise Scores", color='#00d15f')
    plt.xlabel("Categories")
    plt.ylabel("Score")
    plt.xticks(rotation=30, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    bar_stream = io.BytesIO()
    plt.savefig(bar_stream, format='png', bbox_inches="tight", dpi=100)
    bar_stream.seek(0)
    plt.close()

    pdf = FPDF()
    pdf.add_page()

    try:
        logo_path = os.path.abspath('logo2.png')
        pdf.image(logo_path, x=10, y=8, w=40)
    except Exception as e:
        print(f"Error adding logo: {e}")

    # pdf.set_font("Arial", "B", 16)
    # pdf.set_text_color(0, 209, 95)
    # pdf.cell(190, 10, "Forvis Mazars", ln=True, align="C")

    pdf.ln(20)
    pdf.set_font("Arial", "", 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(200, 10, f"Client: {form.get('client_name', 'N/A')}", ln=True)
    pdf.cell(200, 10, f"Total Weighted Score: {final_percentage}%", ln=True)
    pdf.cell(200, 10, f"Security Posture: {posture}", ln=True)

    pdf.ln(10)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "Category-wise Breakdown", ln=True)

    pdf.set_font("Arial", "", 12)
    for cat, result in category_results.items():
        pdf.cell(200, 10, f"{cat}: {result['score']}/{result['total']} - Weighted: {round(result['weighted_score'], 2)}%", ln=True)

    pdf.ln(10)
    pdf.multi_cell(0, 10, "This report includes a comprehensive assessment of technical and governance-level controls. Please review the recommendations provided to enhance your security posture.")

    # Save pie chart temporarily
    pie_chart_path = 'pie_chart.png'
    with open(pie_chart_path, 'wb') as f:
        f.write(chart_stream.read())
    pdf.image(pie_chart_path, x=50, y=None, w=90)
    os.remove(pie_chart_path)

    # Save bar graph temporarily
    bar_chart_path = 'bar_chart.png'
    with open(bar_chart_path, 'wb') as f:
        f.write(bar_stream.read())
    pdf.image(bar_chart_path, x=30, y=None, w=150)
    os.remove(bar_chart_path)

    pdf.ln(10)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "Roadmap Recommendation", ln=True, align="L")
    pdf.ln(5)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, roadmap)

    response = make_response(pdf.output(dest="S").encode("latin1", errors="ignore"))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=cyber_risk_report.pdf'
    return response

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
