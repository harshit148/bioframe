# Release notes

## [Upcoming release](https://github.com/open2c/bioframe/compare/v0.6.2...HEAD)

## [v0.6.2](https://github.com/open2c/bioframe/compare/v0.6.1...v0.6.2)

Changes:
* cols and df_view_col passed to downstream functions by @smitkadvani in https://github.com/open2c/bioframe/pull/182

Fixes:
* Update to new UCSC hgdownload url by @golobor and @nvictus in https://github.com/open2c/bioframe/pull/187

## [v0.6.1](https://github.com/open2c/bioframe/compare/v0.6.0...v0.6.1)
Date 2024-01-08

API changes:

Default behavior of `ensure_nullable` option in `overlap` was modified to minimize the possibility of regressions in libraries that depend on legacy behavior. 

* The new option was renamed `ensure_int` and is `True` by default. It ensures that output coordinate columns are always returned with an integer dtype, as was the case in prior versions. This is achieved by converting columns having non-nullable NumPy dtypes to Pandas nullable ones in the specific case where the result of an **outer join** generates missing values; otherwise, column dtypes are preserved unchanged in the output. 
* Unlike previous minor versions of bioframe, the nullable dtype chosen will have the **same underlying type** as the corresponding column from the input (i.e, an input dataframe using `np.uint32` start coordinates may yield a `pd.UInt32` start column in the output). 
* This behavior can be turned off by setting `ensure_int` to `False`, in which case outer joins on dataframes using NumPy dtypes may produce floating point output columns when missing values are introduced (stored as `NaN`), following the native casting behavior of such columns.

## [v0.6.0](https://github.com/open2c/bioframe/compare/v0.5.1...v0.6.0)
Date 2024-01-04

API changes:
* `overlap`: In previous versions, output coordinate columns were always converted to Pandas "nullable" `Int64` dtype before returning outer join results. In the interest of flexibility, memory efficiency, and least surprise, the coordinate columns returned in the output dataframe now preserve dtype from the input dataframes, following native type casting rules if missing data are introduced. We introduce the `ensure_nullable` argument to force Pandas nullable dtypes in the output coordinates. See the [docs](https://bioframe.readthedocs.io/en/latest/api-intervalops.html#bioframe.ops.overlap) for more details. (#178)

Bug fixes:
* Fixed `coverage` with custom `cols1` (#170)

Documentation:
* Added contributing guidelines and NumFOCUS affiliation.
* Updated README and added CITATION.cff file.
* Updated performance benchmarks.


## [v0.5.1](https://github.com/open2c/bioframe/compare/v0.5.0...v0.5.1)
Date 2023-11-08

Bug fixes:
* Series are treated like dict in `make_chromarms`


## [v0.5.0](https://github.com/open2c/bioframe/compare/v0.4.1...v0.5.0)

Date 2023-10-05

API changes:
* New builtin curated genome assembly database (metadata, chromsizes, cytobands):
  * `bioframe.list_assemblies()`
  * `bioframe.assembly_info()`
* New UCSC RGB color converter utility #158
* Options added to `pair_by_distance`

Bug fixes:
* Make expand throw an error if both pad and scale are passed (#148)
* Fixes to bioframe.select query interval semantics (#147)

Maintenance:
* Migrate to hatch build system and pyproject.toml
* Various refactorings


## [v0.4.1](https://github.com/open2c/bioframe/compare/v0.4.0...v0.4.1)

Date 2023-04-22

Bug fixes:
* Fix bug introduced in the last release in `select` and `select_*` query interval semantics. Results of select are now consistent with the query interval being interpreted as half-open, closed on the left.


## [v0.4.0](https://github.com/open2c/bioframe/compare/v0.3.3...v0.4.0)

Date 2023-03-23

API changes:
* New strand-aware directionality options for `closest()` via `direction_col` #129.
* New index-based range query selectors on single bioframes to complement `select()` #128:
    * `select_mask()` returns boolean indices corresponding to intervals that overlap the query region
    * `select_indices()` returns integer indices corresponding to intervals that overlap the query region
    * `select_labels()` returns pandas label indices corresponding to intervals that overlap the query region

Bug fixes:
* Import fixes in sandbox
* Relax bioframe validator to permit using same column as start and end (e.g. point variants).

## [v0.3.3](https://github.com/open2c/bioframe/compare/v0.3.2...v0.3.3)

Date: 2022-02-28

Bug fixes:
* fixed a couple functions returning an error instance instead of raising
* fetch_mrna link fixed

## [v0.3.2](https://github.com/open2c/bioframe/compare/v0.3.1...v0.3.2)

Date: 2022-02-01

Bug fixes:
* fixed error in is_contained
* tutorial updates

## [v0.3.1](https://github.com/open2c/bioframe/compare/v0.3.0...v0.3.1)

Date : 2021-11-15

API changes:

* `bioframe.sort_bedframe` does not append columns or modify their dtypes.

## [v0.3.0](https://github.com/open2c/bioframe/compare/v0.2.0...v0.3.0)

Date : 2021-08-31

Conceptual changes:
* we formulated strict definitions for genomic intervals, dataframes, and 
    their various properties. All bioframe functions are expected to follow
    to these definitions tightly.  

API changes:
* reorganize modules: 
    * ops - operations on genomic interval dataframes 
    * extras - miscellaneous operations, most involving
        genomic sequences and gene annotations
    * vis - visualizations of genomic interval dataframes
    * core.arrops - operations on genomic interval arrays
    * core.checks - tests for definitions of genomic interval dataframes
    * core.construction - construction and sanitation of genomic interval dataframes
    * core.specs - specifications for the implementation of genomic intervals in pandas.dataframes 
        (i.e. column names, datatypes, etc)
    * core.stringops - operations on genomic interval strings
    * io.fileops - I/O on common file formats for genomic data
    * io.schemas - schemas for standard tabular formats for genomic data storage
    * io.resources - interfaces to popular online genomic data resources 

* new functions: extras.pair_by_distance, ops.sort_bedframe, ops.assign_view, 
    dataframe constructors

* existing functions:
    * expand: take negative values and fractional values
    * overlap: change default suffixes, keep_order=True
    * subtract: add return_index and keep_order

* enable pd.NA for missing values, typecasting

New data:
* add schemas for bedpe, gap, UCSCmRNA, pgsnp
* add tables with curated detailed genome assembly information

Bugfixes:
* None?..

Miscellaneous:
* speed up frac_gc is faster now
* drop support for Python 3.6, add support for 3.9


## [v0.2.0](https://github.com/open2c/bioframe/compare/v0.1.0...v0.2.0)

Date : 2020-12-02

API changes
* `read_chromsizes` and `fetch_chromsizes`: add new `as_bed` parameter.
* `read_chromsizes` and `fetch_chromsizes`: revert to filtering chromosome names by default, but clearly expose `filter_chroms` kwarg.

Bug fixes
* Fixed `bioframe.split`
* Restored `frac_genome_coverage`


## [v0.1.0](https://github.com/open2c/bioframe/compare/v0.0.12...v0.1.0)

Date : 2020-09-23

First beta release.

### What's new

* New extensive dataframe genomic interval arithmetic toolsuite.
* Improved region handling and region querying functions.
* [Documentation!](https://bioframe.readthedocs.io/)

### Maintenance

* Dropped Python 2 support
* Refactoring of various genome operations and resources.
* Improved testing and linting
