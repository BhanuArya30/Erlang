import math

def erlang_b(servers, intensity):
    """
    Calculate the ErlangB formula, which determines the probability of call blocking.
    
    :param servers: Number of telephone lines (float)
    :param intensity: Traffic intensity (float)
    :return: Probability of call blocking (float)
    """
    def min_max(value, min_val, max_val):
        return max(min(value, max_val), min_val)

    if servers < 0 or intensity < 0:
        return 0

    max_iterate = int(servers)
    val = intensity
    last = 1  # for server = 0
    b = 0

    try:
        for count in range(1, max_iterate + 1):
            b = (val * last) / (count + (val * last))
            last = b
    except:
        b = 0

    return min_max(b, 0, 1)


def erlang_c(servers, intensity):
    """
    Calculate the ErlangC formula, which determines the probability of a caller being placed in the queue.
    
    :param servers: Number of agents (float)
    :param intensity: Arrival rate of calls / Completion rate of calls (float)
    :return: Probability of a caller being placed in the queue (float)
    """
    def min_max(value, min_val, max_val):
        return max(min(value, max_val), min_val)

    if servers < 0 or intensity < 0:
        return 0

    try:
        b = erlang_b(servers, intensity)
        c = b / (((intensity / servers) * b) + (1 - (intensity / servers)))
    except:
        c = 0

    return min_max(c, 0, 1)


def fractional_agents(sla, service_time, calls_per_hour, aht):
    """
    Calculate the number of agents required to service a given number of calls to meet the service level.
    
    :param sla: % of calls to be answered within the ServiceTime period (float, e.g., 0.95 for 95%)
    :param service_time: Target answer time in seconds (int, e.g., 15)
    :param calls_per_hour: Number of calls received in one hour period (float)
    :param aht: Call duration including after call work in seconds (int, e.g., 180)
    :return: Number of agents required (float)
    """
    MAX_ACCURACY = 0.00001  # Define MAX_ACCURACY constant

    sla = min(sla, 1)
    birth_rate = calls_per_hour
    death_rate = 3600 / aht

    # Calculate traffic intensity
    traffic_rate = birth_rate / death_rate

    # Calculate number of Erlangs hours
    erlangs = round((birth_rate * aht) / 3600)

    # Start at number of agents for 100% Utilisation
    no_agents = max(1, int(erlangs))
    utilisation = traffic_rate / no_agents

    # Now get real and get number below 100%
    while utilisation >= 1:
        no_agents += 1
        utilisation = traffic_rate / no_agents

    sl_queued = 0
    max_iterate = no_agents * 100

    # Try each number of agents until the correct SLA is reached
    for _ in range(max_iterate):
        last_slq = sl_queued
        utilisation = traffic_rate / no_agents
        if utilisation < 1:
            server = no_agents
            c = erlang_c(server, traffic_rate)
            # Find the level of SLA with this number of agents
            sl_queued = 1 - c * math.exp((traffic_rate - server) * service_time / aht)
            sl_queued = max(sl_queued, 0)
            if sl_queued >= sla or sl_queued > (1 - MAX_ACCURACY):
                break
        no_agents += 1

    return no_agents


if __name__=="__main__":
    sla = 0.9
    service_time = 240
    calls_per_hour = 1325
    aht = 630
    print(578)
    agents_required = fractional_agents(sla, service_time, calls_per_hour, aht)
    print(f"Agents required: {agents_required}")