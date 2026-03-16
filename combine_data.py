import pandas as pd
import os
from utils import is_social_only

def calculate_priority(row):
    score = 0
    
    # 1. Website Status (Highest priority: No Website)
    website = str(row.get('website', 'N/A'))
    if website == "N/A":
        score += 10
    elif is_social_only(website):
        score += 5
        
    # 2. Contactability
    phone = str(row.get('phone', 'N/A'))
    if phone != "N/A" and len(phone) > 5:
        score += 5
        
    # 3. Data Quality (Found in multiple sources)
    # This is handled during aggregation below
        
    return score

def combine_all_leads(output_file="leads.csv"):
    files = ["snupit_leads.csv", "cylex_leads.csv", "maps_leads.csv"]
    all_data = []

    print("Combining data files...")
    for f in files:
        if os.path.exists(f):
            try:
                df = pd.read_csv(f)
                all_data.append(df)
            except Exception as e:
                print(f"Warning: Could not read {f}: {e}")
        else:
            print(f"Note: {f} not found, skipping.")

    if not all_data:
        print("No data found to combine.")
        return

    combined_df = pd.concat(all_data, ignore_index=True)
    
    # Track how many sources each business was found in
    source_counts = combined_df.groupby('name')['source'].count().reset_index()
    source_counts.columns = ['name', 'source_count']

    # Pre-cleaning: drop duplicates based on Name
    before_count = len(combined_df)
    combined_df.drop_duplicates(subset="name", keep="first", inplace=True)
    
    # Merge source counts back
    combined_df = combined_df.merge(source_counts, on='name', how='left')
    
    # Calculate Priority Score
    combined_df['priority_score'] = combined_df.apply(calculate_priority, axis=1)
    
    # Add bonus for multiple sources (+2 per occurrence after the first)
    combined_df['priority_score'] += (combined_df['source_count'] - 1) * 2
    
    # Sort by score (Descending)
    combined_df.sort_values(by='priority_score', ascending=False, inplace=True)
    
    # Clean up columns for output
    final_cols = ['name', 'phone', 'website', 'priority_score', 'source']
    # Ensure all columns exist
    for col in final_cols:
        if col not in combined_df.columns:
            combined_df[col] = "N/A"
            
    combined_df = combined_df[final_cols]
    after_count = len(combined_df)

    combined_df.to_csv(output_file, index=False)
    print(f"Successfully combined {after_count} unique leads (dropped {before_count - after_count} duplicates).")
    print(f"Leads sorted by Priority Score. Final file: {output_file}")

if __name__ == "__main__":
    combine_all_leads()