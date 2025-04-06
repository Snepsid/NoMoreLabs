# NoMoreLabs
# Calculate Comrade Rarity

This Python script calculates the rarity of traits for a collection of NFTs and ranks the NFTs based on their total rarity scores. It outputs two files: one for the rarity rankings of the NFTs and another for the rarity scores of individual traits.

## Features

- **Trait Frequency Calculation**: Counts the occurrences of each trait value across the collection.
- **Rarity Score Calculation**: Computes rarity scores for each trait using the formula:
  ```
  Rarity Score = Total Items / Frequency of Trait Value
  ```
- **NFT Ranking**: Ranks NFTs based on their total rarity scores, starting from rank #5.
- **Trait Rarity Output**: Outputs a ranked list of traits based on their rarity scores.

## Outputs

### 1. `Comrade-rarity.txt`
This file contains the ranked list of NFTs based on their total rarity scores. Each line includes:
- The rank of the NFT (starting from #5).
- The NFT's item number.
- The rarest trait of the NFT and its value.

**Example:**
```
Rank 00005 - Comrade #00017 | Rarest trait = Background - Super Rare Holographic Ittybits Background
Rank 00006 - Comrade #00010 | Rarest trait = Eyes - Visoor Pink
Rank 00007 - Comrade #00005 | Rarest trait = Eyes - Block Vision ETHS Heart
```

### 2. `Comrade-trait-scores.txt`
This file contains the ranked list of traits based on their rarity scores. Each line includes:
- The rank of the trait (starting from #1).
- The trait type and value.
- The rarity score of the trait.
- The frequency of the trait value in the collection.

**Example:**
```
Rank 00001 - Background - Sir Pinkalot | rarity score = 9818.00 | frequency = 1 / 9818
Rank 00002 - Accessories - None | rarity score = 4909.00 | frequency = 2 / 9818
Rank 00003 - Type - Scriboor | rarity score = 3272.67 | frequency = 3 / 9818
```

## How to Use

1. **Prepare the Metadata File**:
   - Ensure the metadata file is named `Comrade-metadata.json` and is located in the same directory as the script.
   - The metadata file should follow the structure:
     ```json
     {
         "collection_items": [
             {
                 "name": "1",
                 "attributes": [
                     {"trait_type": "Background", "value": "Sir Pinkalot"},
                     {"trait_type": "Accessories", "value": "None"}
                 ]
             },
             ...
         ]
     }
     ```

2. **Run the Script**:
   - Execute the script using Python:
     ```bash
     python Comrade-calculator.py
     ```

3. **View the Outputs**:
   - The script generates two output files:
     - `Comrade-rarity.txt`: Contains the NFT rankings.
     - `Comrade-trait-scores.txt`: Contains the trait rarity scores.

## Notes

- Traits like `Affiliation` and `Classification` are excluded from the rarity calculations.
- The script assumes the `name` field in the metadata represents the item number and does not modify it.

## Acknowledgments

Special thanks to:
- [chopperdaddy](https://github.com/chopperdaddy)
- [Ethereum Phunks](https://ethereumphunks.com)
- [VirtualAlaska](https://github.com/VirtualAlaska)
- [mfpurrs](https://x.com/mfpurrs)
- [Snepsid](https://github.com/Snepsid)
- [Nakamingos](https://nakamingos.io)

## License

This project is licensed under the CC0 1.0 Universal (Public Domain Dedication). See the `LICENSE` file for details.
