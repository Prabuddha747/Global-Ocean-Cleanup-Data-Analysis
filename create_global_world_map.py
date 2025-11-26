import pandas as pd
import folium
from folium.plugins import FastMarkerCluster, MarkerCluster, HeatMap
import numpy as np
import os
from datetime import datetime

def create_global_world_map():
    """Create a comprehensive global ocean cleanup map with all countries"""
    
    print("Loading global ocean cleanup data...")
    
    # Load the global dataset
    try:
        global_data = pd.read_csv('data/global_ocean_cleanup_data.csv', low_memory=False)
        print(f"Loaded {len(global_data)} cleanup records from {global_data['Country'].nunique()} countries")
    except FileNotFoundError:
        print("Global dataset not found. Please run generate_global_cleanup_data.py first.")
        return None
    
    # Create the global map
    print("Creating global map...")
    world_map = folium.Map(
        location=[20, 0],  # Center of the world
        tiles="cartodbdark_matter",
        zoom_start=2,
        max_bounds=True,
        max_zoom=18,
        min_zoom=1
    )
    
    # Define color scheme for different regions
    region_colors = {
        'North America': '#FF6B6B',      # Red
        'South America': '#4ECDC4',      # Teal
        'Europe': '#45B7D1',             # Blue
        'Asia': '#96CEB4',               # Green
        'Africa': '#FFEAA7',             # Yellow
        'Oceania': '#DDA0DD',            # Plum
        'Other': '#A8A8A8'               # Gray
    }
    
    # Assign regions to countries
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
    
    # Add region column
    global_data['Region'] = global_data['Country'].apply(get_region)
    
    # Create marker clusters for each region
    region_clusters = {}
    for region in region_colors.keys():
        region_clusters[region] = MarkerCluster(
            name=f"{region} Cleanup Sites",
            icon_create_function=f"""
            function(cluster) {{
                return L.divIcon({{
                    html: '<div style="background-color: {region_colors[region]}; color: white; border-radius: 50%; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; font-weight: bold;">' + cluster.getChildCount() + '</div>',
                    className: 'marker-cluster',
                    iconSize: [30, 30]
                }});
            }}
            """
        )
    
    # Sample data for performance (use every 10th record for initial map)
    sample_data = global_data[::10].copy()
    print(f"Using sample of {len(sample_data)} records for map performance")
    
    # Add markers to the map
    print("Adding cleanup sites to map...")
    for i, row in sample_data.iterrows():
        try:
            # Parse GPS coordinates
            gps = str(row['GPS']).split(',')
            lat = float(gps[0].strip())
            lon = float(gps[1].strip())
            
            # Calculate radius based on pounds collected
            pounds = row['Pounds'] if pd.notna(row['Pounds']) else 0
            radius = max(50, min(1000, pounds * 5))  # Smaller radius for global view
            
            # Get region and color
            region = row['Region']
            color = region_colors.get(region, '#A8A8A8')
            
            # Create circle marker
            folium.Circle(
                location=[lat, lon],
                radius=radius,
                popup=f"""
                <b>{region} Cleanup Site</b><br>
                <b>Country:</b> {row['Country']}<br>
                <b>Location:</b> {row['Zone']}<br>
                <b>Date:</b> {row['Cleanup Date']}<br>
                <b>Group:</b> {row['Group Name']}<br>
                <b>People:</b> {row['People']}<br>
                <b>Pounds:</b> {pounds:.2f}<br>
                <b>Total Items:</b> {row['Total Items Collected']}
                """,
                color=color,
                fillColor=color,
                fillOpacity=0.3,
                weight=1
            ).add_to(region_clusters[region])
            
        except (ValueError, IndexError) as e:
            continue
    
    # Add all clusters to the map
    for cluster in region_clusters.values():
        cluster.add_to(world_map)
    
    # Add layer control
    folium.LayerControl().add_to(world_map)
    
    # Add a comprehensive legend
    legend_html = '''
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 250px; height: 200px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:14px; padding: 10px; border-radius: 5px;">
    <h4 style="margin-top:0;">Global Ocean Cleanup Map</h4>
    <p><i class="fa fa-circle" style="color:#FF6B6B"></i> North America</p>
    <p><i class="fa fa-circle" style="color:#4ECDC4"></i> South America</p>
    <p><i class="fa fa-circle" style="color:#45B7D1"></i> Europe</p>
    <p><i class="fa fa-circle" style="color:#96CEB4"></i> Asia</p>
    <p><i class="fa fa-circle" style="color:#FFEAA7"></i> Africa</p>
    <p><i class="fa fa-circle" style="color:#DDA0DD"></i> Oceania</p>
    <p><i class="fa fa-circle" style="color:#A8A8A8"></i> Other</p>
    <hr>
    <p><small>Circle size represents pounds collected</small></p>
    </div>
    '''
    world_map.get_root().html.add_child(folium.Element(legend_html))
    
    # Save the map
    output_path = "maps/global_world_ocean_cleanup_map.html"
    world_map.save(output_path)
    print(f"Global world map saved to: {output_path}")
    
    return world_map

