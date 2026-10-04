import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from datetime import date

# =========================================================
# PENNYWISE
# Track. Understand. Take Control.
# =========================================================

st.set_page_config(
    page_title="PennyWise",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# COLORS / DESIGN
# =========================================================

BG = "#F4F6F5"
DARK = "#17221D"
GREEN = "#2F7D5B"
SOFT_GREEN = "#DDEFE6"
YELLOW = "#E9B949"
TEXT = "#18201C"
MUTED = "#737C76"
WHITE = "#FFFFFF"
RED = "#B85C5C"

# =========================================================
# DATA
# =========================================================

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

DATA_FILE = DATA_DIR / "transactions.csv"

COLUMNS = [
    "id",
    "date",
    "type",
    "description",
    "category",
    "amount"
]

CATEGORIES = [
    "Food",
    "Transport",
    "Shopping",
    "Bills",
    "Education",
    "Health",
    "Entertainment",
    "Salary",
    "Freelance",
    "Other"
]


def load_data():
    if DATA_FILE.exists():
        df = pd.read_csv(DATA_FILE)

        if not df.empty:
            df["date"] = pd.to_datetime(df["date"]).dt.date
            df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
            return df

    return pd.DataFrame(columns=COLUMNS)


def save_data(df):
    df.to_csv(DATA_FILE, index=False)


if "transactions" not in st.session_state:
    st.session_state.transactions = load_data()


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    f"""
    <style>

    .stApp {{
        background-color: {BG};
        color: {TEXT};
    }}

    [data-testid="stSidebar"] {{
        background-color: {DARK};
    }}

    [data-testid="stSidebar"] * {{
        color: white !important;
    }}

    .brand {{
        font-size: 27px;
        font-weight: 800;
        letter-spacing: 2px;
        color: white;
        margin-bottom: 0;
    }}

    .brand-sub {{
        color: #AEB9B2;
        font-size: 13px;
        margin-top: -5px;
        margin-bottom: 30px;
    }}

    .page-title {{
        font-size: 36px;
        font-weight: 800;
        color: {TEXT};
        margin-bottom: 3px;
    }}

    .page-subtitle {{
        color: {MUTED};
        font-size: 15px;
        margin-bottom: 25px;
    }}

    .metric-card {{
        background: {WHITE};
        border-radius: 18px;
        padding: 22px;
        border: 1px solid #E5E9E6;
        min-height: 135px;
    }}

    .metric-label {{
        color: {MUTED};
        font-size: 14px;
        margin-bottom: 8px;
    }}

    .metric-value {{
        font-size: 28px;
        font-weight: 800;
        color: {TEXT};
    }}

    .income {{
        color: {GREEN};
    }}

    .expense {{
        color: {RED};
    }}

    .balance {{
        color: {TEXT};
    }}

    .section-title {{
        font-size: 21px;
        font-weight: 750;
        color: {TEXT};
        margin-top: 25px;
        margin-bottom: 12px;
    }}

    .transaction-card {{
        background: white;
        border: 1px solid #E5E9E6;
        border-radius: 14px;
        padding: 14px 18px;
        margin-bottom: 8px;
    }}

    .transaction-name {{
        font-weight: 700;
        color: {TEXT};
    }}

    .transaction-category {{
        color: {MUTED};
        font-size: 12px;
    }}

    .positive {{
        color: {GREEN};
        font-weight: 800;
    }}

    .negative {{
        color: {RED};
        font-weight: 800;
    }}

    .info-box {{
        background: {SOFT_GREEN};
        padding: 18px;
        border-radius: 14px;
        color: {TEXT};
        margin-bottom: 20px;
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand">PENNYWISE</div>
        <div class="brand-sub">Finance Manager</div>
        """,
        unsafe_allow_html=True
    )

    page = st.radio(
        "NAVIGATION",
        [
            "Dashboard",
            "Add Transaction",
            "Transactions",
            "Analytics"
        ],
        label_visibility="visible"
    )

    st.markdown("---")

    st.caption("Track. Understand. Take Control.")


# =========================================================
# CALCULATIONS
# =========================================================

df = st.session_state.transactions.copy()

if not df.empty:
    total_income = df.loc[df["type"] == "Income", "amount"].sum()
    total_expenses = df.loc[df["type"] == "Expense", "amount"].sum()
else:
    total_income = 0
    total_expenses = 0

