# Erlang Calculator

This Python script provides functions to calculate various metrics related to call center operations using Erlang formulas.

## Features

- Calculate the probability of call blocking (Erlang B)
- Calculate the probability of a caller being placed in a queue (Erlang C)
- Determine the number of agents required to meet a specific service level

## Functions

### `erlang_b(servers, intensity)`

Calculates the Erlang B formula, which determines the probability of call blocking.

- `servers`: Number of telephone lines (float)
- `intensity`: Traffic intensity (float)
- Returns: Probability of call blocking (float)

### `erlang_c(servers, intensity)`

Calculates the Erlang C formula, which determines the probability of a caller being placed in the queue.

- `servers`: Number of agents (float)
- `intensity`: Arrival rate of calls / Completion rate of calls (float)
- Returns: Probability of a caller being placed in the queue (float)

### `fractional_agents(sla, service_time, calls_per_hour, aht)`

Calculates the number of agents required to service a given number of calls to meet the service level.

- `sla`: % of calls to be answered within the ServiceTime period (float, e.g., 0.95 for 95%)
- `service_time`: Target answer time in seconds (int, e.g., 15)
- `calls_per_hour`: Number of calls received in one hour period (float)
- `aht`: Call duration including after call work in seconds (int, e.g., 180)
- Returns: Number of agents required (float)

## Usage

To use this script, you can import the functions into your own Python code or run the script directly. When run as a main script, it calculates the number of agents required for a specific scenario:

```python
if __name__ == "__main__":
    sla = 0.9
    service_time = 240
    calls_per_hour = 1325
    aht = 630
    agents_required = fractional_agents(sla, service_time, calls_per_hour, aht)
    print(f"Agents required: {agents_required}")
```

## Dependencies

This script requires the `math` module, which is part of Python's standard library.

