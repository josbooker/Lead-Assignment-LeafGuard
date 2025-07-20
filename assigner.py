
import pandas as pd
from geocode_cache import get_coordinates, get_distance
import json

def load_reps(filepath="reps.json"):
    with open(filepath, "r") as file:
        return json.load(file)

def assign_leads(leads_df, reps):
    # Add lat/lng to leads
    leads_df["full_address"] = leads_df["Address"] + ", " + leads_df["City"] + ", " + leads_df["State"] + " " + leads_df["Zip"]
    leads_df["lat"] = leads_df["full_address"].apply(lambda x: get_coordinates(x)["lat"])
    leads_df["lng"] = leads_df["full_address"].apply(lambda x: get_coordinates(x)["lng"])

    # Prepare rep data
    rep_assignments = {rep["name"]: [] for rep in reps}
    rep_lead_counts = {rep["name"]: 0 for rep in reps}

    # Assign leads
    for _, lead in leads_df.iterrows():
        distances = []
        for rep in reps:
            if rep_lead_counts[rep["name"]] < rep["max_leads"]:
                rep_coords = get_coordinates(rep["home_base"])
                distance = get_distance(rep_coords, {"lat": lead["lat"], "lng": lead["lng"]})
                distances.append((rep["name"], distance))
        if distances:
            best_rep = min(distances, key=lambda x: x[1])[0]
            rep_assignments[best_rep].append(lead["full_address"])
            rep_lead_counts[best_rep] += 1
            leads_df.at[lead.name, "Assigned Rep"] = best_rep
            leads_df.at[lead.name, "Distance (mi)"] = dict(distances)[best_rep]

    return leads_df
