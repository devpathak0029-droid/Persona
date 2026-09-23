import sys
import os
import json
from pathlib import Path

# Add the project root to sys.path to import from src and data
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from data.synthetic.test_data import PERSONA_A_POSTS, PERSONA_B_POSTS, PERSONA_C_POSTS
from src.persona.profile_builder import build_profile
from src.comparison.pairwise import compare_profiles
from src.persona.migration import detect_migration

def run():
    print("Building Profile A...")
    profile_a = build_profile("Persona_A", PERSONA_A_POSTS)
    
    print("Building Profile B...")
    profile_b = build_profile("Persona_B", PERSONA_B_POSTS)
    
    print("Building Profile C...")
    profile_c = build_profile("Persona_C", PERSONA_C_POSTS)

    print("Comparing Profiles A and B...")
    comp_a_b = compare_profiles(profile_a, profile_b)
    
    print("Comparing Profiles A and C...")
    comp_a_c = compare_profiles(profile_a, profile_c)
    
    print("Detecting migration between A and B...")
    migration_a_b = detect_migration(profile_a, profile_b, PERSONA_A_POSTS, PERSONA_B_POSTS)

    output = {
        "profiles": {
            "Persona_A": profile_a,
            "Persona_B": profile_b,
            "Persona_C": profile_c
        },
        "comparisons": {
            "A_vs_B": comp_a_b,
            "A_vs_C": comp_a_c
        },
        "migration_detection": {
            "A_to_B": migration_a_b
        }
    }

    output_file = project_root / "integration_output.json"
    with open(output_file, "w") as f:
        json.dump(output, f, indent=2, default=str)

    print(f"\nIntegration run complete. Results saved to {output_file}")
    
    # Print some summary results
    print("\nSummary:")
    print(f"Similarity A vs B: Style={comp_a_b['style_similarity']:.2f}, Semantic={comp_a_b['semantic_similarity']:.2f}, Behavior={comp_a_b['behavioral_association']:.2f}")
    print(f"Similarity A vs C: Style={comp_a_c['style_similarity']:.2f}, Semantic={comp_a_c['semantic_similarity']:.2f}, Behavior={comp_a_c['behavioral_association']:.2f}")
    
    mig_detected = migration_a_b['detected']
    print(f"Migration A -> B Detected: {mig_detected}")
    if mig_detected:
        print(f"Migration Confidence Score: {sum(migration_a_b['signals'].values())/5.0:.2f}")

if __name__ == "__main__":
    run()
