"""
Script to run API tests with Allure reporting
"""
import subprocess
import sys
import os


def main():
    """Run tests and generate Allure report"""
    print("=" * 60)
    print("Running ioka API Tests")
    print("=" * 60)
    
    # Run tests
    print("\n[1/2] Running tests...")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "--alluredir=allure-results", "-v"],
        cwd=os.path.dirname(os.path.abspath(__file__))
    )
    
    if result.returncode != 0:
        print("\n⚠️  Some tests failed!")
        return result.returncode
    
    print("\n[2/2] Tests completed successfully!")
    print("\n" + "=" * 60)
    print("To view Allure report, run:")
    print("  allure serve allure-results")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

