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

# ---------- Tanglish scam ----------
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

# ---------- Tanglish safe (includes tricky ones) ----------
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
    # Looks scary (KYC / EB / OTP words) but is NOT a scam
    "tricky": [
        "Ungal EB bill Rs.{n} pay panna last date 20th. Official TNPDCL app la pay pannunga.",
        "Ungal {bank} credit card bill Rs.{n} due on 25th. Official app la pay pannunga.",
        "Amma, KYC update panna bank ku poganum, naalaiku varuviya?",
        "Dei, OTP vanthucha? Naan anuppiten, check pannu.",
        "Amma, EB bill katta sonnanga. Naalaiku office la pay pannidren.",
    ],
}

# ---------- Tamil script ----------
SCAM_TA = {
    "kyc": [
        "{bank} KYC காலாவதியாகிவிட்டது. 24 மணி நேரத்திற்குள் புதுப்பிக்காவிட்டால் கணக்கு முடக்கப்படும். {link}",
        "உங்கள் {bank} வங்கி கணக்கு இன்று இரவு முடக்கப்படும். KYC புதுப்பிக்க {link} கிளிக் செய்யவும்",
        "உங்கள் PAN கார்டு புதுப்பிக்கப்படவில்லை. கணக்கு நிறுத்தப்படும். உடனே {phone} அழைக்கவும்",
    ],
    "otp": [
        "நான் {bank} அதிகாரி பேசுகிறேன். உங்கள் மொபைலுக்கு வந்த OTP ஐ சொல்லுங்கள்.",
        "உங்கள் UPI PIN காலாவதியாகிவிட்டது. புதிய PIN அமைக்க பழைய PIN ஐ அனுப்பவும்.",
    ],
    "lottery": [
        "வாழ்த்துக்கள்! நீங்கள் {amt} பரிசு வென்றுள்ளீர்கள். பெற {link} கிளிக் செய்யவும்.",
        "உங்கள் எண்ணுக்கு {amt} பரிசு விழுந்துள்ளது. கட்டணம் ரூ.{fee} செலுத்தவும் {phone}",
    ],
    "job": [
        "வீட்டிலிருந்தே வேலை! தினமும் ரூ.{ret} சம்பாதிக்கலாம். WhatsApp {phone}",
        "பகுதி நேர வேலை: ரூ.{fee} செலுத்துங்கள், ஒரு மணி நேரத்தில் ரூ.{ret} திரும்ப கிடைக்கும். {link}",
    ],
    "eb": [
        "உங்கள் மின் இணைப்பு இன்று இரவு துண்டிக்கப்படும். உடனே {phone} அழைக்கவும்",
        "மின் கட்டணம் நிலுவையில் உள்ளது. அபராதம் தவிர்க்க {link} மூலம் செலுத்துங்கள்.",
    ],
}

SAFE_TA = [
    "உங்கள் மின் கட்டணம் ரூ.{n} செலுத்தப்பட்டது. நன்றி. - TNPDCL",
    "உங்கள் OTP {otp}. யாரிடமும் பகிர வேண்டாம்.",
    "உங்கள் {bank} கணக்கில் ரூ.{n} வரவு வைக்கப்பட்டது. இருப்பு ரூ.{bal}.",
    "நாளைக்கு மாலை {hr} மணிக்கு சந்திக்கலாமா?",
    "உங்கள் ஆர்டர் #{oid} இன்று டெலிவரி ஆகும்.",
]

# ---------- English ----------
SCAM_EN = {
    "kyc": [
        "Your {bank} account will be blocked today. Update KYC now {link}",
        "Dear customer, your {bank} KYC has expired. Update within 24 hours or your account will be frozen. {link}",
    ],
    "otp": [
        "Share the OTP sent to your phone to complete verification.",
        "This is {bank} officer. Please tell me the OTP you just received.",
    ],
    "lottery": [
        "Congratulations! You won {amt}. Claim your prize at {link}",
    ],
    "job": [
        "Earn Rs.{ret} daily from home. Pay Rs.{fee} registration fee. WhatsApp {phone}",
    ],
    "eb": [
        "Your electricity will be disconnected tonight. Call {phone} immediately.",
    ],
}

SAFE_EN = [
    "Rs.{n} debited from your {bank} account. Avl bal Rs.{bal}.",
    "{otp} is your OTP for login. Do not share with anyone. {bank} never asks for OTP.",
    "Your order #{oid} is out for delivery today.",
]


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


def make(templates, label, stype, n, lang="tanglish"):
    seen, tries = set(), 0
    while len(seen) < n and tries < n * 50:
        tries += 1
        seen.add(noise(fill(random.choice(templates))))
    rows.extend((t, label, stype, lang) for t in seen)


for stype, templates in SCAM.items():
    make(templates, "scam", stype, 40)
for stype, templates in SAFE.items():
    make(templates, "safe", "none", 30)
for stype, templates in SCAM_TA.items():
    make(templates, "scam", stype, 30, "tamil")
make(SAFE_TA, "safe", "none", 40, "tamil")
for stype, templates in SCAM_EN.items():
    make(templates, "scam", stype, 20, "english")
make(SAFE_EN, "safe", "none", 30, "english")

df = pd.DataFrame(rows, columns=["text", "label", "scam_type", "language"])
df = df.sample(frac=1, random_state=42)
df.to_csv("data/raw/generated.csv", index=False, encoding="utf-8")
print(df.shape)
print(df["label"].value_counts())
print(df["language"].value_counts())