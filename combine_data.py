import pandas as pd
import os

def combine_all_leads(output_file="leads.csv"):
    files = ["snupit_leads.csv", "cylex_leads.csv", "maps_leads.csv"]
    all_data = []

    print("Combining data files...")
    for f in files:
        if os.path.exists(f):
            try:
                df = pd.read_csv(f)
                # Ensure consistent columns
                if 'phone' not in df.columns:
                    df['phone'] = "N/A"
                if 'website' not in df.columns:
                    df['website'] = "N/A"
                
                # Reorder columns for consistency
                cols = ['name', 'phone', 'website', 'source']
                # Add missing columns if any
                for col in cols:
                    if col not in df.columns:
                        df[col] = "N/A"
                
                all_data.append(df[cols])
            except Exception as e:
                print(f"Warning: Could not read {f}: {e}")
        else:
            print(f"Note: {f} not found, skipping.")

    if not all_data:
        print("No data found to combine.")
        return

    combined_df = pd.concat(all_data, ignore_index=True)
    
    # Pre-cleaning: drop duplicates based on Name
    before_count = len(combined_df)
    combined_df.drop_duplicates(subset="name", keep="first", inplace=True)
    after_count = len(combined_df)

    combined_df.to_csv(output_file, index=False)
    print(f"Successfully combined {after_count} unique leads (dropped {before_count - after_count} duplicates).")
    print(f"Final leads saved to {output_file}")

if __name__ == "__main__":
    combine_all_leads()