import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os
from cost_calculator import OceanCleanupCostCalculator, add_cost_columns_to_dataframe

def generate_global_cleanup_data():
    """Generate comprehensive global ocean cleanup data for 100+ sites per country"""
    
    # List of countries with significant coastlines and ocean cleanup activities
    countries_data = {
        # North America
        'United States': {'coastal_regions': ['California', 'Florida', 'Texas', 'New York', 'Washington', 'Oregon', 'Louisiana', 'Alaska', 'Hawaii', 'North Carolina', 'South Carolina', 'Georgia', 'Virginia', 'Maryland', 'Delaware', 'New Jersey', 'Connecticut', 'Rhode Island', 'Massachusetts', 'Maine', 'New Hampshire'], 'coastline_length': 19924},
        'Canada': {'coastal_regions': ['British Columbia', 'Newfoundland and Labrador', 'Nova Scotia', 'New Brunswick', 'Prince Edward Island', 'Quebec', 'Ontario', 'Manitoba', 'Saskatchewan', 'Alberta', 'Northwest Territories', 'Yukon', 'Nunavut'], 'coastline_length': 202080},
        'Mexico': {'coastal_regions': ['Baja California', 'Sonora', 'Sinaloa', 'Nayarit', 'Jalisco', 'Colima', 'Michoacan', 'Guerrero', 'Oaxaca', 'Chiapas', 'Tabasco', 'Campeche', 'Yucatan', 'Quintana Roo', 'Tamaulipas', 'Veracruz'], 'coastline_length': 9330},
        
        # South America
        'Brazil': {'coastal_regions': ['Rio de Janeiro', 'Sao Paulo', 'Bahia', 'Ceara', 'Pernambuco', 'Alagoas', 'Sergipe', 'Paraiba', 'Rio Grande do Norte', 'Maranhao', 'Para', 'Amapa', 'Santa Catarina', 'Parana', 'Espirito Santo'], 'coastline_length': 7491},
        'Argentina': {'coastal_regions': ['Buenos Aires', 'Rio Negro', 'Chubut', 'Santa Cruz', 'Tierra del Fuego'], 'coastline_length': 4989},
        'Chile': {'coastal_regions': ['Arica y Parinacota', 'Tarapaca', 'Antofagasta', 'Atacama', 'Coquimbo', 'Valparaiso', 'Metropolitana', 'O Higgins', 'Maule', 'Biobio', 'Araucania', 'Los Rios', 'Los Lagos', 'Aysen', 'Magallanes'], 'coastline_length': 6435},
        'Colombia': {'coastal_regions': ['Atlantico', 'Bolivar', 'Cesar', 'Cordoba', 'La Guajira', 'Magdalena', 'Sucre', 'Antioquia', 'Choco', 'Valle del Cauca', 'Cauca', 'Narino'], 'coastline_length': 3208},
        'Peru': {'coastal_regions': ['Tumbes', 'Piura', 'Lambayeque', 'La Libertad', 'Ancash', 'Lima', 'Ica', 'Arequipa', 'Moquegua', 'Tacna'], 'coastline_length': 2414},
        'Ecuador': {'coastal_regions': ['Esmeraldas', 'Manabi', 'Guayas', 'Santa Elena', 'El Oro'], 'coastline_length': 2237},
        'Venezuela': {'coastal_regions': ['Zulia', 'Falcon', 'Lara', 'Yaracuy', 'Carabobo', 'Aragua', 'Vargas', 'Miranda', 'Anzoategui', 'Sucre', 'Monagas', 'Delta Amacuro'], 'coastline_length': 2800},
        'Uruguay': {'coastal_regions': ['Rocha', 'Maldonado', 'Canelones', 'Montevideo', 'San Jose', 'Colonia', 'Soriano'], 'coastline_length': 660},
        
        # Europe
        'United Kingdom': {'coastal_regions': ['England', 'Scotland', 'Wales', 'Northern Ireland'], 'coastline_length': 12429},
        'France': {'coastal_regions': ['Brittany', 'Normandy', 'Aquitaine', 'Provence', 'Corsica', 'Occitanie', 'Nouvelle-Aquitaine', 'Pays de la Loire', 'Hauts-de-France'], 'coastline_length': 3427},
        'Spain': {'coastal_regions': ['Galicia', 'Asturias', 'Cantabria', 'Basque Country', 'Catalonia', 'Valencia', 'Murcia', 'Andalusia', 'Balearic Islands', 'Canary Islands'], 'coastline_length': 4964},
        'Italy': {'coastal_regions': ['Liguria', 'Tuscany', 'Lazio', 'Campania', 'Calabria', 'Sicily', 'Sardinia', 'Apulia', 'Abruzzo', 'Marche', 'Emilia-Romagna', 'Veneto', 'Friuli-Venezia Giulia'], 'coastline_length': 7600},
        'Germany': {'coastal_regions': ['Schleswig-Holstein', 'Lower Saxony', 'Mecklenburg-Vorpommern', 'Hamburg', 'Bremen'], 'coastline_length': 2389},
        'Netherlands': {'coastal_regions': ['North Holland', 'South Holland', 'Zeeland', 'Friesland', 'Groningen'], 'coastline_length': 451},
        'Norway': {'coastal_regions': ['Finnmark', 'Troms', 'Nordland', 'Trondelag', 'More og Romsdal', 'Vestland', 'Rogaland', 'Agder', 'Vestfold og Telemark', 'Oslo', 'Viken', 'Innlandet'], 'coastline_length': 25148},
        'Sweden': {'coastal_regions': ['Stockholm', 'Vastra Gotaland', 'Skane', 'Halland', 'Blekinge', 'Kalmar', 'Kronoberg', 'Jonkoping', 'Ostergotland', 'Sodermanland', 'Uppsala', 'Vastmanland', 'Dalarna', 'Gavleborg', 'Vasternorrland', 'Jamtland', 'Vasterbotten', 'Norrbotten'], 'coastline_length': 3218},
        'Denmark': {'coastal_regions': ['Zealand', 'Funen', 'Jutland', 'Bornholm'], 'coastline_length': 7314},
        'Portugal': {'coastal_regions': ['North', 'Center', 'Lisbon', 'Alentejo', 'Algarve', 'Azores', 'Madeira'], 'coastline_length': 1793},
        'Greece': {'coastal_regions': ['Attica', 'Central Greece', 'Thessaly', 'Epirus', 'Macedonia', 'Thrace', 'Peloponnese', 'Crete', 'Aegean Islands', 'Ionian Islands'], 'coastline_length': 13676},
        'Turkey': {'coastal_regions': ['Istanbul', 'Marmara', 'Aegean', 'Mediterranean', 'Black Sea'], 'coastline_length': 7200},
        'Russia': {'coastal_regions': ['Kaliningrad', 'Leningrad', 'Murmansk', 'Arkhangelsk', 'Karelia', 'Komi', 'Nenets', 'Yamalo-Nenets', 'Krasnoyarsk', 'Sakha', 'Chukotka', 'Kamchatka', 'Primorsky', 'Khabarovsk', 'Sakhalin', 'Magadan', 'Amur', 'Jewish Autonomous Oblast'], 'coastline_length': 37653},
        
        # Asia
        'China': {'coastal_regions': ['Liaoning', 'Hebei', 'Tianjin', 'Shandong', 'Jiangsu', 'Shanghai', 'Zhejiang', 'Fujian', 'Guangdong', 'Hainan', 'Guangxi', 'Hong Kong', 'Macau'], 'coastline_length': 14500},
        'Japan': {'coastal_regions': ['Hokkaido', 'Tohoku', 'Kanto', 'Chubu', 'Kansai', 'Chugoku', 'Shikoku', 'Kyushu', 'Okinawa'], 'coastline_length': 29751},
        'South Korea': {'coastal_regions': ['Gyeonggi', 'Incheon', 'Gangwon', 'Chungcheong', 'Jeolla', 'Gyeongsang', 'Jeju'], 'coastline_length': 2413},
        'India': {'coastal_regions': ['Maharashtra', 'Goa', 'Karnataka', 'Kerala', 'Tamil Nadu', 'Andhra Pradesh', 'Odisha', 'West Bengal', 'Gujarat', 'Daman and Diu', 'Puducherry', 'Lakshadweep', 'Andaman and Nicobar Islands'], 'coastline_length': 7516},
        'Indonesia': {'coastal_regions': ['Aceh', 'North Sumatra', 'West Sumatra', 'Riau', 'Riau Islands', 'Jambi', 'South Sumatra', 'Bangka Belitung', 'Lampung', 'Banten', 'Jakarta', 'West Java', 'Central Java', 'Yogyakarta', 'East Java', 'Bali', 'West Nusa Tenggara', 'East Nusa Tenggara', 'West Kalimantan', 'Central Kalimantan', 'South Kalimantan', 'East Kalimantan', 'North Kalimantan', 'North Sulawesi', 'Gorontalo', 'Central Sulawesi', 'West Sulawesi', 'South Sulawesi', 'Southeast Sulawesi', 'North Maluku', 'Maluku', 'West Papua', 'Papua'], 'coastline_length': 54716},
        'Philippines': {'coastal_regions': ['Ilocos', 'Cagayan Valley', 'Central Luzon', 'Calabarzon', 'Mimaropa', 'Bicol', 'Western Visayas', 'Central Visayas', 'Eastern Visayas', 'Zamboanga Peninsula', 'Northern Mindanao', 'Davao', 'Soccsksargen', 'Caraga', 'Bangsamoro', 'Cordillera', 'National Capital Region'], 'coastline_length': 36289},
        'Thailand': {'coastal_regions': ['Central', 'Eastern', 'Western', 'Southern'], 'coastline_length': 3219},
        'Vietnam': {'coastal_regions': ['Red River Delta', 'North Central Coast', 'South Central Coast', 'Southeast', 'Mekong Delta'], 'coastline_length': 3444},
        'Malaysia': {'coastal_regions': ['Perlis', 'Kedah', 'Penang', 'Perak', 'Selangor', 'Negeri Sembilan', 'Malacca', 'Johor', 'Pahang', 'Terengganu', 'Kelantan', 'Sabah', 'Sarawak', 'Labuan', 'Putrajaya'], 'coastline_length': 4675},
        'Singapore': {'coastal_regions': ['Central Region', 'East Region', 'North Region', 'Northeast Region', 'West Region'], 'coastline_length': 193},
        'Bangladesh': {'coastal_regions': ['Barisal', 'Chittagong', 'Dhaka', 'Khulna', 'Rajshahi', 'Rangpur', 'Sylhet'], 'coastline_length': 580},
        'Sri Lanka': {'coastal_regions': ['Western', 'Central', 'Southern', 'Northern', 'Eastern', 'North Western', 'North Central', 'Uva', 'Sabaragamuwa'], 'coastline_length': 1340},
        'Myanmar': {'coastal_regions': ['Rakhine', 'Ayeyarwady', 'Yangon', 'Mon', 'Kayin', 'Tanintharyi'], 'coastline_length': 1930},
        
        # Africa
        'South Africa': {'coastal_regions': ['Western Cape', 'Eastern Cape', 'KwaZulu-Natal', 'Northern Cape'], 'coastline_length': 2798},
        'Egypt': {'coastal_regions': ['Alexandria', 'Beheira', 'Kafr el-Sheikh', 'Dakahlia', 'Damietta', 'Port Said', 'Ismailia', 'Suez', 'North Sinai', 'South Sinai', 'Red Sea'], 'coastline_length': 2450},
        'Morocco': {'coastal_regions': ['Tangier-Tetouan-Al Hoceima', 'Rabat-Sale-Kenitra', 'Casablanca-Settat', 'Marrakech-Safi', 'Souss-Massa', 'Guelmim-Oued Noun', 'Laayoune-Sakia El Hamra', 'Dakhla-Oued Ed-Dahab'], 'coastline_length': 1835},
        'Algeria': {'coastal_regions': ['Tlemcen', 'Ain Temouchent', 'Oran', 'Mostaganem', 'Chlef', 'Tipaza', 'Algiers', 'Boumerdes', 'Tizi Ouzou', 'Bejaia', 'Jijel', 'Skikda', 'Annaba', 'El Tarf'], 'coastline_length': 998},
        'Tunisia': {'coastal_regions': ['Bizerte', 'Ariana', 'Tunis', 'Ben Arous', 'Nabeul', 'Sousse', 'Monastir', 'Mahdia', 'Sfax', 'Gabes', 'Medenine', 'Tataouine'], 'coastline_length': 1148},
        'Libya': {'coastal_regions': ['Tripolitania', 'Cyrenaica', 'Fezzan'], 'coastline_length': 1770},
        'Nigeria': {'coastal_regions': ['Lagos', 'Ogun', 'Ondo', 'Edo', 'Delta', 'Bayelsa', 'Rivers', 'Akwa Ibom', 'Cross River'], 'coastline_length': 853},
        'Ghana': {'coastal_regions': ['Greater Accra', 'Central', 'Western', 'Volta'], 'coastline_length': 539},
        'Senegal': {'coastal_regions': ['Dakar', 'Thies', 'Diourbel', 'Fatick', 'Kaolack', 'Kolda', 'Ziguinchor', 'Tambacounda', 'Saint-Louis', 'Matam', 'Kaffrine', 'Kedougou', 'Sedhiou'], 'coastline_length': 531},
        'Kenya': {'coastal_regions': ['Mombasa', 'Kwale', 'Kilifi', 'Tana River', 'Lamu', 'Taita-Taveta'], 'coastline_length': 536},
        'Tanzania': {'coastal_regions': ['Tanga', 'Pwani', 'Dar es Salaam', 'Lindi', 'Mtwara'], 'coastline_length': 1424},
        'Mozambique': {'coastal_regions': ['Cabo Delgado', 'Nampula', 'Zambezia', 'Sofala', 'Inhambane', 'Gaza', 'Maputo'], 'coastline_length': 2470},
        'Madagascar': {'coastal_regions': ['Antsiranana', 'Sava', 'Analanjirofo', 'Atsinanana', 'Vatovavy-Fitovinany', 'Atsimo-Atsinanana', 'Vatovavy', 'Atsimo-Andrefana', 'Androy', 'Anosy'], 'coastline_length': 4828},
        
        # Oceania
        'Australia': {'coastal_regions': ['Western Australia', 'South Australia', 'Victoria', 'Tasmania', 'New South Wales', 'Queensland', 'Northern Territory', 'Australian Capital Territory'], 'coastline_length': 25760},
        'New Zealand': {'coastal_regions': ['Northland', 'Auckland', 'Waikato', 'Bay of Plenty', 'Gisborne', 'Hawke Bay', 'Taranaki', 'Manawatu-Wanganui', 'Wellington', 'Tasman', 'Nelson', 'Marlborough', 'West Coast', 'Canterbury', 'Otago', 'Southland'], 'coastline_length': 15134},
        'Papua New Guinea': {'coastal_regions': ['Central', 'Gulf', 'Milne Bay', 'Oro', 'Western', 'West New Britain', 'East New Britain', 'New Ireland', 'Manus', 'Madang', 'Morobe', 'East Sepik', 'West Sepik', 'Sandaun', 'Enga', 'Southern Highlands', 'Hela', 'Jiwaka', 'Chimbu', 'Eastern Highlands', 'Western Highlands'], 'coastline_length': 5152},
        'Fiji': {'coastal_regions': ['Central', 'Eastern', 'Northern', 'Western'], 'coastline_length': 1129},
        'Solomon Islands': {'coastal_regions': ['Central', 'Choiseul', 'Guadalcanal', 'Isabel', 'Makira-Ulawa', 'Malaita', 'Rennell and Bellona', 'Temotu', 'Western'], 'coastline_length': 5313},
        'Vanuatu': {'coastal_regions': ['Torba', 'Sanma', 'Penama', 'Malampa', 'Shefa', 'Tafea'], 'coastline_length': 2528},
        'Samoa': {'coastal_regions': ['Upolu', 'Savaii'], 'coastline_length': 403},
        'Tonga': {'coastal_regions': ['Tongatapu', 'Vava u', 'Ha apai', 'Eua', 'Niuas'], 'coastline_length': 419},
        'Kiribati': {'coastal_regions': ['Gilbert Islands', 'Phoenix Islands', 'Line Islands'], 'coastline_length': 1143},
        'Marshall Islands': {'coastal_regions': ['Ralik Chain', 'Ratak Chain'], 'coastline_length': 370},
        'Micronesia': {'coastal_regions': ['Yap', 'Chuuk', 'Pohnpei', 'Kosrae'], 'coastline_length': 6112},
        'Palau': {'coastal_regions': ['Koror', 'Aimeliik', 'Airai', 'Melekeok', 'Ngaraard', 'Ngarchelong', 'Ngardmau', 'Ngatpang', 'Ngchesar', 'Ngeremlengui', 'Ngiwal', 'Peleliu', 'Sonsorol'], 'coastline_length': 1519},
        'Tuvalu': {'coastal_regions': ['Funafuti', 'Nanumanga', 'Nanumea', 'Niutao', 'Nui', 'Nukufetau', 'Nukulaelae', 'Vaitupu'], 'coastline_length': 24},
        'Nauru': {'coastal_regions': ['Yaren', 'Anabar', 'Anetan', 'Anibare', 'Baiti', 'Boe', 'Buada', 'Denigomodu', 'Ewa', 'Ijuw', 'Meneng', 'Uaboe', 'Ijuw'], 'coastline_length': 30}
    }
    
    # Generate cleanup data for each country
    all_cleanup_data = []
    cleanup_id_counter = 1
    
    for country, info in countries_data.items():
        print(f"Generating data for {country}...")
        
        # Determine number of cleanup sites (100-200 per country based on coastline length)
        num_sites = min(200, max(100, int(info['coastline_length'] / 100)))
        
        for i in range(num_sites):
            # Select random coastal region
            region = random.choice(info['coastal_regions'])
            
            # Generate realistic GPS coordinates based on country
            lat, lon = generate_coordinates_for_country(country, region)
            
            # Generate cleanup data
            cleanup_data = generate_single_cleanup_record(
                cleanup_id_counter, country, region, lat, lon
            )
            
            all_cleanup_data.append(cleanup_data)
            cleanup_id_counter += 1
    
    # Create DataFrame
    df = pd.DataFrame(all_cleanup_data)
    
    # Add comprehensive cost analysis to each cleanup point
    print("Calculating costs for each cleanup point...")
    df_with_costs = add_cost_columns_to_dataframe(df)
    
    # Save to CSV
    output_file = 'data/global_ocean_cleanup_data_with_costs.csv'
    df_with_costs.to_csv(output_file, index=False)
    
    # Also save original data without costs
    original_output_file = 'data/global_ocean_cleanup_data.csv'
    df.to_csv(original_output_file, index=False)
    
    print(f"\nGenerated {len(df)} cleanup records for {len(countries_data)} countries")
    print(f"Data with costs saved to: {output_file}")
    print(f"Original data saved to: {original_output_file}")
    
    # Print cost summary
    print_cost_summary(df_with_costs)
    
    return df_with_costs

