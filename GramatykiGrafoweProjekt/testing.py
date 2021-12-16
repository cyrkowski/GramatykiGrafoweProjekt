from GramatykiGrafoweProjekt import CannotApplyProductionError
import pytest


def assert_production_cannot_be_applied(Production, Graph):
    with pytest.raises(CannotApplyProductionError):
        Production(Graph)