def create_heatmap_view():
    """Create a heatmap view of the global cleanup data"""
    
    print("Creating heatmap view...")
    
    # Load the global dataset
    try:
        global_data = pd.read_csv('data/global_ocean_cleanup_data.csv', low_memory=False)
    except FileNotFoundError:
        print("Global dataset not found. Please run generate_global_cleanup_data.py first.")
        return None
    
    # Create heatmap
    heatmap = folium.Map(
        location=[20, 0],
        tiles="cartodbdark_matter",
        zoom_start=2
    )
    
    # Prepare data for heatmap
    heat_data = []
    for i, row in global_data.iterrows():
        try:
            gps = str(row['GPS']).split(',')
            lat = float(gps[0].strip())
            lon = float(gps[1].strip())
            weight = row['Pounds'] if pd.notna(row['Pounds']) else 0
            heat_data.append([lat, lon, weight])
        except (ValueError, IndexError):
            continue
    
    # Add heatmap layer
    HeatMap(heat_data, name="Cleanup Intensity Heatmap").add_to(heatmap)
    
    # Add layer control
    folium.LayerControl().add_to(heatmap)
    
    # Save heatmap
    output_path = "maps/global_ocean_cleanup_heatmap.html"
    heatmap.save(output_path)
    print(f"Heatmap saved to: {output_path}")
    
    return heatmap

def create_country_focused_maps():
    """Create focused maps for each major region"""
    
    print("Creating country-focused maps...")
    
    # Load the global dataset
    try:
        global_data = pd.read_csv('data/global_ocean_cleanup_data.csv', low_memory=False)
    except FileNotFoundError:
        print("Global dataset not found. Please run generate_global_cleanup_data.py first.")
        return None
    
    # Define major regions with their center coordinates
    regions = {
        'North_America': {'center': [45, -100], 'countries': ['United States', 'Canada', 'Mexico']},
        'Europe': {'center': [54, 10], 'countries': ['United Kingdom', 'France', 'Spain', 'Italy', 'Germany', 'Netherlands', 'Norway', 'Sweden', 'Denmark', 'Portugal', 'Greece', 'Turkey']},
        'Asia': {'center': [35, 100], 'countries': ['China', 'Japan', 'South Korea', 'India', 'Indonesia', 'Philippines', 'Thailand', 'Vietnam', 'Malaysia', 'Singapore', 'Bangladesh', 'Sri Lanka', 'Myanmar']},
        'Africa': {'center': [0, 20], 'countries': ['South Africa', 'Egypt', 'Morocco', 'Algeria', 'Tunisia', 'Libya', 'Nigeria', 'Ghana', 'Senegal', 'Kenya', 'Tanzania', 'Mozambique', 'Madagascar']},
        'Oceania': {'center': [-25, 140], 'countries': ['Australia', 'New Zealand', 'Papua New Guinea', 'Fiji', 'Solomon Islands', 'Vanuatu', 'Samoa', 'Tonga']},
        'South_America': {'center': [-15, -60], 'countries': ['Brazil', 'Argentina', 'Chile', 'Colombia', 'Peru', 'Ecuador', 'Venezuela', 'Uruguay']}
    }
    
    for region_name, region_info in regions.items():
        print(f"Creating {region_name} focused map...")
        
        # Filter data for this region
        region_data = global_data[global_data['Country'].isin(region_info['countries'])]
        
        if len(region_data) == 0:
            continue
        
        # Create map
        region_map = folium.Map(
            location=region_info['center'],
            tiles="cartodbdark_matter",
            zoom_start=4
        )
        
        # Create marker cluster
        cluster = MarkerCluster(name=f"{region_name} Cleanup Sites")
        
        # Add markers
        for i, row in region_data.iterrows():
            try:
                gps = str(row['GPS']).split(',')
                lat = float(gps[0].strip())
                lon = float(gps[1].strip())
                
                pounds = row['Pounds'] if pd.notna(row['Pounds']) else 0
                radius = max(100, min(2000, pounds * 10))
                
                folium.Circle(
                    location=[lat, lon],
                    radius=radius,
                    popup=f"""
                    <b>{row['Country']} Cleanup Site</b><br>
                    <b>Location:</b> {row['Zone']}<br>
                    <b>Date:</b> {row['Cleanup Date']}<br>
                    <b>Group:</b> {row['Group Name']}<br>
                    <b>People:</b> {row['People']}<br>
                    <b>Pounds:</b> {pounds:.2f}<br>
                    <b>Total Items:</b> {row['Total Items Collected']}
                    """,
                    color="#FF6B6B",
                    fillColor="#FF6B6B",
                    fillOpacity=0.4,
                    weight=2
                ).add_to(cluster)
                
            except (ValueError, IndexError):
                continue
        
        cluster.add_to(region_map)
        folium.LayerControl().add_to(region_map)
        
        # Save map
        output_path = f"maps/{region_name}_ocean_cleanup_map.html"
        region_map.save(output_path)
        print(f"{region_name} map saved to: {output_path}")

