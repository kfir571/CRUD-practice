# project/src/smoke_service.py
from __future__ import annotations
import json
from typing import Any, Callable

# טעינת .env מכל מקום בפרויקט (לא חובה אם כבר טענת במקום אחר)
try:
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv())
except Exception:
    pass

import pandas as pd

# מייבא רק פונקציות משלב 4
from connector.service import (
    get_posts_with_users,
    get_number_post_per_user,
    posts_with_keyword,   # שם הפונקציה כפי שמימשת
    get_longest_posts,
)

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

passed = 0
failed = 0

def ok(msg: str) -> None:
    global passed
    passed += 1
    print(f"{GREEN}PASS{RESET} - {msg}")

def fail(msg: str, err: Exception | None = None) -> None:
    global failed
    failed += 1
    if err:
        print(f"{RED}FAIL{RESET} - {msg}: {err}")
    else:
        print(f"{RED}FAIL{RESET} - {msg}")

def run_step(name: str, fn: Callable[[], Any]) -> Any:
    print(f"\n{YELLOW}==> {name}{RESET}")
    try:
        out = fn()
        ok(name)
        return out
    except AssertionError as e:
        fail(f"{name} (Assertion)", e)
    except Exception as e:
        fail(f"{name} (Unexpected)", e)

def pretty_table(df: pd.DataFrame, cols: list[str] | None = None, max_rows: int = 10) -> None:
    if cols:
        df = df[[c for c in cols if c in df.columns]]
    print(df.head(max_rows).to_string(index=False))

def main() -> int:
    # S1: get_posts_with_users – מחזיר DataFrame תקין עם userName
    df = run_step("S1 get_posts_with_users() returns DataFrame with userName", lambda: get_posts_with_users())
    if isinstance(df, pd.DataFrame):
        try:
            assert not df.empty, "DataFrame is empty"
            for col in ["id", "userId", "title", "body", "userName"]:
                assert col in df.columns, f"missing column: {col}"
            ok("Validate DataFrame shape/columns")
            pretty_table(df, cols=["id", "userId", "userName", "title"], max_rows=10)
        except AssertionError as e:
            fail("Validate DataFrame shape/columns", e)

    # S2: get_number_post_per_user – מחזיר מיפוי ושהסכום תואם לכמות הפוסטים
    counts = run_step("S2 get_number_post_per_user() returns mapping", lambda: get_number_post_per_user())
    if isinstance(counts, dict):
        try:
            assert counts, "empty mapping"
            assert all(isinstance(k, str) for k in counts.keys()), "keys must be userName (str)"
            assert all(isinstance(v, int) and v >= 0 for v in counts.values()), "values must be non-negative int"
            # סכום הספירות מול מספר הפוסטים בטבלה
            total_posts = len(df) if isinstance(df, pd.DataFrame) else sum(counts.values())
            assert sum(counts.values()) == total_posts, "sum(counts) != total posts"
            ok("Validate counts mapping and totals")
            # הצגה תמציתית
            top = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)
            print("\nTop users by post_count:")
            for name, c in top:
                print(f" - {name}: {c}")
                # הצג רק כמה ראשונים
                if top.index((name, c)) >= 4:
                    break
        except AssertionError as e:
            fail("Validate counts mapping and totals", e)

    # S3: posts_with_keyword – חיפוש לפי מילת מפתח (רגיש רישיות אצלך)
    ids = run_step('S3 posts_with_keyword("quia") returns list of IDs', lambda: posts_with_keyword("quia"))
    if isinstance(ids, list):
        try:
            assert all(isinstance(i, int) for i in ids), "IDs must be integers"
            # הצגה תמציתית של תוצאות
            if ids:
                subset = df[df["id"].isin(ids)][["id", "userName", "title"]] if isinstance(df, pd.DataFrame) else None
                print("\nSearch results for 'quia' (showing up to 10):")
                if subset is not None and not subset.empty:
                    pretty_table(subset.sort_values("id"), max_rows=10)
                else:
                    # אם אין DF זמין מסיבה כלשהי
                    print(ids[:10])
            else:
                print("No matches for 'quia' (this can be valid).")
            ok("Validate keyword search shape")
        except AssertionError as e:
            fail("Validate keyword search", e)

    # S4: get_longest_posts – תומך בפורמט הנוכחי שלך (list עם dict יחיד userName->body)
    data = run_step("S4 get_longest_posts(5) returns supported structure", lambda: get_longest_posts(5))
    if data is not None:
        try:
            assert isinstance(data, list) and len(data) >= 1, "expected list with at least one element"
            first = data[0]
            assert isinstance(first, dict), "expected first element to be a dict (userName -> body)"
            assert first, "first dict is empty"
            # בדיקה שהערכים הם טקסטים (גוף פוסט)
            assert all(isinstance(v, str) for v in first.values()), "values must be strings (post bodies)"
            # הצג אורכים
            lens = sorted([(k, len(v)) for k, v in first.items()], key=lambda kv: kv[1], reverse=True)
            print("\nLongest posts (by body length) – userName & length:")
            for name, L in lens[:5]:
                print(f" - {name}: {L}")
            ok("Validate longest-posts structure and body lengths")
        except AssertionError as e:
            fail("Validate longest-posts structure", e)

    # סיכום
    total = passed + failed
    print("\n" + "=" * 40)
    print(f"Total: {total} | {GREEN}Passed: {passed}{RESET} | {RED}Failed: {failed}{RESET}")
    print("=" * 40)
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
