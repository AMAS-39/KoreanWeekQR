#!/usr/bin/env python3
"""
Check current participant data
"""

import pandas as pd

def check_data():
    try:
        df = pd.read_excel('korea_week_split(1).xlsx')
        
        print("📊 Current Participant Data:")
        print("=" * 50)
        print(f"Total participants: {len(df)}")
        
        # Check days
        days = df['selectedDay'].unique()
        print(f"\n📅 Days found: {list(days)}")
        
        # Count by day
        print("\n📋 Participants by Day:")
        for day in sorted(days):
            if pd.isna(day) or day == '':
                continue
            count = len(df[df['selectedDay'] == day])
            print(f"  {day}: {count} participants")
        
        # Check emails
        valid_emails = df[df['email'].notna() & (df['email'] != '')]
        print(f"\n📧 Participants with emails: {len(valid_emails)}")
        
        # Show first few participants
        print("\n👥 First 5 participants:")
        for i, row in df.head().iterrows():
            print(f"  {i+1}. {row['fullName']} - {row['selectedDay']} - {row['email']}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_data()
