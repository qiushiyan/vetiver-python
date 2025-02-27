from .vetiver_model import VetiverModel
from .utils import inform
import warnings
import logging

_log = logging.getLogger(__name__)


class ModelCard(UserWarning):
    def __init__(
        self,
        message="""
        Model Cards provide a framework for transparent, responsible reporting.
        Use the vetiver `.qmd` Quarto template as a place to start,
        with vetiver.model_card()""",
    ):
        self.message = message
        super().__init__(self.message)


def vetiver_pin_write(board, model: VetiverModel, versioned: bool = True):
    """
    Pin a trained VetiverModel along with other model metadata.

    Parameters
    ----------
    board:
        A pin board, created by `pins.board_folder()` or another `board_` function.
    model: vetiver.VetiverModel
        VetiverModel to be written to board
    versioned: bool
        Whether or not the pin should be versioned

    Example
    -------
    >>> import vetiver
    >>> from pins import board_temp
    >>> model_board = board_temp(versioned = True, allow_pickle_read = True)
    >>> X, y = vetiver.get_mock_data()
    >>> model = vetiver.get_mock_model().fit(X, y)
    >>> v = vetiver.VetiverModel(model = model, model_name = "my_model", ptype_data = X)
    >>> vetiver.vetiver_pin_write(model_board, v)
    """
    if not board.allow_pickle_read:
        raise NotImplementedError  # must be pickle-able

    inform(
        _log,
        "Model Cards provide a framework for transparent, responsible "
        "reporting. \n Use the vetiver `.qmd` Quarto template as a place to start, \n "
        "with vetiver.model_card()",
    )

    board.pin_write(
        model.model,
        name=model.model_name,
        type="joblib",
        description=model.description,
        metadata={
            "required_pkgs": model.metadata.get("required_pkgs"),
            "ptype": None if model.ptype is None else model.ptype().json(),
        },
        versioned=versioned,
    )


def vetiver_pin_read(board, name: str, version: str = None) -> VetiverModel:
    """
    Read pin and populate VetiverModel

    Parameters
    ----------
    board:
        A pin board, created by `pins.board_folder()` or another `board_` function.
    name: string
        Pin name
    version: str
        Retrieve a specific version of a pin.

    Returns
    --------
    vetiver.VetiverModel

    Notes
    -----
    If reading a board from RSConnect, the `board` argument must be in
    "username/modelname" format.

    """

    warnings.warn(
        "vetiver_pin_read will be removed in v1.0.0. Use classmethod "
        "VetiverModel.from_pin() instead",
        DeprecationWarning,
    )

    v = VetiverModel.from_pin(board=board, name=name, version=version)

    return v
