import re

# (regex, Tanglish explanation, Tamil script explanation)
RULES = [
    (r"\[link\]|http|bit\.ly|click",
     "Link click panna sollidhu",
     "இணைப்பை கிளிக் செய்ய சொல்கிறது"),
    (r"otp|\bpin\b|cvv",
     "OTP / PIN / CVV kekkudhu. Bank idhai eppavum kekkaadhu",
     "OTP / PIN / CVV கேட்கிறது. வங்கி இதை ஒருபோதும் கேட்காது"),
    (r"udane|inniki ratri|24 hours|immediately|today|tonight|urgent|இன்று|உடனே|மணி நேர",
     "Urgent nu bayamuruthudhu, yosikka neram tharala",
     "அவசரம் என்று பயமுறுத்துகிறது, யோசிக்க நேரம் தரவில்லை"),
    (r"block|suspend|freeze|disconnect|cut aagum|close aagum|முடக்க|துண்டிக்க|நிறுத்தப்படும்",
     "Account / connection cut aagum nu mirattudhu",
     "கணக்கு / இணைப்பு துண்டிக்கப்படும் என்று மிரட்டுகிறது"),
    (r"deposit|fee|registration|processing|gpay|கட்டணம்",
     "Panam anuppa sollidhu",
     "பணம் அனுப்ப சொல்கிறது"),
    (r"lottery|prize|lucky|congratulations|gift|free|பரிசு|வாழ்த்துக்கள்",
     "Prize / gift aasai kaattudhu",
     "பரிசு / இலவசம் என்று ஆசை காட்டுகிறது"),
    (r"work from home|part-time|part time|per task|telegram|வேலை",
     "Easy ah panam sambaadhikalaam nu sollidhu",
     "எளிதாக பணம் சம்பாதிக்கலாம் என்கிறது"),
]

ADVICE = {
    "scam": (
        "Link click pannadheenga. OTP / PIN yaarukkum sollaadheenga. Bank oda official number ku neengale call pannunga.",
        "இணைப்பை கிளிக் செய்யாதீர்கள். OTP / PIN யாரிடமும் சொல்லாதீர்கள். வங்கியின் அதிகாரப்பூர்வ எண்ணை நீங்களே அழைக்கவும்.",
    ),
    "suspicious": (
        "Confirm aagura varaikkum nambaadheenga. Official app / website la nerukku check pannunga.",
        "உறுதியாகும் வரை நம்பாதீர்கள். அதிகாரப்பூர்வ ஆப் / இணையதளத்தில் நேரடியாக சரிபாருங்கள்.",
    ),
    "safe": (
        "Risk illa maathiri theriyudhu. Aanaalum OTP yaarukkum share pannadheenga.",
        "ஆபத்து இல்லை போல் தெரிகிறது. இருந்தாலும் OTP யாருடனும் பகிராதீர்கள்.",
    ),
}


def explain(message, label):
    """Returns (reasons, advice). Each is a list/tuple of (tanglish, tamil)."""
    text = message.lower()
    reasons = []
    if label != "safe":
        for pattern, tanglish, tamil in RULES:
            if re.search(pattern, text):
                reasons.append((tanglish, tamil))
    return reasons, ADVICE[label]