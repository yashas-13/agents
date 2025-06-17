"""Logistics Routing Agent."""

import psycopg2
import pandas as pd
from ortools.constraint_solver import pywrapcp, routing_enums_pb2


def fetch_deliveries(conn):
    query = "SELECT id, address_lat, address_lon FROM deliveries WHERE status='pending';"
    return pd.read_sql(query, conn)


def plan_routes(df):
    manager = pywrapcp.RoutingIndexManager(len(df), 1, 0)
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        from_node = df.iloc[manager.IndexToNode(from_index)]
        to_node = df.iloc[manager.IndexToNode(to_index)]
        return int(((from_node.address_lat - to_node.address_lat) ** 2 + (from_node.address_lon - to_node.address_lon) ** 2) ** 0.5 * 1000)

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC

    solution = routing.SolveWithParameters(search_parameters)
    if solution:
        route = []
        index = routing.Start(0)
        while not routing.IsEnd(index):
            route.append(manager.IndexToNode(index))
            index = solution.Value(routing.NextVar(index))
        return route
    return []


def main():
    conn = psycopg2.connect(dbname='scm', user='user', password='pass', host='localhost')
    df = fetch_deliveries(conn)
    route = plan_routes(df)
    print('Planned route:', route)


if __name__ == '__main__':
    main()
