"""
generate_dataset.py
--------------------
Builds a labeled dataset of spam / ham (not spam) emails and saves it to
data/spam_dataset.csv

This uses template-based generation with randomized filler content so the
final dataset has real variety (hundreds of unique emails) without needing
an internet connection to download a dataset.
"""

import csv
import random

random.seed(42)

# ---------------------------------------------------------------------------
# SPAM building blocks
# ---------------------------------------------------------------------------
spam_subjects = [
    "You have WON a prize!!!", "Claim your free reward now",
    "URGENT: Your account will be suspended", "Congratulations Winner",
    "Limited time offer - act now", "Get rich quick with this one trick",
    "You are pre-approved for a loan", "Free gift card waiting for you",
    "Your PayPal account has been locked", "Make $5000 a week from home",
    "Exclusive deal just for you", "Verify your bank account immediately",
    "You've been selected for a cash prize", "Hot singles in your area",
    "Lowest price on medication guaranteed", "Your package could not be delivered",
    "Final notice: unpaid invoice", "Work from home and earn big",
    "Your Amazon order needs verification", "Double your Bitcoin investment today",
]

spam_bodies = [
    "Dear Winner, you have been selected to receive {amount} in cash. "
    "Click the link below within 24 hours to claim your reward before it expires. "
    "Act now, this offer will not last!",

    "Congratulations! Your email address has won our {amount} lottery draw. "
    "To release your funds, send your full name, address and bank details to "
    "our claims department immediately.",

    "URGENT ACTION REQUIRED: We detected unusual activity on your account. "
    "Verify your identity now by clicking the secure link or your account will "
    "be permanently suspended within 24 hours.",

    "Hello, this is your final notice. You owe {amount} on an unpaid invoice. "
    "Pay immediately using the link below to avoid legal action and extra fees.",

    "Make {amount} per week working from home! No experience needed. "
    "Just sign up today, enter your credit card for a small processing fee, "
    "and start earning instantly. Limited spots available!",

    "You have been pre-approved for a loan of {amount} with 0% interest! "
    "No credit check required. Click here now to claim your cash before this "
    "amazing offer disappears forever.",

    "Buy cheap medication online, no prescription needed! Huge discounts up to "
    "90% off. Fast, discreet shipping worldwide. Order now and save big, "
    "limited stock available!!!",

    "Your account has been locked due to suspicious login attempts. Click the "
    "link below and enter your username and password to restore full access "
    "immediately or your account will be deleted.",

    "CONGRATULATIONS!!! You are today's lucky visitor. You've won a brand new "
    "iPhone and {amount} cash. Claim your free gift now by clicking the link, "
    "offer expires in 10 minutes!",

    "Invest just {amount} in our crypto program today and watch it double in "
    "48 hours guaranteed! Thousands are already earning passive income, don't "
    "miss out, click now to join!",

    "Dear Customer, we could not deliver your package. Pay a small redelivery "
    "fee of {amount} by clicking the link below within 24 hours or the item "
    "will be returned to sender.",

    "Hot deal alert! Get {amount} off your next purchase, plus a free bonus "
    "gift. Click below, enter your card details and checkout now before this "
    "flash sale ends tonight!",

    "This is not a scam! Real people are earning {amount} a month from their "
    "phone. Click the link, register with your email and bank info, and start "
    "cashing out today.",

    "Your subscription payment of {amount} failed. Update your billing "
    "information immediately by clicking the secure link below to avoid "
    "service interruption.",

    "Single people in your area want to meet you tonight! Sign up free now "
    "and start chatting, no credit card required for the first {amount} of "
    "credits!",
]

amounts = ["$1,000,000", "$5,000", "$10,000", "$500", "$50,000", "$2,500",
           "$999", "$25,000", "£10,000", "€8,000", "$100,000", "$750"]

spam_signoffs = [
    "\nClick here to claim now: http://bit.ly/claim-reward",
    "\nVerify now: http://secure-login-update.com",
    "\nAct fast, offer expires soon! http://free-cash-now.net",
    "\nDo not reply to this email. Visit http://winners-portal.info to proceed.",
    "\nCall now: 1-800-555-0199 or click http://money-fast.biz",
]

# ---------------------------------------------------------------------------
# HAM (legitimate) building blocks
# ---------------------------------------------------------------------------
ham_subjects = [
    "Meeting reschedule for tomorrow", "Project update - Q3 report",
    "Lunch this weekend?", "Notes from today's class",
    "Invoice #4521 for your records", "Reminder: Dentist appointment",
    "Team standup notes", "Happy birthday!",
    "Flight itinerary confirmation", "Question about the assignment",
    "Weekly newsletter - tech digest", "Your order has shipped",
    "Draft for review", "Family dinner this Sunday",
    "Feedback on the proposal", "Interview confirmation",
    "Photos from the trip", "Book club next Thursday",
    "Server maintenance notice", "Thank you for your purchase",
]

