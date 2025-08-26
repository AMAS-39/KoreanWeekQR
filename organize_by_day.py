#!/usr/bin/env python3
"""
Organize participants by day and create separate Excel files
"""

import pandas as pd
import os

def organize_participants_by_day():
    """Organize participants by day and create separate files"""
    print("📊 Organizing participants by day...")
    
    try:
        # Load the main Excel file
        df = pd.read_excel('korea_week_split(1).xlsx')
        
        # Get unique days
        days = df['selectedDay'].unique()
        print(f"📅 Found {len(days)} days: {list(days)}")
        
        # Create separate files for each day
        for day in days:
            if pd.isna(day) or day == '':
                continue
                
            # Filter participants for this day
            day_participants = df[df['selectedDay'] == day]
            
            # Create filename
            filename = f"korea_week_{day.lower().replace(' ', '_')}.xlsx"
            
            # Save to Excel
            day_participants.to_excel(filename, index=False)
            
            print(f"✅ Created {filename} with {len(day_participants)} participants")
        
        # Show summary
        print("\n📋 Summary by day:")
        for day in days:
            if pd.isna(day) or day == '':
                continue
            count = len(df[df['selectedDay'] == day])
            print(f"  {day}: {count} participants")
        
        print(f"\n🎉 Organization complete! Check the new Excel files.")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def show_day_summary():
    """Show summary of participants by day"""
    print("📊 Showing participant summary by day...")
    
    try:
        df = pd.read_excel('korea_week_split(1).xlsx')
        
        print("\n📋 Participants by Day:")
        print("-" * 40)
        
        for day in sorted(df['selectedDay'].unique()):
            if pd.isna(day) or day == '':
                continue
            count = len(df[df['selectedDay'] == day])
            print(f"{day}: {count} participants")
        
        total = len(df)
        print("-" * 40)
        print(f"Total: {total} participants")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🇰🇷 Korea Week 2025 - Participant Organization")
    print("=" * 50)
    
    print("\nWhat would you like to do?")
    print("1. Show participant summary by day")
    print("2. Create separate Excel files by day")
    print("3. Exit")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        show_day_summary()
    elif choice == "2":
        organize_participants_by_day()
    elif choice == "3":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice.")
