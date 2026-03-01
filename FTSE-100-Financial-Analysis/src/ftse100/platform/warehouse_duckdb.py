from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, Tuple

import duckdb


def _create_table_from_parquet(con: duckdb.DuckDBPyConnection, fq_name: str, parquet_path: Path) -> None:
    parquet_path = parquet_path.resolve()
    schema, table = fq_name.split(".", 1)
    con.execute(f"CREATE SCHEMA IF NOT EXISTS {schema};")
    con.execute(f"CREATE OR REPLACE TABLE {schema}.{table} AS SELECT * FROM read_parquet('{parquet_path.as_posix()}');")


def build_duckdb_warehouse(
    *,
    db_path: Path,
    parquet_tables: Dict[str, Path],
) -> Path:
    """Build a local DuckDB warehouse file populated with platform tables.

    Parameters
    ----------
    db_path:
        Where to write the DuckDB database (e.g. v2_modernisation_realtime/db/warehouse.duckdb)
    parquet_tables:
        Mapping of fully-qualified table name -> parquet file path.
        Example: {'bronze.ftse100_intraday_1m_bronze': Path('.../bronze.parquet')}
    """
    db_path.parent.mkdir(parents=True, exist_ok=True)

    # If a placeholder/invalid file exists, rebuild cleanly.
    if db_path.exists():
        db_path.unlink()

    con = duckdb.connect(database=str(db_path), read_only=False)
    try:
        con.execute("PRAGMA threads=4;")
        for fq, p in parquet_tables.items():
            _create_table_from_parquet(con, fq, p)
        con.execute("ANALYZE;")
    finally:
        con.close()
    return db_path
