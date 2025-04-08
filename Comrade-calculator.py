import json
from collections import defaultdict

# Step 1: Read the JSON File
with open(r"merged_output.json", 'r') as json_file:
    nft_data = json.load(json_file)
    total_retrieved = len(nft_data['collection_items'])

# Step 2: Print Status
if total_retrieved == 9940:
    print("Retrieved 9,940 Comrades.\nCalculating rarity...")
else:
    print(f"Retrieved the wrong number of Comrades. Expected 9,940 but retrieved {total_retrieved}.")

# Define traits to exclude
traits_to_exclude = {"Affiliation", "Classification"}

# Step 3: Calculate Trait Value Frequencies
trait_value_counts = defaultdict(int)
total_items = len(nft_data['collection_items'])

for item in nft_data['collection_items']:
    for attr in item['attributes']:  # Loop through each attribute in the NFT
        trait_type = attr.get('trait_type')  # Ensure 'trait_type' exists
        trait_value = attr.get('value')      # Ensure 'value' exists
        if trait_type and trait_value and trait_type not in traits_to_exclude:
            trait_value_counts[(trait_type, trait_value)] += 1

# Step 4: Calculate Rarity Score for Each Trait
def calculate_rarity_score(trait_type, trait_value):
    frequency = trait_value_counts[(trait_type, trait_value)]
    return total_items / frequency  # Rarity Score formula

# Step 5: Calculate Total Rarity Scores and Rankings
nft_rankings = []

for nft in nft_data['collection_items']:
    nft_traits = nft['attributes']
    total_rarity_score = 0  # Initialize total rarity score for the NFT
    rarity_scores = []  # Store rarity scores for each trait for later retrieval
    special_rank = None  # Initialize special rank

    # Check for special ranks
    classification = next((attr.get("value") for attr in nft_traits if attr.get("trait_type") == "Classification"), None)
    name = nft.get("name", "")
    index = nft.get("index", "Unknown")  # Use "index" for numeric identifiers

    # Determine special rank based on classification and name
    if classification == "Honorary Citizen":
        special_rank = 0
    elif classification == "Legends of Block City":
        special_rank = 2
    if "Techno Lord" in name:
        special_rank = 1
    elif "Gold Pass" in name:
        special_rank = 3
    elif "Silver Pass" in name:
        special_rank = 4

    # Calculate rarity scores for non-special items
    for trait in nft_traits:
        trait_type = trait.get('trait_type')  # Ensure 'trait_type' exists
        trait_value = trait.get('value')      # Ensure 'value' exists
        if trait_type in traits_to_exclude or trait_type == 'rarity':  # Skip excluded traits
            continue
        
        rarity_score = calculate_rarity_score(trait_type, trait_value)
        total_rarity_score += rarity_score  # Sum all trait rarity scores for the NFT
        rarity_scores.append((trait_type, trait_value, rarity_score))  # Store for later

    if rarity_scores or special_rank is not None:
        # Find the rarest trait based on the highest rarity score
        rarest_trait = max(rarity_scores, key=lambda x: x[2]) if rarity_scores else ("None", "None", 0)
        nft_rankings.append((index, name, total_rarity_score, rarest_trait, special_rank))

# Step 6: Order NFTs by Special Rank and Rarity Score
nft_rankings.sort(key=lambda x: (x[4] if x[4] is not None else float('inf'), -x[2]))  # Sort by rank, then rarity score

# Step 7: Save Rarity Rankings to a Markdown File
md_filename = r"Comrade-rarity.md"

disclaimer = """\
⚠️ **NoMoreLabs Approved Disclaimer** ⚠️  

Greetings, Comrade Collector! Please note that the rankings provided by this script are **not guaranteed**, **subject to change**, and should not be used as a definitive measure of value, rarity, or your worth as a human being (or robot).  

The calculations are based on cold, unfeeling math and may not reflect the true essence of your beloved Comrades. Remember, rarity does not equate to monetary value, emotional attachment, or your ability to barter for piles of shitcoins in Block City.  

**NoMoreLabs reminds you:**  
- Rankings are for **entertainment purposes only**.  
- Traits and scores may shift faster than a floorbagorb in The Drains Plains.  
- Do not attempt to use these rankings to impress scriboors, yeti people, or your local General.  

By using this script, you acknowledge that NoMoreLabs (and its affiliates) are not responsible for any disputes, existential crises, or trading mishaps that may arise. Collect responsibly, and may your Comrades always have the rarest of traits and the shiniest of hats!  

**Remember, Comrade: The real rarity is the friends we made along the way.**  
"""