ham_bodies = [
    "Hi {name}, just wanted to confirm we're still on for the meeting at "
    "{time} tomorrow. Let me know if you need to move it. Talk soon!",

    "Hey, here are the notes from today's lecture. I also attached the "
    "slides in case you missed anything. Let me know if you have questions "
    "before the exam.",

    "Hello {name}, attached is the invoice for last month's services. "
    "Payment is due within 30 days. Please let us know if you have any "
    "questions about the charges.",

    "Hi team, quick reminder that our standup is at {time} today. Please "
    "come prepared with updates on your current tasks. See everyone then.",

    "Hey {name}, happy birthday! Hope you have an amazing day. Let's grab "
    "lunch sometime this week to celebrate properly.",

    "Hi, this is a confirmation of your flight itinerary. Departure is at "
    "{time} on Friday. Please arrive at the airport at least two hours "
    "early. Safe travels!",

    "Hi Professor, I had a question about problem 3 on the assignment. "
    "Could we go over it briefly during office hours this week? Thanks in "
    "advance.",

    "Hello {name}, thanks for shopping with us. Your order has shipped and "
    "should arrive within 3-5 business days. You can track it using the "
    "link in your account dashboard.",

    "Hey, here's the draft document for your review. Let me know your "
    "thoughts and any edits before {time}. Appreciate the feedback as "
    "always.",

    "Hi {name}, are we still on for family dinner this Sunday at {time}? "
    "Mom is making her famous lasagna, would be great to see you.",

    "Hi, thanks for submitting your proposal. Overall it looks solid, I've "
    "left a few comments in the shared doc. Let's discuss during our call "
    "on {time}.",

    "Hello {name}, this is to confirm your interview scheduled for {time}. "
    "The interview will be conducted over video call, link attached. Good "
    "luck!",

    "Hey, sharing the photos from our trip last week, they turned out "
    "great! Let me know which ones you'd like printed for the album.",

    "Hi everyone, our book club meets this Thursday at {time} to discuss "
    "the first half of the novel. Looking forward to the discussion.",

    "This is a scheduled maintenance notice. Our servers will be down for "
    "updates on {time}. We apologize for any inconvenience this may cause.",

    "Hi {name}, thank you for your recent purchase. Your receipt is "
    "attached for your records. Reach out if you have any questions about "
    "your order.",
]

names = ["Alex", "Priya", "Sam", "Jordan", "Maria", "Chris", "Aisha", "Liam",
         "Wei", "Fatima", "Noah", "Sofia", "Ravi", "Emma", "Diego"]
times = ["9:00 AM", "2:30 PM", "11:00 AM", "4:00 PM", "10:15 AM", "6:00 PM",
         "Monday morning", "Friday afternoon", "12:00 PM", "3:45 PM"]

ham_signoffs = [
    "\nBest,\nSarah", "\nThanks,\nJohn", "\nCheers,\nEmma", "\nRegards,\nDavid",
    "\nSee you then,\nMike", "\nTalk soon,\nLisa", "",
]


def build_row(subject, body_template, filler_pool, signoff_pool, label):
    body = body_template.format(
        amount=random.choice(amounts) if "{amount}" in body_template else "",
        name=random.choice(names) if "{name}" in body_template else "",
        time=random.choice(times) if "{time}" in body_template else "",
    )
    signoff = random.choice(signoff_pool)
    text = f"{subject}. {body}{signoff}"
    return {"text": text, "label": label}


def main(n_per_class=180):
    rows = []
    for _ in range(n_per_class):
        subject = random.choice(spam_subjects)
        body = random.choice(spam_bodies)
        rows.append(build_row(subject, body, amounts, spam_signoffs, "spam"))

    for _ in range(n_per_class):
        subject = random.choice(ham_subjects)
        body = random.choice(ham_bodies)
        rows.append(build_row(subject, body, names, ham_signoffs, "ham"))

    random.shuffle(rows)

    # de-duplicate exact repeats while keeping variety high
    seen = set()
    unique_rows = []
    for r in rows:
        if r["text"] not in seen:
            seen.add(r["text"])
            unique_rows.append(r)

    with open("data/spam_dataset.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["text", "label"])
        writer.writeheader()
        writer.writerows(unique_rows)

    print(f"Generated {len(unique_rows)} unique emails "
          f"({sum(1 for r in unique_rows if r['label']=='spam')} spam, "
          f"{sum(1 for r in unique_rows if r['label']=='ham')} ham)")


if __name__ == "__main__":
    main()
