# from flask import Flask, render_template, request, make_response, redirect, url_for, session
# from fpdf import FPDF
# import matplotlib.pyplot as plt
# import matplotlib
# matplotlib.use('Agg')
# import io
# import os
# import json
# from waitress import serve
# import base64

# app = Flask(__name__)
# app.secret_key = '2141343523'


# score_map = {"Yes": 1, "No": 0}

# categories = {
#     "Applications": {
#         "fields": ["app_platforms", "waf", "siem", "apt_protection"],
#         "weight": 20
#     },
#     "Data Protection": {
#         "fields": ["big_data_analytics", "data_encryption", "email_security"],
#         "weight": 20
#     },
#     "Access Management": {
#         "fields": ["idm", "sso"],
#         "weight": 10
#     },
#     "Endpoint Security": {
#         "fields": [
#             "antivirus_hips", "endpoint_patch", "config_mgmt", "endpoint_vuln",
#             "aaa", "endpoint_2fa", "pim"
#         ],
#         "weight": 25
#     },
#     "Infrastructure": {
#         "fields": [
#             "infra_firewall", "ips", "vpn", "web_gateway", "network_antivirus",
#             "wireless_security"
#         ],
#         "weight": 25
#     }
# }

# def calculate_scores(form):
#     total_weighted_score = 0
#     category_results = {}

#     for category, data in categories.items():
#         fields = data["fields"]
#         weight = data["weight"]

#         implemented = sum(score_map.get(form.get(field, "No"), 0) for field in fields)
#         total = len(fields)
#         weighted_score = (implemented / total) * weight if total else 0

#         category_results[category] = {
#             "score": implemented,
#             "total": total,
#             "weight": weight,
#             "weighted_score": weighted_score
#         }

#         total_weighted_score += weighted_score

#     final_percentage = round(total_weighted_score, 2)
#     posture = (
#         "Strong" if final_percentage >= 80 else
#         "Moderate" if final_percentage >= 50 else
#         "Weak"
#     )

#     roadmap = (
#         "Long-Term (12-24 Months):\n"
#         "- Access & Endpoint Management:\n"
#         "  - Implement advanced IAM solutions, including Single Sign-On (SSO) and Privileged Access Management (PAM).\n"
#         "  - Deploy endpoint detection and response (EDR) solutions across all devices.\n"
#         "- Industry-Specific Controls:\n"
#         "  - Achieve relevant industry certifications (e.g., PCI DSS, HIPAA) based on sector requirements.\n"
#         "  - Regularly assess and update controls to align with evolving industry standards. \n\n"
#         "Mid-Term (6-12 Months):\n"
#         "- Operations & Infrastructure:\n"
#         "  - Establish comprehensive incident and change management processes.\n"
#         "  - Deploy intrusion prevention systems (IPS) and secure VPNs for remote access.\n"
#         "- Application & Data Security:\n"
#         "  - Integrate Web Application Firewalls (WAF) and Security Information and Event Management (SIEM) tools.\n"
#         "  - Ensure sensitive data is encrypted both at rest and in transit. \n\n"
#         "Short-Term (0-6 Months):\n"
#         "- Governance & Compliance:\n"
#         "  - Appoint a Data Protection Officer (DPO) or Chief Information Security Officer (CISO).\n"
#         "  - Develop and implement a Cyber Crisis Management Plan (CCMP).\n"
#         "  - Ensure compliance with CERT-IN's 6-hour incident reporting requirement.\n"
#         "- Technical Controls:\n"
#         "  - Implement or enhance firewall configurations.\n"
#         "  - Automate patch management processes.\n"
#         "  - Enforce 2FA across all applications and endpoints."
#     )

#     return category_results, final_percentage, posture, roadmap

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/start_assessment', methods=['POST'])

# def start_assessment():
#     session['client_name'] = request.form['client_name']
#     session['client_email'] = request.form['client_email']
#     # session['client_industry'] = request.form['client_industry']
#     return redirect(url_for('assessment'))

# @app.route('/submit', methods=['POST'])
# def submit():
#     client_name = session.get('client_name', 'N/A')
#     client_email = session.get('client_email', 'N/A')

# @app.route('/assessment')
# def assessment():
#     return render_template('assessment.html')

# @app.route('/generate_report', methods=['POST'])
# def generate_report():
#     form = request.form.to_dict()
#     category_results, final_percentage, posture, roadmap = calculate_scores(form)

