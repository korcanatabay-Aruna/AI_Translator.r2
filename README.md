# 🌿 Sutta Translator - AI Destekli Budist Metin Çevirisi

Ufuk Hoca tarzında Budist suttalara (metinlerine) otomatik Türkçe çeviri yapan yapay zeka destekli web uygulaması. LangGraph ve RAG (Retrieval-Augmented Generation) teknolojisi ile geliştirilmiştir.

## 🎯 Özellikler

- **Otomatik Çeviri**: İngilizce Pali Canon metinlerini Türkçeye çevirir
- **Stil Kontrolü**: Ufuk Hoca'nın samimi, öğretici üslubunu korur
- **RAG Teknolojisi**: Paralel çevirilerden öğrenerek tutarlılık sağlar
- **Chunk Destekli**: Uzun metinleri parçalara ayırarak işler
- **İyileştirme Döngüsü**: Çeviriyi otomatik olarak rafine eder
- **Kullanıcı Dostu Arayüz**: Gradio ile basit ve etkileşimli kullanım

## 🚀 Kurulum

### Gereksinimler

- Python 3.8+
- OpenAI API anahtarı

### Adımlar

1. **Repository'yi klonlayın:**
```bash
git clone https://github.com/korcanatabay-Aruna/AI_Translator.r2.git
cd AI_Translator.r2
```

2. **Sanal ortam oluşturun (önerilen):**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Gerekli paketleri yükleyin:**
```bash
pip install -r requirements.txt
```

4. **Ortam değişkenlerini ayarlayın:**

`.env` dosyası oluşturun ve OpenAI API anahtarınızı ekleyin:
```
OPENAI_API_KEY=your_api_key_here
```

5. **Uygulamayı başlatın:**
```bash
python app.py
```

Uygulama `http://localhost:7860` adresinde çalışacaktır.

## 📁 Proje Yapısı

```
.
├── app.py                  # Ana Gradio uygulaması
├── langgraph_workflow.py   # LangGraph iş akışı tanımları
├── rag_utils.py           # RAG ve vektör veritabanı işlemleri
├── chunking.py            # Metin parçalama fonksiyonları
├── style_checker.py       # Stil kontrol mekanizması
├── requirements.txt       # Python bağımlılıkları
├── chroma_db/            # ChromaDB vektör veritabanı
└── data/
    └── corpus/           # Referans çeviri korpusu (.docx dosyaları)
```

## 🔧 Kullanım

### Web Arayüzü

1. Uygulamayı başlatın: `python app.py`
2. Tarayıcıda açılan arayüze gidin
3. İngilizce Sutta metnini girin
4. "🔄 Çevir" butonuna tıklayın
5. Çeviriyi inceleyin:
   - "✅ Onayla": Çeviriyi kabul edin
   - "🔁 Geliştir": Çeviriyi rafine edin

### Yeni Korpus Ekleme

`data/corpus/` klasörüne yeni çeviriler ekleyebilirsiniz:

**Format:**
- İngilizce: `SN 11.25.eng.docx`
- Türkçe: `SN 11.25.tr.docx`

Örnek dosya adları:
- `DN 16.eng.docx` / `DN 16.tr.docx`
- `SN 56.11.eng.docx` / `SN 56.11.tr.docx`

## 🧠 Teknoloji Stack

- **LangGraph**: İş akışı yönetimi
- **LangChain**: LLM entegrasyonu
- **OpenAI GPT-4**: Çeviri modeli
- **ChromaDB**: Vektör veritabanı
- **Sentence Transformers**: Embedding modeli
- **Gradio**: Web arayüzü
- **Python-docx**: Word dosyası işleme

## 🎨 Çeviri Stili

Çeviriler Ufuk Hoca'nın karakteristik üslubunu takip eder:

- **Samimi ve öğretici ton**
- **Günlük dile yakın ifadeler**
- **Karakteristik kalıplar:**
  - "Duydum ki..."
  - "İzdeşler!"
  - "Kutlu Kişi"
  - "Yüceler Yücesi"

## 🔄 İş Akışı

```
1. Metin Girişi
   ↓
2. Chunking (Parçalama)
   ↓
3. RAG ile Bağlam Getirme
   ↓
4. GPT-4 ile Çeviri
   ↓
5. Stil Kontrolü
   ↓
6. [Gerekirse] İyileştirme
   ↓
7. Final Çıktı
```

## 📝 Lisans

Bu proje eğitim ve araştırma amaçlıdır.

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Pull request göndermekten çekinmeyin.

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/yeniOzellik`)
3. Commit yapın (`git commit -m 'Yeni özellik eklendi'`)
4. Push edin (`git push origin feature/yeniOzellik`)
5. Pull Request açın

## 📧 İletişim

Sorularınız için issue açabilirsiniz.

---

**Not**: Bu uygulama OpenAI API kullanır ve kullanım ücretleri uygulanır.