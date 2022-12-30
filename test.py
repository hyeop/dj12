from gtts import gTTS
from googletrans import Translator

tr = Translator()

st = """I’ve written too many negative stories about digital media platforms in recent months. I’ve started to worry. Am I turning into Dr. Doom and Mr. Gloom?

In all fairness, my predictions have proven sadly accurate. After I served up these dismal forecasts for Facebook, Spotify, Netflix, and others, their share prices took a steep dive.

I’m not sure that’s a good thing—I’d like to see digital media improve and flourish. When they falter, we all pay a price. But each of these companies is now suffering for a good reason. Their dominance led to arrogance, and they decided to impose all sorts of heavy-handed policies on users.

But I finally have good news to share. I have a positive case study—and we can learn from it.

Here’s the surprise: This company has been a failure at digital media, and has succeeded by embracing the most antiquated technology of them all: the printed book.

That’s quite an achievement. So let’s look at the turnaround at Barnes & Noble."""

a = tr.translate(st, src="en", dest="ko")
tts = gTTS(a.text, lang="ko")
tts.save('china.mp3')