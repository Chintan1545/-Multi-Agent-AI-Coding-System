import multiprocessing
import sys
import io
import re

MAX_INT = 10**9    # cap huge numbers
MAX_RANGE = 10**6  # cap range lengths

# 🔹 Top-level function (required for Windows multiprocessing)
def _target_func(queue, code):
    try:
        # 1️⃣ Cap huge numbers
        def replacer(match):
            num = int(match.group())
            return str(min(num, MAX_INT))
        safe_code = re.sub(r'\b\d{10,}\b', replacer, code)

        # 2️⃣ Safe range replacement
        def safe_range(*args):
            r = range(*args)
            if len(r) > MAX_RANGE:
                r = range(MAX_RANGE)
            return r

        # 3️⃣ Redirect stdout
        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()
        exec(safe_code, {"range": safe_range})
        output = buffer.getvalue()
        sys.stdout = old_stdout

        queue.put(("success", output))
    except Exception as e:
        queue.put(("error", str(e)))

def run_code_safely(code: str, timeout: int = 10):
    """
    Execute Python code safely with timeout.
    """
    queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=_target_func, args=(queue, code))
    process.start()
    process.join(timeout)

    if process.is_alive():
        process.terminate()
        return "⏱️ Execution timed out."

    if queue.empty():
        return "⚠️ No output captured."

    status, result = queue.get()
    if status == "success":
        return result if result else "✅ Code executed successfully (no output)."
    else:
        return f"❌ Error: {result}"
