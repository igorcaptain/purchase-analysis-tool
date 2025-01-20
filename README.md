# Purchase Analysis Tool

## Overview
This Python-based purchase analysis tool provides comprehensive insights into sales data, customer segmentation, and product recommendations. It's designed to help businesses understand their sales patterns, customer behavior, and make data-driven decisions.

## Key Features
- **Sales Analysis**
  - Top-selling products identification
  - Category performance analysis
  - Customer spending patterns
  - Comprehensive sales metrics

- **Customer Segmentation**
  - Dynamic customer clustering
  - Behavior-based segmentation
  - Customizable segmentation thresholds
  - Detailed segment analysis

- **Product Recommendations**
  - Personalized product suggestions
  - Matrix factorization-based recommendations
  - Category-aware recommendations
  - Configurable recommendation count

## Quick Start

### Prerequisites
- Anaconda or Miniconda installed on your system
- Python 3.12.8 or higher

### Installation
1. Clone the repository:
```bash
git clone <repository-url>
cd purchase-analysis-tool
```

2. Create and activate a new conda environment:
```bash
conda create -n purchase-analysis python=3.12.8
conda activate purchase-analysis
```

3. Install required packages:
```bash
pip install -r src/requirements.txt
```

## Usage

### Command Line Interface
The tool provides three main commands: analyze, classify, and recommend.

#### Analysis Command
```bash
python src/cli.py analyze [options]

Options:
  --data PATH           Path to data file (default: purchase_data.csv)
  --type TYPE          Analysis type: products|categories|customers|full (default: full)
  --limit N            Limit for top products/customers (default: 5)
  --json               Output in JSON format
```

#### Classification Command
```bash
python src/cli.py classify [options]

Options:
  --data PATH           Path to data file (default: purchase_data.csv)
  --clusters N         Number of clusters (default: 5)
  --customer ID        Get segment for specific customer ID
  --high-percentile N  Percentile for high-value thresholds (default: 0.75)
  --medium-percentile N Percentile for medium-value thresholds (default: 0.50)
  --recency-multiplier N Multiplier for recency threshold (default: 1.0)
  --json               Output in JSON format
```

#### Recommendation Command
```bash
python src/cli.py recommend [options]

Options:
  --data PATH          Path to data file (default: purchase_data.csv)
  --customer ID        Customer ID for recommendations
  --num N             Number of recommendations (default: 5)
  --json              Output in JSON format
```

### Example Usage
```bash
# Generate full analysis report
python src/cli.py analyze --data test_data/purchase_data.csv --type full --limit 10

# Get customer segmentation
python src/cli.py classify --data test_data/purchase_data.csv --clusters 6 --high-percentile 0.8

# Get product recommendations for a customer
python src/cli.py recommend --data test_data/purchase_data.csv --customer C001 --num 5

```

### Data Format
The tool expects a CSV file with the following columns:
- Customer ID
- Product ID
- Product Category
- Purchase Amount
- Purchase Date

A sample dataset generator is included in `src/dataset_generator.py`.

Few sample datasets are included in `test_data` folder.