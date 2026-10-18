# 🛡️ Tanglish Scam Shield

Detects scam messages written in Tamil, English, and Tanglish
(code-mixed), and explains *why* a message is risky in simple Tamil.

## Problem
Most scam detectors work only for English. In Tamil Nadu, scam
messages (fake KYC, EB bill, OTP requests) often come in Tanglish,
and elders and first-time digital payment users fall for them.

## Goal
Given a text message, classify it as:
- `scam`
- `suspicious`
- `safe`

and give a short Tamil explanation.

## MVP Scope
- ✅ Text messages only (SMS / WhatsApp paste)
- ❌ Not in MVP: voice calls, images, notification reading

## Scam Types Covered
1. Fake KYC / bank account block
2. OTP / UPI PIN request
3. Lottery / prize / gift
4. Fake job offer / part-time income
5. EB bill / electricity disconnection

## Dataset
- Anonymized and synthetic messages (no real names, numbers, links)
- Placeholders used: `[PHONE]`, `[LINK]`, `[NAME]`, `[ACCOUNT]`
- Format: `text,label,scam_type,language`

## Tech Stack (planned)
Python, Scikit-learn / DistilBERT, Flutter, Firebase

## Status
🚧 Step 1: Scope + dataset (in progress)

## Author
Jothi S