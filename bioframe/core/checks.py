import pandas as pd
import numpy as np
from .. import ops
from . import construction
from . import specs
from .specs import _get_default_colnames, _verify_columns, _verify_column_dtypes


def is_bedframe(
    df,
    raise_errors=False,
    cols=None,
):
    """
    Checks that a genomic interval dataframe `df` has:
    - chrom, start, end columns
    - columns have valid dtypes (object/string/categorical, int, int)
    - all starts < ends.

    raise_errors:bool
        If true, raises errors instead of returning a boolean False for invalid properties.
        Default false.

    cols : (str, str, str) or None
        The names of columns containing the chromosome, start and end of the
        genomic intervals, provided separately for each set. The default
        values are 'chrom', 'start', 'end'.

    Returns
    -------
    is_bedframe:bool

    """
    ck1, sk1, ek1 = _get_default_colnames() if cols is None else cols

    if not _verify_columns(df, [ck1, sk1, ek1], return_as_bool=True):
        if raise_errors:
            raise TypeError("Invalid column names")
        return False

    if not _verify_column_dtypes(df, cols=[ck1, sk1, ek1], return_as_bool=True):
        if raise_errors:
            raise TypeError("Invalid column dtypes")
        return False

    if ((df[ek1] - df[sk1]) < 0).any():
        if raise_errors:
            raise ValueError(
                "Invalid genomic interval dataframe: starts exceed ends for "
                + str(np.sum(((df[ek1] - df[sk1]) < 0)))
                + " intervals"
            )
        return False

    return True


def is_cataloged(
    df, view_df, raise_errors=False, df_view_col="view_region", view_name_col="name"
):
    """
    tests if all regions names in a bioframe `df` are present in the view `view_df`.

    df : pandas.DataFrame

    view_df : pandas.DataFrame

    df_view_col: str
        Name of column from df that indicates region in view.

    view_name_col: str
        Name of column from view that specifies unique region name.

    Returns
    -------
    is_cataloged:bool

    """
    if not _verify_columns(df, [df_view_col], return_as_bool=True):
        if raise_errors is True:
            raise ValueError(f"Could not find ‘{df_view_col}’ column in df")
        return False

    if not _verify_columns(view_df, [view_name_col], return_as_bool=True):
        if raise_errors is True:
            raise ValueError(f"Could not find ‘{view_name_col}’ column in view_df")
        return False

    if not set(df[df_view_col].values).issubset(set(view_df[view_name_col].values)):
        if raise_errors is True:
            raise ValueError(
                "The following regions in df[df_view_col] not in view_df[view_name_col]: \n"
                + "{}".format(
                    set(df[df_view_col].values).difference(
                        set(view_df[view_name_col].values)
                    )
                )
            )
        return False

    return True


def is_overlapping(df, cols=None):
    """
    tests if any genomic intervals in a bioframe `df` overlap

    Returns
    -------
    is_overlapping:bool

    """

    ck1, sk1, ek1 = _get_default_colnames() if cols is None else cols

    df_merged = ops.merge(df, cols=cols)

    total_interval_len = np.sum((df[ek1] - df[sk1]).values)
    total_interval_len_merged = np.sum((df_merged[ek1] - df_merged[sk1]).values)

    if total_interval_len > total_interval_len_merged:
        return True
    else:
        return False


def is_viewframe(region_df, raise_errors=False, view_name_col="name", cols=None):
    """
    Checks that region_df is a valid view, namely:
    - it satisfies requirements for a bedframe, including columns for ('chrom', 'start', 'end')
    - it has an additional column, view_name_col, with default 'name'
    - it does not contain null values
    - entries in the view_name_col are unique.
    - intervals are non-overlapping

    raise_errors:bool
        If true, raises errors instead of returning a boolean for invalid properties.
        Default false.

    Returns
    -------
    is_viewframe:bool

    """

    ck1, sk1, ek1 = _get_default_colnames() if cols is None else cols

    if not _verify_columns(
        region_df, [ck1, sk1, ek1, view_name_col], return_as_bool=True
    ):
        if raise_errors:
            raise TypeError("Invalid view: invalid column names")
        return False

    if not is_bedframe(region_df, cols=cols):
        if raise_errors:
            raise ValueError("Invalid view: not a bedframe")
        return False

    if pd.isna(region_df).values.any():
        if raise_errors:
            raise ValueError("Invalid view: cannot contain NAs")
        return False

    if len(set(region_df[view_name_col])) < len(region_df[view_name_col].values):
        if raise_errors:
            raise ValueError(
                "Invalid view: entries in region_df[view_name_col] must be unique"
            )
        return False

    if is_overlapping(region_df, cols=cols):
        if raise_errors:
            raise ValueError("Invalid view: entries must be non-overlapping")
        return False

    return True