def print_cost_summary(df):
    """Print comprehensive cost summary for the global cleanup data"""
    print("\n" + "="*60)
    print("GLOBAL OCEAN CLEANUP COST ANALYSIS SUMMARY")
    print("="*60)
    
    # Basic statistics
    total_events = len(df)
    total_people = df['People'].sum()
    total_pounds = df['Pounds'].sum()
    total_miles = df['Miles'].sum()
    
    # Cost statistics
    total_volunteer_cost = df['volunteer_cost'].sum()
    total_direct_costs = df['total_direct_costs'].sum()
    total_carbon_cost = df['carbon_cost'].sum()
    total_cost = df['total_cost'].sum()
    
    print(f"Total Cleanup Events: {total_events:,}")
    print(f"Total People Involved: {total_people:,}")
    print(f"Total Pounds Collected: {total_pounds:,.2f}")
    print(f"Total Miles Covered: {total_miles:,.2f}")
    print(f"Total Countries: {df['Country'].nunique()}")
    
    print(f"\nCOST BREAKDOWN:")
    print(f"Volunteer Time Value: ${total_volunteer_cost:,.2f}")
    print(f"Direct Costs (Equipment, Transport, etc.): ${total_direct_costs:,.2f}")
    print(f"Carbon Footprint Cost: ${total_carbon_cost:,.2f}")
    print(f"TOTAL COST: ${total_cost:,.2f}")
    
    print(f"\nEFFICIENCY METRICS:")
    print(f"Average Cost per Event: ${total_cost/total_events:,.2f}")
    print(f"Average Cost per Person: ${total_cost/total_people:,.2f}")
    print(f"Average Cost per Pound: ${total_cost/total_pounds:,.2f}")
    print(f"Average Pounds per Person: {total_pounds/total_people:.2f}")
    
    # Top 10 countries by total cost
    country_costs = df.groupby('Country')['total_cost'].sum().sort_values(ascending=False).head(10)
    print(f"\nTOP 10 COUNTRIES BY TOTAL COST:")
    for i, (country, cost) in enumerate(country_costs.items(), 1):
        print(f"{i:2d}. {country}: ${cost:,.2f}")
    
    print("="*60)