def generate_statistics():
    """Generate comprehensive statistics for the global dataset"""
    
    print("Generating global statistics...")
    
    # Load the global dataset
    try:
        global_data = pd.read_csv('data/global_ocean_cleanup_data.csv', low_memory=False)
    except FileNotFoundError:
        print("Global dataset not found. Please run generate_global_cleanup_data.py first.")
        return None
    
    # Add region column if it doesn't exist
    if 'Region' not in global_data.columns:
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
    
    print(f"\n=== GLOBAL OCEAN CLEANUP STATISTICS ===")
    print(f"Total Cleanup Events: {len(global_data):,}")
    print(f"Countries Involved: {global_data['Country'].nunique()}")
    print(f"Total People Involved: {global_data['People'].sum():,}")
    print(f"Total Pounds Collected: {global_data['Pounds'].sum():,.2f}")
    print(f"Total Items Collected: {global_data['Total Items Collected'].sum():,}")
    print(f"Average Items per Cleanup: {global_data['Total Items Collected'].mean():.2f}")
    print(f"Average Pounds per Cleanup: {global_data['Pounds'].mean():.2f}")
    
    # Top countries by cleanup activity
    print(f"\n=== TOP 10 COUNTRIES BY CLEANUP ACTIVITY ===")
    country_stats = global_data.groupby('Country').agg({
        'Cleanup ID': 'count',
        'People': 'sum',
        'Pounds': 'sum',
        'Total Items Collected': 'sum'
    }).round(2)
    country_stats.columns = ['Cleanup Events', 'Total People', 'Total Pounds', 'Total Items']
    top_countries = country_stats.sort_values('Cleanup Events', ascending=False).head(10)
    print(top_countries)
    
    # Regional statistics
    print(f"\n=== REGIONAL STATISTICS ===")
    region_stats = global_data.groupby('Region').agg({
        'Cleanup ID': 'count',
        'People': 'sum',
        'Pounds': 'sum',
        'Total Items Collected': 'sum'
    }).round(2)
    region_stats.columns = ['Cleanup Events', 'Total People', 'Total Pounds', 'Total Items']
    print(region_stats)
    
    return global_data

if __name__ == "__main__":
    print("Creating comprehensive global ocean cleanup visualization...")
    
    # Generate statistics
    data = generate_statistics()
    
    if data is not None:
        # Create global world map
        world_map = create_global_world_map()
        
        # Create heatmap view
        heatmap = create_heatmap_view()
        
        # Create regional focused maps
        create_country_focused_maps()
        
        print("\n=== MAPS CREATED SUCCESSFULLY ===")
        print("Files saved:")
        print("- maps/global_world_ocean_cleanup_map.html")
        print("- maps/global_ocean_cleanup_heatmap.html")
        print("- maps/North_America_ocean_cleanup_map.html")
        print("- maps/Europe_ocean_cleanup_map.html")
        print("- maps/Asia_ocean_cleanup_map.html")
        print("- maps/Africa_ocean_cleanup_map.html")
        print("- maps/Oceania_ocean_cleanup_map.html")
        print("- maps/South_America_ocean_cleanup_map.html")
