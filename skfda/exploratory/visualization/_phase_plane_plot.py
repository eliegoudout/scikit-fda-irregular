"""Phase-Plane Plot Module.

This module contains the functionality in charge of plotting
two different functions as coordinates, this can be done giving
one FData, with domain 1 and codomain 2, or giving two FData, both
of them with domain 1 and codomain 1.
"""

from typing import Any, List, Optional, TypeVar

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from ...representation import FData
from ._utils import _get_figure_and_axes, _set_figure_layout

S = TypeVar('S', Figure, Axes, List[Axes])


class PhasePlanePlot:
    """Phase-Plane Plot visualization.

    This class contains the functionality in charge of plotting
    two different functions as coordinates, this can be done giving
    one FData, with domain 1 and codomain 2, or giving two FData, both
    of them with domain 1 and codomain 1.
    Args:
        fdata1: functional data set that we will use for the graph. If it has
            a dim_codomain = 1, the fdata2 will be needed.
        fdata2: optional functional data set, that will be needed if the fdata1
            has dim_codomain = 1.
    """
    def __init__(
        self,
        fdata1: FData,
        fdata2: Optional[FData] = None,
    ) -> None:
        self.fdata1 = fdata1
        self.fdata2 = fdata2

    def plot(
        self,
        chart: Optional[S] = None,
        *,
        fig: Optional[Figure] = None,
        ax: Optional[Axes] = None,
        **kwargs: Any,
    ) -> Figure:
        """
        Plot Phase-Plane graph.

        Plot the functions as coordinates. If two functions are passed
        it will concatenate both into one only FData.
        Args:
            chart: figure over with the graphs are plotted or axis over
                where the graphs are plotted. If None and ax is also
                None, the figure is initialized.
            fig: figure over with the graphs are plotted in case ax is not
                specified. If None and ax is also None, the figure is
                initialized.
            ax: axis where the graphs are plotted. If None, see param fig.
            kwargs: optional arguments.
        Returns:
            fig (figure object): figure object in which the phase-plane
            graph will be plotted.
        """
        fig, axes = _get_figure_and_axes(chart, fig, ax)

        if (
            self.fdata2 is not None
        ):
            if (
                self.fdata1.dim_domain == self.fdata2.dim_domain
                and self.fdata1.dim_codomain == self.fdata2.dim_codomain
                and self.fdata1.dim_domain == 1
                and self.fdata1.dim_codomain == 1
            ):
                self.fd_final = self.fdata1.concatenate(
                    self.fdata2, as_coordinates=True
                )
            else:
                raise ValueError(
                    "Error in data arguments,",
                    "codomain or domain is not correct.",
                )
        else:
            self.fd_final = self.fdata1

        if (
            self.fd_final.dim_domain == 1
            and self.fd_final.dim_codomain == 2
        ):
            fig, axes = _set_figure_layout(
                fig, axes, dim=2, n_axes=1,
            )
            axes[0].plot(
                self.fd_final.data_matrix[0][:, 0].tolist(),
                self.fd_final.data_matrix[0][:, 1].tolist(),
                **kwargs,
            )
        else:
            raise ValueError(
                "Error in data arguments,",
                "codomain or domain is not correct.",
            )

        fig.suptitle("Phase-Plane Plot")
        axes[0].set_xlabel("Function 1")
        axes[0].set_ylabel("Function 2")

        return fig