balance = total_income - total_expenses
transaction_count = len(df)


# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":

    st.markdown(
        '<div class="page-title">Good money habits start here.</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">Your personal financial overview.</div>',
        unsafe_allow_html=True
    )

    # Metrics

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">TOTAL INCOME</div>
                <div class="metric-value income">PKR {total_income:,.0f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">TOTAL EXPENSES</div>
                <div class="metric-value expense">PKR {total_expenses:,.0f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">CURRENT BALANCE</div>
                <div class="metric-value balance">PKR {balance:,.0f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">TRANSACTIONS</div>
                <div class="metric-value">{transaction_count}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Charts

    st.markdown(
        '<div class="section-title">Financial Overview</div>',
        unsafe_allow_html=True
    )

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:

        overview_df = pd.DataFrame({
            "Type": ["Income", "Expenses"],
            "Amount": [total_income, total_expenses]
        })

        fig = px.bar(
            overview_df,
            x="Type",
            y="Amount",
            title="Income vs Expenses"
        )

        fig.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            showlegend=False,
            margin=dict(l=20, r=20, t=50, b=20)
        )

        st.plotly_chart(fig, use_container_width=True)

    with chart_col2:

        if not df.empty:

            expense_df = df[df["type"] == "Expense"]

            if not expense_df.empty:

                category_df = (
                    expense_df
                    .groupby("category")["amount"]
                    .sum()
                    .reset_index()
                )

                fig2 = px.pie(
                    category_df,
                    names="category",
                    values="amount",
                    title="Spending by Category",
                    hole=0.55
                )

                fig2.update_layout(
                    paper_bgcolor="white",
                    margin=dict(l=20, r=20, t=50, b=20)
                )

                st.plotly_chart(
                    fig2,
                    use_container_width=True
                )

            else:
                st.info("Add some expenses to see spending categories.")

        else:
            st.info("Add transactions to unlock your analytics.")

    # Recent Transactions

    st.markdown(
        '<div class="section-title">Recent Transactions</div>',
        unsafe_allow_html=True
    )

    if df.empty:

        st.markdown(
            """
            <div class="info-box">
                No transactions yet. Add your first transaction to start tracking your money.
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        recent = df.sort_values(
            "date",
            ascending=False
        ).head(5)

        for _, row in recent.iterrows():

            amount_class = (
                "positive"
                if row["type"] == "Income"
                else "negative"
            )

            sign = "+" if row["type"] == "Income" else "-"

            st.markdown(
                f"""
                <div class="transaction-card">
                    <div style="display:flex;justify-content:space-between;">
                        <div>
                            <div class="transaction-name">
                                {row["description"]}
                            </div>
                            <div class="transaction-category">
                                {row["category"]} • {row["date"]}
                            </div>
                        </div>

                        <div class="{amount_class}">
                            {sign} PKR {row["amount"]:,.0f}
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


# =========================================================
# ADD TRANSACTION
# =========================================================

elif page == "Add Transaction":

    st.markdown(
        '<div class="page-title">Add Transaction</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">Record money coming in or going out.</div>',
        unsafe_allow_html=True
    )

    with st.form("transaction_form"):

        col1, col2 = st.columns(2)

        with col1:

            transaction_type = st.selectbox(
                "Transaction Type",
                ["Expense", "Income"]
            )

            amount = st.number_input(
                "Amount (PKR)",
                min_value=1.0,
                step=100.0
            )

            category = st.selectbox(
                "Category",
                CATEGORIES
            )

        with col2:

            transaction_date = st.date_input(
                "Date",
                value=date.today()
            )

            description = st.text_input(
                "Description",
                placeholder="e.g. Grocery shopping"
            )

        submitted = st.form_submit_button(
            "Add Transaction",
            use_container_width=True
        )

        if submitted:

            if not description.strip():

                st.error("Please enter a description.")

            else:

                new_id = (
                    int(df["id"].max()) + 1
                    if not df.empty
                    else 1
                )

                new_transaction = pd.DataFrame(
                    [{
                        "id": new_id,
                        "date": transaction_date,
                        "type": transaction_type,
                        "description": description.strip(),
                        "category": category,
                        "amount": amount
                    }]
                )

                st.session_state.transactions = pd.concat(
                    [
                        st.session_state.transactions,
                        new_transaction
                    ],
                    ignore_index=True
                )

                save_data(st.session_state.transactions)

                st.success(
                    f"{transaction_type} of PKR {amount:,.0f} added successfully!"
                )


# =========================================================
# TRANSACTIONS
# =========================================================

elif page == "Transactions":

    st.markdown(
        '<div class="page-title">Transactions</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">View, search and manage your financial activity.</div>',
        unsafe_allow_html=True
    )

    if df.empty:

        st.info("No transactions available yet.")

    else:

        search = st.text_input(
            "Search",
            placeholder="Search description or category..."
        )

        filter_type = st.selectbox(
            "Filter by type",
            ["All", "Income", "Expense"]
        )

        filtered_df = df.copy()

        if search:

            filtered_df = filtered_df[
                filtered_df["description"]
                .str.contains(search, case=False, na=False)
                |
                filtered_df["category"]
                .str.contains(search, case=False, na=False)
            ]

        if filter_type != "All":

            filtered_df = filtered_df[
                filtered_df["type"] == filter_type
            ]

        filtered_df = filtered_df.sort_values(
            "date",
            ascending=False
        )

        st.write(
            f"Showing **{len(filtered_df)}** transaction(s)"
        )

        for _, row in filtered_df.iterrows():

            col1, col2, col3 = st.columns([4, 2, 1])

            with col1:

                st.markdown(
                    f"""
                    <div class="transaction-card">
                        <div class="transaction-name">
                            {row["description"]}
                        </div>
                        <div class="transaction-category">
                            {row["category"]} • {row["date"]}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col2:

                sign = "+" if row["type"] == "Income" else "-"
                amount_class = (
                    "positive"
                    if row["type"] == "Income"
                    else "negative"
                )

                st.markdown(
                    f"""
                    <div style="padding-top:18px;"
                         class="{amount_class}">
                        {sign} PKR {row["amount"]:,.0f}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col3:

                if st.button(
                    "Delete",
                    key=f"delete_{row['id']}"
                ):

                    st.session_state.transactions = (
                        st.session_state.transactions[
                            st.session_state.transactions["id"]
                            != row["id"]
                        ]
                    )

                    save_data(
                        st.session_state.transactions
                    )

                    st.rerun()


# =========================================================
# ANALYTICS
# =========================================================

elif page == "Analytics":

    st.markdown(
        '<div class="page-title">Analytics</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">Understand where your money is going.</div>',
        unsafe_allow_html=True
    )

    if df.empty:

        st.info(
            "Add transactions first. Your analytics will appear here."
        )

    else:

        # Income vs Expense

        st.markdown(
            '<div class="section-title">Income vs Expenses</div>',
            unsafe_allow_html=True
        )

        monthly = df.copy()

        monthly["month"] = pd.to_datetime(
            monthly["date"]
        ).dt.strftime("%b %Y")

        monthly_summary = (
            monthly
            .groupby(["month", "type"])["amount"]
            .sum()
            .reset_index()
        )

        fig = px.bar(
            monthly_summary,
            x="month",
            y="amount",
            color="type",
            barmode="group",
            title="Monthly Cash Flow"
        )

        fig.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # Spending categories

        st.markdown(
            '<div class="section-title">Spending Breakdown</div>',
            unsafe_allow_html=True
        )

        expenses = df[
            df["type"] == "Expense"
        ]

        if not expenses.empty:

            category_summary = (
                expenses
                .groupby("category")["amount"]
                .sum()
                .sort_values(ascending=False)
                .reset_index()
            )

            fig2 = px.bar(
                category_summary,
                x="amount",
                y="category",
                orientation="h",
                title="Expenses by Category"
            )

            fig2.update_layout(
                plot_bgcolor="white",
                paper_bgcolor="white"
            )

            st.plotly_chart(
                fig2,
                use_container_width=True
            )

        else:

            st.info("No expenses recorded yet.")

        # Monthly overview table

        st.markdown(
            '<div class="section-title">Transaction Data</div>',
            unsafe_allow_html=True
        )

        display_df = df.copy()

        display_df["amount"] = display_df["amount"].apply(
            lambda x: f"PKR {x:,.0f}"
        )

        display_df = display_df[
            [
                "date",
                "type",
                "description",
                "category",
                "amount"
            ]
        ]

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "PENNYWISE • Track. Understand. Take Control."
)
