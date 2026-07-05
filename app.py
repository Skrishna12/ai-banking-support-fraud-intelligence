import streamlit as st
import joblib

from src.sentiment import predict_sentiment
from src.risk_engine import calculate_risk
from src.action_engine import get_actions
from src.rag_pipeline import retrieve_context

# --------------------------------------------------
# Load Intent Model
# --------------------------------------------------
intent_model = joblib.load("models/intent_classifier.pkl")

# --------------------------------------------------
# Streamlit Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="AI Banking Support & Fraud Intelligence",
    page_icon="🏦",
    layout="wide"
)

# --------------------------------------------------
# Header
# --------------------------------------------------
st.title("🏦 AI Banking Support & Fraud Intelligence")
st.markdown(
    """
AI-powered banking assistant for fraud detection,
customer support, and fraud intelligence.
"""
)

# --------------------------------------------------
# Example Queries
# --------------------------------------------------
with st.expander("Example Queries"):
    st.markdown("""
- Someone transferred ₹50,000 from my account without permission.
- I forgot my internet banking password and cannot login.
- My KYC verification failed after uploading documents.
- What is the status of my home loan application?
- My debit card was used for purchases I didn't make.
""")

# --------------------------------------------------
# Sidebar Inputs
# --------------------------------------------------
with st.sidebar:

    st.header("Transaction Information")

    amount = st.number_input(
        "Transaction Amount (₹)",
        min_value=0.0,
        value=0.0
    )

    is_international = st.checkbox(
        "International Transaction"
    )

    failed_logins = st.number_input(
        "Failed Login Attempts",
        min_value=0,
        value=0
    )

    unusual_location = st.checkbox(
        "Unusual Location"
    )

    account_age = st.number_input(
        "Account Age (days)",
        min_value=0,
        value=365
    )

# --------------------------------------------------
# Customer Query
# --------------------------------------------------
query = st.text_area(
    "Enter Customer Query",
    placeholder="Example: Someone transferred ₹50,000 from my account without permission."
)

# --------------------------------------------------
# Analyze Button
# --------------------------------------------------
if st.button("Analyze Query"):

    if query.strip() == "":
        st.warning("Please enter a customer query.")
        st.stop()

    query_lower = query.lower()

    # --------------------------------------------------
    # Intent Classification
    # --------------------------------------------------
    intent = intent_model.predict([query])[0]

    # --------------------------------------------------
    # Account Access Override
    # --------------------------------------------------
    account_access_keywords = [
        "locked out",
        "cannot login",
        "cannot log in",
        "unable to login",
        "unable to log in",
        "otp not received",
        "not receiving otp",
        "cannot receive otp",
        "mobile banking app",
        "account locked",
        "password reset"
    ]

    if any(word in query_lower for word in account_access_keywords):
        intent = "Account Access"

    # --------------------------------------------------
    # Fraud Override
    # --------------------------------------------------
    fraud_keywords = [
        "fraud",
        "unauthorized",
        "phishing",
        "sms scam",
        "fake sms",
        "clicked a link",
        "malicious link",
        "scam",
        "stolen",
        "compromised",
        "hack",
        "hacked",
        "suspicious transaction",
        "card stolen",
        "credential theft",
        "fake website",
        "account blocked message"
    ]

    if any(keyword in query_lower for keyword in fraud_keywords):
        intent = "Fraud/Unauthorized"

    # --------------------------------------------------
    # Sentiment Analysis
    # --------------------------------------------------
    sentiment_result = predict_sentiment(query)

    sentiment = sentiment_result["sentiment"]
    confidence = sentiment_result["confidence"]

    # --------------------------------------------------
    # Banking Sentiment Override
    # --------------------------------------------------
    negative_keywords = [
        "fraud",
        "scam",
        "unauthorized",
        "stolen",
        "phishing",
        "hack",
        "blocked",
        "compromised",
        "fake sms",
        "otp",
        "pin"
    ]

    if any(word in query_lower for word in negative_keywords):
        sentiment = "negative"
        confidence = 0.99

    # --------------------------------------------------
    # RAG Retrieval
    # --------------------------------------------------
    retrieved_docs = retrieve_context(query)

    # --------------------------------------------------
    # Risk Assessment
    # --------------------------------------------------
    risk_result = calculate_risk(
        intent=intent,
        sentiment=sentiment,
        amount=amount,
        is_international=is_international,
        failed_login_attempts=failed_logins,
        unusual_location=unusual_location,
        account_age_days=account_age
    )

    # --------------------------------------------------
    # Action Recommendation
    # --------------------------------------------------
    actions = get_actions(
        risk_result["risk_level"],
        intent
    )

    # --------------------------------------------------
    # Results
    # --------------------------------------------------
    st.divider()

    st.header("Analysis Results")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Intent", intent)

    with col2:
        st.metric("Sentiment", sentiment.title())

    with col3:
        st.metric(
            "Confidence",
            f"{confidence*100:.1f}%"
        )

    with col4:
        st.metric(
            "Risk Score",
            risk_result["risk_score"]
        )

    with col5:
        st.metric(
            "Risk Level",
            risk_result["risk_level"]
        )

    # --------------------------------------------------
    # Risk Indicator
    # --------------------------------------------------
    if risk_result["risk_level"] == "Critical":
        st.error(
            f"🚨 Risk Level: {risk_result['risk_level']}"
        )

    elif risk_result["risk_level"] == "High":
        st.warning(
            f"⚠️ Risk Level: {risk_result['risk_level']}"
        )

    elif risk_result["risk_level"] == "Medium":
        st.info(
            f"ℹ️ Risk Level: {risk_result['risk_level']}"
        )

    else:
        st.success(
            f"✅ Risk Level: {risk_result['risk_level']}"
        )

    # --------------------------------------------------
    # Risk Factors
    # --------------------------------------------------
    st.subheader("Risk Factors")

    if risk_result["risk_reasons"]:
        for reason in risk_result["risk_reasons"]:
            st.write(f"• {reason}")
    else:
        st.success("No significant risk factors detected.")

    # --------------------------------------------------
    # Recommended Actions
    # --------------------------------------------------
    st.subheader("Recommended Actions")

    for action in actions:
        st.write(f"✅ {action}")

    # --------------------------------------------------
    # Retrieved Banking Knowledge
    # --------------------------------------------------
    st.subheader("📚 Retrieved Banking Knowledge")

    for i, doc in enumerate(retrieved_docs, 1):

        source = doc.metadata.get(
            "source",
            "Unknown"
        )

        with st.expander(
            f"Knowledge Source {i} ({source})"
        ):
            st.write(doc.page_content)

    # --------------------------------------------------
    # AI Summary
    # --------------------------------------------------
    st.subheader("AI Summary")

    summary = f"""
Customer query classified as **{intent}**
with **{sentiment} sentiment**.

Overall fraud risk score is
**{risk_result['risk_score']}**
resulting in a
**{risk_result['risk_level']}**
risk level.

Recommended operational actions have been
generated automatically for banking staff review.
"""

    st.info(summary)

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown("---")

st.caption(
    """
Built using Streamlit, Hugging Face Transformers,
FAISS, LangChain, Scikit-Learn and MySQL.
"""
)