#     # Generate Pie Chart
#     labels = ['Score Received', 'Score Missed']
#     sizes = [final_percentage, 100 - final_percentage]
#     colors = ['#00d15f', '#ff4c4c']
#     explode = (0.1, 0)

#     plt.figure(figsize=(5, 5))
#     plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140, explode=explode)
#     plt.title("Overall Assessment Result", color='#00d15f')
#     plt.tight_layout()

#     pie_stream = io.BytesIO()
#     plt.savefig(pie_stream, format='png', bbox_inches="tight", dpi=100)
#     pie_stream.seek(0)
#     plt.close()

#     chart_base64 = base64.b64encode(pie_stream.read()).decode('utf-8')

#     # Generate Bar Graph for Category Scores
#     categories_list = list(category_results.keys())
#     scores_list = [v['score'] for v in category_results.values()]
#     totals_list = [v['total'] for v in category_results.values()]

#     plt.figure(figsize=(8, 5))
#     bars = plt.bar(categories_list, scores_list, color='#00d15f')
#     plt.ylim(0, max(totals_list) + 1)
#     plt.title("Category-wise Scores", color='#00d15f')
#     plt.xlabel("Categories")
#     plt.ylabel("Score")
#     plt.xticks(rotation=30, ha='right')
#     plt.grid(axis='y', linestyle='--', alpha=0.7)

#     bar_stream = io.BytesIO()
#     plt.savefig(bar_stream, format='png', bbox_inches="tight", dpi=100)
#     bar_stream.seek(0)
#     plt.close()

#     bar_chart_base64 = base64.b64encode(bar_stream.read()).decode('utf-8')
    

#     return render_template('report.html',
#                            form=form,
#                            category_results=category_results,
#                            final_percentage=final_percentage,
#                            posture=posture,
#                            roadmap=roadmap,
#                            scores=category_results,
#                            chart_base64=chart_base64,
#                            bar_chart_base64=bar_chart_base64)

# @app.route('/download', methods=['POST'])
# def download():
#     client_name = session.get('client_name', 'Client')
#     form = json.loads(request.form['form_data'])
#     category_results, final_percentage, posture, roadmap = calculate_scores(form)

#     # Pie Chart
#     labels = ['Score Received', 'Score Missed']
#     sizes = [final_percentage, 100 - final_percentage]
#     colors = ['#00d15f', '#ff4c4c']
#     explode = (0.1, 0)

#     plt.figure(figsize=(5, 5))
#     plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140, explode=explode)
#     plt.title("Overall Assessment Result", color='#00d15f')
#     plt.tight_layout()

#     chart_stream = io.BytesIO()
#     plt.savefig(chart_stream, format='png', bbox_inches="tight", dpi=100)
#     chart_stream.seek(0)
#     plt.close()

#     # Bar Graph
#     categories_list = list(category_results.keys())
#     scores_list = [v['score'] for v in category_results.values()]
#     totals_list = [v['total'] for v in category_results.values()]

#     plt.figure(figsize=(8, 5))
#     bars = plt.bar(categories_list, scores_list, color='#00d15f')
#     plt.ylim(0, max(totals_list) + 1)
#     plt.title("Category-wise Scores", color='#00d15f')
#     plt.xlabel("Categories")
#     plt.ylabel("Score")
#     plt.xticks(rotation=30, ha='right')
#     plt.grid(axis='y', linestyle='--', alpha=0.7)

#     bar_stream = io.BytesIO()
#     plt.savefig(bar_stream, format='png', bbox_inches="tight", dpi=100)
#     bar_stream.seek(0)
#     plt.close()

#     pdf = FPDF()
#     pdf.add_page()

#     try:
#         logo_path = os.path.abspath('logo1.png')
#         pdf.image(logo_path, x=10, y=8, w=40)
#     except Exception as e:
#         print(f"Error adding logo: {e}")

#     pdf.ln(20)
#     pdf.set_font("Arial", "", 12)
#     pdf.set_text_color(0, 0, 0)
#     # client_name = session.get('client_name', 'Client')
#     # pdf.cell(200, 10, f"Client: {form.get('client_name', 'N/A')}", ln=True)
#     pdf.cell(200, 10, f"Client Name: {client_name} ", ln=True)
#     pdf.cell(200, 10, f"Total Weighted Score: {final_percentage}%", ln=True)
#     pdf.cell(200, 10, f"Security Posture: {posture}", ln=True)

#     pdf.ln(10)
#     pdf.set_font("Arial", "B", 14)
#     pdf.cell(200, 10, "Category-wise Breakdown", ln=True)