def generate_coordinates_for_country(country, region):
    """Generate realistic GPS coordinates for a country/region"""
    
    # Country-specific coordinate ranges
    country_coords = {
        'United States': {'lat_range': (24.5, 49.0), 'lon_range': (-125.0, -66.9)},
        'Canada': {'lat_range': (41.7, 83.1), 'lon_range': (-141.0, -52.6)},
        'Mexico': {'lat_range': (14.5, 32.7), 'lon_range': (-118.4, -86.7)},
        'Brazil': {'lat_range': (-33.8, 5.3), 'lon_range': (-73.9, -34.8)},
        'Argentina': {'lat_range': (-55.1, -21.8), 'lon_range': (-73.6, -53.6)},
        'Chile': {'lat_range': (-56.0, -17.5), 'lon_range': (-75.6, -66.4)},
        'Colombia': {'lat_range': (-4.2, 15.5), 'lon_range': (-81.7, -66.9)},
        'Peru': {'lat_range': (-18.3, -0.0), 'lon_range': (-84.6, -68.7)},
        'Ecuador': {'lat_range': (-5.0, 1.7), 'lon_range': (-92.0, -75.2)},
        'Venezuela': {'lat_range': (0.6, 15.9), 'lon_range': (-73.4, -59.8)},
        'Uruguay': {'lat_range': (-35.0, -30.1), 'lon_range': (-58.4, -53.1)},
        'United Kingdom': {'lat_range': (49.9, 60.8), 'lon_range': (-8.2, 1.8)},
        'France': {'lat_range': (41.3, 51.1), 'lon_range': (-5.1, 9.6)},
        'Spain': {'lat_range': (27.6, 43.8), 'lon_range': (-9.3, 4.3)},
        'Italy': {'lat_range': (35.5, 47.1), 'lon_range': (6.6, 18.5)},
        'Germany': {'lat_range': (47.3, 55.1), 'lon_range': (5.9, 15.0)},
        'Netherlands': {'lat_range': (50.8, 53.6), 'lon_range': (3.4, 7.2)},
        'Norway': {'lat_range': (58.0, 80.8), 'lon_range': (4.6, 31.3)},
        'Sweden': {'lat_range': (55.3, 69.1), 'lon_range': (11.0, 24.2)},
        'Denmark': {'lat_range': (54.6, 57.8), 'lon_range': (8.1, 15.2)},
        'Portugal': {'lat_range': (36.9, 42.2), 'lon_range': (-9.5, -6.2)},
        'Greece': {'lat_range': (34.8, 41.7), 'lon_range': (19.4, 29.7)},
        'Turkey': {'lat_range': (35.8, 42.1), 'lon_range': (25.7, 44.8)},
        'Russia': {'lat_range': (41.2, 81.9), 'lon_range': (-180.0, 180.0)},
        'China': {'lat_range': (18.2, 53.6), 'lon_range': (73.6, 135.1)},
        'Japan': {'lat_range': (24.2, 45.5), 'lon_range': (123.0, 145.8)},
        'South Korea': {'lat_range': (33.1, 38.6), 'lon_range': (124.6, 131.9)},
        'India': {'lat_range': (6.7, 37.1), 'lon_range': (68.2, 97.4)},
        'Indonesia': {'lat_range': (-11.0, 6.1), 'lon_range': (95.0, 141.0)},
        'Philippines': {'lat_range': (4.6, 21.1), 'lon_range': (116.9, 126.6)},
        'Thailand': {'lat_range': (5.6, 20.5), 'lon_range': (97.3, 105.6)},
        'Vietnam': {'lat_range': (8.6, 23.4), 'lon_range': (102.1, 109.5)},
        'Malaysia': {'lat_range': (0.9, 7.4), 'lon_range': (99.6, 119.3)},
        'Singapore': {'lat_range': (1.2, 1.5), 'lon_range': (103.6, 104.0)},
        'Bangladesh': {'lat_range': (20.7, 26.6), 'lon_range': (88.0, 92.7)},
        'Sri Lanka': {'lat_range': (5.9, 9.8), 'lon_range': (79.7, 81.9)},
        'Myanmar': {'lat_range': (9.8, 28.5), 'lon_range': (92.2, 101.2)},
        'South Africa': {'lat_range': (-47.0, -22.1), 'lon_range': (16.5, 32.9)},
        'Egypt': {'lat_range': (22.0, 31.7), 'lon_range': (24.7, 36.9)},
        'Morocco': {'lat_range': (21.4, 35.9), 'lon_range': (-17.0, -1.0)},
        'Algeria': {'lat_range': (18.9, 37.1), 'lon_range': (-8.7, 12.0)},
        'Tunisia': {'lat_range': (30.2, 37.5), 'lon_range': (7.5, 11.6)},
        'Libya': {'lat_range': (19.5, 33.2), 'lon_range': (9.3, 25.2)},
        'Nigeria': {'lat_range': (4.3, 13.9), 'lon_range': (2.7, 14.7)},
        'Ghana': {'lat_range': (4.7, 11.2), 'lon_range': (-3.3, 1.3)},
        'Senegal': {'lat_range': (12.3, 16.7), 'lon_range': (-17.5, -11.3)},
        'Kenya': {'lat_range': (-4.7, 5.5), 'lon_range': (33.9, 41.9)},
        'Tanzania': {'lat_range': (-11.7, -0.9), 'lon_range': (29.3, 40.3)},
        'Mozambique': {'lat_range': (-26.9, -10.5), 'lon_range': (30.2, 40.8)},
        'Madagascar': {'lat_range': (-25.6, -11.9), 'lon_range': (43.2, 50.5)},
        'Australia': {'lat_range': (-43.6, -10.7), 'lon_range': (113.3, 153.6)},
        'New Zealand': {'lat_range': (-47.3, -34.4), 'lon_range': (166.5, 178.6)},
        'Papua New Guinea': {'lat_range': (-12.0, -1.0), 'lon_range': (140.8, 159.9)},
        'Fiji': {'lat_range': (-20.7, -16.0), 'lon_range': (177.0, -178.1)},
        'Solomon Islands': {'lat_range': (-11.9, -5.3), 'lon_range': (155.5, 166.9)},
        'Vanuatu': {'lat_range': (-20.2, -13.1), 'lon_range': (166.5, 170.2)},
        'Samoa': {'lat_range': (-14.0, -13.4), 'lon_range': (-172.8, -171.4)},
        'Tonga': {'lat_range': (-24.0, -15.6), 'lon_range': (-179.1, -173.9)},
        'Kiribati': {'lat_range': (-4.7, 4.7), 'lon_range': (-174.5, -150.2)},
        'Marshall Islands': {'lat_range': (4.6, 14.7), 'lon_range': (160.8, 172.0)},
        'Micronesia': {'lat_range': (1.0, 10.1), 'lon_range': (137.3, 163.0)},
        'Palau': {'lat_range': (2.9, 8.2), 'lon_range': (131.1, 134.7)},
        'Tuvalu': {'lat_range': (-10.8, -5.6), 'lon_range': (176.0, 179.9)},
        'Nauru': {'lat_range': (-0.6, -0.5), 'lon_range': (166.9, 166.9)}
    }
    
    if country in country_coords:
        lat_range = country_coords[country]['lat_range']
        lon_range = country_coords[country]['lon_range']
        
        lat = random.uniform(lat_range[0], lat_range[1])
        lon = random.uniform(lon_range[0], lon_range[1])
        
        return round(lat, 6), round(lon, 6)
    else:
        # Default fallback
        return round(random.uniform(-60, 60), 6), round(random.uniform(-180, 180), 6)

