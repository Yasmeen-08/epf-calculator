from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

EMPLOYEE_RATE = 0.12      # 12% of basic + DA
EPS_RATE = 0.0833         # 8.33% of employer share goes to pension (EPS)
EPS_WAGE_CAP = 15000      # EPS is calculated on max Rs 15,000


def calculate(basic, age, retire_age, opening, raise_pct, rate, cap_eps):
    years = max(retire_age - age, 1)
    monthly_rate = rate / 12 / 100

    balance = opening
    total_employee = 0
    total_employer = 0
    total_interest = 0
    rows = []

    salary = basic
    for year in range(1, years + 1):
        year_employee = year_employer = year_interest = 0

        for _ in range(12):
            employee = salary * EMPLOYEE_RATE
            eps_base = min(salary, EPS_WAGE_CAP) if cap_eps else salary
            employer = salary * EMPLOYEE_RATE - eps_base * EPS_RATE

            balance += employee + employer
            year_employee += employee
            year_employer += employer
            year_interest += balance * monthly_rate

        balance += year_interest
        total_employee += year_employee
        total_employer += year_employer
        total_interest += year_interest

        rows.append({
            "year": year,
            "age": age + year,
            "employee": round(year_employee),
            "employer": round(year_employer),
            "interest": round(year_interest),
            "balance": round(balance),
            "contributed": round(opening + total_employee + total_employer),
            "interest_total": round(total_interest),
        })

        salary *= 1 + raise_pct / 100

    return {
        "maturity": round(balance),
        "opening": round(opening),
        "employee": round(total_employee),
        "employer": round(total_employer),
        "interest": round(total_interest),
        "years": years,
        "rows": rows,
    }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/calc", methods=["POST"])
def api_calc():
    d = request.get_json()
    result = calculate(
        basic=float(d.get("basic", 0)),
        age=int(d.get("age", 25)),
        retire_age=int(d.get("retire_age", 58)),
        opening=float(d.get("opening", 0)),
        raise_pct=float(d.get("raise_pct", 0)),
        rate=float(d.get("rate", 8.25)),
        cap_eps=bool(d.get("cap_eps", True)),
    )
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)