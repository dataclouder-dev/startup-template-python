import os
import sys

# Add the project root to sys.path
sys.path.append(os.getcwd())

from app.generics.services import generic_service
from app.generics.models.generic_model import GenericModel
from dataclouder_core.models.models import FiltersConfig

def verify():
    print("Testing save_generic (create)...")
    model = GenericModel(
        name="Verification Test",
        description="Testing refactored service",
        type="test",
        image={},
        relation={}
    )
    result = generic_service.save_generic(model)
    print(f"Result: {result}")
    
    # Extract the ID from the result. Depending on the return of find_one_and_replace
    # it might be a dict with '_id'.
    generic_id = result.get("_id")
    print(f"Generic ID: {generic_id}")

    if not generic_id:
        print("Error: No ID returned")
        return

    print("\nTesting find_generics...")
    found = generic_service.find_generics(generic_id)
    print(f"Found: {found}")

    print("\nTesting find_filtered_generics...")
    filters = FiltersConfig(name="Verification Test")
    filtered = generic_service.find_filtered_generics(filters)
    print(f"Filtered (count): {len(filtered)}")

    print("\nTesting save_generic (update)...")
    model.id = generic_id
    model.description = "Updated description"
    update_result = generic_service.save_generic(model)
    print(f"Update Result: {update_result}")

    print("\nTesting delete_generic...")
    delete_result = generic_service.delete_generic(generic_id)
    print(f"Delete Result: {delete_result}")

if __name__ == "__main__":
    verify()