#     pdf.set_font("Arial", "", 12)
#     for cat, result in category_results.items():
#         pdf.cell(200, 10, f"{cat}: {result['score']}/{result['total']} - Weighted: {round(result['weighted_score'], 2)}%", ln=True)

#     pdf.ln(10)
#     pdf.multi_cell(0, 10, "This report includes a comprehensive assessment of technical and governance-level controls. Please review the recommendations provided to enhance your security posture.")

#     pie_chart_path = 'pie_chart.png'
#     with open(pie_chart_path, 'wb') as f:
#         f.write(chart_stream.read())
#     pdf.image(pie_chart_path, x=50, y=None, w=90)
#     os.remove(pie_chart_path)

#     bar_chart_path = 'bar_chart.png'
#     with open(bar_chart_path, 'wb') as f:
#         f.write(bar_stream.read())
#     pdf.image(bar_chart_path, x=30, y=None, w=150)
#     os.remove(bar_chart_path)

#     pdf.ln(10)
#     pdf.set_font("Arial", "B", 14)
#     pdf.cell(200, 10, "Roadmap Recommendation", ln=True, align="L")
#     pdf.ln(5)
#     pdf.set_font("Arial", "", 12)
#     pdf.multi_cell(0, 10, roadmap)

#     response = make_response(pdf.output(dest="S").encode("latin1", errors="ignore"))
#     response.headers['Content-Type'] = 'application/pdf'
#     response.headers['Content-Disposition'] = 'attachment; filename=cyber_risk_report.pdf'
#     return response

# if __name__ == '__main__':
#     serve(app, host='0.0.0.0', port=5000)




from flask import Flask, render_template, request, redirect, url_for, session, make_response
from fpdf import FPDF
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import io
import os
import json
import base64
from waitress import serve

app = Flask(__name__)
app.secret_key = '2141343523'

score_map = {"Yes": 1, "No": 0}

