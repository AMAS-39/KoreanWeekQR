import pandas as pd

def check_data_issues():
    print("🔍 Checking for data issues in Excel file...")
    
    df = pd.read_excel('korea_week_split(1).xlsx')
    print(f"Total rows: {len(df)}")
    
    issues_found = []
    
    for i, row in df.iterrows():
        email = str(row.get('email', '')).strip()
        name = str(row.get('fullName', '')).strip()
        
        # Check for invalid emails
        if email and '@' not in email and email != 'nan':
            issues_found.append(f"Row {i}: {name} - Invalid email: {email}")
        
        # Check for empty names
        if not name or name == 'nan':
            issues_found.append(f"Row {i}: Empty name")
    
    print(f"\nFound {len(issues_found)} potential issues:")
    for issue in issues_found:
        print(f"  ❌ {issue}")
    
    if not issues_found:
        print("  ✅ No obvious data issues found")
    
    # Test the exact processing logic
    print(f"\n🔍 Testing processing logic...")
    participants_data = {}
    
    for i, row in df.iterrows():
        email = str(row.get('email', '')).strip()
        name = str(row.get('fullName', '')).strip()
        
        if not name or name == 'nan':
            print(f"  Skipping row {i}: Empty name")
            continue
        
        # Generate ID
        if email and email != 'nan' and '@' in email:
            id_string = email.lower()
        else:
            id_string = name.lower()
        
        import hashlib
        participant_id = hashlib.md5(id_string.encode()).hexdigest()[:8]
        
        participants_data[participant_id] = {
            'id': participant_id,
            'fullName': name,
            'email': email,
            'selectedDay': row.get('selectedDay', '')
        }
        
        if len(participants_data) <= 15:
            print(f"  Row {i}: {name} - ID: {participant_id}")
    
    print(f"\n✅ Successfully processed: {len(participants_data)} participants")
    
    return len(participants_data)

if __name__ == "__main__":
    check_data_issues()
