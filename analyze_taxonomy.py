#!/usr/bin/env python3
"""
Script to show statistics about the multilingual taxonomy files.
"""

import json
import os
from pathlib import Path


def show_file_stats():
    """Show file size and line count statistics."""
    files = [
        'multilingual-taxonomy.txt',
        'multilingual-taxonomy-formatted.txt', 
        'multilingual-taxonomy.json',
        'multilingual-taxonomy-sample.txt'
    ]
    
    print("📁 Generated Files:")
    print("=" * 50)
    
    for filename in files:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            size_mb = size / (1024 * 1024)
            
            with open(filename, 'r', encoding='utf-8') as f:
                lines = sum(1 for _ in f)
            
            print(f"{filename}:")
            print(f"  Size: {size_mb:.1f} MB ({size:,} bytes)")
            print(f"  Lines: {lines:,}")
            print()


def show_json_stats():
    """Show statistics from the JSON file."""
    json_file = 'multilingual-taxonomy.json'
    
    if not os.path.exists(json_file):
        print(f"❌ {json_file} not found")
        return
    
    print("📊 Taxonomy Statistics:")
    print("=" * 50)
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    metadata = data['metadata']
    categories = data['categories']
    
    print(f"Total Categories: {metadata['total_categories']:,}")
    print(f"Languages: {len(metadata['languages'])}")
    print(f"Wikidata Mappings: {metadata['wikidata_mappings']:,}")
    print(f"Wikidata Coverage: {metadata['wikidata_mappings']/metadata['total_categories']*100:.1f}%")
    print()
    
    print("Languages:")
    lang_list = metadata['languages']
    for i in range(0, len(lang_list), 5):
        print("  " + ", ".join(lang_list[i:i+5]))
    print()
    
    # Analyze hierarchy levels
    level_counts = {}
    for cat_data in categories.values():
        level = cat_data['hierarchy_level']
        level_counts[level] = level_counts.get(level, 0) + 1
    
    print("Hierarchy Distribution:")
    for level in sorted(level_counts.keys()):
        count = level_counts[level]
        percent = count / metadata['total_categories'] * 100
        print(f"  Level {level}: {count:,} categories ({percent:.1f}%)")
    print()
    
    # Find categories without wikidata
    no_wikidata = []
    for cat_id, cat_data in categories.items():
        if not cat_data.get('wikidata_uri'):
            no_wikidata.append(cat_id)
    
    if no_wikidata:
        print(f"Categories without Wikidata ({len(no_wikidata)}):")
        print("  " + ", ".join(no_wikidata[:20]))
        if len(no_wikidata) > 20:
            print(f"  ... and {len(no_wikidata)-20} more")
    else:
        print("✅ All categories have Wikidata mappings!")
    print()


def show_sample_entries():
    """Show a few sample entries."""
    json_file = 'multilingual-taxonomy.json'
    
    if not os.path.exists(json_file):
        return
    
    print("🔍 Sample Entries:")
    print("=" * 50)
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Show first 3 categories
    sample_ids = ['1', '2', '3']
    
    for cat_id in sample_ids:
        if cat_id in data['categories']:
            cat = data['categories'][cat_id]
            print(f"Category {cat_id} (Level {cat['hierarchy_level']}):")
            
            if cat.get('wikidata_uri'):
                print(f"  Wikidata: {cat['wikidata_label']}")
            
            # Show a few language examples
            translations = cat['translations']
            sample_langs = ['en-US', 'fr-FR', 'de-DE', 'ja-JP']
            
            for lang in sample_langs:
                if lang in translations:
                    print(f"  {lang}: {translations[lang]}")
            print()


if __name__ == "__main__":
    print("🌍 Multilingual Google Product Taxonomy")
    print("=" * 60)
    print()
    
    show_file_stats()
    show_json_stats()
    show_sample_entries()
    
    print("✅ Analysis complete!")
    print()
    print("💡 To regenerate files:")
    print("   python3 create_multilingual_taxonomy.py")
    print("   python3 create_formatted_taxonomy.py") 
    print("   python3 create_sample.py")