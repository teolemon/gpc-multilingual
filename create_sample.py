#!/usr/bin/env python3
"""
Script to create a sample of the formatted multilingual taxonomy file.
"""

import os
import csv
import re
import json
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


def create_sample_taxonomy():
    """Create a sample of the multilingual taxonomy file."""
    
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
            
        categories = parse_taxonomy_file(file_path)
        all_languages[lang_code] = categories
        all_category_ids.update(categories.keys())
    
    # Parse wikidata mappings
    wikidata_mappings = parse_query_csv('query.csv')
    
    # Use English as the base structure for hierarchy
    base_lang = 'en-US'
    base_hierarchy = build_hierarchy_structure(all_languages[base_lang])
    
    # Get first 20 categories sorted by depth then by ID
    sample_categories = sorted(
        list(all_category_ids)[:50],  # Take first 50 and then sort them
        key=lambda cat_id: (
            base_hierarchy.get(cat_id, {}).get('depth', 999),
            cat_id
        )
    )[:20]  # Take first 20 after sorting
    
    # Create the sample output
    output_lines = []
    output_lines.append("# Sample Multilingual Google Product Taxonomy")
    output_lines.append("# Generated from monolingual files with wikidata mappings")
    output_lines.append("")
    output_lines.append(f"# Sample shows first 20 categories out of {len(all_category_ids)} total")
    output_lines.append(f"# Languages: {len(all_languages)} ({', '.join(sorted(all_languages.keys()))})")
    output_lines.append(f"# Categories with Wikidata: {len(wikidata_mappings)}")
    output_lines.append("")
    output_lines.append("=" * 80)
    output_lines.append("")
    
    for category_id in sample_categories:
        # Get hierarchy info from base language
        hierarchy_info = base_hierarchy.get(category_id, {})
        depth = hierarchy_info.get('depth', 0)
        
        # Get wikidata mapping if available
        wikidata_info = wikidata_mappings.get(category_id, {})
        wikidata_uri = wikidata_info.get('uri', 'N/A')
        wikidata_label = wikidata_info.get('label', 'N/A')
        
        # Start the entry
        output_lines.append(f"Category ID: {category_id}")
        output_lines.append(f"Hierarchy Level: {depth}")
        
        if wikidata_uri != 'N/A':
            output_lines.append(f"Wikidata: {wikidata_uri}")
            output_lines.append(f"Wikidata Label: {wikidata_label}")
        else:
            output_lines.append("Wikidata: Not available")
        
        output_lines.append("Languages:")
        
        # Collect and sort translations
        for lang_code in sorted(all_languages.keys()):
            if category_id in all_languages[lang_code]:
                category_name = all_languages[lang_code][category_id]
                output_lines.append(f"  {lang_code}: {category_name}")
        
        output_lines.append("")
        output_lines.append("-" * 40)
        output_lines.append("")
    
    # Write the sample output file
    output_file = 'multilingual-taxonomy-sample.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))
    
    print(f"Created sample file: {output_file}")


if __name__ == "__main__":
    create_sample_taxonomy()