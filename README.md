#  Global Ocean Cleanup Data Analysis Project

A comprehensive **data science framework** for analyzing worldwide ocean cleanup activities, including **cost modeling, geographic visualization, and machine learning** insights.

![Ocean Pollution - The Problem We're Solving](cover/pollution.jpg)

*Severe plastic pollution on coastal beaches highlights the critical need for organized cleanup efforts and cost-effective resource allocation.*

![Global Ocean Cleanup Cost Analysis Map](cover/map2.png)

*Interactive global map showing ocean cleanup events across 64 countries with cost-based color coding. Each marker represents cleanup locations, with colors indicating total cost ranges from green (< $1,000) to red (> $15,000).*

### 🎥 Project Demo Video


https://github.com/user-attachments/assets/1f898fb1-51e1-4da7-b682-d6dfd74d1080




<video width="800" controls>
  <source src="https://github.com/user-attachments/assets/b383d125-c279-4364-9315-19af09920d2a" type="video/mp4">
  Your browser does not support the video tag.
</video>

*Watch the demo video to see the project in action, including data generation, cost analysis, and interactive map visualizations.*

---

## Overview

This project provides an end-to-end analytical platform for evaluating global ocean cleanup initiatives, covering:

- 7,355 cleanup events  
- 64 countries  
- Detailed cost modeling and efficiency analysis  
- Country-level statistics and geographic analytics  
- Machine learning-based classification and insights  
- Automated visual reporting  

---

##  Key Features

###  Core Functionality
- Synthetic global dataset generation  
- Geolocation validation & correction  
- Cleanup event cost modeling  
- Interactive Folium-based maps  
- Country-wise summaries and metrics  
- Machine learning classification models  
- Automated reporting  

---

###  Cost Analysis Capabilities
- Volunteer valuation ($25.43/hour — Independent Sector)  
- Equipment and transport cost modeling  
- Waste disposal estimation  
- Administrative overhead  
- Carbon footprint costing  
- Per-country and per-event comparison reports  

---

###  Geographic Coverage

**North America:** USA, Canada, Mexico  
**South America:** Brazil, Argentina, Chile, Colombia, Peru, Ecuador, Venezuela, Uruguay  
**Europe:** UK, France, Spain, Italy, Germany, Netherlands, Norway, Sweden, Denmark, Greece, Portugal, Turkey, Russia  
**Asia:** China, Japan, Korea, India, Indonesia, Philippines, Thailand, Vietnam, Malaysia, Singapore, Bangladesh, Sri Lanka, Myanmar  
**Africa:** South Africa, Egypt, Morocco, Algeria, Tunisia, Libya, Nigeria, Ghana, Senegal, Kenya, Tanzania, Mozambique, Madagascar  
**Oceania:** Australia, New Zealand, PNG, Fiji, Solomon Islands, Vanuatu, Samoa, Tonga, Kiribati, Micronesia, Palau, Tuvalu, Nauru  

---

##  Project Structure

```bash
datascience/
├── data/
│   ├── global_ocean_cleanup_data.csv
│   ├── global_ocean_cleanup_data_with_costs.csv
│   ├── country_cost_analysis.csv
│   └── ...
├── maps/
│   ├── corrected_global_world_map.html
│   └── ...
├── plots/
│   ├── global_cost_analysis.png
│   ├── country_efficiency_analysis.png
│   └── ...
├── cost_calculator.py
├── generate_global_cleanup_data.py
├── create_corrected_global_map.py
├── add_costs_to_existing_data.py
├── simple_cost_analysis.py
├── show_point_costs.py
├── fix_coordinates.py
├── verify_global_data.py
├── ML.ipynb
├── demo.ipynb
├── india_ocean_cleanup_demo.ipynb
├── COST_ANALYSIS_SUMMARY.md
└── README.md
```

---

##  Installation Guide

###  Prerequisites
- Python 3.7 or higher  
- pip  

###  Setup

```bash
cd datascience

python3 -m venv env
source env/bin/activate    # Windows: env\Scripts\activate

pip install pandas numpy matplotlib folium scikit-learn jupyter
```

Or if available:

```bash
pip install -r requirements.txt
```

---

##  Usage

###  Generate Global Dataset

```bash
python3 generate_global_cleanup_data.py
```

Creates:
- data/global_ocean_cleanup_data.csv  
- data/global_ocean_cleanup_data_with_costs.csv  

---

###  Add Costs to Existing Data

```bash
python3 add_costs_to_existing_data.py data/your_data.csv
```

---

###  Create Global Maps

```bash
python3 create_corrected_global_map.py
```

Output:
- maps/corrected_global_world_map.html  

---

###  Generate Cost Reports

```bash
python3 simple_cost_analysis.py
```

Outputs:
- Console summary  
- plots/global_cost_analysis.png  
- plots/country_efficiency_analysis.png  
- data/country_cost_analysis.csv  

---

###  View Individual Event Costs

```bash
python3 show_point_costs.py 10
python3 show_point_costs.py search "India"
```

---

###  Fix Coordinates

```bash
python3 fix_coordinates.py
```

---

###  Validate Data

```bash
python3 verify_global_data.py
```

---

###  Run Notebooks

```bash
jupyter notebook
```

Open:
- ML.ipynb  
- demo.ipynb  
- india_ocean_cleanup_demo.ipynb  

---

## Dataset Description

### Data Fields

**Location**  
- Country  
- Zone  
- State  
- GPS  

**Event Information**
- Cleanup ID  
- Cleanup Date  
- Group Name  
- Cleanup Type  

**Participants**
- People  
- Adults  
- Children  

**Metrics**
- Pounds  
- Miles  
- Bags  
- Items Collected  

**Trash Types**
- Cigarette butts  
- Bottles  
- Bags  
- Fishing gear  
- 50+ categories  

**Cost Fields**
- total_cost  
- volunteer_cost  
- carbon_cost  
- cost_per_pound  
- cost_per_person  

---

## Cost Calculator

**File:** cost_calculator.py  

### Usage Example

```python
from cost_calculator import OceanCleanupCostCalculator

calc = OceanCleanupCostCalculator()

costs = calc.calculate_comprehensive_costs({
    "People": 25,
    "Pounds": 150,
    "Miles": 2,
    "# of bags": 8
})
```

---

### Cost Components

| Category | Rate |
|----------|------|
| Volunteer Time | $25.43/hr |
| Equipment | $5/person |
| Transport | $0.50/mile |
| Disposal | $0.15/lb |
| Admin | $25/event |
| Carbon | $50/ton CO₂ |

---

## Visualizations

### Interactive Maps

The project generates interactive Folium-based maps showing cleanup locations with cost-based color coding. Each marker represents cleanup events, with colors indicating total cost ranges.

#### Regional Focus: India and Sri Lanka

![Regional Ocean Cleanup Map - India and Sri Lanka](cover/map1.png)

*Detailed view of cleanup activities in India and Sri Lanka, showing cost distribution across coastal regions with interactive markers and country-level statistics.*

#### Map Features

- **Color-coded markers** by total cost:
  - 🟢 Green: < $1,000
  - 🟡 Yellow: $1,000 - $5,000
  - 🟠 Orange: $5,000 - $10,000
  - 🔴 Red: $10,000 - $15,000
  - 🔴 Dark Red: > $15,000
- **Interactive popups** with detailed event information
- **Country-level statistics** panel showing top countries by total cost
- **Marker clustering** for better performance with large datasets
- **Zoom and pan** functionality for detailed exploration

### Other Visualizations

**Interactive:**
- Cleanup location map  
- Cost heatmap  
- Clustering  
- Country overlays  

**Static:**
- Cost distributions  
- Efficiency analysis  
- Country comparisons  
- Correlation matrices  

---

##  Global Cost Summary

| Metric | Value |
|--------|-------|
| Total Cost | $64,830,992.62 |
| % Volunteer Cost | 97.8% |
| Avg Cost/Event | $8,814.55 |
| Avg Cost/Pound | $174.73 |
| Avg Cost/Person | $278.19 |

---

##  Machine Learning

Implemented in:
- ML.ipynb  
- ML_classify.ipynb  

Includes:
- Feature engineering  
- Clustering  
- Predictive modeling  
- Country pattern analysis  

---

## Technical Requirements

| Package | Purpose |
|---------|---------|
| pandas | Data prep |
| numpy | Computation |
| matplotlib | Charts |
| folium | Maps |
| scikit-learn | ML |
| jupyter | Notebooks |

---

##  Contributing

1. Maintain CSV structure  
2. Extend cost_calculator.py  
3. Add new countries to generate_global_cleanup_data.py  
4. Follow plotting standards  
5. Validate coordinates before commit  

---

##  Notes

- Dataset is synthetic  
- Rates are based on 2019 estimates  
- Validate real-world data before use  
- Coordinate correction recommended  

---

##  Acknowledgments

- Global Ocean Cleanup Communities  
- Independent Sector (Volunteer Valuation)  
- Open Source Data Science Ecosystems  

