"""Derive obstetric cohort metrics from the Houm Smart-NC mirror.

Aggregate output only: no name, chart number, RRN, or birth date is selected
anywhere. Cells under 5 are masked as ``<5`` before printing.

Usage::

    python derive_cohort_metrics.py --db path/to/smart_rpa.db \\
        --start 20210901 --end 20260831

    python derive_cohort_metrics.py --db ... --start ... --end ... --bound-sweep
    python derive_cohort_metrics.py --db ... --start ... --end ... --era-check

Reads the SQLite mirror read-only through DuckDB. Never writes.

Read SKILL.md before trusting any number this prints. Several metrics are
derivable but not comparable, and the ones this script refuses to emit are
refusals on purpose -- see references/metric-map.md.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import duckdb

DELIVERY = "SUBSTR(code,1,3) IN ('O80','O81','O82','O83','O84') OR code='O757'"
KEY = "org, cn, iseq, mseq"


def connect(db_path: str) -> duckdb.DuckDBPyConnection:
    # ATTACH takes no bind parameters, so the path is inlined. It comes from the
    # operator's own command line, but quote it defensively anyway: reject a path
    # that does not resolve to a file, and double any single quote.
    resolved = Path(db_path).expanduser().resolve(strict=True)
    if not resolved.is_file():
        raise SystemExit(f"not a file: {resolved}")
    literal = str(resolved).replace("'", "''")
    con = duckdb.connect()
    con.execute(f"ATTACH '{literal}' AS s (TYPE sqlite, READ_ONLY)")
    con.execute(
        """CREATE TABLE dx AS SELECT organization_id org, customer_number cn,
           insurance_seq_no iseq, medical_clinic_seq_no mseq,
           UPPER(TRIM(COALESCE(sick_code,''))) code FROM s.diagnoses"""
    )
    con.execute(
        """CREATE TABLE mc AS SELECT organization_id org, customer_number cn,
           insurance_seq_no iseq, medical_clinic_seq_no mseq,
           COALESCE(medical_day,'') AS v_day FROM s.medical_clinics"""
    )
    con.execute(
        """CREATE TABLE rx AS SELECT organization_id org, customer_number cn,
           insurance_seq_no iseq, medical_clinic_seq_no mseq,
           COALESCE(prescription_order_name,'') nm FROM s.prescriptions"""
    )
    return con


def mask(n: int) -> str:
    """The privacy rule every caller has agreed to: never expose a cell under 5."""
    return "<5" if 0 < n < 5 else f"{n:,}"


def build_window(con, start: str, end: str) -> None:
    con.execute(
        f"""CREATE TABLE bv AS SELECT DISTINCT d.{KEY} FROM dx d
            JOIN mc USING ({KEY})
            WHERE mc.v_day BETWEEN ? AND ? AND ({DELIVERY})""",
        [start, end],
    )
    con.execute(
        f"""CREATE TABLE flags AS SELECT b.{KEY},
        MAX(CASE WHEN SUBSTR(d.code,1,3)='O82' OR d.code='O842' THEN 1 ELSE 0 END) cs,
        MAX(CASE WHEN d.code='O821' THEN 1 ELSE 0 END) cs_emerg,
        MAX(CASE WHEN d.code='O820' THEN 1 ELSE 0 END) cs_elec,
        MAX(CASE WHEN SUBSTR(d.code,1,3)='O80' OR d.code IN ('O757','O840','O841')
                  OR SUBSTR(d.code,1,3) IN ('O81','O83') THEN 1 ELSE 0 END) vaginal,
        MAX(CASE WHEN SUBSTR(d.code,1,3) IN ('O81','O83') OR d.code='O841'
                 THEN 1 ELSE 0 END) assisted,
        MAX(CASE WHEN d.code='O757' THEN 1 ELSE 0 END) vbac,
        MAX(CASE WHEN d.code='O700' THEN 1 ELSE 0 END) t1,
        MAX(CASE WHEN d.code='O701' THEN 1 ELSE 0 END) t2,
        MAX(CASE WHEN d.code='O702' THEN 1 ELSE 0 END) t3,
        MAX(CASE WHEN d.code='O703' THEN 1 ELSE 0 END) t4,
        MAX(CASE WHEN SUBSTR(d.code,1,3) IN ('O95','O96','O97') THEN 1 ELSE 0 END) mdeath,
        MAX(CASE WHEN SUBSTR(d.code,1,3)='O71' THEN 1 ELSE 0 END) rupture,
        MAX(CASE WHEN SUBSTR(d.code,1,3)='O72' THEN 1 ELSE 0 END) pph,
        MAX(CASE WHEN SUBSTR(d.code,1,3) IN ('O13','O14','O15') THEN 1 ELSE 0 END) preecl,
        MAX(CASE WHEN SUBSTR(d.code,1,3)='O30' THEN 1 ELSE 0 END) multi,
        MAX(CASE WHEN d.code='O801' THEN 1 ELSE 0 END) breech_vag,
        MAX(CASE WHEN d.code='P95' THEN 1 ELSE 0 END) stillbirth
        FROM bv b JOIN dx d USING ({KEY}) GROUP BY 1,2,3,4"""
    )
    con.execute(
        f"""CREATE TABLE proc AS SELECT b.{KEY},
        MAX(CASE WHEN r.nm LIKE '%회음절개%' THEN 1 ELSE 0 END) episiotomy,
        MAX(CASE WHEN r.nm LIKE '%옥시토신%' OR r.nm LIKE '%옥시톤%' THEN 1 ELSE 0 END) oxytocin,
        MAX(CASE WHEN r.nm LIKE '%경막외%' OR UPPER(r.nm) LIKE '%EPIDURAL%' THEN 1 ELSE 0 END) epidural,
        MAX(CASE WHEN r.nm LIKE '%수중%' THEN 1 ELSE 0 END) water
        FROM bv b LEFT JOIN rx r USING ({KEY}) GROUP BY 1,2,3,4"""
    )


def report(con, start: str, end: str) -> None:
    f = con.execute(
        """SELECT COUNT(*) births, COUNT(DISTINCT cn) mothers, SUM(cs) cs,
           SUM(cs_emerg) cs_emerg,
           SUM(CASE WHEN cs=1 AND cs_emerg=0 AND cs_elec=1 THEN 1 ELSE 0 END) cs_elec,
           SUM(CASE WHEN cs=1 AND cs_emerg=0 AND cs_elec=0 THEN 1 ELSE 0 END) cs_unspec,
           SUM(vaginal) vaginal, SUM(assisted) assisted, SUM(vbac) vbac,
           SUM(t1) t1, SUM(t2) t2, SUM(t3) t3, SUM(t4) t4,
           SUM(mdeath) mdeath, SUM(rupture) rupture, SUM(pph) pph,
           SUM(preecl) preecl, SUM(multi) multi, SUM(breech_vag) breech_vag,
           SUM(CASE WHEN multi=1 AND vaginal=1 THEN 1 ELSE 0 END) multi_vag,
           SUM(stillbirth) stillbirth FROM flags"""
    ).df().iloc[0].astype(int).to_dict()
    p = con.execute(
        """SELECT SUM(episiotomy) episiotomy, SUM(oxytocin) oxytocin,
           SUM(epidural) epidural, SUM(water) water FROM proc"""
    ).df().iloc[0].astype(int).to_dict()
    intact = con.execute(
        f"""SELECT COUNT(*) FROM flags f JOIN proc p USING ({KEY})
            WHERE f.vaginal=1 AND f.t1+f.t2+f.t3+f.t4=0 AND p.episiotomy=0"""
    ).fetchone()[0]

    births, vag = f["births"], f["vaginal"]
    print(f"\n기간 {start} ~ {end}")
    print(f"분만 방문 {births:,}건 / 산모 {f['mothers']:,}명"
          f"  (방문/산모 = {births / max(f['mothers'], 1):.2f})\n")

    rows = [
        ("A07", "제왕절개 (전체)", f["cs"], births),
        ("A08", "제왕절개 (계획)", f["cs_elec"], births),
        ("A09", "제왕절개 (응급)", f["cs_emerg"], births),
        ("", "제왕절개 (구분불명)", f["cs_unspec"], births),
        ("", "질식분만", vag, births),
        ("", "  기구 보조", f["assisted"], births),
        ("A12", "VBAC (전체 분만 대비)", f["vbac"], births),
        ("A13", "자궁파열", f["rupture"], None),
        ("A14", "회음 무손상 (열상·절개 없음)", intact, vag),
        ("", "  1도 열상", f["t1"], vag),
        ("", "  2도 열상 ★코딩관행 확인", f["t2"], vag),
        ("A15", "3도 열상", f["t3"], vag),
        ("A16", "4도 열상", f["t4"], vag),
        ("A17", "모성사망", f["mdeath"], births),
        ("A18", "사산 (P95)", f["stillbirth"], births),
        ("B01", "회음절개", p["episiotomy"], vag),
        ("B04", "경막외 마취", p["epidural"], births),
        ("B10", "수중분만 (청구 기준)", p["water"], vag),
        ("C05", "자간전증", f["preecl"], births),
        ("C06", "다태 질식분만", f["multi_vag"], f["multi"]),
        ("C07", "둔위 질식분만", f["breech_vag"], births),
        ("", "산후출혈 진단 (O72*)", f["pph"], births),
    ]
    print(f"{'ID':<5}{'지표':<30}{'분자':>9}{'분모':>9}{'비율':>9}")
    print("-" * 62)
    for mid, name, num, den in rows:
        ratio = f"{100.0 * num / den:.1f}%" if den else "—"
        print(f"{mid:<5}{name:<30}{mask(num):>9}{(f'{den:,}' if den else '—'):>9}{ratio:>9}")

    print("\n[산출하지 않음 — 근거는 references/metric-map.md]")
    print("  A01/A02 분모, A03/A04 전원, A05/A06 산과력, A10/A11 TOLAC,")
    print("  B02 유도, B03 옥시토신(목적 구분 불가, 원시 건수 "
          f"{p['oxytocin']:,}), B05/B06 실혈량,")
    print("  B07-B09 분만자세, B11-B16 신생아·수유, C01-C04, C08-C10")


def era_check(con) -> None:
    """Coding practice shifts between eras. Never quote a cumulative total
    without looking at this first."""
    print("\n연도별 분만 방문 / 산모 / 방문당비율 (1.0에 가까워야 동일 정의)")
    df = con.execute(
        f"""SELECT SUBSTR(mc.v_day,1,4) yr, COUNT(*) births,
            COUNT(DISTINCT b.cn) mothers,
            ROUND(COUNT(*)*1.0/COUNT(DISTINCT b.cn),2) per_mother
            FROM (SELECT DISTINCT d.{KEY} FROM dx d WHERE {DELIVERY}) b
            JOIN mc USING ({KEY}) WHERE mc.v_day <> ''
            GROUP BY 1 ORDER BY 1"""
    ).df()
    print(df.to_string(index=False))


def bound_sweep(con, start: str, end: str, settled_by: str) -> None:
    """Upper bound on non-Houm delivery. Report the sweep, never one number."""
    con.execute(
        f"""CREATE TABLE anc AS SELECT d.cn, COUNT(DISTINCT mc.v_day) v,
            MAX(mc.v_day) last_anc FROM dx d JOIN mc USING ({KEY})
            WHERE mc.v_day BETWEEN ? AND ?
              AND SUBSTR(d.code,1,3) IN ('Z34','Z35') GROUP BY d.cn""",
        [start, end],
    )
    con.execute(f"CREATE TABLE deliv AS SELECT DISTINCT cn FROM bv")
    con.execute(
        f"""CREATE TABLE loss AS SELECT DISTINCT d.cn FROM dx d JOIN mc USING ({KEY})
            WHERE mc.v_day BETWEEN ? AND ? AND SUBSTR(d.code,1,3) IN
            ('O00','O01','O02','O03','O04','O05','O06','O07','O08')""",
        [start, end],
    )
    print(f"\n타 기관 분만 상한선 — 산전관리 종료 {settled_by} 이전 한정")
    print("★ 전원율이 아닙니다. 본인 선택을 포함하며 참 전원율보다 위에 있습니다.")
    print(f"\n{'산전방문':<12}{'분모':>9}{'호움분만':>10}{'타기관':>9}{'상한%':>9}")
    print("-" * 49)
    for k in (1, 3, 5, 6, 8, 10, 12):
        den = con.execute(
            "SELECT COUNT(*) FROM anc WHERE v>=? AND last_anc<? "
            "AND cn NOT IN (SELECT cn FROM loss)", [k, settled_by]
        ).fetchone()[0]
        out = con.execute(
            "SELECT COUNT(*) FROM anc WHERE v>=? AND last_anc<? "
            "AND cn NOT IN (SELECT cn FROM loss) "
            "AND cn NOT IN (SELECT cn FROM deliv)", [k, settled_by]
        ).fetchone()[0]
        if not den:
            continue
        print(f"{k:>3}회 이상   {den:>9,}{den - out:>10,}{out:>9,}{100.0 * out / den:>8.1f}%")
    print("\n임계값에 따라 답이 크게 움직이면 수렴하지 않는 것이며, "
          "단일 수치로 보고해서는 안 됩니다.")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--db", required=True, help="smart_rpa.db 경로")
    ap.add_argument("--start", required=True, help="YYYYMMDD")
    ap.add_argument("--end", required=True, help="YYYYMMDD")
    ap.add_argument("--settled-by", default=None,
                    help="이 날짜 이전에 산전관리가 끝난 산모만 상한선에 포함 "
                         "(기본: --end 6개월 전)")
    ap.add_argument("--era-check", action="store_true", help="연도별 코딩 관행 점검")
    ap.add_argument("--bound-sweep", action="store_true", help="타 기관 분만 상한선 sweep")
    args = ap.parse_args()

    for label, value in (("--start", args.start), ("--end", args.end)):
        if not (len(value) == 8 and value.isdigit()):
            ap.error(f"{label} must be YYYYMMDD; got {value!r}")

    settled = args.settled_by or f"{int(args.end[:4])}{args.end[4:6]}01"
    if args.settled_by is None:
        y, m = int(args.end[:4]), int(args.end[4:6]) - 6
        if m <= 0:
            y, m = y - 1, m + 12
        settled = f"{y:04d}{m:02d}01"

    con = connect(args.db)
    build_window(con, args.start, args.end)
    if args.era_check:
        era_check(con)
    report(con, args.start, args.end)
    if args.bound_sweep:
        bound_sweep(con, args.start, args.end, settled)
    print("\n5건 미만은 <5로 마스킹했습니다. 집계 수치만 포함합니다.")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
