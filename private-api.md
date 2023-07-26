# Cryptowatch Data Private API (26.07.2023)
This API provides price data retrieved from Cryptowatch. These data are strictly limited to personal use, and any use for commercial purposes is prohibited. Therefore currently the base endpoint is not opened.

## Endpoints
### PriceData
```
GET /price-data/
```
Fetches all price data.

**Parameters:**<br>
None

**Response:**
```JSON
{
  "all data": [
    {
      "id": 1,
      "close_time": 1632745000,
      "chart_sec": "60",
      "pair": "btcfxjpy",
      "open": ,
      "high": ,
      "low": ,
      "close": ,
      "volume": ,
    },
  ]
}
```

### PriceDataRange
```
GET /price-data/range/
```
Fetches price data for a specified range.

**Parameters:**
- `start`: Start time for data retrieval (Unix timestamp). If not specified, data is retrieved from the beginning.
- `end`: End time for data retrieval (Unix timestamp). If not specified, data is retrieved up to the latest.
- `pair`: The currency pair to retrieve. If not specified, all pairs ("btcjpy", "btcfxjpy") are retrieved.

**Response:**
```JSON
{
  "data": [
    {
      "id": 1,
      "close_time": 1632745000,
      "chart_sec": "60",
      "pair": "btcfxjpy",
      "open": ,
      "high": ,
      "low": ,
      "close": ,
      "volume": ,
    },
  ]
}
```