# Prepare ranked data with JSON output
ranked_nft_data = nft_data.copy()
ranked_items = []

with open(md_filename, 'w', encoding="utf-8") as md_file:
    md_file.write(disclaimer + "\n\n")
    
    # Separate special ranked and non-special ranked items
    special_ranked_items = [item for item in nft_rankings if item[4] is not None]
    non_special_ranked_items = [item for item in nft_rankings if item[4] is None]
    
    # Write special ranked items first and track for JSON
    for rank, (index, name, total_rarity_score, rarest_trait, special_rank) in enumerate(special_ranked_items):
        rarest_trait_type, rarest_trait_value, _ = rarest_trait
        rank_text = f"Rank {special_rank:05d}"
        formatted_index = f"Comrade #{index:05d}"
        text = f"{rank_text} - {formatted_index} ({name}) | Rarest trait = {rarest_trait_type} - {rarest_trait_value}\n\n"
        md_file.write(text)
        
        # Prepare the item for JSON update
        for item in ranked_nft_data['collection_items']:
            if item['index'] == index:
                item_to_update = item
                break
        item_to_update['attributes'].append({
            "trait_type": "Rank",
            "value": f"{special_rank:05d}"
        })
        ranked_items.append(item_to_update)
    
    # Continue ranking from 5 for non-special items
    for rank, (index, name, total_rarity_score, rarest_trait, _) in enumerate(non_special_ranked_items, start=5):
        rarest_trait_type, rarest_trait_value, _ = rarest_trait
        rank_text = f"Rank {rank:05d}"
        formatted_index = f"Comrade #{index:05d}"
        text = f"{rank_text} - {formatted_index} ({name}) | Rarest trait = {rarest_trait_type} - {rarest_trait_value}\n\n"
        md_file.write(text)
        
        # Prepare the item for JSON update
        for item in ranked_nft_data['collection_items']:
            if item['index'] == index:
                item_to_update = item
                break
        item_to_update['attributes'].append({
            "trait_type": "Rank",
            "value": f"{rank:05d}"
        })
        ranked_items.append(item_to_update)

print(f"Rarity rankings saved to {md_filename}")

# Step 8: Output updated JSON with ranks
output_json_filename = r"ranked_comrades.json"
with open(output_json_filename, 'w', encoding="utf-8") as json_file:
    json.dump(ranked_nft_data, json_file, indent=2)

print(f"Updated JSON with ranks saved to {output_json_filename}")

# Step 9: Reorder NFTs by Item Number for Output
nft_rankings.sort(key=lambda x: int(x[0]))  # Re-sort by item number (ascending) for display purposes

# Step 10: Calculate and Print Rarity Scores for Traits
trait_scores_filename = r"Comrade-trait-scores.md"

with open(trait_scores_filename, 'w', encoding="utf-8") as trait_scores_file:
    print("\n-------------------------------------------------------------\nRarity Scores for Traits (sorted by most rare to least rare):\n-------------------------------------------------------------")
    sorted_traits = sorted(trait_value_counts.items(), key=lambda x: (x[1] / total_items))  # Sort by rarity score (most rare first)
    
    for rank, (trait, count) in enumerate(sorted_traits, start=1):  # Rank starts at 1
        trait_type, trait_value = trait
        
        # Skip the 'rarity' trait_type and excluded traits
        if trait_type == 'rarity' or trait_type in traits_to_exclude:
            continue
        
        rarity_score = calculate_rarity_score(trait_type, trait_value)
        frequency = count
        
        # Print and write to file
        line = f"Rank {rank:05d} - {trait_type} - {trait_value} | rarity score = {rarity_score:.2f} | frequency = {frequency} / {total_items}\n\n"
        print(line.strip())
        trait_scores_file.write(line)  # Add an extra newline after each entry

print(f"\nRarity scores for traits have been saved to: {trait_scores_filename}")

print("\ns/o to chopperdaddy: https://github.com/chopperdaddy Ethereum Phunks: https://ethereumphunks.com VirtualAlaska: https://github.com/VirtualAlaska and mfpurrs: https://x.com/mfpurrs")
