# CFG'den GNF'ye Dönüştürücü

Bağlamdan Bağımsız Gramerleri (Context-Free Grammar - CFG) Greibach Normal Formuna (GNF) dönüştürmek için geliştirilmiş Python tabanlı masaüstü uygulaması.

Bu uygulama kullanıcıların JSON, TXT ve Excel formatlarında tanımlanmış gramerleri yükleyerek epsilon (ε) üretimlerini kaldırmasına, birim üretimleri temizlemesine ve grameri Greibach Normal Formuna dönüştürmesine olanak sağlar.

---

## Proje Hakkında

Biçimsel Diller ve Otomatlar ile Derleyici Tasarımı derslerinde kullanılan normal form dönüşümleri teorik olarak önemli bir yere sahiptir.

Bu proje, CFG üzerinde gerçekleştirilen temel dönüşüm işlemlerini kullanıcı dostu bir grafik arayüz üzerinden gerçekleştirmek amacıyla geliştirilmiştir.

Uygulama sayesinde kullanıcılar:

* Gramer dosyalarını yükleyebilir,
* Epsilon üretimlerini kaldırabilir,
* Birim üretimleri temizleyebilir,
* GNF dönüşümünü gerçekleştirebilir,
* Sonuçları adım adım inceleyebilir.

---

## Özellikler

### Dosya Desteği

* JSON dosyalarından gramer yükleme
* TXT dosyalarından gramer yükleme
* Excel dosyalarından gramer yükleme

### Gramer İşlemleri

* Epsilon (ε) üretimlerini kaldırma
* Birim üretimleri temizleme
* CFG dönüşümleri

### Greibach Normal Formu

* GNF dönüşümü
* Üretim kurallarının kontrolü
* GNF uygunluk doğrulaması

### Grafik Arayüz

* Tkinter tabanlı kullanıcı arayüzü
* Dosya seçme ekranı
* Sonuçların adım adım görüntülenmesi
* Dönüşüm süreçlerinin görselleştirilmesi

---

## Kullanılan Teknolojiler

* Python
* Tkinter
* JSON
* Pandas
* OpenPyXL

---

## Desteklenen Dosya Formatları

### JSON

Örnek:

```json
{
  "variables": ["S", "A", "B"],
  "terminals": ["a", "b"],
  "start": "S",
  "productions": {
    "S": [["A", "B"], ["b"]],
    "A": [["a"], ["ε"]],
    "B": [["b"]]
  }
}
```

### TXT

Örnek:

```text
S -> AB | b
A -> a | ε
B -> b
```

---

## Program Akışı

```text
Gramer Yükleme
        │
        ▼
Epsilon Temizleme
        │
        ▼
Birim Üretim Temizleme
        │
        ▼
GNF Dönüşümü
        │
        ▼
GNF Uygunluk Kontrolü
```

---

## Proje Yapısı

```text
main.py
grammar1.json
grammar2.json
ornek.txt
```

---

## Çalıştırma

Python yüklü olduğundan emin olun.

Programı çalıştırmak için:

```bash
python main.py
```

---

## Örnek İşlemler

* CFG yükleme
* ε üretimlerini kaldırma
* Birim üretimleri kaldırma
* GNF dönüşümü gerçekleştirme
* Sonuçları doğrulama

---

## Gelecek Çalışmalar

* CFG görselleştirme
* Adım adım dönüşüm animasyonları
* CNF (Chomsky Normal Form) desteği
* Dosya dışa aktarma özellikleri
* Daha gelişmiş hata kontrol mekanizmaları
* Web tabanlı sürüm

---

## Geliştirme Durumu

Proje aktif olarak geliştirilmektedir.

Mevcut sürüm:

* JSON desteği
* TXT desteği
* Excel desteği
* Epsilon temizleme
* Birim üretim temizleme
* GNF dönüşümü
* GNF uygunluk kontrolü

özelliklerini içermektedir.

---

## Lisans

Bu proje eğitim ve akademik çalışmalar amacıyla geliştirilmiştir.

---

**Geliştirici:** Melih Fındık

**Teknolojiler:** Python, Tkinter

**Konu:** Biçimsel Diller, Otomatlar ve Derleyici Tasarımı
