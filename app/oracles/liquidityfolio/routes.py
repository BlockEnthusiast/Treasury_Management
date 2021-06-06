from flask import current_app as app
from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required

from flask import Response
from flask import request

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io


from .forms import AMMForm
from .models import  db, AMM, AMM_Record
# from ..plotter.plotter import Plotter

# Blueprint Configuration
amm_bp = Blueprint(
    'amm_bp', __name__,
    url_prefix='/amm',
    template_folder='templates',
    static_folder='static'
)

# amm_bp.route('/', methods=['GET'])(index)
# amm_bp.route('/', methods=['POST'])(store)
# amm_bp.route('/<int:user_id>', methods=['GET'])(show)
# amm_bp.route('/<int:user_id>/edit', methods=['POST'])(update)
# amm_bp.route('/<int:user_id>', methods=['DELETE'])(destroy)

# """Logged-in page routes."""
# @amm_bp.route('/', methods=['GET'])
# @login_required
# def index():
#     amms = AMM.query.filter_by(user_id=current_user.id).all()
#     if request.data:
#         amm = AMM(name = request.data['name'],
#                 name_x = requests.data['name_x'],
#                 name_y = requests.data['name_y'],
#                 )
#     return render_template(
#             'dashboard.jinja2',
#             title='AMM Index.',
#             template='amm-template',
#             current_user=current_user,
#             amms = amms,
#             body="You are now logged in!"
#         )
# #
# """Logged-in page routes."""
# @amm_bp.route('/new', methods=['GET', 'POST'])
# @login_required
# def new():
#     form = AMMForm()
#     if form.validate_on_submit():
#
#         new_amm = AMM(
#                     name=form.name.data,
#                     name_x=form.name_x.data,
#                     name_y =form.name_y.data,
#                     simulation_id=current_user.active_sim().id
#                     )
#         if form.weight_x.data:
#             new_amm.set_weight_x(form.weight_x.data)
#         new_amm.seed(form.bal_x.data, form.bal_y.data)
#         db.session.add(new_amm)
#         db.session.commit()
#         log_record(new_amm)
#         db.session.commit()
#         return redirect(url_for('simulator_bp.dashboard'))
#     return render_template(
#         'newamm.jinja2',
#         title='New AMM.',
#         form=form,
#         template='new-amm',
#         body="Sign up for a user account."
#     )
#
# """Logged-in page routes."""
# @amm_bp.route('/delete/<int:id>', methods=['GET'])
# @login_required
# def delete(id):
#     target_amm = AMM.query.get(id)
#     if target_amm:
#         db.session.delete(target_amm)
#         db.session.commit()
#     return redirect(url_for('simulator_bp.dashboard'))
#
#
# """Logged-in page routes."""
# @amm_bp.route('/reset/<int:id>', methods=['GET'])
# @login_required
# def reset(id):
#     target_amm = AMM.query.get(id)
#     if target_amm:
#         earliest = None
#         for record in target_amm.records:
#             if earliest == None:
#                 earliest = record
#             elif record.id < earliest.id:
#                 db.session.delete(earliest)
#                 earliest = record
#             else:
#                 db.session.delete(record)
#         target_amm.seed(earliest.bal_x, earliest.bal_y)
#         # db.session.delete(earliest)
#         db.session.commit()
#         return redirect(url_for('simulator_bp.dashboard'))
#     return render_template(
#         'newamm.jinja2',
#         title='New AMM.',
#         form=form,
#         template='new-amm',
#         body="Sign up for a user account."
#     )
#
#
# """Logged-in page routes."""
# @amm_bp.route('/records', methods=['GET'])
# @login_required
# def records():
#     active_sim = current_user.active_sim()
#     amm_record_books = get_amm_record_books(current_user)
#     return render_template(
#         'indexrecords.jinja2',
#         title='Record Index',
#         amm_record_books = amm_record_books,
#         active_sim=active_sim,
#         template='record-index',
#         # body="See records"
#     )
#
# # """Logged-in page routes."""
# # @amm_bp.route('/apply_volume/<float:buy>/<float:sell>/<float:move_size>', methods=['GET', 'POST'])
# # @login_required
# def apply_volume(buy, sell, move_size):
#     sim = current_user.active_sim()
#     amms = sim.amms
#     if amms == []:
#         return False
#     net_vol = buy + sell
#     is_positive = True if net_vol > 0 else False
#     if not is_positive: net_vol *= -1
#     while net_vol > 0:
#         best_priced_pool = None
#         print("\nPool Prices")
#         sim = current_user.active_sim()
#         amms = sim.amms
#         for i, pool in enumerate(amms):
#             if best_priced_pool == None:
#                 best_priced_pool = i
#                 print("Pool: {}, Price: {}".format(pool.name, pool.y_price()))
#             elif amms[i].y_price() > pool.y_price():
#                 print("New Best Pool: {}, Price: {}".format(pool.name, pool.y_price()))
#                 print("diff {}".format(amms[i].y_price()  - pool.y_price()))
#                 best_priced_pool = i
#             else:
#                 print("diff {}".format(amms[i].y_price()  - pool.y_price()))
#
#         move_this = move_size if net_vol > move_size else net_vol
#         net_vol -= move_this
#         if not is_positive: move_this *=-1
#         old_price = amms[best_priced_pool].y_price()
#         amms[best_priced_pool].apply_volume(move_this)
#         new_price = amms[best_priced_pool].y_price()
#         db.session.commit()
#         print("\tbest {}".format(amms[best_priced_pool].y_price()))
#         print("\tbest {}".format(amms[best_priced_pool].id))
#         print("\t\tMoved Market {}".format(new_price - old_price))
#     for amm in amms:
#         mrr = amm.most_recent_record()
#         if mrr.bal_x != amm.bal_x and mrr.bal_y != amm.bal_y:
#             create_record(amm)
#     db.session.commit()
#     return True
#
#
# def create_record(amm):
#     print("LOGGING ALL THE RECORDS!!!!!!")
#     record = AMM_Record(
#         amm_id = amm.id,
#         token_price_x = amm.x_price(),
#         bal_x = amm.bal_x,
#         weight_x = amm.weight_x,
#         token_price_y = amm.y_price(),
#         bal_y = amm.bal_y,
#         weight_y = amm.weight_y,
#         constant_product = amm.constant_product()
#     )
#     db.session.add(record)
#     return record
#
# def get_amm_record_books(_current_user):
#     active_sim = current_user.active_sim()
#     amm_record_books = []
#     for amm in active_sim.amms:
#         amm_record_book = AMM_Record.query.filter_by(amm_id = amm.id).order_by(AMM_Record.id.desc()).all()
#         amm_record_books.append(amm_record_book)
#     return amm_record_books