categories = {
    "Applications": {
        "fields": ['app_platforms', 
        'waf', 
        'siem', 
        'apt_protection',
        'amt_access',
        'amt_verify',
        'amt_net',
        'amt_pass',
        'amt_roles',
        'amt_locked',
        'amt_leaked',
        'amt_spam',
        'amt_backup',
        'amt_db',
        'amt_train',
        
        ],
        "weight": 25
    },
    # "Data Protection": {
    #     "fields": ["big_data_analytics", "data_encryption", "email_security"],
    #     "weight": 20
    # },
    # "Access Management": {
    #     "fields": ["idm", "sso"],
    #     "weight": 10
    # },
    "Endpoint Security": {
        "fields": [
                    "antivirus_installed",
        "malware_protection",
        "patch_updates",
        "track_changes",
        "secure_login",
        "remove_old_logins",
        "mobile_secured",
        "mobile_mgmt",
        "tamper_alert"
        ],
        "weight": 25
    },
    "Infrastructure": {
        "fields": [
            "network_firewall", "secure_setup", "wifi_encryption", "vpn_usage", "internet_filtering",
            "intrusion_detection", "network_audit"
        ],
        "weight": 25
    },
    "Security Operations": {
    "fields": [
        "device_inventory", "system_monitoring", "24_7_monitoring",
        "incident_response_plan", "patch_management", "change_management",
        "access_review", "external_support"
    ],
    "weight": 25  # or any weight you want
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
        "  - Regularly assess and update controls to align with evolving industry standards.\n\n"
        "Mid-Term (6-12 Months):\n"
        "- Operations & Infrastructure:\n"
        "  - Establish comprehensive incident and change management processes.\n"
        "  - Deploy intrusion prevention systems (IPS) and secure VPNs for remote access.\n"
        "- Application & Data Security:\n"
        "  - Integrate Web Application Firewalls (WAF) and Security Information and Event Management (SIEM) tools.\n"
        "  - Ensure sensitive data is encrypted both at rest and in transit.\n\n"
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
    return render_template('index.html')

@app.route('/start_assessment', methods=['POST'])
def start_assessment():
    session.clear()
    session['client_name'] = request.form.get('client_name')
    session['client_email'] = request.form.get('client_email')

    return redirect(url_for('endpoint'))

@app.route('/endpoint', methods=['GET', 'POST'])
def endpoint():
    if request.method == 'POST':
        session.update(request.form.to_dict())
        return redirect(url_for('infrastructure'))
    return render_template('endpoint.html')

@app.route('/infrastructure', methods=['GET', 'POST'])
def infrastructure():
    if request.method == 'POST':
        session.update(request.form.to_dict())
        return redirect(url_for('applications'))
    return render_template('infrastructure.html')

@app.route('/applications', methods=['GET', 'POST'])
def applications():
    if request.method == 'POST':
        session.update(request.form.to_dict())
        return redirect(url_for('operations'))
    return render_template('applications.html')

# @app.route('/applications', methods=['GET', 'POST'])
# def applications():
#     if request.method == 'POST':
#         print("Form submitted for Applications:", request.form)  # Debugging
#         session.update(request.form.to_dict())
#         return redirect(url_for('operations'))
#     return render_template('applications.html')

# @app.route('/applications', methods=['GET', 'POST'])
# def applications():
#     if request.method == 'POST' and request.form:
#         print("Form submitted for Applications:", request.form)
#         session.update(request.form.to_dict())
#         return redirect(url_for('generate_report'))  # Ensure only valid submissions redirect
#     return render_template('applications.html')


# Fix this route's function name and path
@app.route('/operations', methods=['GET', 'POST'])
def operations():
    if request.method == 'POST':
        session.update(request.form.to_dict())
        return redirect(url_for('generate_report'))
    return render_template('operations.html')  # Fixed typo from 'opearations.html'


@app.route('/generate_report', methods=['GET', 'POST'])
def generate_report():
    if request.method == 'POST':
        session.update(request.form.to_dict())  # capture last form values

    form = dict(session)
    category_results, final_percentage, posture, roadmap = calculate_scores(form)

    # Create pie chart
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

    # Create bar chart
    categories_list = list(category_results.keys())
    scores_list = [v['score'] for v in category_results.values()]
    totals_list = [v['total'] for v in category_results.values()]

    plt.figure(figsize=(8, 5))
    plt.bar(categories_list, scores_list, color='#00d15f')
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

@app.route('/download', methods=['GET', 'POST'])
def download():
    form = dict(session)
    client_name = form.get('client_name', 'Client')
    category_results, final_percentage, posture, roadmap = calculate_scores(form)

    # Generate Pie Chart
    labels = ['Score Received', 'Score Missed']
    sizes = [final_percentage, 100 - final_percentage]
    colors = ['#00d15f', '#ff4c4c']
    explode = (0.1, 0)

    plt.figure(figsize=(5, 5))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140, explode=explode)
    plt.title("Overall Assessment Result", color='#00d15f')
    pie_stream = io.BytesIO()
    plt.savefig(pie_stream, format='png', bbox_inches="tight", dpi=100)
    pie_stream.seek(0)
    plt.close()

    # Generate Bar Chart
    categories_list = list(category_results.keys())
    scores_list = [v['score'] for v in category_results.values()]
    totals_list = [v['total'] for v in category_results.values()]

    plt.figure(figsize=(8, 5))
    plt.bar(categories_list, scores_list, color='#00d15f')
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

    # Save charts temporarily
    pie_path = "pie_chart.png"
    bar_path = "bar_chart.png"
    with open(pie_path, "wb") as f:
        f.write(pie_stream.read())
    with open(bar_path, "wb") as f:
        f.write(bar_stream.read())

    # Create PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, f"Cyber Security Assessment Report - {client_name}", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 10, f"Overall Score: {final_percentage}%\nSecurity Posture: {posture}")
    pdf.ln(5)

    # Insert Pie Chart
    pdf.image(pie_path, x=10, y=pdf.get_y(), w=90)
    pdf.ln(90)  # Add vertical space after pie

    # Insert Bar Chart (scale to fit)
    pdf.image(bar_path, x=10, y=pdf.get_y(), w=130)
    pdf.ln(130)  # Enough spacing to prevent cutoff

    # Category Breakdown
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, "Category-wise Breakdown", ln=True)
    pdf.set_font("Arial", '', 12)
    for category, data in category_results.items():
        pdf.cell(0, 10, f"{category}: {data['score']}/{data['total']} (Weight: {data['weight']})", ln=True)

    # Roadmap
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, "Recommended Roadmap", ln=True)
    pdf.set_font("Arial", '', 10)
    for line in roadmap.strip().split('\n'):
        pdf.multi_cell(0, 5, line)

    # Output PDF
    pdf_bytes = pdf.output(dest='S').encode('latin1')

    # Clean up
    os.remove(pie_path)
    os.remove(bar_path)

    response = make_response(pdf_bytes)
    response.headers['Content-Disposition'] = f'attachment; filename={client_name}_Cyber_Assessment_Report.pdf'
    response.headers['Content-Type'] = 'application/pdf'
    return response




if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
