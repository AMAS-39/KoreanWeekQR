import pandas as pd
import hashlib
import json

def debug_vercel_loading():
    """Test the exact same loading logic as app.py"""
    try:
        print("🔍 Starting Vercel debug test...")
        
        # Load Excel file
        df = pd.read_excel('korea_week_split(1).xlsx')
        print(f"📊 Excel file loaded: {len(df)} rows")
        
        participants_data = {}
        processed_count = 0
        skipped_count = 0
        
        for index, row in df.iterrows():
            # Generate consistent ID based on email and name (same as app.py)
            email = str(row.get('email', '')).strip()
            name = str(row.get('fullName', '')).strip()
            
            # Skip if no name
            if not name or name == 'nan':
                skipped_count += 1
                continue
            
            # Create a consistent hash-based ID (same as app.py)
            if email and email != 'nan':
                id_string = email.lower()
            else:
                id_string = name.lower()
            
            participant_id = hashlib.md5(id_string.encode()).hexdigest()[:8]
            
            # Clean activities data (same as app.py)
            activities = row.get('activities', '')
            if isinstance(activities, str):
                if activities.startswith('["') and activities.endswith('"]'):
                    activities = activities.replace('"', '').replace('[', '').replace(']', '').split(',')
                elif activities:
                    activities = [activities.strip()]
                else:
                    activities = []
            else:
                activities = []
            
            participants_data[participant_id] = {
                'id': participant_id,
                'fullName': name,
                'age': row.get('age', ''),
                'email': email,
                'phone': str(row.get('phone', '')),
                'city': row.get('city', ''),
                'selectedDay': row.get('selectedDay', ''),
                'activities': activities,
                'dietary': row.get('dietary', ''),
                'emergencyName': row.get('emergencyName', ''),
                'emergencyPhone': str(row.get('emergencyPhone', '')),
                'emergencyRelation': row.get('emergencyRelation', ''),
                'checked_in': False,
                'check_in_time': None
            }
            processed_count += 1
        
        print(f"✅ Successfully processed: {processed_count} participants")
        print(f"❌ Skipped: {skipped_count} rows")
        print(f"📋 Final participants in dictionary: {len(participants_data)}")
        
        # Show sample data
        print("\n📝 Sample participants:")
        for i, (pid, pdata) in enumerate(list(participants_data.items())[:5]):
            print(f"  {i+1}. {pdata['fullName']} - ID: {pid} - Email: {pdata['email']}")
        
        # Check for any issues
        print(f"\n🔍 Analysis:")
        print(f"  - Excel rows: {len(df)}")
        print(f"  - Processed: {processed_count}")
        print(f"  - Skipped: {skipped_count}")
        print(f"  - Final count: {len(participants_data)}")
        
        if len(participants_data) < 100:
            print(f"⚠️  WARNING: Only {len(participants_data)} participants loaded!")
            print("   This might be the issue with Vercel.")
        
        return len(participants_data)
        
    except Exception as e:
        print(f"❌ Error during debug: {e}")
        import traceback
        traceback.print_exc()
        return 0

if __name__ == "__main__":
    debug_vercel_loading()
