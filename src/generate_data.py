import random
import pandas as pd

random.seed(42)

banks = ["SBI", "HDFC", "ICICI", "Canara Bank", "Indian Bank", "IOB", "Axis Bank"]
greets = ["Dear customer,", "Sir,", "Madam,", "Dear user,", "Anna,", ""]
times = ["inniki ratri", "naalaikku", "24 hours kulla", "indha vaaram", "udane"]
links = ["[LINK]", "bit.ly/[LINK]", "http://[LINK]"]
phones = ["[PHONE]", "+91 [PHONE]"]
amts = ["Rs.25,00,000", "Rs.10 lakh", "Rs.5,00,000", "Rs.50,000"]
gifts = ["iPhone", "Smart TV", "Laptop", "gold coin"]
cos = ["Amazon", "Flipkart", "YouTube", "Instagram"]

SCAM = {
    "kyc": [
        "{g} ungal {bank} account {time} block aagidum. KYC update panna inga click pannunga {link}",
        "{bank} KYC expire aagiduchu. {time} update pannala na account freeze aagum. {link}",
        "{g} ungal {bank} account suspend aagum. PAN update panna {phone} ku call pannunga",
        "{bank} alert: KYC pending. {time} update pannunga illa na account close aagum {link}",
    ],
    "otp": [
        "{g} naan {bank} officer pesuren. Ungal mobile ku vandha OTP sollunga, account verify pannanum.",
        "{bank}: Ungal UPI PIN expire aagiduchu. Pudhu PIN set panna old PIN reply pannunga.",
        "Refund {amt} varum. OTP ah {phone} ku share pannunga {link}",
        "{g} card block aagama irukka CVV and OTP anuppunga.",
    ],
    "lottery": [
        "Congratulations! Neenga {amt} lucky draw la jeichirukeenga. Claim panna {link} click pannunga.",
        "{g} ungal number ku {amt} prize vandhirukku. Processing fee Rs.{fee} anuppunga {phone}",
        "Free {gift} ungalukku! {time} mattum, register pannunga {link}",
    ],
    "job": [
        "Work from home job! Dhinam Rs.{ret} sambaadhikalaam. WhatsApp {phone}",
        "Part-time job: Rs.{fee} deposit pannunga, 1 hour la Rs.{ret} thirumba kidaikkum. {link}",
        "{co} la product rating panna Rs.{task} per task. Telegram group join pannunga {link}",
    ],
    "eb": [
        "TNEB: Ungal current bill pending. {time} connection cut aagum. Udane {phone} ku call pannunga.",
        "EB office: Meter reading update pannala. Fine thavirkka inga pay pannunga {link}",
        "{g} ungal EB bill update pannala. Power disconnection {time}. {link}",
    ],
}

SAFE = {
    "bank_alert": [
        "Ungal account Rs.{n} debit aagirukku at [NAME] Store. Avl bal Rs.{bal}. - {bank}",
        "Rs.{n} credited to your {bank} account. Avl bal Rs.{bal}.",
        "Ungal {bank} account la Rs.{n} UPI payment success. Ref no {oid}.",
    ],
    "otp_real": [
        "Ungal OTP {otp}. Idhai yaaridamum share pannadheenga. Valid for 10 mins.",
        "{otp} is your OTP for {bank} login. Do not share with anyone.",
        "{otp} thaan ungal verification code. Yaarukkum sollaadheenga.",
    ],
    "delivery": [
        "Ungal order #{oid} inniki delivery aagum. Delivery partner: [NAME].",
        "Ungal {co} parcel out for delivery. OTP {otp} delivery boy ku mattum kudunga.",
        "Order #{oid} dispatch aayiduchu. Naalaikku ungal veetu ku varum.",
    ],
    "eb_paid": [
        "Ungal EB bill Rs.{n} payment received. Thank you. - TNPDCL",
        "TNPDCL: Bill payment Rs.{n} success. Receipt {oid}.",
    ],
    "chat": [
        "Anna, naalaiku {hr} mani ku meet pannalaam, okva?",
        "Amma, naan office la irundhu kelamburen. Dinner ku vandhuduven.",
        "Dei, exam timetable vandhucha? Hall ticket download pannitiya?",
        "Reminder: Naalaiku {hr} AM ku doctor appointment irukku.",
        "Bro, project submission naalaiku, nee mudichitiya?",
    ],
}


def fill(t):
    return t.format(
        g=random.choice(greets), bank=random.choice(banks),
        time=random.choice(times), link=random.choice(links),
        phone=random.choice(phones), amt=random.choice(amts),
        gift=random.choice(gifts), co=random.choice(cos),
        fee=random.choice([500, 1000, 2000, 5000]),
        ret=random.choice([1500, 3000, 5000]),
        task=random.choice([50, 100, 200]),
        n=random.randint(100, 5000), bal=random.randint(1000, 90000),
        otp=random.randint(100000, 999999), oid=random.randint(1000, 9999),
        hr=random.randint(1, 11),
    )


def noise(text):
    if random.random() < 0.3:
        text = text.replace("pannunga", "panunga")
    if random.random() < 0.15:
        text = text.lower()
    if random.random() < 0.1:
        text = text.upper()
    if random.random() < 0.2:
        text += random.choice([" 🙏", " ⚠️", " !!", " URGENT"])
    return " ".join(text.split())


rows = []


def make(templates, label, stype, n):
    seen, tries = set(), 0
    while len(seen) < n and tries < n * 50:
        tries += 1
        seen.add(noise(fill(random.choice(templates))))
    rows.extend((t, label, stype, "tanglish") for t in seen)


for stype, templates in SCAM.items():
    make(templates, "scam", stype, 40)
for stype, templates in SAFE.items():
    make(templates, "safe", "none", 30)

df = pd.DataFrame(rows, columns=["text", "label", "scam_type", "language"])
df = df.sample(frac=1, random_state=42)
df.to_csv("data/raw/generated.csv", index=False, encoding="utf-8")
print(df.shape)
print(df["label"].value_counts())