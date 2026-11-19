import streamlit as st
import pandas as pd

st.set_page_config(page_title="EPF Calculator", page_icon="💰", layout="wide")

EMPLOYEE_RATE = 0.12
EPS_RATE = 0.0833
EPS_WAGE_CAP = 15000


def inr(n):
    """Format a number the Indian way, e.g. ₹40,68,209."""
    s = str(int(round(n)))
    if len(s) > 3:
        head, tail = s[:-3], s[-3:]
        parts = []
        while len(head) > 2:
            parts.insert(0, head[-2:])
            head = head[:-2]
        if head:
            parts.insert(0, head)
        s = ",".join(parts + [tail])
    return "₹" + s


def calculate(basic, age, retire_age, opening, raise_pct, rate, cap_eps):
    years = max(retire_age - age, 1)
    monthly_rate = rate / 12 / 100

    balance = opening
    total_employee = total_employer = total_interest = 0
    rows = []
    salary = basic

    for year in range(1, years + 1):
        y_emp = y_er = y_int = 0
        for _ in range(12):
            employee = salary * EMPLOYEE_RATE
            eps_base = min(salary, EPS_WAGE_CAP) if cap_eps else salary
            employer = salary * EMPLOYEE_RATE - eps_base * EPS_RATE

            balance += employee + employer
            y_emp += employee
            y_er += employer
            y_int += balance * monthly_rate

        balance += y_int
        total_employee += y_emp
        total_employer += y_er
        total_interest += y_int

        rows.append({
            "year": year,
            "employee": y_emp,
            "employer": y_er,
            "interest": y_int,
            "balance": balance,
            "contributed": opening + total_employee + total_employer,
            "interest_total": total_interest,
        })
        salary *= 1 + raise_pct / 100

    return {
        "maturity": balance,
        "employee": total_employee,
        "employer": total_employer,
        "interest": total_interest,
        "years": years,
        "rows": rows,
    }


st.title("EPF Calculator")
st.caption(
    "Employees' Provident Fund corpus at retirement. "
    "Interest is worked out monthly and credited at the end of each year."
)

left, right = st.columns([1, 2], gap="large")

with left:
    st.subheader("Your details")
    basic = st.number_input("Monthly basic + DA (₹)", min_value=0, value=30000, step=1000)
    age = st.number_input("Current age", min_value=18, max_value=70, value=25)
    retire_age = st.number_input("Retirement age", min_value=19, max_value=75, value=58)
    opening = st.number_input("Current EPF balance (₹)", min_value=0, value=0, step=10000)
    raise_pct = st.number_input("Yearly salary increase (%)", min_value=0.0, value=5.0, step=0.5)
    rate = st.number_input(
        "Interest rate (% a year)", min_value=0.0, value=8.25, step=0.05,
        help="Declared yearly by EPFO. Change it to match the current rate.",
    )
    cap_eps = st.checkbox("Cap pension (EPS) wage at ₹15,000", value=True)

if retire_age <= age:
    st.warning("Retirement age must be higher than your current age.")
    st.stop()

r = calculate(basic, age, retire_age, opening, raise_pct, rate, cap_eps)

with right:
    st.subheader("Maturity value")
    st.markdown(f"## {inr(r['maturity'])}")
    if r["maturity"] >= 1e7:
        st.caption(f"About {r['maturity'] / 1e7:.2f} crore after {r['years']} years")
    else:
        st.caption(f"About {r['maturity'] / 1e5:.2f} lakh after {r['years']} years")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("You contribute", inr(r["employee"]))
    c2.metric("Employer adds", inr(r["employer"]))
    c3.metric("Interest earned", inr(r["interest"]))
    c4.metric("Interest share", f"{r['interest'] / r['maturity'] * 100:.1f}%")

    st.subheader("Balance by year")
    chart_df = pd.DataFrame({
        "Year": [x["year"] for x in r["rows"]],
        "Amount invested": [round(x["contributed"]) for x in r["rows"]],
        "Interest": [round(x["interest_total"]) for x in r["rows"]],
    }).set_index("Year")
    st.bar_chart(chart_df, color=["#4fc3c0", "#e5a93d"])

    st.subheader("Year by year")
    table = pd.DataFrame({
        "Year": [x["year"] for x in r["rows"]],
        "You": [inr(x["employee"]) for x in r["rows"]],
        "Employer": [inr(x["employer"]) for x in r["rows"]],
        "Interest": [inr(x["interest"]) for x in r["rows"]],
        "Closing balance": [inr(x["balance"]) for x in r["rows"]],
    })
    st.dataframe(table, hide_index=True)

    st.subheader("How the numbers work")
    st.markdown(
        "- You pay 12% of basic + DA every month.\n"
        "- Your employer also pays 12%, but 8.33% (of wages up to ₹15,000) goes to the "
        "pension scheme (EPS). The rest goes into your EPF.\n"
        "- Interest is worked out every month on the running balance and added at year end.\n"
        "- The salary increase applies from the start of each new year.\n"
        "- This is an estimate. Rates and rules can change, so check with EPFO."
    )

st.divider()
st.caption("Made by Yasmeen Khan")
