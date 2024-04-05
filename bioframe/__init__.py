try:
    from importlib.metadata import PackageNotFoundError, version
except ImportError:
    from importlib_metadata import PackageNotFoundError, version

try:
    __version__ = version("bioframe")
except PackageNotFoundError:
    __version__ = "unknown"

__all__ = [
    "arrops",
    "from_any",
    "from_dict",
    "from_list",
    "from_series",
    "is_bedframe",
    "is_cataloged",
    "is_chrom_dtype",
    "is_complete_ucsc_string",
    "is_contained",
    "is_covering",
    "is_overlapping",
    "is_sorted",
    "is_tiling",
    "is_viewframe",
    "make_viewframe",
    "parse_region",
    "parse_region_string",
    "sanitize_bedframe",
    "to_ucsc_string",
    "update_default_colnames",
    "binnify",
    "digest",
    "frac_gc",
    "frac_gene_coverage",
    "frac_mapped",
    "make_chromarms",
    "pair_by_distance",
    "seq_gc",
    "SCHEMAS",
    "UCSCClient",
    "assemblies_available",
    "assembly_info",
    "fetch_centromeres",
    "fetch_chromsizes",
    "load_fasta",
    "read_bam",
    "read_bigbed",
    "read_bigwig",
    "read_chromsizes",
    "read_pairix",
    "read_tabix",
    "read_table",
    "to_bigbed",
    "to_bigwig",
    "assign_view",
    "closest",
    "cluster",
    "complement",
    "count_overlaps",
    "coverage",
    "expand",
    "merge",
    "overlap",
    "select",
    "select_indices",
    "select_labels",
    "select_mask",
    "setdiff",
    "sort_bedframe",
    "subtract",
    "trim",
    "plot_intervals",
    "to_ucsc_colorstring",
]

from .core import (
    arrops,
    from_any,
    from_dict,
    from_list,
    from_series,
    is_bedframe,
    is_cataloged,
    is_chrom_dtype,
    is_complete_ucsc_string,
    is_contained,
    is_covering,
    is_overlapping,
    is_sorted,
    is_tiling,
    is_viewframe,
    make_viewframe,
    parse_region,
    parse_region_string,
    sanitize_bedframe,
    to_ucsc_string,
    update_default_colnames,
)
from .extras import (
    binnify,
    digest,
    frac_gc,
    frac_gene_coverage,
    frac_mapped,
    make_chromarms,
    pair_by_distance,
    seq_gc,
)
from .io import (
    SCHEMAS,
    UCSCClient,
    assemblies_available,
    assembly_info,
    fetch_centromeres,
    fetch_chromsizes,
    load_fasta,
    read_bam,
    read_bigbed,
    read_bigwig,
    read_chromsizes,
    read_pairix,
    read_tabix,
    read_table,
    to_bigbed,
    to_bigwig,
)
from .ops import (
    assign_view,
    closest,
    cluster,
    complement,
    count_overlaps,
    coverage,
    expand,
    merge,
    overlap,
    select,
    select_indices,
    select_labels,
    select_mask,
    setdiff,
    sort_bedframe,
    subtract,
    trim,
)
from .vis import plot_intervals, to_ucsc_colorstring

del version, PackageNotFoundError
