from __future__ import annotations

import logging
from pathlib import (
    Path,
)

from ..models import (
    Trip,
    Job,
    Vehicle,
    Surface,
    Fleet,
    GeometricSurface,
)
from .abc import (
    Loader,
)

logger = logging.getLogger(__name__)


class FileLoader(Loader):

    def __init__(self, file_path: Path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_path = file_path

        self._fleet = None
        self._job = None
        self._surface = None

    def synchronize(self):
        with self.file_path.open() as file:
            data = tuple(tuple(int(v) for v in line.split()) for line in file.readlines())
            row = data[0]
            self._surface = self._build_surface(*row[0:2])
            self._fleet = self._build_fleet(row[2])
            # TODO: Set bonus and number of steps (Config object)
            #
            self._job = self._build_job(data[1:])

    def _build_surface(self, rows: int, columns: int) -> Surface:
        return GeometricSurface()

    def _build_fleet(self, n: int, capacity: int = 1):
        initial = self._surface.get_or_create_position(lat=0, lon=0)
        vehicles = set(Vehicle(initial, capacity=capacity) for _ in range(n))
        return Fleet(vehicles)

    def _build_job(self, raw, *args, **kwargs):
        trips = set(self._build_trip(str(i), *row) for i, row in enumerate(raw))
        return Job(trips, *args, **kwargs)

    def _build_trip(self, identifier: str, x1: float, y1: float, x2: float, y2: float, earliest: float,
                    latest: float) -> Trip:
        origin = self._surface.get_or_create_position(lat=x1, lon=y1)
        destination = self._surface.get_or_create_position(lat=x2, lon=y2)
        timeout = latest - earliest
        trip = Trip(identifier, origin, destination, earliest, timeout)
        return trip

    @property
    def fleet(self) -> Fleet:
        if self._fleet is None:
            self.synchronize()
        return self._fleet

    @property
    def job(self) -> Job:
        if self._job is None:
            self.synchronize()
        return self._job

    @property
    def surface(self) -> Surface:
        if self._surface is None:
            self.synchronize()
        return self._surface
