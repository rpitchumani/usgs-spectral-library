"""
Om Sri Arunachala Shiva
"""
import pathlib
from pathlib import Path
from glob import glob
import pandas as pd
import plotly.graph_objects as go
from splib07a import SPLIB07A


if __name__ == "__main__":
    
    path_main_usgs = Path("../../data-sets/usgs/splib07")
    path_ascii_splib07a = path_main_usgs / "ASCIIdata/ASCIIdata_splib07a"
    path_index_splib07a = path_main_usgs / "indexes" / "datatable_splib07a.html"
    
    chapter_name = "ChapterM_Minerals"
    material_name = "Actinolite_HS116.1B"
    
    path_ascii_chapter = path_ascii_splib07a / chapter_name
    
    list_df_splib07a = pd.read_html(path_index_splib07a, extract_links="body")
    
    df_minerals = list_df_splib07a[1].copy().droplevel(0, axis=1).droplevel(0, axis=1)
    df_minerals = df_minerals.loc[:, ~df_minerals.columns.str.contains("Unnamed")]


    df_minerals[["Material Name", "x"]] = pd.DataFrame(
        df_minerals["Spectrum Title"].tolist(),
        index=df_minerals.index
    )
        
    
    splib = SPLIB07A(path_main_usgs=path_main_usgs)