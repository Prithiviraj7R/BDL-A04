# BDL-A04

The implementations of different stages of the pipeline are present inside the src directory.

The problem involves setting up a pipeline to verify the
consistency of a climatological dataset acquired from the
National Centers for Environmental Information, spanning
from 1901 to 2024 and comprising data from over 13400
stations. The dataset includes multiple readings such as Altimeter, DewPointTemperature, DryBulbTemperature, Precipitation, and others, collected hourly. The pipeline aims to extract monthly aggregates from the data files and compare them
against computed monthly averages from hourly data points.
The estimated monthly aggregates will be evaluated using the
R2 score, with a threshold of 0.9 denoting consistency (C).

Below is the DAG pipeline created using DVC (Data Version Control):

![Screenshot 2024-04-01 154031](https://github.com/Prithiviraj7R/BDL-A04/assets/142074094/e2710b5f-871b-4c29-b7ad-08b74877b452)

The results of the experiments run using DVC can be visualized and compared with DVC Studio.

![Screenshot 2024-04-01 161154](https://github.com/Prithiviraj7R/BDL-A04/assets/142074094/fe82864f-ef50-419a-b0e0-8627bb0b3c47)

![Screenshot 2024-04-01 173459](https://github.com/Prithiviraj7R/BDL-A04/assets/142074094/56a47112-4cfe-44a5-bb1c-1b200f7a942e)

The pipeline for checking the consistency of the data consists of the following stages:

1. **Download Stage:** The initial stage of the pipeline randomly selects a specific number of files determined by the "n locs" parameter in the params.yaml file and from the designated year. These files undergo a check to verify the presence of data in the monthly aggregate columns and the corresponding hourly feature columns. If at least one such pair exists, the file is marked for further processing; otherwise, it is removed from the saved directory.

2. **Preparation Stage:** The second stage of the pipeline focuses on extracting monthly aggregates from the downloaded files.

3. **Processing Stage:** This stage calculates monthly aggregates from the hourly data corresponding to the extracted monthly aggregates in the preparation stage.

4. **Evaluation Stage:** The final stage of evaluation calculates the average R2 score for all the files that underwent preparation and processing. If the R2 metric is higher than 0.90, the data is then tagged as 'Consistent' (C). This final R2 metric is then saved and logged in DVC (Data Version Control).
