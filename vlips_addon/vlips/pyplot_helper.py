import logging

import matplotlib.pyplot as plt

from .constants import *

log = logging.getLogger(__name__)


class PyplotHelper:
    @staticmethod
    def setup_pyplot():
        """
        Set Pyplot up.

        """

        log.info("Set Pyplot up")
        log.debug("setup_pyplot()")

        params = {'legend.fontsize': PYPLOT_LEGEND_FONT_SIZE,
                  'figure.figsize': PYPLOT_FIGURE_SIZE,
                  'axes.labelsize': PYPLOT_AXES_LABEL_SIZE,
                  'axes.titlesize': PYPLOT_AXES_TITLE_SIZE,
                  'xtick.labelsize': PYPLOT_XTICK_LABEL_SIZE,
                  'ytick.labelsize': PYPLOT_YTICK_LABEL_SIZE,
                  'axes.titlepad': PYPLOT_AXES_TITLE_PAD}
        plt.rcParams.update(params)
