#!/usr/bin/env python3
import requests
import json

def get_app_name(app_id):
    """Get game name from Steam API"""
    url = "https://store.steampowered.com/api/appdetails"
    params = {"appids": app_id}
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return data[str(app_id)]["data"]["name"] if data[str(app_id)]["success"] else "Unknown Game"

def get_app_reviews(app_id, num_per_page=20, cursor="*"):
    """Get user reviews for a Steam game"""
    url = "https://store.steampowered.com/appreviews/" + str(app_id)
    params = {
        "json": 1,
        "num_per_page": num_per_page,
        "cursor": cursor
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    return response.json()

if __name__ == "__main__":
    app_id = 2201320
    
    try:
        game_name = get_app_name(app_id)
        reviews = get_app_reviews(app_id)
        summary = reviews['query_summary']
        print(f"Reviews for: {game_name}")
        print(f"Total Reviews: {summary['total_reviews']}")
        print(f"Rating: {summary['review_score_desc']} ({summary['review_score']}/10)")
        print(f"Positive: {summary['total_positive']} | Negative: {summary['total_negative']}")
        print(f"\nRecent Reviews ({len(reviews['reviews'])}):")
        for review in reviews['reviews'][:5]:
            print(f"- {'👍' if review['voted_up'] else '👎'} {review['review'][:100]}...")
    except requests.RequestException as e:
        print(f"Error: {e}")