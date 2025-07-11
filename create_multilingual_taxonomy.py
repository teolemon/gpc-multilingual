#!/usr/bin/env python3
"""
Script to create a multilingual taxonomy file from monolingual taxonomy files
and wikidata mappings.
"""

import os
import csv
import re
from collections import defaultdict, OrderedDict
from pathlib import Path


def parse_taxonomy_file(file_path):
    """Parse a single taxonomy file and extract category data."""
    categories = {}
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            # Parse format: "ID - Category > Subcategory > ..."
            match = re.match(r'^(\d+)\s*-\s*(.+)$', line)
            if match:
                category_id = int(match.group(1))
                category_path = match.group(2)
                categories[category_id] = category_path
    
    return categories


def parse_query_csv(file_path):
    """Parse the query.csv file to extract wikidata mappings."""
    wikidata_mappings = {}
    
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        
        for row in reader:
            if len(row) >= 3:
                wikidata_uri = row[0]
                label = row[1]
                try:
                    category_id = int(row[2])
                    wikidata_mappings[category_id] = {
                        'uri': wikidata_uri,
                        'label': label
                    }
                except ValueError:
                    # Skip malformed entries where category_id is not a number
                    print(f"Skipping malformed entry: {row}")
                    continue
    
    return wikidata_mappings


def extract_language_code(filename):
    """Extract language code from filename like 'taxonomy-with-ids.en-US.txt'"""
    match = re.search(r'taxonomy-with-ids\.([^.]+)\.txt$', filename)
    return match.group(1) if match else None


def build_hierarchy_structure(categories):
    """Build a hierarchical structure from category paths."""
    hierarchy = {}
    
    for category_id, path in categories.items():
        parts = [part.strip() for part in path.split(' > ')]
        
        # Store the full path and its depth
        hierarchy[category_id] = {
            'path': parts,
            'depth': len(parts),
            'full_path': path
        }
    
    return hierarchy


def create_multilingual_taxonomy():
    """Create the multilingual taxonomy file."""
    
    # Get all taxonomy files
    taxonomy_files = list(Path('.').glob('taxonomy-with-ids.*.txt'))
    
    # Parse all taxonomy files
    all_languages = {}
    all_category_ids = set()
    
    print(f"Found {len(taxonomy_files)} taxonomy files")
    
    for file_path in taxonomy_files:
        lang_code = extract_language_code(file_path.name)
        if not lang_code:
            continue
            
        print(f"Parsing {file_path.name} (language: {lang_code})")
        categories = parse_taxonomy_file(file_path)
        all_languages[lang_code] = categories
        all_category_ids.update(categories.keys())
        print(f"  Found {len(categories)} categories")
    
    # Parse wikidata mappings
    print("\nParsing query.csv for wikidata mappings...")
    wikidata_mappings = parse_query_csv('query.csv')
    print(f"Found {len(wikidata_mappings)} wikidata mappings")
    
    # Use English as the base structure for hierarchy
    base_lang = 'en-US'
    if base_lang not in all_languages:
        print(f"Warning: Base language {base_lang} not found, using first available language")
        base_lang = list(all_languages.keys())[0]
    
    base_hierarchy = build_hierarchy_structure(all_languages[base_lang])
    
    # Sort categories by depth then by ID for proper hierarchical order
    sorted_categories = sorted(
        all_category_ids,
        key=lambda cat_id: (
            base_hierarchy.get(cat_id, {}).get('depth', 999),
            cat_id
        )
    )
    
    # Create the multilingual output
    output_lines = []
    output_lines.append("# Multilingual Google Product Taxonomy")
    output_lines.append("# Generated from monolingual files with wikidata mappings")
    output_lines.append("# Format: ID | hierarchy_depth | wikidata_uri | language_code:category_name | ...")
    output_lines.append("")
    
    for category_id in sorted_categories:
        # Get hierarchy info from base language
        hierarchy_info = base_hierarchy.get(category_id, {})
        depth = hierarchy_info.get('depth', 0)
        
        # Get wikidata mapping if available
        wikidata_info = wikidata_mappings.get(category_id, {})
        wikidata_uri = wikidata_info.get('uri', '')
        
        # Collect translations from all languages
        translations = []
        for lang_code in sorted(all_languages.keys()):
            if category_id in all_languages[lang_code]:
                category_name = all_languages[lang_code][category_id]
                translations.append(f"{lang_code}:{category_name}")
        
        # Format the output line
        line_parts = [
            str(category_id),
            str(depth),
            wikidata_uri,
        ]
        line_parts.extend(translations)
        
        output_lines.append(" | ".join(line_parts))
    
    # Write the output file
    output_file = 'multilingual-taxonomy.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))
    
    print(f"\nCreated multilingual taxonomy file: {output_file}")
    print(f"Total categories: {len(sorted_categories)}")
    print(f"Languages included: {', '.join(sorted(all_languages.keys()))}")
    print(f"Categories with wikidata mappings: {len(wikidata_mappings)}")


if __name__ == "__main__":
    create_multilingual_taxonomy()