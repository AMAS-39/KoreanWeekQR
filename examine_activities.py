#!/usr/bin/env python3
"""
Examine activities data in Excel file to understand the format
"""

import pandas as pd

def examine_activities():
    """Examine the activities column to understand its format"""
    try:
        df = pd.read_excel('korea_week_split(1).xlsx')
        
        print("🔍 Examining activities data...")
        print(f"Total rows: {len(df)}")
        print("\n" + "="*50)
        
        # Show first 10 rows of activities
        for i, row in df.head(10).iterrows():
            activities = row.get('activities', '')
            full_name = row.get('fullName', '')
            print(f"\nRow {i+1}: {full_name}")
            print(f"Activities (raw): {activities}")
            print(f"Type: {type(activities)}")
            
            # Try different parsing methods
            if isinstance(activities, str):
                print(f"Length: {len(activities)}")
                print(f"Starts with '[': {activities.startswith('[') if activities else False}")
                print(f"Ends with ']': {activities.endswith(']') if activities else False}")
                
                # Method 1: Simple split
                if activities.startswith('["') and activities.endswith('"]'):
                    parsed1 = activities.replace('"', '').replace('[', '').replace(']', '').split(',')
                    print(f"Method 1 (split): {parsed1}")
                
                # Method 2: JSON parsing
                try:
                    import json
                    parsed2 = json.loads(activities)
                    print(f"Method 2 (JSON): {parsed2}")
                except:
                    print("Method 2 (JSON): Failed")
                
                # Method 3: Manual parsing
                if activities.startswith('["') and activities.endswith('"]'):
                    # Remove [" and "] and split by ","
                    content = activities[2:-2]  # Remove [" and "]
                    parsed3 = [item.strip() for item in content.split('","')]
                    print(f"Method 3 (manual): {parsed3}")
            
            print("-" * 30)
        
        # Show some examples of different formats
        print("\n" + "="*50)
        print("📊 ACTIVITIES FORMAT ANALYSIS")
        print("="*50)
        
        unique_formats = df['activities'].value_counts().head(10)
        print("\nMost common activity formats:")
        for format_str, count in unique_formats.items():
            print(f"\nFormat: {format_str}")
            print(f"Count: {count}")
            
            # Try to parse this format
            if isinstance(format_str, str) and format_str.startswith('["') and format_str.endswith('"]'):
                content = format_str[2:-2]
                parsed = [item.strip() for item in content.split('","')]
                print(f"Parsed: {parsed}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    examine_activities()
