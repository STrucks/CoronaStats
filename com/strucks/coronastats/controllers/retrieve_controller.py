import connexion
import six

from com.strucks.coronastats.models.overview_data_row import OverviewDataRow  # noqa: E501
from com.strucks.coronastats import util


def current(location):  # noqa: E501
    """Get Current

    Gets the current data for a specific location # noqa: E501

    :param location: The location of interest
    :type location: str

    :rtype: OverviewDataRow
    """
    return 'do some magic!'


def getsince(location, days):  # noqa: E501
    """Your GET endpoint

    Gets the data since a given amount of days for a specific location # noqa: E501

    :param location: The location of interest
    :type location: str
    :param days: The amount of days of interest
    :type days: 

    :rtype: List[OverviewDataRow]
    """
    return 'do some magic!'