def is_contained(
    df,
    view_df,
    raise_errors=False,
    df_view_col="view_region",
    view_name_col="name",
    cols=None,
):
    """
    tests if all genomic intervals in a bioframe `df` are cataloged and do not extend beyond their
    associated region in the view `view_df`.

    df : pandas.DataFrame

    view_df : pandas.DataFrame
        Valid viewframe.

    df_view_col:
        Column from df used to associate interviews with view regions.
        Default `view_region`.

    cols: (str, str, str)
        Column names for chrom, start, end in df.

    Returns
    -------
    is_contained:bool

    """

    ck1, sk1, ek1 = _get_default_colnames() if cols is None else cols

    if not is_cataloged(
        df, view_df, df_view_col=df_view_col, view_name_col=view_name_col
    ):
        if raise_errors:
            raise ValueError("df not cataloged in view_df")
        return False

    df_trim = ops.trim(
        df, view_df=view_df, df_view_col=df_view_col, view_name_col=view_name_col
    )
    is_start_trimmed = np.any(df[sk1].values != df_trim[sk1].values)
    is_end_trimmed = np.any(df[ek1].values != df_trim[ek1].values)

    if is_start_trimmed or is_end_trimmed:
        if raise_errors:
            raise ValueError("df not contained in view_df")
        return False
    else:
        return True


def is_covering(df, view_df, view_name_col="name", cols=None):
    """
    tests if a view `view_df` is covered by the set of genomic intervals in the bedframe `df`
    this is true if the complement is empty.

    Note this does not depend on regions assigned to intervals in df, if any, since regions are re-assigned in complement.

    Returns
    -------
    is_covering:bool

    """

    if ops.complement(
        df,
        view_df=view_df,
        view_name_col=view_name_col,
        cols=cols,
    ).empty:
        return True
    else:
        return False


def is_tiling(
    df,
    view_df,
    raise_errors=False,
    df_view_col="view_region",
    view_name_col="name",
    cols=None,
):
    """
    tests if a view `view_df` is tiled by the set of genomic intervals in the bedframe `df`
    this is true if:
    - df is not overlapping
    - df is covering view_df
    - df is contained in view_df

    Returns
    -------
    is_tiling:bool

    """

    view_df = construction.make_viewframe(
        view_df, view_name_col=view_name_col, cols=cols
    )

    if is_overlapping(df):
        if raise_errors:
            raise ValueError("overlaps")
        return False
    if not is_covering(df, view_df, view_name_col=view_name_col, cols=None):
        if raise_errors:
            raise ValueError("not covered")
        return False
    if not is_contained(
        df, view_df, df_view_col=df_view_col, view_name_col=view_name_col, cols=None
    ):
        if raise_errors:
            raise ValueError("not contained")
        return False
    return True


def is_sorted(
    df,
    view_df=None,
    infer_assignment=True,
    reset_index=True,
    df_view_col="view_region",
    view_name_col="name",
    cols=None,
):
    """
    Tests if a bedframe is changed by sorting.

    Returns
    -------
    is_sorted : bool

    """

    df_sorted = ops.sort_bedframe(
        df.copy(),
        view_df=view_df,
        infer_assignment=infer_assignment,
        reset_index=reset_index,
        df_view_col=df_view_col,
        view_name_col=view_name_col,
        cols=cols,
    )

    if df.equals(df_sorted):
        return True
    else:
        return False