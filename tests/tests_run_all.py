import os
import importlib.util
import time

# ANSI escape codes
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def run_all_tests():
    test_files = [
        "test_physics_model.py",
        "test_no_threats.py",
        "test_threat_flip.py",
        "test_high_momentum.py",
        "test_counter_torque.py"
    ]

    print(f"\n{YELLOW}🧪 Running all physics test cases:{RESET}\n")
    total_start_time = time.time()

    for filename in test_files:
        path = os.path.join(os.path.dirname(__file__), filename)
        print(f"\n==============================")
        print(f"▶️  {filename}")
        print(f"==============================")
        
        start_time = time.time()
        try:
            spec = importlib.util.spec_from_file_location("test_module", path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if hasattr(module, "run_test"):
                module.run_test()
                print(f"{GREEN}✅ Test passed successfully!{RESET}")
            else:
                print(f"{YELLOW}⚠️  No run_test() function found in this test file.{RESET}")
        except Exception as e:
            print(f"{RED}❌ Test failed with error: {e}{RESET}")

        end_time = time.time()
        print(f"⏱️ Test duration: {end_time - start_time:.3f} seconds")

    total_end_time = time.time()
    print(f"\n{GREEN}✅ All tests completed.{RESET}")
    print(f"🕒 Total time: {total_end_time - total_start_time:.2f} seconds")

if __name__ == '__main__':
    run_all_tests()
