import pandas as pd
import hashlib

def test_data_loading():
    try:
        df = pd.read_excel('korea_week_split(1).xlsx')
        print(f"Total rows in Excel: {len(df)}")
        
        participants_data = {}
        count = 0
        
        for index, row in df.iterrows():
            email = str(row.get('email', '')).strip()
            name = str(row.get('fullName', '')).strip()
            
            if not name or name == 'nan':
                continue
                
            # Generate consistent ID
            if email and email != 'nan':
                id_string = email.lower()
            else:
                id_string = name.lower()
            
            participant_id = hashlib.md5(id_string.encode()).hexdigest()[:8]
            
            participants_data[participant_id] = {
                'id': participant_id,
                'fullName': name,
                'email': email,
                'phone': str(row.get('phone', '')),
                'city': row.get('city', ''),
                'selectedDay': row.get('selectedDay', ''),
            }
            count += 1
        
        print(f"Successfully processed {count} participants")
        print(f"Participants in dictionary: {len(participants_data)}")
        
        # Show first 5 participants
        print("\nFirst 5 participants:")
        for i, (pid, pdata) in enumerate(list(participants_data.items())[:5]):
            print(f"{i+1}. {pdata['fullName']} - ID: {pid}")
            
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    test_data_loading()
