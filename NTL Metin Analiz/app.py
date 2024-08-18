from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import spacy
from langdetect import detect
from googletrans import Translator
import tkinter as tk
from tkinter import scrolledtext

def cevir_ve_analiz_et(text):
    dil = detect(text)
    translator = Translator()
    if dil != 'en':
        text = translator.translate(text, src=dil, dest='en').text
    return text

def duygu(text):
    text=cevir_ve_analiz_et(text)
    print(text)
    analyzer = SentimentIntensityAnalyzer()
    sentiment_score = analyzer.polarity_scores(text)
    
    if sentiment_score['compound'] > 0.05:
        return "Pozitif"
    elif sentiment_score['compound'] < -0.05:
        return "Negatif"
    else:
        return "Nötr"

def metinAnalizi(text):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    toplamCumle = len(list(doc.sents))
    toplamKelime = len(doc)
    kelimeSayisi = {}
    for token in doc:
        if token.is_alpha:
            word = token.text.lower()
            if word in kelimeSayisi:
                kelimeSayisi[word] += 1
            else:
                kelimeSayisi[word] = 1
    
    ozet = ' '.join([token.text for token in doc[:100]]) + ('...' if toplamKelime > 100 else '')
    return toplamCumle, toplamKelime, kelimeSayisi, ozet

def rapor():
    text = metin_boyut.get("1.0",tk.END).strip()
    if not text:
        result_output.config(state=tk.NORMAL)
        result_output.delete(1.0, tk.END)
        result_output.insert(tk.END, "Girdi metni boş veya geçersiz")
        result_output.config(state=tk.DISABLED)
        return
    
    toplamCumle, toplamKelime, kelimeSayisi, ozet = metinAnalizi(text)
    duygu_sonuc=duygu(text)
    result_output.config(state=tk.NORMAL)
    result_output.delete(1.0, tk.END)
    result_output.insert(tk.END, f"Bu bir {duygu_sonuc} cümlesidir\n")
    result_output.insert(tk.END, f"Toplam Cümle Sayısı: {toplamCumle}\n")
    result_output.insert(tk.END, f"Toplam Kelime Sayısı: {toplamKelime}\n")
    result_output.insert(tk.END, "\nKelimelerin Tekrar Sayısı:\n")
    for word, count in kelimeSayisi.items():
        result_output.insert(tk.END, f"{word}: {count}\n")
    result_output.insert(tk.END, f"\nMetnin Özeti: {ozet}")
    result_output.config(state=tk.DISABLED)


pencere= tk.Tk()
pencere.geometry("600x450")
pencere.title("Metin Analizi ve Duygu Analizi")
metin = tk.Label(pencere, text="Metni Girin:")
metin.pack()
metin_boyut=scrolledtext.ScrolledText(pencere, wrap=tk.WORD, width=60, height=10)
metin_boyut.pack()
buton1=tk.Button(pencere,text="Analiz Et",command=rapor)
buton1.pack()
result_output = scrolledtext.ScrolledText(pencere, wrap=tk.WORD, width=60, height=15, state=tk.DISABLED)
result_output.pack()
pencere.mainloop()

