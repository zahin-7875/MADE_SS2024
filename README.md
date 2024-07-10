# Impact of Global Greenhouse Gas Emissions on the Extent of Arctic and Antarctic Sea Ice : A Comprehensive Analysis

## Overview

This project investigates the relationship between global greenhouse gas emissions and the extent of sea ice in the Arctic and Antarctic regions. By combining datasets on greenhouse gas emissions and sea ice extent, the study aims to determine if increased emissions correlate with a reduction in sea ice over the past few decades.

## Data Sources

1. **International Greenhouse Gas Emissions**

   - **URL**: [Kaggle - International Greenhouse Gas Emissions](https://www.kaggle.com/datasets/unitednations/international-greenhouse-gas-emissions)
   - **Details**: This dataset includes global emissions data from 1990 to 2014, covering gases such as CO2, CH4, and N2O from various sources including industry, transportation, and agriculture.

2. **Daily Sea Ice Extent Data**
   - **URL**: [Kaggle - Daily Sea Ice Extent Data](https://www.kaggle.com/datasets/nsidcorg/daily-sea-ice-extent-data)
   - **Details**: This dataset provides daily records of sea ice extent from 1978 to 2015, detailing the ice extent in both the Northern and Southern Hemispheres.

## Analysis Process

1. **Data Preprocessing**

   - Cleaning and preparing the greenhouse gas and sea ice datasets.
   - Aggregating daily sea ice data to annual averages and merging with emissions data based on the year.

2. **Descriptive Statistics**

   - Calculating and analyzing the distribution patterns of emissions and sea ice extent.

3. **Trend Analysis**

   - Examining changes over time in greenhouse gas emissions and sea ice extent.

4. **Correlation Analysis**

   - Assessing the linear relationship between emissions and sea ice extent, resulting in a weak correlation coefficient of 0.003249.

5. **Time Series Analysis**

   - Visualizing the combined trends of emissions and sea ice extent.

6. **Multivariate Analysis**
   - Using scatter plots and pair plots to explore potential relationships between multiple variables.

## Tools and Libraries

- **Pandas** for data manipulation and cleaning.
- **NumPy** for numerical calculations.
- **Matplotlib** and **Seaborn** for data visualization.
- **SQLite** for database management.
- **Kaggle API** for dataset access and management.

## Conclusion

The study found a weak direct link between greenhouse gas emissions and sea ice extent. Despite the weak correlation, the data highlights the significant impact of human activities on climate change, emphasizing the need for strategies to reduce emissions and protect polar regions. This research underscores the importance of further exploring the indirect effects and long-term impacts of emissions on polar ice to better understand and mitigate the consequences of climate change.
