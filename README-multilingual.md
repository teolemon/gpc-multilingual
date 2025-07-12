# Multilingual Google Product Taxonomy

This repository contains a **multilingual version** of the Google Product Taxonomy that combines all language variants with Wikidata mappings, transformed from individual monolingual taxonomy files.

## 📊 Overview

- **Total Categories**: 5,595
- **Languages**: 19 (cs-CZ, da-DK, de-CH, de-DE, en-AU, en-GB, en-US, es-ES, fr-CH, fr-FR, it-IT, ja-JP, nl-NL, no-NO, pl-PL, pt-BR, ru-RU, sv-SE, tr-TR)  
- **Wikidata Coverage**: 5,592 categories (99.9%) have Wikidata mappings
- **Hierarchy Levels**: Up to 8 levels deep

## 📁 Files Generated

### Core Output Files

1. **`multilingual-taxonomy.txt`** (11MB) - Compact pipe-separated format for easy parsing
2. **`multilingual-taxonomy-formatted.txt`** (12MB) - Human-readable formatted version
3. **`multilingual-taxonomy.json`** (13MB) - Structured JSON for programmatic use  
4. **`multilingual-taxonomy-sample.txt`** (32KB) - Sample showing the first 20 categories

### Source Processing Scripts

- **`create_multilingual_taxonomy.py`** - Creates the pipe-separated format
- **`create_formatted_taxonomy.py`** - Creates human-readable and JSON formats
- **`create_sample.py`** - Creates the sample file

## 🌍 Structure

Each category entry contains:

- **Category ID**: Unique Google Product Category identifier
- **Hierarchy Level**: Depth in the taxonomy tree (1-8)
- **Wikidata URI**: Link to corresponding Wikidata entity (if available)
- **Wikidata Label**: Human-readable label from Wikidata
- **Translations**: Category name and full path in all 19 languages

## 💡 Example Entry

```
Category ID: 1
Hierarchy Level: 1
Wikidata: http://www.wikidata.org/entity/Q116957923
Wikidata Label: animal or pet supply
Languages:
  cs-CZ: Chovatelství
  da-DK: Dyr og tilbehør til kæledyr
  de-CH: Tiere & Tierbedarf
  de-DE: Tiere & Tierbedarf
  en-AU: Animals & Pet Supplies
  en-GB: Animals & Pet Supplies
  en-US: Animals & Pet Supplies
  es-ES: Productos para mascotas y animales
  fr-CH: Animaux et articles pour animaux de compagnie
  fr-FR: Animaux et articles pour animaux de compagnie
  it-IT: Articoli per animali
  ja-JP: ペット・ペット用品
  nl-NL: Dieren
  no-NO: Dyr og kjæledyrutstyr
  pl-PL: Zwierzęta i artykuły dla zwierząt
  pt-BR: Animais e suprimentos para animais de estimação
  ru-RU: Животные и товары для питомцев
  sv-SE: Djur och tillbehör till husdjur
  tr-TR: Hayvanlar ve Evcil Hayvan Ürünleri
```

## 🔗 JSON Structure

```json
{
  "metadata": {
    "total_categories": 5595,
    "languages": ["cs-CZ", "da-DK", ...],
    "wikidata_mappings": 5592
  },
  "categories": {
    "1": {
      "hierarchy_level": 1,
      "wikidata_uri": "http://www.wikidata.org/entity/Q116957923",
      "wikidata_label": "animal or pet supply",
      "translations": {
        "en-US": "Animals & Pet Supplies",
        "fr-FR": "Animaux et articles pour animaux de compagnie",
        "de-DE": "Tiere & Tierbedarf",
        ...
      }
    }
  }
}
```

## 🚀 Usage

### Load JSON in Python
```python
import json

with open('multilingual-taxonomy.json', 'r', encoding='utf-8') as f:
    taxonomy = json.load(f)

# Get category in specific language
category_1_french = taxonomy['categories']['1']['translations']['fr-FR']
print(category_1_french)  # "Animaux et articles pour animaux de compagnie"
```

### Parse Pipe-Separated Format
```python
with open('multilingual-taxonomy.txt', 'r', encoding='utf-8') as f:
    for line in f:
        if line.startswith('#') or not line.strip():
            continue
        parts = line.strip().split(' | ')
        category_id = parts[0]
        hierarchy_level = parts[1] 
        wikidata_uri = parts[2]
        translations = parts[3:]  # Each is "lang:category_path"
```

## 📋 Source Files

The multilingual taxonomy was generated from:

- **19 monolingual taxonomy files**: `taxonomy-with-ids.{lang}.txt`
- **Wikidata mappings**: `query.csv` containing mappings from category IDs to Wikidata entities

## ⚙️ Generation Process

1. **Parse** all 19 monolingual taxonomy files to extract category hierarchies
2. **Parse** `query.csv` to extract Wikidata entity mappings  
3. **Merge** all language versions using English (en-US) as the base hierarchy
4. **Sort** categories by hierarchy depth and ID for proper ordering
5. **Generate** multiple output formats (TXT, JSON, formatted)

## 🎯 Use Cases

- **E-commerce platforms**: Multilingual product categorization
- **Search engines**: Cross-language product understanding  
- **Data analysis**: Multilingual product taxonomy research
- **Machine learning**: Training multilingual classification models
- **Internationalization**: Consistent product categories across markets

## 📈 Statistics

| Metric | Value |
|--------|-------|
| Total Categories | 5,595 |
| Languages | 19 |
| Wikidata Coverage | 99.9% |
| Max Hierarchy Depth | 8 levels |
| Output Formats | 4 (TXT, JSON, formatted, sample) |

## 🏗️ Technical Details

- **Encoding**: UTF-8 throughout
- **Base Language**: English (en-US) for hierarchy structure
- **Ordering**: By hierarchy depth, then by category ID
- **Error Handling**: Malformed entries in source files are skipped with logging
- **Memory Efficiency**: Streaming processing for large files

---

*Generated from Google Product Taxonomy data with Wikidata entity mappings.*