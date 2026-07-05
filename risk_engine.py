def calculate_risk(
        intent,
        sentiment,
        amount=0,
        is_international=False,
        failed_login_attempts=0,
        unusual_location=False,
        account_age_days=365
):
    risk_score = 0
    reasons = []

    # -----------------------
    # Intent Risk
    # -----------------------
    if intent == "Fraud/Unauthorized":
        risk_score += 50
        reasons.append(
            "Fraud-related customer intent detected"
        )

    elif intent == "Account Access":
        risk_score += 20
        reasons.append(
            "Account access issue detected"
        )

    elif intent == "KYC":
        risk_score += 10
        reasons.append(
            "KYC verification request"
        )

    elif intent == "Loan":
        risk_score += 5
        reasons.append(
            "Loan-related query"
        )

    # -----------------------
    # Sentiment Risk
    # -----------------------
    if sentiment == "negative":
        risk_score += 30
        reasons.append(
            "Negative customer sentiment"
        )

    elif sentiment == "neutral":
        risk_score += 10

    # -----------------------
    # Transaction Amount
    # -----------------------
    if amount >= 500000:
        risk_score += 40
        reasons.append(
            "Very high transaction amount"
        )

    elif amount >= 100000:
        risk_score += 30
        reasons.append(
            "High transaction amount"
        )

    elif amount >= 50000:
        risk_score += 20
        reasons.append(
            "Moderately high transaction amount"
        )

    elif amount >= 10000:
        risk_score += 10
        reasons.append(
            "Elevated transaction amount"
        )

    # -----------------------
    # International Transaction
    # -----------------------
    if is_international:
        risk_score += 20
        reasons.append(
            "International transaction detected"
        )

    # -----------------------
    # Failed Login Attempts
    # -----------------------
    if failed_login_attempts >= 5:
        risk_score += 25
        reasons.append(
            "Multiple failed login attempts"
        )

    elif failed_login_attempts >= 3:
        risk_score += 15
        reasons.append(
            "Several failed login attempts"
        )

    # -----------------------
    # Unusual Location
    # -----------------------
    if unusual_location:
        risk_score += 20
        reasons.append(
            "Transaction from unusual location"
        )

    # -----------------------
    # New Account Risk
    # -----------------------
    if account_age_days < 30:
        risk_score += 15
        reasons.append(
            "Recently opened account"
        )

    # -----------------------
    # Final Classification
    # -----------------------
    if risk_score >= 90:
        risk_level = "Critical"

    elif risk_score >= 60:
        risk_level = "High"

    elif risk_score >= 30:
        risk_level = "Medium"

    else:
        risk_level = "Low"

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "risk_reasons": reasons
    }


# Testing only
if __name__ == "__main__":

    result = calculate_risk(
        intent="Fraud/Unauthorized",
        sentiment="negative",
        amount=150000,
        is_international=True,
        failed_login_attempts=5,
        unusual_location=True,
        account_age_days=10
    )

    print(result)