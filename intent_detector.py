"""
Intent detection — maps customer speech to one of:
  confirm | cancel | reschedule | unclear

Supports: English, Hindi, Kannada, Marathi, Telugu
"""

import re

# ── Keyword maps per language ──────────────────────────────────────────────────
INTENTS = {
    "confirm": {
        "en": ["yes", "yeah", "yep", "confirm", "ok", "okay", "sure", "absolutely",
               "correct", "right", "accept", "go ahead", "do it", "proceed"],
        "hi": ["हाँ", "हां", "ठीक", "हां जी", "बिल्कुल", "पक्का", "मंजूर", "हा", "confirm"],
        "kn": ["ಹೌದು", "ಸರಿ", "ಆಗಬಹುದು", "ಖಂಡಿತ", "ಒಪ್ಪಿಗೆ", "yes"],
        "mr": ["हो", "होय", "ठीक", "बरं", "नक्की", "मान्य", "yes"],
        "te": ["అవును", "సరే", "ఓకే", "అవు", "తప్పకుండా", "yes"],
    },
    "cancel": {
        "en": ["no", "nope", "cancel", "don't", "dont", "refuse", "nah",
               "not now", "stop", "reject", "deny", "negative"],
        "hi": ["नहीं", "नहीं चाहिए", "रद्द", "बंद करो", "मत करो", "no"],
        "kn": ["ಬೇಡ", "ಇಲ್ಲ", "ರದ್ದು", "ನಿಲ್ಲಿಸಿ", "no"],
        "mr": ["नाही", "नको", "रद्द करा", "नको आहे", "no"],
        "te": ["వద్దు", "లేదు", "రద్దు", "వద్దు అని", "no"],
    },
    "reschedule": {
        "en": ["later", "reschedule", "call back", "not now", "another time",
               "tomorrow", "wait", "hold on", "some other time"],
        "hi": ["बाद में", "कल", "थोड़ी देर बाद", "दोबारा", "later"],
        "kn": ["ನಂತರ", "ಮತ್ತೆ ಕರೆ ಮಾಡಿ", "ನಾಳೆ", "later"],
        "mr": ["नंतर", "उद्या", "थांबा", "later"],
        "te": ["తర్వాత", "రేపు", "మళ్ళీ చేయండి", "later"],
    }
}


def detect_intent(speech: str, language: str = "en") -> str:
    """
    Detect the customer's intent from transcribed speech.
    Returns: 'confirm' | 'cancel' | 'reschedule' | 'unclear'
    """
    if not speech or not speech.strip():
        return "unclear"

    text = speech.lower().strip()
    lang = language if language in ["en", "hi", "kn", "mr", "te"] else "en"

    for intent, lang_keywords in INTENTS.items():
        keywords = lang_keywords.get(lang, []) + lang_keywords.get("en", [])
        for kw in keywords:
            if kw.lower() in text:
                return intent

    # Fallback: digit-based DTMF (shouldn't reach here but safety net)
    if "1" in text:
        return "confirm"
    if "2" in text:
        return "cancel"
    if "3" in text:
        return "reschedule"

    return "unclear"


# ── Response messages per language & intent ────────────────────────────────────
RESPONSES = {
    "confirm": {
        "en": "Great! Your order has been confirmed. Thank you for your time. Have a wonderful day!",
        "hi": "बहुत अच्छा! आपका ऑर्डर पुष्टि हो गया है। धन्यवाद!",
        "kn": "ಉತ್ತಮ! ನಿಮ್ಮ ಆರ್ಡರ್ ದೃಢೀಕರಿಸಲಾಗಿದೆ. ಧನ್ಯವಾದ!",
        "mr": "छान! तुमची ऑर्डर पुष्टी झाली आहे. धन्यवाद!",
        "te": "చాలా మంచిది! మీ ఆర్డర్ నిర్ధారించబడింది. ధన్యవాదాలు!",
    },
    "cancel": {
        "en": "Understood. Your order has been cancelled. We hope to serve you again soon. Goodbye!",
        "hi": "समझ गया। आपका ऑर्डर रद्द कर दिया गया है। जल्दी फिर मिलेंगे। अलविदा!",
        "kn": "ಅರ್ಥ ಮಾಡಿಕೊಂಡೆ. ನಿಮ್ಮ ಆರ್ಡರ್ ರದ್ದುಗೊಳಿಸಲಾಗಿದೆ. ಧನ್ಯವಾದ!",
        "mr": "समजलो. तुमची ऑर्डर रद्द केली आहे. पुन्हा भेटू. निरोप!",
        "te": "అర్థమైంది. మీ ఆర్డర్ రద్దు చేయబడింది. త్వరలో మళ్ళీ కలుద్దాం!",
    },
    "reschedule": {
        "en": "No problem! We will call you again later to confirm your order. Have a great day!",
        "hi": "कोई बात नहीं। हम आपको बाद में वापस कॉल करेंगे। धन्यवाद!",
        "kn": "ಸರಿ! ನಾವು ನಿಮಗೆ ನಂತರ ಮತ್ತೆ ಕರೆ ಮಾಡುತ್ತೇವೆ. ಧನ್ಯವಾದ!",
        "mr": "ठीक आहे! आम्ही नंतर परत कॉल करू. धन्यवाद!",
        "te": "సరే! మేము మీకు తర్వాత మళ్ళీ కాల్ చేస్తాము. ధన్యవాదాలు!",
    },
    "unclear": {
        "en": "Sorry, I did not understand that. Let me repeat your order details.",
        "hi": "माफ करें, मैं समझ नहीं पाया। आपका ऑर्डर फिर से दोहराता हूं।",
        "kn": "ಕ್ಷಮಿಸಿ, ನನಗೆ ಅರ್ಥವಾಗಲಿಲ್ಲ. ನಿಮ್ಮ ಆರ್ಡರ್ ಮತ್ತೆ ಹೇಳುತ್ತೇನೆ.",
        "mr": "माफ करा, मला समजले नाही. तुमची ऑर्डर पुन्हा सांगतो.",
        "te": "క్షమించండి, నాకు అర్థం కాలేదు. మీ ఆర్డర్ మళ్ళీ చెప్తాను.",
    },
}


def get_response_message(intent: str, language: str = "en") -> str:
    """Return appropriate voice response message for given intent & language."""
    lang = language if language in ["en", "hi", "kn", "mr", "te"] else "en"
    return RESPONSES.get(intent, RESPONSES["unclear"]).get(lang, RESPONSES[intent]["en"])
