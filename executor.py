import subprocess
import tempfile
import os


def run_java(code):

    with tempfile.TemporaryDirectory() as temp_dir:

        java_file = os.path.join(temp_dir, "Main.java")

        with open(java_file, "w", encoding="utf-8") as file:
            file.write(code)

        # Compile
        compile_result = subprocess.run(
            ["javac", java_file],
            capture_output=True,
            text=True,
            timeout=5
        )

        if compile_result.returncode != 0:
            return {
                "success": False,
                "output": compile_result.stderr
            }

        # Run
        run_result = subprocess.run(
            ["java", "-cp", temp_dir, "Main"],
            capture_output=True,
            text=True,
            timeout=5
        )

        if run_result.returncode != 0:
            return {
                "success": False,
                "output": run_result.stderr
            }

        return {
            "success": True,
            "output": run_result.stdout
        }
    
if __name__ == "__main__":
    code = """
public class Main {
    public static void main(String[] args) {
        System.out.println("Hello DSA"
    }
}
"""

    result = run_java(code)

    print(result)