def generate_single_cleanup_record(cleanup_id, country, region, lat, lon):
    """Generate a single cleanup record with realistic data"""
    
    # Generate cleanup date (random date in the last 2 years)
    start_date = datetime.now() - timedelta(days=730)
    end_date = datetime.now()
    random_date = start_date + timedelta(days=random.randint(0, 730))
    cleanup_date = random_date.strftime('%m/%d/%Y')
    
    # Generate group name
    group_names = [
        f"{region} Beach Cleaners", f"{region} Ocean Guardians", f"{region} Coastal Warriors",
        f"{region} Marine Savers", f"{region} Cleanup Crew", f"{region} Eco Warriors",
        f"{region} Blue Guardians", f"{region} Ocean Protectors", f"{region} Beach Warriors",
        f"{region} Coastal Cleaners", f"{region} Marine Protectors", f"{region} Ocean Heroes"
    ]
    group_name = random.choice(group_names)
    
    # Generate people count
    adults = random.randint(1, 50)
    children = random.randint(0, min(20, adults // 2))
    people = adults + children
    
    # Generate cleanup metrics
    pounds = round(random.uniform(0.1, 100.0), 2)
    miles = round(random.uniform(0.01, 5.0), 4)
    bags = random.randint(0, 20)
    
    # Generate trash item counts
    cigarette_butts = random.randint(0, 100)
    food_wrappers = random.randint(0, 50)
    takeout_plastic = random.randint(0, 30)
    takeout_foam = random.randint(0, 20)
    bottle_caps_plastic = random.randint(0, 40)
    bottle_caps_metal = random.randint(0, 20)
    lids_plastic = random.randint(0, 30)
    straws = random.randint(0, 25)
    utensils = random.randint(0, 15)
    bottles_plastic = random.randint(0, 35)
    bottles_glass = random.randint(0, 20)
    cans = random.randint(0, 25)
    grocery_bags = random.randint(0, 30)
    other_plastic_bags = random.randint(0, 25)
    paper_bags = random.randint(0, 15)
    cups_paper = random.randint(0, 20)
    cups_plastic = random.randint(0, 25)
    cups_foam = random.randint(0, 15)
    fishing_buoys = random.randint(0, 10)
    fishing_net = random.randint(0, 8)
    fishing_line = random.randint(0, 15)
    rope = random.randint(0, 12)
    fishing_gear = random.randint(0, 5)
    six_pack_holders = random.randint(0, 10)
    other_packaging = random.randint(0, 20)
    other_bottles = random.randint(0, 15)
    strapping_bands = random.randint(0, 8)
    tobacco_packaging = random.randint(0, 12)
    other_clean_swell = random.randint(0, 10)
    appliances = random.randint(0, 3)
    balloons = random.randint(0, 15)
    cigar_tips = random.randint(0, 8)
    lighters = random.randint(0, 10)
    construction = random.randint(0, 5)
    fireworks = random.randint(0, 3)
    tires = random.randint(0, 2)
    toys = random.randint(0, 12)
    other_trash = random.randint(0, 15)
    condoms = random.randint(0, 5)
    diapers = random.randint(0, 3)
    syringes = random.randint(0, 2)
    tampons = random.randint(0, 4)
    hygiene = random.randint(0, 8)
    foam_pieces = random.randint(0, 30)
    glass_pieces = random.randint(0, 25)
    plastic_pieces = random.randint(0, 50)
    
    # Calculate total items
    total_items = (cigarette_butts + food_wrappers + takeout_plastic + takeout_foam + 
                  bottle_caps_plastic + bottle_caps_metal + lids_plastic + straws + 
                  utensils + bottles_plastic + bottles_glass + cans + grocery_bags + 
                  other_plastic_bags + paper_bags + cups_paper + cups_plastic + 
                  cups_foam + fishing_buoys + fishing_net + fishing_line + rope + 
                  fishing_gear + six_pack_holders + other_packaging + other_bottles + 
                  strapping_bands + tobacco_packaging + other_clean_swell + appliances + 
                  balloons + cigar_tips + lighters + construction + fireworks + tires + 
                  toys + other_trash + condoms + diapers + syringes + tampons + 
                  hygiene + foam_pieces + glass_pieces + plastic_pieces)
    
    return {
        'Cleanup ID': f"GLOBAL{cleanup_id:06d}",
        'Zone': f"{region}, {country}",
        'State': f"{region}, {country}",
        'Country': country,
        'GPS': f"{lat}, {lon}",
        'Cleanup Type': random.choice(['Land (beach, shoreline and inland)', 'Water (boat, kayak, paddleboard)', 'Underwater (diving)']),
        'Cleanup Date': cleanup_date,
        'Group Name': group_name,
        'Adults': adults,
        'Children': children,
        'People': people,
        'Pounds': pounds,
        'Miles': miles,
        '# of bags': bags,
        'Cigarette Butts': cigarette_butts,
        'Food Wrappers (candy, chips, etc.)': food_wrappers,
        'Take Out/Away Containers (Plastic)': takeout_plastic,
        'Take Out/Away Containers (Foam)': takeout_foam,
        'Bottle Caps (Plastic)': bottle_caps_plastic,
        'Bottle Caps (Metal)': bottle_caps_metal,
        'Lids (Plastic)': lids_plastic,
        'Straws, Stirrers': straws,
        'Forks, Knives, Spoons': utensils,
        'Beverage Bottles (Plastic)': bottles_plastic,
        'Beverage Bottles (Glass)': bottles_glass,
        'Beverage Cans': cans,
        'Grocery Bags (Plastic)': grocery_bags,
        'Other Plastic Bags': other_plastic_bags,
        'Paper Bags': paper_bags,
        'Cups, Plates (Paper)': cups_paper,
        'Cups, Plates (Plastic)': cups_plastic,
        'Cups, Plates (Foam)': cups_foam,
        'Fishing Buoys, Pots & Traps': fishing_buoys,
        'Fishing Net & Pieces': fishing_net,
        'Fishing Line (1 yard/meter = 1 piece)': fishing_line,
        'Rope (1 yard/meter = 1 piece)': rope,
        'Fishing Gear (Clean Swell)': fishing_gear,
        '6-Pack Holders': six_pack_holders,
        'Other Plastic/Foam Packaging': other_packaging,
        'Other Plastic Bottles (oil, bleach, etc.)': other_bottles,
        'Strapping Bands': strapping_bands,
        'Tobacco Packaging/Wrap': tobacco_packaging,
        'Other Packaging (Clean Swell)': other_clean_swell,
        'Appliances (refrigerators, washers, etc.)': appliances,
        'Balloons': balloons,
        'Cigar Tips': cigar_tips,
        'Cigarette Lighters': lighters,
        'Construction Materials': construction,
        'Fireworks': fireworks,
        'Tires': tires,
        'Toys': toys,
        'Other Trash (Clean Swell)': other_trash,
        'Condoms': condoms,
        'Diapers': diapers,
        'Syringes': syringes,
        'Tampons/Tampon Applicators': tampons,
        'Personal Hygiene (Clean Swell)': hygiene,
        'Foam Pieces': foam_pieces,
        'Glass Pieces': glass_pieces,
        'Plastic Pieces': plastic_pieces,
        'Total Items Collected': total_items
    }

if __name__ == "__main__":
    print("Generating global ocean cleanup dataset...")
    print("This may take several minutes due to the large dataset size...")
    
    # Set random seed for reproducibility
    random.seed(42)
    np.random.seed(42)
    
    # Generate the data
    df = generate_global_cleanup_data()
    
    print(f"\nDataset Summary:")
    print(f"Total records: {len(df)}")
    print(f"Countries: {df['Country'].nunique()}")
    print(f"Date range: {df['Cleanup Date'].min()} to {df['Cleanup Date'].max()}")
    print(f"Total people involved: {df['People'].sum():,}")
    print(f"Total pounds collected: {df['Pounds'].sum():,.2f}")
    print(f"Total items collected: {df['Total Items Collected'].sum():,}")
    
    # Show sample of data
    print(f"\nSample data:")
    print(df[['Cleanup ID', 'Country', 'Zone', 'GPS', 'People', 'Pounds', 'Total Items Collected']].head(10))
