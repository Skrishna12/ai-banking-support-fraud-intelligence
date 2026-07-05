def get_actions(risk_level, intent):

    actions = []

    # -------------------------
    # Critical Risk
    # -------------------------
    if risk_level == "Critical":

        actions = [
            "Block all cards immediately.",
            "Freeze customer account temporarily.",
            "Escalate to fraud investigation team.",
            "Reset internet banking credentials.",
            "Notify customer via SMS and email.",
            "Generate Suspicious Activity Report."
        ]

    # -------------------------
    # High Risk
    # -------------------------
    elif risk_level == "High":

        if intent == "Fraud/Unauthorized":

            actions = [
                "Block card immediately.",
                "Raise fraud dispute case.",
                "Escalate to fraud operations team.",
                "Issue provisional credit if eligible.",
                "Request customer identity verification."
            ]

        elif intent == "Account Access":

            actions = [
                "Lock account temporarily.",
                "Force password reset.",
                "Enable additional authentication."
            ]

        else:

            actions = [
                "Escalate case to support team.",
                "Request additional verification."
            ]

    # -------------------------
    # Medium Risk
    # -------------------------
    elif risk_level == "Medium":

        if intent == "KYC":

            actions = [
                "Request updated KYC documents.",
                "Verify PAN and Aadhaar details.",
                "Schedule manual verification."
            ]

        elif intent == "Loan":

            actions = [
                "Request additional income documents.",
                "Forward application to loan officer."
            ]

        else:

            actions = [
                "Create support ticket.",
                "Monitor customer activity."
            ]

    # -------------------------
    # Low Risk
    # -------------------------
    else:

        actions = [
            "Provide customer information.",
            "Continue normal service processing.",
            "No escalation required."
        ]

    return actions


# Testing only
if __name__ == "__main__":

    actions = get_actions(
        "Critical",
        "Fraud/Unauthorized"
    )

    print("\nRecommended Actions:\n")

    for action in actions:
        print("-", action)