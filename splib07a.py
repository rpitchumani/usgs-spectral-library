"""
Om Sri Arunachala Shiva
"""

from typing import Dict
from loguru import logger
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go



class SPLIB07A:
    
    def __init__(
        self,
        path_main_usgs: Path
    ):
        
        self.path_main_usgs = path_main_usgs
        
        self.path_ascii_splib07a = \
            path_main_usgs / "ASCIIdata/ASCIIdata_splib07a"
        self.path_index_splib07a = \
            path_main_usgs / "indexes" / "datatable_splib07a.html"
            
        self._read_index_datatable()
        
    def _clean_datatable(self, df: pd.DataFrame) -> pd.DataFrame:
        
        df_clean = (
            df.copy()
            .droplevel(0, axis=1)
            .droplevel(0, axis=1)
        )

        df_clean = (
            df_clean.loc[:, ~df_clean.columns.str.contains("Unnamed")]
        )
        df_clean[["Material Name", "x"]] = pd.DataFrame(
            df_clean["Spectrum Title"].tolist(),
            index=df_clean.index
        )
        
        df_clean.drop(columns=["Spectrum Title", "x"], inplace=True)
        df_clean.rename(
            columns={"Material Name": "Spectrum Title"}, inplace=True
        )
        
        df_clean.set_index("Spectrum Title", inplace=True)
        
        return df_clean        
        
    def _read_index_datatable(self):
        
        list_dfs_splib07a = pd.read_html(
            self.path_index_splib07a, 
            extract_links="body"
        )
        
        # First data frame is corner of a table in HTML
        
        self.tables = {
            
            df_splib07a.columns[0][1]: self._clean_datatable(df_splib07a)
            
            for df_splib07a in list_dfs_splib07a[1:]            
        }
        
        logger.info(
            f"Found {len(self.tables)}:\n"
            f"{list(self.tables.keys())}"
        )
                
    def get_wavelength(self, material_name: str) -> Dict:
        
        df = self.tables.get("Chapter 1: Minerals")
        
        df_material = df[df.index.str.contains(material_name)]
        
        path_from_html_ascii_wavelengths = (
            Path(df_material.iloc[0]["ASCII Wavelengths (µm)"][1][3:])
        )
        
        path_ascii_wavelengths = (
            self.path_main_usgs / path_from_html_ascii_wavelengths
        )

        path_from_html_ascii_spectrum = (
            Path(df_material.iloc[0]["ASCII Spectrum (µm)"][1][3:])
        )
        
        path_ascii_spectrum = (
            self.path_main_usgs / path_from_html_ascii_spectrum
        )
        
        df_ascii_wavelengths = pd.read_csv(path_ascii_wavelengths)
        information_wavelengths = df_ascii_wavelengths.columns[0]
        df_ascii_wavelengths.columns = ["wavelength (micron)"]
        
        df_ascii_spectrum = pd.read_csv(path_ascii_spectrum)
        information_spectrum = df_ascii_spectrum.columns[0]
        df_ascii_spectrum.columns = ["value"]

        dict_wavelength = {
            
            "information_wavelengths": information_wavelengths,
            "information_spectrum": information_spectrum,
            "df_wavelengths": df_ascii_wavelengths,
            "df_spectrum": df_ascii_spectrum
            
        }
        
        # logger.info(df_material)
        
        return dict_wavelength
        
    
    def plotly_wavelength(self, dict_wavelength: Dict) -> go.Figure:
        
        information_wavelengths = (
            dict_wavelength.get("information_wavelengths")
        )
        
        information_spectrum = (
            dict_wavelength.get("information_spectrum")
        )
        
        df_wavelengths = dict_wavelength.get("df_wavelengths")
        df_spectrum = dict_wavelength.get("df_spectrum")
        
        fig = go.Figure()
        
        fig.add_trace(
            go.Scatter(
                x=df_wavelengths["wavelength (micron)"],
                y=df_spectrum["value"],
                name=information_spectrum,
                line=dict(
                    width=3
                )
            )
        )
        
        fig.update_layout(
            title=f"{information_spectrum}",
            xaxis=dict(
                title="Wavelength (µm)",
                linewidth=3,
                showline=True,
                ticks="inside",
                mirror=True,
                gridcolor="gray",
                gridwidth=1,
                showgrid=True
            ),
            yaxis=dict(
                title="Reflectance",
                linewidth=3,
                showline=True,
                ticks="inside",
                mirror=True,
                gridcolor="gray",
                gridwidth=1,
                showgrid=True
            ),
            width=1000,
            height=600,
            template="none"
        )
        
        return fig