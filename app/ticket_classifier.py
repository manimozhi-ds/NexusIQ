import streamlit as st

def classify_ticket(text):
    text = text.lower()

    if any(word in text for word in ["bill", "charged", "payment", "invoice", "refund"]):
        return "Billing Issue", "High"

    elif any(word in text for word in ["internet", "network", "slow", "connection", "wifi"]):
        return "Technical Issue", "High"

    elif any(word in text for word in ["login", "password", "account", "profile"]):
        return "Account Issue", "Medium"

    elif any(word in text for word in ["cancel", "leave", "terminate", "unsubscribe"]):
        return "Cancellation Request", "High"
    
    elif any(word in text for word in ["ticket", "booking", "date", "reschedule", "change", "flight","reservation"]):
        return "Booking Issue", "Medium"

    else:
        return "General Support", "Low"


def show_ticket_classifier():
    st.header("Support Ticket Analytics")

    ticket = st.text_area("Enter customer support ticket")

    if st.button("Classify Ticket"):
        category, priority = classify_ticket(ticket)

        st.subheader("Ticket Intelligence Result")
        st.write(f"**Category:** {category}")
        st.write(f"**Priority:** {priority}")

        if priority == "High":
            st.error("Recommended action: Escalate to support team immediately.")
        elif priority == "Medium":
            st.warning("Recommended action: Assign to customer support queue.")
        else:
            st.success("Recommended action: Handle through standard support workflow.")