# EPF Calculator

A web app that estimates your **Employees' Provident Fund (EPF)** corpus at retirement. Built with Python and Streamlit.

**Live demo:** https://epf-calculator-v7xguingba5bepyatw9rgz.streamlit.app/

## Features

- Enter monthly basic + DA, current age, retirement age and current EPF balance
- Set the yearly salary increase and the interest rate
- Option to cap the pension (EPS) wage at ₹15,000
- Shows the maturity value, total contributions and interest earned
- Year-by-year balance chart and table, updated live
- Amounts shown in the Indian format (₹40,68,209)

## How the calculation works

1. The employee pays **12%** of basic + DA every month.
2. The employer also pays **12%**. Of this, **8.33%** (on wages up to ₹15,000) goes to the pension scheme (EPS) and the rest goes into EPF.
3. Interest is worked out every month on the running balance (yearly rate ÷ 12) and added to the balance at the end of each year.
4. The salary increase applies from the start of each new year.
5. This repeats until the retirement age. The final balance is the maturity value.

> This is an estimate. Actual EPFO figures can differ slightly, and the interest rate is declared by EPFO every year.

## Tech stack

- Python
- Streamlit
- Pandas

## Run it locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install streamlit
python -m streamlit run app.py
```

Then open http://localhost:8501 in your browser.

## Project structure

```
epf-calculator/
├── app.py
├── requirements.txt
└── README.md
```

## Deployment

Deployed for free on [Streamlit Community Cloud](https://share.streamlit.io) directly from this GitHub repository.
Live Demo : https://epf-calculator-v7xguingba5bepyatw9rgz.streamlit.app/
## Author

**Yasmeen Khan**
GitHub: [@Yasmeen-08](https://github.com/Yasmeen-08)
