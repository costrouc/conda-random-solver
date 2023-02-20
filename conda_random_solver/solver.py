from functools import lru_cache
import typing
import logging
import random

from conda_random_solver import __version__

from conda.core.solve import Solver
from conda.core.subdir_data import SubdirData
from conda.models.channel import Channel
from conda.base.constants import REPODATA_FN
from conda.common.constants import NULL
from conda._vendor.boltons.setutils import IndexedSet

logger = logging.getLogger(f"conda.{__name__}")


class RandomSolver(Solver):
    def __init__(
        self,
        prefix: str,
        channels: typing.Tuple[str],
        subdirs: typing.Tuple[str] = (),
        specs_to_add: typing.List[str] = (),
        specs_to_remove: typing.List[str]  = (),
        repodata_fn: str = REPODATA_FN,
        command: str = NULL,
    ):
        super().__init__(
            prefix,
            channels,
            subdirs=subdirs,
            specs_to_add=specs_to_add,
            specs_to_remove=specs_to_remove,
            repodata_fn=repodata_fn,
            command=command,
        )
        logger.warning(f"{prefix=} {channels=} {subdirs=} {specs_to_add=} {specs_to_remove=} {repodata_fn=} {command=}")

    @staticmethod
    @lru_cache(maxsize=None)
    def user_agent():
        """
        Expose this identifier to allow conda to extend its user agent if required
        """
        return f"conda-random-solver={__version__}"

    def solve_final_state(
        self,
        update_modifier=NULL,
        deps_modifier=NULL,
        prune=NULL,
        ignore_pinned=NULL,
        force_remove=NULL,
        should_retry_solve=False,
    ):
        logger.warning(f"{update_modifier=} {deps_modifier=} {prune=} {ignore_pinned=} {force_remove=} {should_retry_solve=}")

        package_records = []
        for channel in self.channels:
            for url in channel.urls(subdirs=self.subdirs):
                channel_url = Channel.from_url(url)
                subdir_data = SubdirData(channel_url, repodata_fn=self._repodata_fn)
                subdir_data.load()
                package_records.extend(list(subdir_data.iter_records()))

        return IndexedSet(random.sample(package_records, 10))
