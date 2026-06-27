import re, html
from django import forms
from .models import ContactMessage

_INPUT = (
    "w-full bg-white/5 border border-white/10 text-white placeholder-white/30 "
    "rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-cyan-400 "
    "focus:ring-1 focus:ring-cyan-400 transition-all duration-200 backdrop-blur-sm"
)
_TEXTAREA = (
    "w-full bg-white/5 border border-white/10 text-white placeholder-white/30 "
    "rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-cyan-400 "
    "focus:ring-1 focus:ring-cyan-400 transition-all duration-200 backdrop-blur-sm resize-none"
)

class ContactForm(forms.ModelForm):
    SPAM_KEYWORDS = ["casino", "viagra", "lottery", "winner", "buy now", "free offer"]
    URL_PATTERN = re.compile(r"https?://|www\.", re.IGNORECASE)

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"class": _INPUT, "placeholder": "Your full name", "maxlength": 150}),
            "email": forms.EmailInput(attrs={"class": _INPUT, "placeholder": "your@email.com"}),
            "subject": forms.TextInput(attrs={"class": _INPUT, "placeholder": "What is this about?", "maxlength": 300}),
            "message": forms.Textarea(attrs={"class": _TEXTAREA, "placeholder": "Tell me about your project or idea...", "rows": 6, "maxlength": 3000}),
        }

    def sanitise(self, v): 
        return html.escape(v.strip())

    def _check_spam(self, v, field):
        for kw in self.SPAM_KEYWORDS:
            if kw in v.lower():
                raise forms.ValidationError(f"Your {field} looks like spam.")
        return v

    def clean_name(self):
        n = self.sanitise(self.cleaned_data["name"])
        if len(n) < 2: 
            raise forms.ValidationError("Name too short.")
        if not re.match(r"^[\w\s\-\x27\.]+$", n):
            raise forms.ValidationError("Name has invalid characters.")
        return n

    def clean_email(self):
        e = self.cleaned_data["email"].strip().lower()
        bad = ["mailinator.com", "10minutemail.com", "guerrillamail.com"]
        if e.split("@")[-1] in bad:
            raise forms.ValidationError("Disposable emails not accepted.")
        return e

    def clean_subject(self):
        s = self.sanitise(self.cleaned_data["subject"])
        if len(s) < 5: 
            raise forms.ValidationError("Subject too short.")
        return self._check_spam(s, "subject")

    def clean_message(self):
        m = self.sanitise(self.cleaned_data["message"])
        if len(m) < 20: 
            raise forms.ValidationError("Write at least 20 characters.")
        if len(m) > 3000: 
            raise forms.ValidationError("Message too long (max 3000).")
        if self.URL_PATTERN.search(m):
            raise forms.ValidationError("URLs are not allowed in messages.")
        return self._check_spam(m, "message")