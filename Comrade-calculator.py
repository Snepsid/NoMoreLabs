import json
from collections import defaultdict

# Step 1: Read the JSON File
with open(r"Comrade-metadata.json", 'r') as json_file:
    nft_data = json.load(json_file)
    total_retrieved = len(nft_data['collection_items'])

# Step 2: Print Status
if total_retrieved == 9818:
    print("Retrieved 9,818 Comrades.\nCalculating rarity...")
else:
    print(f"Retrieved the wrong number of Comrades. Expected 9,818 but retrieved {total_retrieved}.")

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

    for trait in nft_traits:
        trait_type = trait.get('trait_type')  # Ensure 'trait_type' exists
        trait_value = trait.get('value')      # Ensure 'value' exists
        if trait_type in traits_to_exclude or trait_type == 'rarity':  # Skip excluded traits
            continue
        
        rarity_score = calculate_rarity_score(trait_type, trait_value)
        total_rarity_score += rarity_score  # Sum all trait rarity scores for the NFT
        rarity_scores.append((trait_type, trait_value, rarity_score))  # Store for later

    if rarity_scores:
        # Find the rarest trait based on the highest rarity score
        rarest_trait = max(rarity_scores, key=lambda x: x[2])
        nft_rankings.append((nft['name'], total_rarity_score, rarest_trait))

# Step 6: Order NFTs by Rarity Score (Descending)
nft_rankings.sort(key=lambda x: x[1], reverse=True)  # Sort by total rarity score (highest first)

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

with open(md_filename, 'w', encoding="utf-8") as md_file:
    md_file.write(disclaimer + "\n\n")
    starting_rank = 5  # Start rankings from #5
    for rank, (nft_name, total_rarity_score, rarest_trait) in enumerate(nft_rankings, start=starting_rank):
        rarest_trait_type, rarest_trait_value, _ = rarest_trait
        text = f"Rank {rank:05d} - Comrade #{int(nft_name):05d} | Rarest trait = {rarest_trait_type} - {rarest_trait_value}\n\n"
        md_file.write(text)  # Add an extra newline after each entry

# Step 8: Reorder NFTs by Item Number for Output
nft_rankings.sort(key=lambda x: int(x[0]))  # Re-sort by item number (ascending) for display purposes

# Step 9: Calculate and Print Rarity Scores for Traits
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
