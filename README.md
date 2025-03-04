sarimax-model-with-tomorrow.io-data
using SARIMAX model and grid search for making reggresion on tommorrow.io's wheather data
To understand SARIMAX model initally we need to chech what ARIMA models do. Here is my notes about the model down below:

[Document 4.docx](https://github.com/user-attachments/files/19066586/Document.4.docx)#


it is written in turkish you may use translate to understand in your own language.
And then here is a summerize for sarimax model wich I took from this(https://datascientest.com/en/sarimax-model-what-is-it-how-can-it-be-applied-to-time-series) website:


When temporal data show seasonal variations, the SARIMA model takes over the scene. The term “Seasonal” is added to ARIMA to indicate that this model can capture patterns that repeat at regular intervals.

Seasonal variations can occur over short periods, such as a company’s monthly sales, or over longer periods, such as climatic data. By incorporating a seasonal component (S), the SARIMA model can model these recurring patterns and improve forecasts. You can see an example of a non-stationary time series showing seasonality in the graph below, which represents the evolution of an airline’s annual passenger numbers.


While the SARIMA model already offers a powerful method for modeling seasonal time series, there may be external factors influencing these data. This is where the SARIMAX (Seasonal ARIMA with eXogenous variables) model comes in, opening the door to an even richer analysis.

Covariates, also known as exogenous variables, are external elements that can influence the time series under study. In the context of a company’s monthly sales, covariates might include advertising expenditure, special events or vacations. The SARIMAX model makes it possible to incorporate these covariates into the analysis, thereby allowing for external factors that may affect the trends observed.

So I used tommrow.io API for some free and actual data of Kayseri's wheather data.

