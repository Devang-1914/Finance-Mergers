import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt 
import pandas as pd
import matplotlib.pyplot as plt

def calculate_pe_ratio(eps, share_price):
    """Calculate the Price-to-Earnings (P/E) Ratio."""
    return share_price / eps


def calculate_de_ratio(total_debt, total_equity):
    """Calculate the Debt-to-Equity (D/E) Ratio."""
    return total_debt / total_equity


def calculate_roe(net_income, shareholder_equity):
    """Calculate the Return on Equity (ROE)."""
    return net_income / shareholder_equity


def merger_type_and_comments(post_merger_de, stake_a, stake_b):
    """Recommend merger type based on stake percentages and provide comments."""
    if stake_a > 65:
        merger_type = "Acquisition"
        stake_comment = "Company A holds a majority stake, indicating a clear acquisition.🤑"
    elif stake_a > 50:
        merger_type = "Majority Acquisition"
        stake_comment = "Company A retains control, but the merger is closer to a partnership.🥳"
    else:
        merger_type = "Merger of Equals"
        stake_comment = "Stake percentages suggest a merger of equals, with balanced control.🫱🏼‍🫲🏻"

    de_comment = "The post-merger debt-to-equity ratio is within a healthy range." if post_merger_de < 1 else "High post-merger D/E ratio indicates significant leverage, posing financial risks."

    return merger_type, stake_comment, de_comment


def merger_analysis(earnings_a, shares_a, share_price_a, total_debt_a, total_equity_a,
                    earnings_b, shares_b, share_price_b, total_debt_b, total_equity_b,
                    purchase_price_b):
    """Perform an expanded financial analysis of a merger scenario."""

    # Pre-Merger Calculations
    eps_a = earnings_a / shares_a
    eps_b = earnings_b / shares_b
    pe_a = calculate_pe_ratio(eps_a, share_price_a)
    pe_b = calculate_pe_ratio(eps_b, share_price_b)
    de_a = calculate_de_ratio(total_debt_a, total_equity_a)
    de_b = calculate_de_ratio(total_debt_b, total_equity_b)
    roe_a = calculate_roe(earnings_a, total_equity_a)
    roe_b = calculate_roe(earnings_b, total_equity_b)

    # Assume the acquisition is paid in shares; calculate new shares issued by A to B shareholders
    new_shares_issued = purchase_price_b / share_price_a

    # Post-Merger Calculations
    combined_earnings = earnings_a + earnings_b
    total_new_shares = shares_a + new_shares_issued
    post_merger_eps = combined_earnings / total_new_shares
    combined_debt = total_debt_a + total_debt_b
    combined_equity = total_equity_a + total_equity_b + (new_shares_issued * share_price_a) - purchase_price_b
    post_merger_de = calculate_de_ratio(combined_debt, combined_equity)
    post_merger_pe = calculate_pe_ratio(post_merger_eps,
                                        share_price_a)  # Assuming share price remains constant for simplicity

    # Calculate stake percentages
    stake_a = (shares_a / total_new_shares) * 100
    stake_b = (new_shares_issued / total_new_shares) * 100

    # Determine merger type and generate comments
    merger_type, stake_comment, de_comment = merger_type_and_comments(post_merger_de, stake_a, stake_b)

    return eps_a, eps_b, pe_a, pe_b, de_a, de_b, roe_a, roe_b, post_merger_eps, post_merger_de, post_merger_pe, \
           stake_a, stake_b, merger_type, stake_comment, de_comment


# Example inputs
details = merger_analysis(
    earnings_a=5000000, shares_a=1000000, share_price_a=10, total_debt_a=2000000, total_equity_a=8000000,
    earnings_b=2000000, shares_b=500000, share_price_b=8, total_debt_b=1000000, total_equity_b=4000000,
    purchase_price_b=10000000
)


def app():
    import streamlit as st

    # Display an image file
    image_path = 'merger.jpg'  # Replace with your actual image path
    st.image(image_path)

    st.markdown('<div style="text-align: center;"><h1>Merger Analysis Tool</h1></div>', unsafe_allow_html=True)
    # st.title('Merger Analysis Tool')

    # Company A Input
    in_col1, in_col2 = st.columns(2)
    with in_col1:
        st.subheader('Company A Input')
        earnings_a = st.number_input('Earnings', value=5000000)
        shares_a = st.number_input('Number of shares', value=1000000)
        share_price_a = st.number_input('Price per share', value=10.0)
        total_debt_a = st.number_input('Total Debt', value=2000000)
        total_equity_a = st.number_input('Total Equity', value=8000000)

    # Company B Input
    with in_col2:
        st.subheader('Company B Input')
        earnings_b = st.number_input('Earnings', value=2000000)
        shares_b = st.number_input('Number of shares', value=500000)
        share_price_b = st.number_input('Price per share', value=8.0)
        total_debt_b = st.number_input('Total Debt', value=1000000)
        total_equity_b = st.number_input('Total Equity', value=4000000)

    # Acquisition Price
    purchase_price_b = st.number_input('Purchase Price for Company B', value=10000000)

    # Analysis Button
    #     print(results)

    if st.button('Analyze Merger', key='analyze_button', help='Click to analyze the merger'):
            # Your analysis code...
        results = merger_analysis(
                earnings_a, shares_a, share_price_a, total_debt_a, total_equity_a,
                earnings_b, shares_b, share_price_b, total_debt_b, total_equity_b,
                purchase_price_b
            )

        # Define the output variables, adjusted to separate Company A and Company B
        st.subheader("Merger Analysis Results")
        output_variables = {
            'Metrics': [
                'Earnings Per Share', 'Price-To-Earnings Ratio', 'Debt-To-Equity Ratio', 'Return on Earnings',  # Pre-merger metrics repeated for both companies

                'Stake owned (%)'  # Stake is a unique metric, applied to both
            ],
            'Company A': [
                results[0], results[2], results[4], results[6],  # Pre-merger metrics for Company A

                results[11]  # Stake of Company A
            ],
            'Company B': [
                results[1], results[3], results[5], results[7],  # Pre-merger metrics for Company B

                results[12]  # Stake of Company B
            ]
        }
         # Create a pandas DataFrame
        df = pd.DataFrame(output_variables)
        st.dataframe(df)

        col1, col2, col3 = st.columns(3)
        col1.metric(label="Post Merger EPS", value=f"{results[8]:.4f}")  # Format to display 4 decimal points
        col2.metric(label="Post Merger D/E", value=f"{results[9]:.4f}")  # Format to display 4 decimal points
        col3.metric(label="Post Merger P/E (using A's share price)", value=f"{results[10]:.4f}")  # Format to display 4 decimal points

        st.markdown(f"""
            #### Merger Type
            {results[13]}

            #### Stake Comment
            {results[14]}

            #### D/E Ratio Comment
            {results[15]}
        """)

        stake_data = [results[11], results[12]]
        labels = ['Company A', 'Company B']

        st.markdown(f"#### Ownership Stake Post-Merger")
        fig = go.Figure(data=[go.Pie(labels=labels, values=stake_data, hole=.3)])
        fig.update_layout(margin=dict(l=0, r=0, t=30, b=0))

        st.plotly_chart(fig)

if __name__ == '__main__':
    app()