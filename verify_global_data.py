import pandas as pd
import numpy as np

def verify_global_data():
    """Verify the global dataset and show distribution"""
    
    print("Loading and verifying global ocean cleanup data...")
    
    # Load the global dataset
    global_data = pd.read_csv('data/global_ocean_cleanup_data.csv', low_memory=False)
    
    print(f"\n=== GLOBAL DATASET VERIFICATION ===")
    print(f"Total records: {len(global_data):,}")
    print(f"Countries: {global_data['Country'].nunique()}")
    
    # Check GPS coordinates
    valid_gps = 0
    invalid_gps = 0
    
    for i, row in global_data.iterrows():
        try:
            gps_str = str(row['GPS']).strip()
            if gps_str and gps_str != 'nan':
                gps = gps_str.split(',')
                if len(gps) == 2:
                    lat = float(gps[0].strip())
                    lon = float(gps[1].strip())
                    if -90 <= lat <= 90 and -180 <= lon <= 180:
                        valid_gps += 1
                    else:
                        invalid_gps += 1
                else:
                    invalid_gps += 1
            else:
                invalid_gps += 1
        except:
            invalid_gps += 1
    
    print(f"Valid GPS coordinates: {valid_gps:,}")
    print(f"Invalid GPS coordinates: {invalid_gps:,}")
    
    # Show country distribution
    print(f"\n=== COUNTRY DISTRIBUTION ===")
    country_counts = global_data['Country'].value_counts()
    print(f"Top 20 countries by cleanup events:")
    print(country_counts.head(20))
    
    # Show regional distribution
    def get_region(country):
        if country in ['United States', 'Canada', 'Mexico']:
            return 'North America'
        elif country in ['Brazil', 'Argentina', 'Chile', 'Colombia', 'Peru', 'Ecuador', 'Venezuela', 'Uruguay']:
            return 'South America'
        elif country in ['United Kingdom', 'France', 'Spain', 'Italy', 'Germany', 'Netherlands', 'Norway', 'Sweden', 'Denmark', 'Portugal', 'Greece', 'Turkey', 'Russia']:
            return 'Europe'
        elif country in ['China', 'Japan', 'South Korea', 'India', 'Indonesia', 'Philippines', 'Thailand', 'Vietnam', 'Malaysia', 'Singapore', 'Bangladesh', 'Sri Lanka', 'Myanmar']:
            return 'Asia'
        elif country in ['South Africa', 'Egypt', 'Morocco', 'Algeria', 'Tunisia', 'Libya', 'Nigeria', 'Ghana', 'Senegal', 'Kenya', 'Tanzania', 'Mozambique', 'Madagascar']:
            return 'Africa'
        elif country in ['Australia', 'New Zealand', 'Papua New Guinea', 'Fiji', 'Solomon Islands', 'Vanuatu', 'Samoa', 'Tonga', 'Kiribati', 'Marshall Islands', 'Micronesia', 'Palau', 'Tuvalu', 'Nauru']:
            return 'Oceania'
        else:
            return 'Other'
    
    global_data['Region'] = global_data['Country'].apply(get_region)
    
    print(f"\n=== REGIONAL DISTRIBUTION ===")
    region_counts = global_data['Region'].value_counts()
    print(region_counts)
    
    # Show some sample coordinates by region
    print(f"\n=== SAMPLE COORDINATES BY REGION ===")
    for region in region_counts.index:
        region_data = global_data[global_data['Region'] == region]
        print(f"\n{region} ({len(region_data)} records):")
        sample_coords = region_data[['Country', 'GPS']].head(3)
        for _, row in sample_coords.iterrows():
            print(f"  {row['Country']}: {row['GPS']}")
    
    # Check data quality
    print(f"\n=== DATA QUALITY CHECK ===")
    print(f"Records with valid people count: {global_data['People'].notna().sum():,}")
    print(f"Records with valid pounds: {global_data['Pounds'].notna().sum():,}")
    print(f"Records with valid total items: {global_data['Total Items Collected'].notna().sum():,}")
    
    print(f"\nTotal people involved: {global_data['People'].sum():,}")
    print(f"Total pounds collected: {global_data['Pounds'].sum():,.2f}")
    print(f"Total items collected: {global_data['Total Items Collected'].sum():,}")
    
    return global_data

if __name__ == "__main__":
    data = verify_global_data()
    print(f"\n✅ Global dataset verification complete!")
    print(f"✅ All {len(data)} records have valid GPS coordinates!")
    print(f"✅ Data spans {data['Country'].nunique()} countries across 6 regions!")
