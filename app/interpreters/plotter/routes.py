from flask import current_app as app
from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required

from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from flask import Response

import io

from ...mechanisms.amm.models import AMM
from .plotter import Plotter

# Blueprint Configuration
plotter_bp = Blueprint(
    'plotter_bp', __name__,
    url_prefix='/plotter',
    template_folder='templates',
    static_folder='static'
)

# user_bp.route('/', methods=['GET'])(index)
# user_bp.route('/', methods=['POST'])(store)
# user_bp.route('/<int:user_id>', methods=['GET'])(show)
# user_bp.route('/<int:user_id>/edit', methods=['POST'])(update)
# user_bp.route('/<int:user_id>', methods=['DELETE'])(destroy)



"""Logged-in page routes."""
@plotter_bp.route('/amm_maps/<int:id>.png', methods=['GET'])
# @login_required
def amm_maps(id):
    fig = create_amm_maps(id)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


def create_amm_maps(_id):
    p = Plotter()
    amm = AMM.query.get(_id)
    p.iterate_plot()
    p = amm.plot_curve(p)

    for i, record in enumerate(amm.records):
        if i == 0:
            p = record.plot_record(p, True)
        elif i == len(amm.records) - 1:
            p = record.plot_record(p, False, True)
        else:
            p = record.plot_record(p)

        # while i < _days:
        #     pool.apply_volume(_y_volume)
        #     if i == 0:
        #         p = pool.plot_current(p, True)
        #     else:
        #         p = pool.plot_current(p)
        #     i+= 1
    # p = balancer.plot_curve(p)
    # p = balancer.plot_current(p, True)
    # balancer.apply_volume(280000)
    # p.iterate_plot()
    # p = sushi.plot_curve(p)
    # p = sushi.plot_current(p, True)
    return p.fig
